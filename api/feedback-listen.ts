/**
 * 听懂再复述 - 意见反馈API
 * 存储用户反馈到 Vercel 函数日志
 */

export const config = {
  runtime: 'edge',
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
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  try {
    const feedback = await request.json();

    console.log('📝 听写工具新反馈:', JSON.stringify({
      type: feedback.type,
      detail: feedback.detail?.substring(0, 500),
      page: feedback.page,
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
