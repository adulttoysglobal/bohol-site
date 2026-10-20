/**
 * Adult Toys Global B2B OEM/ODM Inquiry & RFQ Backend Edge Endpoint
 * Cloudflare Pages Functions (/api/enquiry) and standard Fetch/Edge runtimes.
 *
 * Automatically forwards every quotation request and inquiry to:
 * - Direct Email: adulttoysglobal1997@gmail.com (via FormSubmit / Resend Edge dispatch)
 * - Cloudflare KV: Persistent server-side store (if LEADS_KV bound)
 * - Webhook / CRM: Feishu / DingTalk / WeCom / Slack / Zapier (if WEBHOOK_URL set)
 */

const TARGET_INBOX = 'adulttoysglobal1997@gmail.com';

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
    let message = String(data.message || '').trim();

    // If no message but has selected items or models, auto-generate standard quotation requirement
    const items = Array.isArray(data.items) ? data.items : [];
    const models = Array.isArray(data.models) ? data.models : [];
    
    if (!message) {
      if (items.length > 0) {
        message = `Wholesale RFQ calculation for ${items.length} products. Please quote FOB/DDP freight to ${data.country || data.destination || 'destination'}.`;
      } else if (models.length > 0) {
        message = `Inquiry for models: ${models.join(', ')}. Please provide catalog and OEM quotation.`;
      } else {
        message = 'Customer requested wholesale product catalog and pricing.';
      }
    }

    if (!name && !email && !data.phone) {
      return new Response(
        JSON.stringify({ ok: false, error: 'Please provide at least a contact email or phone number.' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const cleanPhone = String(data.phone || '').replace(/[^0-9]/g, '');
    const whatsappLink = cleanPhone ? `https://wa.me/${cleanPhone}` : 'N/A';

    // Format products list for email table
    let productsText = 'None specified';
    if (items.length > 0) {
      productsText = items.map((it, idx) => 
        `[${idx + 1}] ${it.name || it.code || it.id} (Qty: ${it.quantity || 1} pcs, Packaging: ${it.packaging || 'Standard'})`
      ).join('\n');
    } else if (models.length > 0) {
      productsText = models.join(', ');
    }

    const record = {
      id: data.id || `RFQ-${Date.now().toString(36).toUpperCase()}`,
      source: data.source || 'Website RFQ System',
      name: name || 'Prospective B2B Buyer',
      email: email || 'No email provided',
      company: String(data.company || '').trim() || 'Private Buyer / Retailer',
      phone: String(data.phone || '').trim() || 'Not provided',
      type: String(data.type || data.businessType || 'Wholesale / OEM Private Label'),
      market: String(data.market || data.country || '').trim() || 'Global',
      destinationAddress: String(data.destinationAddress || data.destination || data.zip || '').trim() || 'To be confirmed',
      shippingMode: String(data.shippingMode || 'DDP Air Freight (Tax Included)'),
      urgency: String(data.urgency || 'Standard Order'),
      quantity: String(data.quantity || (items.length ? items.reduce((s, i) => s + (i.quantity || 0), 0) + ' units' : '500+ pcs')),
      models,
      items,
      message,
      pageUrl: String(data.pageUrl || 'https://adulttoysglobal.com'),
      submittedAt: data.submittedAt || new Date().toISOString()
    };

    // 1. Dispatch Email via FormSubmit to adulttoysglobal1997@gmail.com
    try {
      await fetch(`https://formsubmit.co/ajax/${TARGET_INBOX}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Referer': 'https://adulttoysglobal.com',
          'Origin': 'https://adulttoysglobal.com'
        },
        body: JSON.stringify({
          _subject: `🔥 New B2B Wholesale RFQ [${record.id}] from ${record.name} (${record.market})`,
          _replyto: record.email,
          _template: 'table',
          _captcha: 'false',
          'Inquiry Reference ID': record.id,
          'Client Name': record.name,
          'Company / Store': record.company,
          'Business Email': record.email,
          'Phone / WhatsApp': record.phone,
          'Direct WhatsApp 1-Click': whatsappLink,
          'Destination Country': record.market,
          'Destination City / Address': record.destinationAddress,
          'Shipping Method': record.shippingMode,
          'Cooperation Type': record.type,
          'Target Quantity': record.quantity,
          'Selected Products / Models': productsText,
          'Buyer Note / Requirements': record.message,
          'Submission Source': record.source,
          'Page URL': record.pageUrl,
          'Submitted At (UTC)': record.submittedAt
        })
      });
    } catch (mailErr) {
      console.error('FormSubmit email forwarding error:', mailErr);
    }

    // 2. Optional Resend API Email Dispatch (if RESEND_API_KEY configured in Cloudflare Pages)
    if (env && env.RESEND_API_KEY) {
      try {
        await fetch('https://api.resend.com/emails', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${env.RESEND_API_KEY}`
          },
          body: JSON.stringify({
            from: 'BOHOL RFQ System <leads@adulttoysglobal.com>',
            to: [TARGET_INBOX],
            subject: `🔥 New B2B Wholesale RFQ [${record.id}] from ${record.name} (${record.market})`,
            html: `
              <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 650px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px;">
                <h2 style="color: #0f172a; margin-top: 0; border-bottom: 2px solid #2563eb; padding-bottom: 10px;">New B2B Wholesale Quotation Request</h2>
                <p><strong>Reference ID:</strong> ${record.id}</p>
                <p><strong>Client Name:</strong> ${record.name} (${record.company})</p>
                <p><strong>Email:</strong> <a href="mailto:${record.email}">${record.email}</a></p>
                <p><strong>Phone / WhatsApp:</strong> ${record.phone} &nbsp; <a href="${whatsappLink}" style="background: #25D366; color: #fff; padding: 3px 8px; border-radius: 4px; text-decoration: none; font-size: 12px;">Chat on WhatsApp</a></p>
                <p><strong>Country / Port:</strong> ${record.market} (${record.destinationAddress})</p>
                <p><strong>Shipping Mode:</strong> ${record.shippingMode}</p>
                <p><strong>Total Quantity:</strong> ${record.quantity}</p>
                <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 15px 0;" />
                <h3 style="color: #1e293b;">Selected Products:</h3>
                <pre style="background: #f8fafc; padding: 12px; border-radius: 6px; font-size: 13px; line-height: 1.5;">${productsText}</pre>
                <h3 style="color: #1e293b;">Buyer Message / Customization:</h3>
                <p style="background: #f1f5f9; padding: 12px; border-radius: 6px; font-size: 14px;">${record.message}</p>
                <p style="font-size: 12px; color: #64748b; margin-top: 20px;">Source: ${record.source} · URL: ${record.pageUrl}</p>
              </div>
            `
          })
        });
      } catch (resendErr) {
        console.error('Resend email error:', resendErr);
      }
    }

    // 3. Persistent storage in Cloudflare KV if bound
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

    // 4. Real-time Webhook Push (Feishu, DingTalk, WeCom, Zapier, Telegram, etc.)
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
              text: `🔔 [Adult Toys Global 收到新外贸询盘]\n单据编号: ${record.id}\n采购客户: ${record.name} (${record.company})\n邮箱: ${record.email}\n电话/WhatsApp: ${record.phone}\n目的国家: ${record.market}\n采购数量: ${record.quantity}\n意向产品: ${productsText}\n客户需求: ${record.message}\n直接回盘: ${whatsappLink}`
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
        message: 'Inquiry received successfully and dispatched to sales engineering team.'
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
    console.error('Error handling inquiry submission:', err);
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
