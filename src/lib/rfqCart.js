/**
 * B2B Multi-Product RFQ & Freight Calculation Cart Engine
 * Manages multi-product selections, quantities, packaging options, and quotation submissions.
 */

const STORAGE_KEY = 'bohol_rfq_cart';
const LEADS_KEY = 'bohol_rfq_leads';

export function getRfqCart() {
  if (typeof window === 'undefined') return [];
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    console.error('Failed to read RFQ cart:', e);
    return [];
  }
}

export function saveRfqCart(items) {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
    window.dispatchEvent(new CustomEvent('rfq-cart-updated', { detail: { items } }));
  } catch (e) {
    console.error('Failed to save RFQ cart:', e);
  }
}

export function addToRfqCart(item) {
  const current = getRfqCart();
  const idx = current.findIndex((i) => i.id === item.id);
  if (idx > -1) {
    // Increase quantity or update packaging
    current[idx].quantity = (current[idx].quantity || 50) + (item.quantity || 50);
    if (item.packaging) current[idx].packaging = item.packaging;
  } else {
    current.push({
      id: item.id,
      name: item.name,
      code: item.code || item.id,
      category: item.category || 'Adult Wellness',
      subCategory: item.subCategory || "Men's Toys",
      vendor: item.vendor || 'BOHOL Direct OEM',
      image: item.image || '/images/spotlight-big-mouth.webp',
      quantity: item.quantity || 50,
      packaging: item.packaging || '100% Discreet Box'
    });
  }
  saveRfqCart(current);
  return current;
}

export function removeFromRfqCart(id) {
  const current = getRfqCart().filter((i) => i.id !== id);
  saveRfqCart(current);
  return current;
}

export function updateRfqCartQty(id, qty) {
  const current = getRfqCart();
  const idx = current.findIndex((i) => i.id === id);
  if (idx > -1) {
    current[idx].quantity = Math.max(1, parseInt(qty, 10) || 1);
    saveRfqCart(current);
  }
  return current;
}

export function updateRfqCartPackaging(id, packaging) {
  const current = getRfqCart();
  const idx = current.findIndex((i) => i.id === id);
  if (idx > -1) {
    current[idx].packaging = packaging;
    saveRfqCart(current);
  }
  return current;
}

export function clearRfqCart() {
  saveRfqCart([]);
}

export function isItemInRfqCart(id) {
  return getRfqCart().some((i) => i.id === id);
}

/**
 * Builds a structured, professional English RFQ brief for email / clipboard / WhatsApp
 */
export function buildRfqSummaryText(formData, items) {
  const now = new Date().toISOString().replace('T', ' ').slice(0, 19) + ' UTC';
  const totalUnits = items.reduce((sum, item) => sum + (item.quantity || 0), 0);

  const lines = [
    '=================================================================',
    '  OFFICIAL B2B WHOLESALE & FREIGHT QUOTATION REQUEST (RFQ)',
    '=================================================================',
    `Date & Time: ${now}`,
    `Reference ID: ${formData.id || 'RFQ-' + Date.now().toString(36).toUpperCase()}`,
    '',
    '-----------------------------------------------------------------',
    '1. CONTACT & COMPANY INFORMATION',
    '-----------------------------------------------------------------',
    `Client Name:     ${formData.name || 'Not provided'}`,
    `Company / Store: ${formData.company || 'Private Buyer / Retailer'}`,
    `Business Email:  ${formData.email || 'Not provided'}`,
    `WhatsApp / Phone:${formData.phone || 'Not provided'}`,
    `Business Type:   ${formData.businessType || 'Wholesale Buyer'}`,
    '',
    '-----------------------------------------------------------------',
    '2. SHIPPING DESTINATION & FREIGHT CALCULATION',
    '-----------------------------------------------------------------',
    `Destination Country: ${formData.country || 'Global Delivery'}`,
    `City / State / Zip:  ${formData.destinationAddress || formData.zip || 'To be specified'}`,
    `Shipping Preference: ${formData.shippingMode || 'DDP Air Freight (Tax & Duty Included)'}`,
    `Urgency / Delivery:  ${formData.urgency || 'Standard Order Replenishment'}`,
    '',
    '-----------------------------------------------------------------',
    `3. SELECTED PRODUCTS FOR QUOTATION (${items.length} Models · ${totalUnits} Total Units)`,
    '-----------------------------------------------------------------'
  ];

  if (!items || items.length === 0) {
    lines.push('  No products specified. Please consult catalogue.');
  } else {
    items.forEach((item, idx) => {
      lines.push(
        `[${idx + 1}] ${item.name} (${item.code || item.id})`,
        `    Sub-Category: ${item.subCategory || item.category || 'General'}`,
        `    Target Quantity: ${item.quantity || 50} units`,
        `    Packaging Option: ${item.packaging || '100% Discreet Box'}`,
        `    Vendor / QC: ${item.vendor || 'BOHOL Direct OEM'}`,
        ''
      );
    });
  }

  lines.push(
    '-----------------------------------------------------------------',
    '4. OEM / ODM & CUSTOMIZATION REQUIREMENTS',
    '-----------------------------------------------------------------',
    `Customization Level: ${formData.customization || 'Standard Wholesale Units'}`,
    `Client Requirements: ${formData.message || 'Please provide FOB and DDP pricing, estimated shipping freight, gross weight/volume, and production lead time.'}`,
    '',
    '=================================================================',
    'This RFQ brief has been generated via BOHOL & 9Rabbit Official B2B System.',
    'Factory Response SLA: Within 12-24 hours with complete price breakdown & freight options.',
    '================================================================='
  );

  return lines.join('\n');
}

/**
 * Builds WhatsApp 1-Click Message URL
 */
export function buildRfqWhatsAppUrl(formData, items, phone = '+8618588583798') {
  const totalUnits = items.reduce((sum, item) => sum + (item.quantity || 0), 0);
  const prodSummary = items
    .map((item, i) => `${i + 1}. *[${item.code || item.id}] ${item.name}* - Qty: ${item.quantity} pcs (${item.packaging || 'Discreet Box'})`)
    .join('\n');

  const text = `*New Wholesale & Freight Quote Request (${formData.id || 'RFQ'})*

Hello BOHOL & 9Rabbit Team,
I would like to request an official wholesale price and shipping freight quotation for the following ${items.length} products (${totalUnits} total units):

${prodSummary}

*Destination for Freight Calculation:*
- Country: ${formData.country || 'USA'}
- Address / Zip: ${formData.destinationAddress || formData.zip || 'Not provided'}
- Preferred Shipping: ${formData.shippingMode || 'DDP Air (Tax Included)'}

*My Contact Details:*
- Name: ${formData.name || '-'}
- Company: ${formData.company || '-'}
- Email: ${formData.email || '-'}
- Phone/WhatsApp: ${formData.phone || '-'}
- Customization: ${formData.customization || 'Wholesale'}
- Notes: ${formData.message || 'Please quote FOB & DDP freight.'}

Looking forward to your quotation. Thank you!`;

  return `https://wa.me/${phone.replace(/[^0-9]/g, '')}?text=${encodeURIComponent(text)}`;
}

/**
 * Generates an RFQ ID in standard enterprise format: RFQ-YYYYMMDD-XXXX
 */
export function generateRfqId() {
  const now = new Date();
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, '0');
  const d = String(now.getDate()).padStart(2, '0');
  const rand = Math.floor(1000 + Math.random() * 9000);
  return `RFQ-${y}${m}${d}-${rand}`;
}

/**
 * Infers destination country name from international phone dialing prefix
 */
export function inferCountryFromPhone(phone) {
  const clean = String(phone || '').replace(/[^0-9]/g, '');
  if (!clean) return '';
  if (clean.startsWith('1')) return 'United States';
  if (clean.startsWith('44')) return 'United Kingdom';
  if (clean.startsWith('49')) return 'Germany';
  if (clean.startsWith('33')) return 'France';
  if (clean.startsWith('45')) return 'Denmark';
  if (clean.startsWith('39')) return 'Italy';
  if (clean.startsWith('34')) return 'Spain';
  if (clean.startsWith('31')) return 'Netherlands';
  if (clean.startsWith('81')) return 'Japan';
  if (clean.startsWith('82')) return 'South Korea';
  if (clean.startsWith('61')) return 'Australia';
  if (clean.startsWith('64')) return 'New Zealand';
  if (clean.startsWith('65')) return 'Singapore';
  if (clean.startsWith('971')) return 'United Arab Emirates';
  if (clean.startsWith('86')) return 'China';
  return '';
}

/**
 * Saves RFQ lead to local storage, triggers multi-tab sync, and notifies listeners
 */
export async function saveRfqLead(payload) {
  if (typeof window === 'undefined') return true;

  if (!payload.id || !payload.id.startsWith('RFQ-20')) {
    payload.id = generateRfqId();
  }
  if (!payload.submittedAt) {
    payload.submittedAt = new Date().toISOString();
  }
  if (!payload.country && payload.phone) {
    payload.country = inferCountryFromPhone(payload.phone) || 'United States';
  }

  try {
    const leads = JSON.parse(localStorage.getItem(LEADS_KEY) || '[]');
    leads.unshift(payload);
    localStorage.setItem(LEADS_KEY, JSON.stringify(leads.slice(0, 300)));
  } catch (e) {
    console.error('Failed to save RFQ lead to localStorage:', e);
  }

  // Cross-tab broadcast synchronization
  try {
    if (typeof BroadcastChannel !== 'undefined') {
      const bc = new BroadcastChannel('bohol_rfq_sync');
      bc.postMessage({ type: 'NEW_LEAD', lead: payload });
    }
  } catch (e) {}

  window.dispatchEvent(new CustomEvent('bohol_rfq_submitted', { detail: payload }));

  // Attempt backend API post (optional fallback)
  try {
    const res = await fetch('/api/enquiry', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.ok;
  } catch (e) {
    return true;
  }
}
