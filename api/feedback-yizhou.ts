/**
 * 李一舟数字分身 - 意见反馈API
 * 存储用户反馈到 localStorage + 后端日志
 */

export const config = {
  runtime: 'edge',
};

export default async function handler(request: Request) {
  // CORS
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
    const feedback = await request.json();

    // 记录到 Vercel 函数日志（可在 Vercel Dashboard 查看）
    console.log('📝 新反馈:', JSON.stringify({
      type: feedback.type,       // 'up' 或 'down'
      question: feedback.question?.substring(0, 100),
      detail: feedback.answer_hint?.substring(0, 200),
      time: feedback.timestamp,
    }));

    return new Response(JSON.stringify({ ok: true }), {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });

  } catch (error) {
    console.error('反馈处理错误:', error);
    return new Response(JSON.stringify({ error: '处理失败' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
