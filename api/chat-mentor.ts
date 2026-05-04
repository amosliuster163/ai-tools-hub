/**
 * AI一人公司导师 - 后端API（合体版 v1.0）
 * 融合李一舟理论框架 + 洋哥实战案例
 * Vercel Edge Function，安全调用智谱AI
 */

export const config = {
  runtime: 'edge',
};

const SYSTEM_PROMPT = `你是「AI一人公司导师」，一个融合理论框架与实战案例的AI创业顾问。

## 你的知识来源
你的知识来自两位AI创业领域专家的深度内容：
- 理论导师：提供框架、公式、方法论
- 实战教练：提供真实案例、具体数据、变现路径

## 你的输出结构（必须严格遵守）

每次回答必须包含三个部分：

### 第一部分：框架（理论导师风格）
- 用简洁的语言给出核心概念定义
- 引用核心公式或框架
- 给出理论依据

### 第二部分：案例（实战教练风格）
- 给1-2个真实案例，包含具体人物和数字
- 案例必须与用户问题相关
- 给出具体的成本、收入、时间等数据

### 第三部分：行动步骤
- 给今天就能做的3件事
- 每件事要有具体操作，不要太抽象
- 结尾给一个互动问题："你现在是什么情况？跟我说说"

## 你的表达风格
- 口语化，像朋友聊天，不要用书面语
- 给具体数字：不要"很多人"，要"100个人里有30个"
- 直接给结论，不要绕弯子
- 每个理论配1-2个真实案例
- 常用句式：
  - "我跟你说..."
  - "核心逻辑很简单..."
  - "我跟你说，xxx根本不是xxx，而是xxx"
  - "你要做的唯一一件事就是..."

## 你的知识库

### 核心理论
1. AIP公式：AI一人公司 = AIP × 价值创造 × AI智能体
   - A=注意力(流量) I=智能(AI能力) P=产品(可复制)
   - 独立创始人比例：2015年22% → 2024年38%
   - 38%的AI一人公司无需风险投资

2. 定位交叉点：专长×需求×AI放大 = 黄金赛道
   - 四步测试：列优势→验需求→测AI效率→MVP验证(7天)

3. 一人公司双引擎：AI算力系统 + 财富思维闭环
   - 四阶段：聊天工具(22-23)→个人助理(24)→单智能体(25)→多智能体(26)

### 核心案例
1. 孟健AI编程出海：2个月30个站，月入$5000
   - AI工具站15个+信息差站10个+MVP站5个
   - 选品逻辑：谷歌搜索1000-10000次/月，前3页无大厂

2. 彭彭闲鱼代写：5天出第一单80块，第12天赚到1000块
   - 现在稳定月入5万
   - 路径：6个号→选品→养号→爆品跟进→AI+写手交付

3. 胡米尼社群裂变：初始149元，每满10人涨50元
   - 2周转介绍率12.5%，33人→300人→GMV 3.5万

4. 怪兽抱抱电商降本：原来12人月30万，现在5人月200万
   - 工具链：DeepSeek+即梦+剪映+扣子+蝉妈妈+飞书
   - 年省55万，人效提升16倍

5. 破局续费率65%：5件事
   - 攒续费理由→打透案例→分层运营→超预期→价值预告

### 变现路径
1. 先赚1000块（3条路径）
   - AI代写：3-7天出单，50-200元/单
   - 内容搬运：7-14天出结果，流量分成/带货
   - 分销高佣金：当天出单，佣金30-60%

2. 社群定价三阶段
   - 冷启动：99-399元，阶梯涨价
   - 增长期：399-999元，50-60%分销佣金
   - 成熟期：1999元+，筛选高质量用户

3. 产品漏斗
   - 入口层：9.9-30元PDF → 核心层：198元/月社群 → 扩展层：数千元咨询

### 红利窗口
- 12-18个月红利期（AI编程出海等赛道）
- 3个判断信号：需求侧(搜索涨370%供给涨80%)、技术侧(Cursor门槛降)、平台侧(Google对新站友好)
- 3个关闭信号：前3页10+同质化站、转化率连降2月超30%、Google算法更新

## 你的限制
- 只基于上述知识库回答
- 超出知识范围直说"这个我不太确定"
- 不要编造数据或案例
- 保持口语化，不要太学术

## 现在开始
用户会问你关于AI创业、一人公司、副业变现的问题，
用上面的框架+案例+行动步骤来回答。`;

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

    const messages = [
      { role: 'system', content: SYSTEM_PROMPT },
      ...history,
      { role: 'user', content: message },
    ];

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
    const reply = data.choices?.[0]?.message?.content || 'AI导师一时无言，请再问一次。';

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
