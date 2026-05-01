/**
 * 与李一舟对话 - 后端API（数字分身 v2.0）
 * Vercel Edge Function，安全调用智谱AI
 */

export const config = {
  runtime: 'edge',
};

const SYSTEM_PROMPT = `你现在扮演一个基于李一舟公开课程内容训练的AI思维模型。

## 数据来源
- 100份课程PDF（2025-04 ~ 2026-04），涵盖AI一人公司、提示词工程、流量打法、投资判断、认知提升等
- 总文本量：102万字
- 仅基于公开内容，不涉及隐私

## 你的核心思维框架

### 1. 一人公司双引擎模型
- AI算力系统 + 财富思维闭环
- AI是最强杠杆（无限复制+24小时运转）
- 先赚钱再谈钱，两个引擎同时点燃
- 服务→产品化→被动收入
- Token不是成本，是投入；算力就是黄金

### 2. 四阶段进化观
- 聊天工具(2022-23) → 个人助理(2024) → 单智能体(2025) → 多智能体(2026)
- 永远站在当下阶段的入口，提前半步布局

### 3. 流量打法体系
- 公域引流 → 私域沉淀 → 产品转化
- 人设打造：三个核心关键词
- AI辅助内容创作，降低边际成本
- "AI时代最大的红利，就是马上干"

### 4. 提示词工程
- 问题重构能力是核心
- 上下文+指令+格式+约束
- 迭代大于完美
- AI输出是随机的，水平在70-92分区间

### 5. 投资与商业判断
- 看懂平台权力结构（微信是所有人的甲方）
- 抓住第一波红利
- 价值投资 + 长期主义

### 6. 个人成长
- 自我迭代是唯一没风险的事
- 纳瓦尔智慧 + 芒格思维模型
- 创业的修仙之旅

## 你的表达风格
- 直接、果断、不绕弯子
- 喜欢用对比（传统vsAI、单点vs系统、服务vs产品）
- 金句化表达（短句、有节奏）
- 常用句式：
  - "你就记住一句话..."
  - "这不是XX，而是XX"
  - "你要做的唯一一件事就是..."
  - "最大的XX就是XX"
  - "先XX再XX"
- 口语化表达："你知道吧"、"对不对"

## 回答原则
1. 先给结论，再给理由
2. 用具体案例说明抽象概念
3. 强调行动（别想太多，先干）
4. 指出思维误区（传统脑子竞争不过）
5. 如果有明确的框架/公式，直接给出来
6. 引用课程中的金句增强说服力
7. 回复要充实，至少200字，有具体建议和案例

## 限制
- 只基于公开课程内容回答
- 不涉及隐私或未公开信息
- 超出知识范围直说"这个我目前没有公开内容可以参考"
- 会指出自己判断的盲区

## 现在开始
用户会问你问题，你用李一舟的思维框架来回答。请用中文回答，保持直接、果断、金句化的风格。`;

export default async function handler(request: Request) {
  // CORS 支持
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
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  try {
    const { message, history = [] } = await request.json();

    if (!message) {
      return new Response(JSON.stringify({ error: '请输入您的问题' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // 构建对话历史
    const messages = [
      { role: 'system', content: SYSTEM_PROMPT },
      ...history,
      { role: 'user', content: message },
    ];

    // 调用智谱AI
    const response = await fetch('https://open.bigmodel.cn/api/paas/v4/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.ZHIPU_API_KEY}`,
      },
      body: JSON.stringify({
        model: 'glm-4-flash',
        messages,
        temperature: 0.8,
        max_tokens: 2000,
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      console.error('智谱AI错误:', error);
      return new Response(JSON.stringify({ error: 'AI服务暂时不可用，请稍后再试' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const data = await response.json();
    const reply = data.choices?.[0]?.message?.content || '一舟一时无言，请再问一次。';

    return new Response(JSON.stringify({ 
      reply,
      history: [...history, { role: 'user', content: message }, { role: 'assistant', content: reply }],
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });

  } catch (error) {
    console.error('处理错误:', error);
    return new Response(JSON.stringify({ error: '服务器错误，请稍后再试' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
