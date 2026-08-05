/**
 * 知识卡片在线生成器 - 后端代理
 * Vercel Edge Function，安全调用 DeepSeek（key 在服务端，不暴露给浏览器）
 * 调用方式: POST /api/knowledge-cards  { prompt: string }
 * 无 Key 用户走这里（消耗站长 DEEPSEEK_API_KEY 额度）；
 * 用户自带 Key 时前端直连 DeepSeek，不经过本接口。
 */

export const config = {
  runtime: 'edge',
  maxDuration: 300,
};

const SYSTEM_PROMPT = `你是「知识卡片生成引擎」。用户给出主题提示词，你产出一组可分享的知识卡片，每张卡片把一件事讲透。

必须只输出一个合法 JSON 对象，不要输出 markdown 代码块、不要任何解释文字。格式：
{
  "title": "封面大标题（如：乔布斯拆解 · 40张卡片）",
  "kicker": "封面英文小标（如：STEVE JOBS · A DECONSTRUCTION）",
  "subtitle": "封面副标题（如：生平 · 作品 · 思考 · 起落 · 启发）",
  "categories": { "life": "生平轨迹", ... },
  "terms": [ {卡片对象} ]
}

每张卡片对象字段：
- termId: 3字母前缀+4位数字编号（如 job-0007, fin-0012）
- termZh: 卡片标题，2-20字，一眼看懂
- category: 必须属于 categories 里的某个 key
- definition: 定义，30-160字，写全不要截断
- plainAnalogy: 说人话，用生活化类比让外行秒懂，禁止引入新黑话
- whyItMatters: 为什么重要，一句话说清价值
- misuse: 常见误读，必须有实质内容（这是信息增量最高的栏，禁止写"无"或留空；想不出这条的误读就换选题）
- relatedTerms: 关联词数组，最多5个，和其他卡片串成知识网
- metricHint: 关键数字（销量/价格/年份/规模），没有把握就留空字符串
- riskFlag: "none" 或风险标签（advertising/qualification/dataPrivacy/counterfeit/fraud/minor/overPerm/dataLeak/hallucination/promptInjection）
- sourceType: industryConsensus（行业共识）/ documented（有据可查）/ inferred（推断）
- confidence: 可信度 0-1

硬性规则：
1. 张数严格等于用户要求的数量。
2. misuse 是每张卡的灵魂，逐张检查不能为空。
3. 不编造数据：不确定的数字删掉或留空，需要数据就基于公开常识。
4. confidence<0.6 的卡片要谨慎措辞。
5. 人物类必须包含失败与争议内容（fall 段至少3张），否则整套牌是吹捧，立不住。
6. 正文用简体中文，字段名保持英文 camelCase。`;

const SKELETON_GUIDE = {
  auto: "根据主题自动判断最合适的分类骨架（人物→五段式；行业黑话→产业链路；产品→模块；通用知识→通用分类）。",
  person: "分类骨架用人物五段式：life(生平轨迹)/works(伟大作品)/mind(核心思考)/fall(起落沉浮)/lesson(创业启示)。fall 段必须至少3张，写失败与争议，否则整套是吹捧。",
  slang: "分类骨架用产业链路式：品类/交易/价格/品相/玩法/风险，覆盖这个圈子真正有壁垒的黑话。",
  product: "分类骨架用架构模块式：概览/能力/扩展/记忆/交互，讲清这个产品每个模块是什么、解决什么问题。",
  general: "分类骨架用通用知识7类：流量获取/转化成交/产品形态/商业模式/数据指标/交付履约/合规风控，或按主题自定更贴切的分类。",
};

export default async function handler(request: Request) {
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
    });
  }

  if (request.method !== 'POST') {
    return json({ ok: false, error: '仅支持 POST' }, 405);
  }

  let body: any;
  try {
    body = await request.json();
  } catch {
    return json({ ok: false, error: '请求体不是合法 JSON' }, 400);
  }

  const prompt: string = (body.prompt || '').toString().trim();
  if (!prompt) {
    return json({ ok: false, error: '缺少 prompt' }, 400);
  }

  const apiKey = process.env.DEEPSEEK_API_KEY;
  if (!apiKey) {
    return json({ ok: false, error: 'NO_KEY: 站长未配置 DEEPSEEK_API_KEY 环境变量' }, 503);
  }

  const userPrompt = prompt.includes('张数') && prompt.includes('分类骨架')
    ? prompt
    : `主题：${prompt}\n张数：20 张\n分类骨架：${SKELETON_GUIDE.auto}\n请按上述要求输出 JSON。`;

  try {
    const upstream = await fetch('https://api.deepseek.com/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: 'deepseek-chat',
        messages: [
          { role: 'system', content: SYSTEM_PROMPT },
          { role: 'user', content: userPrompt },
        ],
        response_format: { type: 'json_object' },
        temperature: 0.7,
        max_tokens: 8192,
      }),
    });

    if (!upstream.ok) {
      const t = await upstream.text();
      return json({ ok: false, error: `DeepSeek 上游错误 ${upstream.status}: ${t.slice(0, 200)}` }, 502);
    }

    const up = await upstream.json();
    const content: string = up.choices?.[0]?.message?.content || '';
    let data: any;
    try {
      data = JSON.parse(content);
    } catch {
      return json({ ok: false, error: 'AI 返回的不是合法 JSON，请重试' }, 502);
    }

    if (!Array.isArray(data.terms) || !data.terms.length) {
      return json({ ok: false, error: 'AI 返回缺少 terms 数组，请重试' }, 502);
    }

    return json({
      ok: true,
      data: {
        title: data.title,
        kicker: data.kicker,
        subtitle: data.subtitle,
        categories: data.categories,
        terms: data.terms,
      },
      usage: up.usage,
    });
  } catch (e: any) {
    return json({ ok: false, error: '代理调用失败: ' + (e?.message || e) }, 502);
  }
}

function json(obj: any, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
    },
  });
}
