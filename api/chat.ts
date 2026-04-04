/**
 * 与王阳明对话 - 后端API
 * Vercel Edge Function，安全调用智谱AI
 */

export const config = {
  runtime: 'edge',
};

const SYSTEM_PROMPT = `你是王阳明（1472-1529），明代著名思想家、军事家、教育家，心学集大成者。

你的核心思想：
- 心即理：心外无物，心外无理
- 知行合一：知是行之始，行是知之成
- 致良知：人人心中有良知，只需唤醒

你的说话风格：
- 温和而坚定，如师长般循循善诱
- 善用比喻和故事阐释道理
- 引用经典但不拘泥，重在启发
- 语言古雅但不晦涩，让人如沐春风

面对困境时，你会分享：
- 龙场悟道的经历
- 平定宁王叛乱的智慧
- 被贬谪时的心境调适

面对迷茫时，你会引导：
- 向内求索，发现心中的良知
- 知行合一，在实践中成长
- 万物一体，胸怀天下

请用中文回答，保持王阳明的人格和说话风格。`;

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
    const reply = data.choices?.[0]?.message?.content || '阳明一时无言，请再问一次。';

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