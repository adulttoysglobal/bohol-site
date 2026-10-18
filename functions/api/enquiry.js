/**
 * BOHOL B2B OEM/ODM Inquiry Backend Endpoint
 * Compatible with Cloudflare Pages Functions (/api/enquiry) and standard Fetch/Edge runtimes.
 *
 * Environment Variables supported when deployed:
 * - WEBHOOK_URL: Optional DingTalk / Feishu / Slack / Custom CRM webhook URL to push real-time notifications
 * - CRM_API_KEY: Optional Bearer token if forwarding to an external CRM API
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
      source: data.source || 'website',
      name,
      email,
      company: String(data.company || '').trim(),
      phone: String(data.phone || '').trim(),
      type: String(data.type || 'OEM / Private Label'),
      market: String(data.market || '').trim(),
      quantity: String(data.quantity || '').trim(),
      models: Array.isArray(data.models) ? data.models : [],
      message,
      pageUrl: String(data.pageUrl || ''),
      submittedAt: data.submittedAt || new Date().toISOString()
    };

    // Optional: Forward to external CRM / Feishu / DingTalk / Webhook if configured in env
    if (env && env.WEBHOOK_URL) {
      await fetch(env.WEBHOOK_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(env.CRM_API_KEY ? { Authorization: `Bearer ${env.CRM_API_KEY}` } : {})
        },
        body: JSON.stringify({
          msg_type: 'text',
          content: {
            text: `[BOHOL New Factory RFQ] ${record.id}\nName: ${record.name}\nEmail: ${record.email}\nCompany: ${record.company}\nPhone: ${record.phone}\nType: ${record.type}\nQty: ${record.quantity}\nModels: ${record.models.join(', ')}\nMessage: ${record.message}`
          },
          lead: record
        })
      });
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
