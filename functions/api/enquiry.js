/**
 * Adult Toys Global B2B OEM/ODM Inquiry Backend Endpoint
 * Compatible with Cloudflare Pages Functions (/api/enquiry) and standard Fetch/Edge runtimes.
 *
 * Environment Variables supported when deployed in Cloudflare:
 * - WEBHOOK_URL: Optional DingTalk / Feishu / WeCom / Slack / Custom CRM webhook URL to push real-time notifications
 * - CRM_API_KEY: Optional Bearer token if forwarding to an external CRM API
 * - LEADS_KV: Optional Cloudflare KV namespace binding for persistent server-side storage of leads
 */

export async function onRequestPost(context) {
  const { request, env } = context;

  try {
    const contentType = request.headers.get('content-type') || '';
    let data = {};

    if (contentType.includes('application/json')) {
      data = await request.json();
    } else {
      const formData = await request.formData();
      data = Object.fromEntries(formData.entries());
      if (formData.has('models')) {
        data.models = formData.getAll('models');
      }
    }

    // Anti-spam honeypot check
    if (data.website_hp) {
      return new Response(JSON.stringify({ ok: true, spamFiltered: true }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const name = String(data.name || '').trim();
    const email = String(data.email || '').trim();
    const message = String(data.message || '').trim();

    if (!name || !email || !message) {
      return new Response(
        JSON.stringify({ ok: false, error: 'Missing required fields: name, email, or message.' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const record = {
      id: data.id || `RFQ-${Date.now().toString(36).toUpperCase()}`,
      source: data.source || '官网前台表单',
      name,
      email,
      company: String(data.company || '').trim(),
      phone: String(data.phone || '').trim(),
      type: String(data.type || 'OEM / Private Label'),
      market: String(data.market || data.country || '').trim(),
      quantity: String(data.quantity || '').trim(),
      models: Array.isArray(data.models) ? data.models : [],
      message,
      pageUrl: String(data.pageUrl || ''),
      submittedAt: data.submittedAt || new Date().toISOString()
    };

    // 1. Persistent storage in Cloudflare KV if bound
    if (env && env.LEADS_KV) {
      try {
        await env.LEADS_KV.put(`rfq:${record.id}`, JSON.stringify(record));
        const recentJson = await env.LEADS_KV.get('recent_lead_ids');
        const recentIds = recentJson ? JSON.parse(recentJson) : [];
        if (!recentIds.includes(record.id)) {
          recentIds.unshift(record.id);
          await env.LEADS_KV.put('recent_lead_ids', JSON.stringify(recentIds.slice(0, 200)));
        }
      } catch (kvErr) {
        console.error('KV storage error:', kvErr);
      }
    }

    // 2. Real-time Webhook Push (Feishu, DingTalk, WeCom, Zapier, Telegram, etc.)
    if (env && env.WEBHOOK_URL) {
      try {
        await fetch(env.WEBHOOK_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...(env.CRM_API_KEY ? { Authorization: `Bearer ${env.CRM_API_KEY}` } : {})
          },
          body: JSON.stringify({
            msg_type: 'text',
            content: {
              text: `🔔 [Adult Toys Global 收到新外贸询盘]\n单据编号: ${record.id}\n采购客户: ${record.name} (${record.company || '个人买家'})\n邮箱: ${record.email}\n电话/WhatsApp: ${record.phone || '未填'}\n目的国家: ${record.market || '未指明'}\n合作类型: ${record.type}\n采购数量: ${record.quantity || '500+ pcs'}\n意向机型: ${record.models.join(', ') || '全系'}\n客户需求: ${record.message}`
            },
            lead: record
          })
        });
      } catch (webhookErr) {
        console.error('Webhook push error:', webhookErr);
      }
    }

    return new Response(
      JSON.stringify({
        ok: true,
        id: record.id,
        receivedAt: record.submittedAt,
        message: 'Inquiry received successfully.'
      }),
      {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      }
    );
  } catch (err) {
    return new Response(
      JSON.stringify({ ok: false, error: 'Failed to process inquiry payload.' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}

export async function onRequestGet(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const token = url.searchParams.get('auth') || request.headers.get('authorization')?.replace('Bearer ', '');

  // Protect admin inquiries read endpoint
  if (token !== 'abc199704203975') {
    return new Response(JSON.stringify({ ok: false, error: 'Unauthorized: Admin token required.' }), {
      status: 401,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    });
  }

  const leads = [];
  if (env && env.LEADS_KV) {
    try {
      const recentJson = await env.LEADS_KV.get('recent_lead_ids');
      const recentIds = recentJson ? JSON.parse(recentJson) : [];
      for (const id of recentIds) {
        const item = await env.LEADS_KV.get(`rfq:${id}`);
        if (item) {
          leads.push(JSON.parse(item));
        }
      }
    } catch (kvErr) {
      console.error('KV retrieval error:', kvErr);
    }
  }

  return new Response(JSON.stringify({ ok: true, leads }), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    }
  });
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    }
  });
}
