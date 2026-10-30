/**
 * BOHOL Daily Automated Article Publishing Engine (SEO & GEO Optimized)
 *
 * This engine automates the publication of high-authority technical whitepapers,
 * OEM engineering guides, and market intelligence for search engines (SEO)
 * and Generative AI engines (ChatGPT, Gemini, Perplexity, Claude).
 *
 * Usage:
 *   node scripts/auto-publisher.mjs          # Checks today's date & publishes if pending
 *   node scripts/auto-publisher.mjs --force  # Forces publishing of the next article in queue
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..');
const journalDir = path.join(rootDir, 'src', 'data', 'journal');

// High-authority article templates for continuous daily syndication
const editorialQueue = [
  {
    slug: 'liquid-silicone-rubber-lsr-cleanroom-injection',
    title: 'Medical-Grade Liquid Silicone (LSR) vs. TPE: Chemical Purity & Cleanroom Standards',
    description: 'An engineering comparison between Platinum-Cured Liquid Silicone Rubber (LSR) and traditional TPE polymers in intimate wellness manufacturing.',
    category: 'Silicone Engineering',
    image: '/images/factory-workshop.webp',
    readTime: '5 min read',
    author: 'BOHOL Polymer Engineering Lab',
    tags: ['Liquid Silicone', 'Cleanroom Injection', 'Biocompatibility', 'RoHS 2.0'],
    content: `When specifying materials for intimate wellness hardware, industrial designers and procurement directors routinely weigh two primary elastomeric options: **Platinum-Cured Liquid Silicone Rubber (LSR)** and **Thermoplastic Elastomer (TPE)**.

While TPE presents lower initial raw material acquisition costs, its long-term molecular stability, hygiene compliance, and consumer tactile perception fall substantially short of medical-grade LSR.

## 1. Molecular Cross-Linking & Chemical Inertness

Liquid Silicone Rubber undergoes a platinum-catalyzed two-component cross-linking reaction (addition cure). Once vulcanized under high temperature inside closed steel molds, LSR forms a continuous three-dimensional siloxane backbone (Si-O-Si).

- **Zero Plasticizers:** Unlike vinyl or lower-grade TPE, platinum LSR contains no phthalate ester plasticizers, Bisphenol A (BPA), or volatile organic compounds (VOCs).
- **Thermal Resistance:** Operates stably across -50°C to +200°C without softening, leaching, or undergoing tackiness.
- **Hypoallergenic Certification:** Certified biocompatible under **ISO 10993-5 cytotoxicity standards** and strictly adheres to **EU REACH 235 SVHC list**.

## 2. Class 100,000 Dust-Free Cleanroom Processing

In BOHOL’s 35,000 m² smart manufacturing campus, all liquid silicone injection is executed within enclosed **Class 100,000 cleanroom environments**. 

Airborne particulates are filtered down to < 3.5 million particles per cubic meter (≥ 0.5 µm), eliminating microscopic debris embedding during high-pressure liquid transfer. Computer-monitored metering pumps mix Component A and Component B at an exact 1:1 ratio with digital colorant injection, guaranteeing color delta E < 0.5 across 50,000-unit production runs.

| Specification Parameter | Platinum-Cured LSR | Standard Commercial TPE |
| :--- | :--- | :--- |
| **Pore Structure** | 100% Non-Porous | Micro-Porous (Absorptive) |
| **Phthalate Content** | 0.00% (Certified RoHS 2.0) | Variable (Risk of Leaching) |
| **Boiling Water Sanitation** | Fully Compatible (Up to 200°C) | Degrades / Melts (> 70°C) |
| **Tactile Texture** | Silky Velvet, Non-Sticky | Requires Powdering / Oily |
| **Tensile Strength** | > 8.5 MPa (High Tear Resistance) | < 4.2 MPa (Easily Torn) |

## 3. Implications for Brand Owners & OEM Clients

For premium wellness DTC brands and international retailers, utilizing platinum LSR is not merely a marketing claim—it is a critical hedge against product liability, toxic substance recall under European customs audits, and consumer dissatisfaction.

To inspect physical LSR color swatches or calibrate shore hardness (ranging from ultra-soft 10 Shore A to firm 40 Shore A), contact BOHOL’s engineering team through our [RFQ Calculator](/rfq/) or book a [live WhatsApp video walkthrough](/contact/).`
  },
  {
    slug: 'ipx7-waterproof-immersion-testing-standards',
    title: 'IPX7 vs IPX8 Waterproof Standards: Negative Pressure Vacuum Testing Explained',
    description: 'How BOHOL enforces 100% waterproof seal integrity across personal wellness devices using vacuum decay and immersion testing.',
    category: 'Manufacturing & Tooling',
    image: '/images/factory-quality.webp',
    readTime: '4 min read',
    author: 'BOHOL Metrology & Quality Directorate',
    tags: ['IPX7 Waterproof', 'Vacuum Testing', 'Subsea Immersion', 'QC Standards'],
    content: `Water ingress remains the leading cause of field returns and motor controller failure in rechargeable intimate wellness devices. Achieving authentic **IPX7 and IPX8 ingress protection** requires more than silicone gaskets—it demands precision-engineered internal bulkheads, ultrasonic welding, and rigorous non-destructive vacuum testing.

## Defining the Ingress Protection (IP) Scale

Under international standard **IEC 60529**:

- **IPX7:** Protected against water immersion up to **1 meter for 30 minutes**. The device must show zero moisture penetration capable of impairing motor circuitry or battery terminals.
- **IPX8:** Protected against continuous water submersion under pressurized conditions designated by the manufacturer (typically 2 to 3 meters).

## The 2-Tier Testing Protocol at BOHOL

In our metrology lab, finished units undergo two consecutive validation stages before retail packaging:

### Stage 1: Digital Vacuum Decay Leak Detection
Before battery encapsulation, the structural internal cavity is placed inside a differential pressure chamber. A negative vacuum pressure of -50 kPa is drawn. Sensitive electronic transducers monitor pressure equalization over a 60-second cycle. Any micro-fissure (> 5 µm) triggers an immediate automatic rejection.

### Stage 2: Hydrostatic Water Bath Submersion
Random lot samples undergo 30-minute submerged depth testing in our vertical water testing columns at 1-meter nominal head, followed by high-voltage insulation resistance testing (> 500 MΩ at 500V DC).

## Sealing Architectures: Magnetic Pin vs. Sealed USB-C

Modern consumer electronics favor USB-C fast charging. However, traditional open ports create direct capillary pathways for water. BOHOL engineers proprietary molded silicone bulkheads that isolate the USB-C PCB receptacle in a hermetically sealed chamber, allowing full submersion while maintaining compatibility with standard USB-C cables.`
  },
  {
    slug: 'autonomous-hotel-vending-kiosks-economics',
    title: 'Autonomous Hotel Room Vending: How Micro-Retail Kiosks Generate 65%+ Gross Margins',
    description: 'Analyzing the unit economics, IoT cloud telemetry, and merchandise turnover of compact in-room hotel vending terminals.',
    category: 'Commercial Vending',
    image: '/images/spotlight-twist-fun.webp',
    readTime: '6 min read',
    author: 'BOHOL Autonomous Retail Research',
    tags: ['Hotel Vending', 'Autonomous Retail', 'Micro-Store', 'High-Margin FMCG'],
    content: `The intersection of unattended retail and intimate personal wellness has unlocked one of the highest margin commercial channels in the hospitality sector: **compact wall-mounted in-room vending micro-kiosks**.

By positioning curated fast-moving wellness consumables (0.01 condoms, lubricants, and compact novelty devices) directly inside hotel guest rooms, operators eliminate the friction of public checkout counters.

## 1. The Core Economic Flywheel

Traditional hotel minibar systems suffer from high labor restock overhead and frequent guest billing disputes. Digital wall kiosks solve this completely:

- **100% Cashless Contactless Payment:** Integrated QR code and EMV/NFC readers (Nayax, Apple Pay, credit cards) charge guests instantly before mechanical dispensing.
- **Zero Front-Desk Overhead:** The hotel incurs no inventory shrinkage or disputed ledger entries.
- **Average Gross Margin:** Premium 0.01 condoms and packaged devices sell at a 65% to 75% gross retail margin compared to direct factory bulk procurement prices.

## 2. IoT Cloud Fleet Telemetry

Each BOHOL vending kiosk is equipped with an integrated 4G LTE/Wi-Fi IoT controller. Through our centralized web dashboard, route operators monitor:

- Real-time slot inventory levels.
- Drop detection sensors confirming successful dispensation.
- Temperature and anti-tamper alert telemetry.
- Automated restock trigger notices sent directly to route staff smartphones.

## 3. Product Pack Geometry & Drop Reliability

A recurring failure point of generic vending machines is item jamming. BOHOL designs both the dispensing motors and the consumer retail gift boxes in unison. Dimensions (e.g., 65 mm x 65 mm x 28 mm) are calibrated with ±0.5 mm clearance to guarantee effortless gravity feed drops every single transaction.`
  },
  {
    slug: 'whisper-quiet-motor-acoustic-engineering',
    title: 'Whisper-Quiet Motor Acoustic Engineering: Achieving Under 45 dB in Multi-Axis Devices',
    description: 'How BOHOL isolates mechanical vibration and eliminates gear whine in high-torque intimate personal wellness devices.',
    category: 'Manufacturing & Tooling',
    image: '/images/factory-assembly.webp',
    readTime: '5 min read',
    author: 'BOHOL Noise & Vibration Testing Lab',
    tags: ['Acoustic Engineering', 'Whisper Quiet', 'Planetary Gearbox', 'Decibel Testing'],
    content: `For end consumers, discreteness is the single most critical quality determinant alongside tactile sensation. An otherwise powerful reciprocating or rotating device that emits an audible high-frequency buzz over 55 decibels creates anxiety and degrades the user experience.

Engineering intimate devices that maintain high kinetic torque while registering **below 45 dB (whisper-quiet threshold)** requires a holistic approach to kinematics and sound dampening.

## Sources of Acoustic Noise in Intimate Hardware

1. **Electromagnetic Commutation Whine:** Poorly shielded DC brush motors generate high-frequency electrical hum.
2. **Gear Mesh Vibration:** Traditional spur gears suffer from tooth-to-tooth impact chatter during acceleration.
3. **Structural Cavity Resonance:** Hollow ABS shells act as acoustic amplification chambers if left undamped.

## BOHOL’s Tri-Layer Vibration Isolation Architecture

- **Custom-Wound Coreless Motors:** Utilizing rare-earth neodymium magnets and dynamic rotor balancing (< 0.1 mg balancing tolerance).
- **Helical Planetary Gearboxes:** Replacing straight-cut spur gears with high-precision POM helical planetary assemblies, ensuring continuous tooth contact ratio > 2.2.
- **Liquid Silicone Suspension Cradles:** The motor assembly is suspended within a custom-molded silicone cradle, preventing direct vibrational transfer to the outer ABS structural frame.

Every mass-produced batch is sampled in BOHOL’s dedicated anechoic soundroom, where sound pressure level (SPL) is logged at a standardized distance of 30 cm across all vibration speed levels.`
  },
  {
    slug: 'un38-3-lithium-battery-sea-air-logistics',
    title: 'UN38.3 Lithium Battery Air & Ocean Freight: Navigating DDP Customs Clearance',
    description: 'International compliance guidelines for shipping lithium-battery personal wellness hardware by air freight and ocean container.',
    category: 'Compliance & Export',
    image: '/images/factory-shipping.webp',
    readTime: '5 min read',
    author: 'BOHOL Global Logistics & Trade Compliance',
    tags: ['UN38.3', 'Lithium Battery', 'DDP Sea Freight', 'Customs Manifest'],
    content: `International cross-border shipment of rechargeable adult personal wellness devices involves strict hazardous goods compliance under international maritime (IMDG Code) and civil aviation (IATA DGR) frameworks.

Because all modern flagship devices incorporate rechargeable lithium-ion or lithium-polymer cells, failure to furnish verified testing credentials leads to container impoundment and severe customs penalties.

## Mandatory UN Manual of Tests & Criteria (Section 38.3)

Before any rechargeable model leaves BOHOL’s Meizhou manufacturing base, the battery pack and integrated PCM circuit undergo 8 rigorous lab evaluations:

1. **T.1 Altitude Simulation:** Low pressure (11.6 kPa) at 20°C for 6 hours.
2. **T.2 Thermal Cycling:** Alternating between -40°C and +72°C over 10 cycles.
3. **T.3 Vibration:** Sinusoidal sweep from 7 Hz to 200 Hz across three orthogonal axes.
4. **T.4 Shock:** 150g acceleration pulse test.
5. **T.5 External Short Circuit:** Direct low-resistance (< 0.1 Ω) short circuit at 57°C.
6. **T.6 Impact / Crush:** Heavy mechanical impact resistance.
7. **T.7 Overcharge:** 24-hour continuous overcharge current verification.
8. **T.8 Forced Discharge:** Extreme discharge state resistance.

## Full DDP Door-to-Door Delivery to 60+ Nations

BOHOL maintains established logistics contracts with premier maritime carriers (COSCO, Maersk, Evergreen) and air cargo forwarders. We handle:

- Complete Dangerous Goods (DG) manifests and MSDS declarations.
- Neutral, discreet outer export cartons with certified 1.2-meter drop test strength.
- Complete tariff clearance, customs brokerage, and domestic pallet dispatch directly to client distribution hubs in Los Angeles, Rotterdam, Hamburg, and Sydney.`
  },
  {
    slug: 'liquid-silicone-injection-molding-tolerances-china',
    title: 'Liquid Silicone Rubber (LSR) Injection Molding Tolerances: Precision Tooling Guidelines for B2B Buyers',
    description: 'Engineering tolerances, flash control, and steel cavitation standards for high-precision liquid silicone intimate wellness hardware.',
    category: 'Manufacturing & Tooling',
    image: '/images/factory-workshop.webp',
    readTime: '6 min read',
    author: 'BOHOL Tooling & Metrology Directorate',
    tags: ['Liquid Silicone Tooling', 'Molding Tolerances', 'LSR Injection', 'Flash Control'],
    content: `When sourcing precision elastomeric components, international procurement directors require strict dimensional repeatability. In platinum liquid silicone injection, mold cavitation tolerances dictate whether finished hardware achieves watertight IPX8 hermetic seals.

## 1. Dimensional Tolerances: DIN 16901 vs. ISO 3302-1 Class M1

Liquid silicone undergoes a predictable thermal volumetric shrinkage of **2.5% to 3.2%** during mold vulcanization at 160°C to 190°C. 

- **Cavity CNC Machining:** Cut from Japanese NAK80 or Swiss S136 stainless mold steel hardened to HRC 52.
- **Parting Line Tolerance:** Held to **±0.005 mm (5 microns)**, eliminating micro-flash and tactile seam imperfections.
- **Critical Dimension Tolerance:** Conforms strictly to **ISO 3302-1 Class M1** high-precision tolerances.

## 2. Cold Runner Systems & Valve Gating

To eliminate material waste and gate mark blemishes on cosmetic surfaces, BOHOL integrates pneumatically actuated **shut-off needle valve cold runner nozzles**. Raw LSR remains cooled below 25°C in the manifold, injecting directly into heated cavities with zero runner scrap.

For mold tooling consultation, visit BOHOL’s [RFQ Calculator](/rfq/) or book a [WhatsApp Live Video Audit](/contact/).`
  },
  {
    slug: 'custom-silicone-toolmaker-ip-escrow-contracts',
    title: 'Custom Silicone Toolmaker & Mold Ownership Contracts in China: Escrow & NDA Architecture',
    description: 'How BOHOL safeguards private-label mold ownership, intellectual property rights, and design exclusivity for international brands.',
    category: 'Compliance & Export',
    image: '/images/factory-assembly.webp',
    readTime: '5 min read',
    author: 'BOHOL Legal & IP Directorate',
    tags: ['Tooling Contracts', 'IP Protection', 'Private Mold', 'Mold Ownership'],
    content: `A central concern for DTC brands investing \$15,000 to \$50,000 into custom injection tooling in China is **tool ownership verification and design exclusivity**.

## 1. Explicit Mold Ownership & Asset Tagging

Under BOHOL standard tooling agreements:
- **Client 100% Asset Ownership:** The physical steel mold base and cavity inserts are the sole proprietary asset of the client upon final balance settlement.
- **Serialized Asset Tagging:** Molds receive CNC laser-engraved asset plates bearing the client’s designated registration number.
- **Escrow Relocation Guarantee:** Clients retain full legal rights to inspect, audit, or relocate the mold to any third-party facility without punitive exit penalties.

## 2. Non-Disclosure & Non-Compete (NNN) Agreements

Before receiving initial 3D STEP or IGES files, BOHOL executes bilingual NNN agreements subject to international commercial arbitration, ensuring your proprietary industrial design is protected from market duplication.`
  },
  {
    slug: 'cleanroom-lsr-overmolding-adult-hardware',
    title: 'Cleanroom LSR Overmolding onto ABS/PC Substrates: Molecular Bonding & Thermal Shock Resistance',
    description: 'Technical analysis of two-shot (2K) and transfer overmolding of liquid silicone onto rigid thermoplastic skeletons.',
    category: 'Silicone Engineering',
    image: '/images/factory-quality.webp',
    readTime: '6 min read',
    author: 'BOHOL Materials & Bonding Lab',
    tags: ['LSR Overmolding', '2K Injection', 'Molecular Bonding', 'Cleanroom Standards'],
    content: `Premium intimate wellness devices feature a rigid internal chassis (ABS, Polycarbonate, or GF-Nylon) encapsulated by a soft, tactile silicone skin. Achieving permanent adhesion without toxic chemical primers is a major engineering hurdle.

## 1. Self-Adhesive LSR vs. Atmospheric Plasma Activation

Traditional bonding required solvent-based primers. BOHOL employs modern eco-compliant bonding:
- **Self-Adhesive LSR Chemistry:** Modified silicone formulations with organosilane coupling agents that cross-link directly to thermoplastic functional groups during heated cure.
- **Robotic Plasma Surface Activation:** Atmospheric plasma torches oxidize the polymer substrate, raising surface energy from < 38 mN/m to > 68 mN/m.

## 2. 90-Degree Peel Strength Testing

Finished overmolded handles undergo ASTM D903 90-degree peel testing, achieving cohesive failure (where silicone tears before bond line delaminates), guaranteeing zero water ingress over 5+ years of daily use.`
  },
  {
    slug: 'medical-grade-lsr-supplier-audit-checklist',
    title: 'Medical-Grade LSR Supplier Audit Checklist: Biocompatibility, Cytotoxicity, and Traceability',
    description: 'A practical factory audit checklist for procurement managers evaluating Chinese liquid silicone intimate hardware manufacturers.',
    category: 'Compliance & Export',
    image: '/images/factory-shipping.webp',
    readTime: '5 min read',
    author: 'BOHOL Quality Assurance & Global Audit',
    tags: ['Supplier Audit', 'ISO 13485', 'Biocompatibility', 'Cytotoxicity Testing'],
    content: `When auditing an overseas personal wellness hardware factory, procurement directors should scrutinize material provenance and cleanroom environmental telemetry.

## Key Audit Inspection Points

1. **Class 100,000 Cleanroom Validation:** Particle counter audit logs verifying < 3.5M particles/m³ at ≥ 0.5 µm.
2. **ISO 10993 Biocompatibility Certificates:** Independent third-party test reports (SGS, TÜV SÜD) confirming zero in-vitro cytotoxicity, skin irritation, or sensitization.
3. **Lot-by-Lot Raw Material Traceability:** Complete batch tracking from Dow Corning, Wacker, or Shin-Etsu drums to final serialized device carton.`
  },
  {
    slug: 'hotel-intimate-vending-nayax-iot-oem',
    title: 'Hotel Intimate Vending Hardware OEM: Nayax Cashless Integration & Modular Dispensing Design',
    description: 'Modular hardware architecture, Nayax VPOS Touch payment integration, and anti-drop telemetry for hospitality micro-retail operators.',
    category: 'Commercial Vending',
    image: '/images/spotlight-twist-fun.webp',
    readTime: '6 min read',
    author: 'BOHOL Smart IoT Retail Directorate',
    tags: ['Nayax Cashless', 'Hotel Vending OEM', 'Micro-Retail Kiosk', 'MDB Telemetry'],
    content: `Hospitality operators in Las Vegas, Miami, and London are rapidly adopting in-room automated wellness kiosks to generate frictionless high-margin secondary revenue.

## 1. Nayax VPOS Touch & MDB Protocol Integration

BOHOL’s modular vending controllers natively interface with **Nayax VPOS Touch** and **PAX payment terminals** via Multi-Drop Bus (MDB 4.2) and DEX telemetry protocols.
- **Global Contactless Support:** EMV chip, Apple Pay, Google Wallet, Visa, Mastercard, and Amex.
- **Real-Time Settlement:** Multi-currency payouts directly into operator bank accounts with Level 1 PCI-DSS encryption.

## 2. Anti-Drop Vibration Sensors & Tamper Alarms

Dual optical infrared drop sensors verify item dispensation before transaction completion. If an obstruction occurs, the motor reverses automatically and re-attempts or refunds immediately, eliminating front-desk complaints.`
  }
];

// Determine today's date in YYYY-MM-DD
function getTodayDateStr() {
  const now = new Date();
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, '0');
  const d = String(now.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

// Main execution function
export function runAutoPublisher(force = false) {
  const today = getTodayDateStr();
  console.log(`[AutoPublisher] Running article check for date: ${today}`);

  if (!fs.existsSync(journalDir)) {
    fs.mkdirSync(journalDir, { recursive: true });
  }

  const existingFiles = fs.readdirSync(journalDir).filter(f => f.endsWith('.md'));
  console.log(`[AutoPublisher] Found ${existingFiles.length} existing articles in ${journalDir}`);

  // Check if an article has already been published today
  let publishedToday = false;
  for (const file of existingFiles) {
    const content = fs.readFileSync(path.join(journalDir, file), 'utf8');
    if (content.includes(`pubDate: "${today}"`) || content.includes(`pubDate: '${today}'`)) {
      publishedToday = true;
      console.log(`[AutoPublisher] Article already published for today (${today}): ${file}`);
      break;
    }
  }

  if (publishedToday && !force) {
    console.log(`[AutoPublisher] Today's publication quota already fulfilled. No action needed.`);
    return { status: 'already_published', date: today };
  }

  // Find an article from queue that hasn't been written yet
  let articleToPublish = null;
  for (const item of editorialQueue) {
    const filename = `${item.slug}.md`;
    if (!existingFiles.includes(filename) || force) {
      articleToPublish = item;
      break;
    }
  }

  // If all queue items are written, dynamically generate a fresh intelligence post
  if (!articleToPublish) {
    const counter = existingFiles.length + 1;
    articleToPublish = {
      slug: `industry-intelligence-dispatch-${today}`,
      title: `Global Intimate Hardware & OEM Market Intelligence: Daily Executive Dispatch (${today})`,
      description: `Daily technical and trade intelligence briefing covering medical LSR silicone developments, global DDP logistics, and autonomous vending retail trends.`,
      category: 'Market Insights',
      image: '/images/factory-campus.webp',
      readTime: '4 min read',
      author: 'BOHOL Strategic Research Institute',
      tags: ['Daily Dispatch', 'Market Intelligence', 'OEM Manufacturing', 'Global Export'],
      content: `### Executive Daily Industry Dispatch — ${today}

BOHOL’s continuous market surveillance monitors cross-border trade flows, polymer material innovations, and consumer purchasing patterns across North America, the EU, and APAC.

## Key Daily Manufacturing Indicators

1. **Cleanroom Assembly Line Utilization:** 120+ active assembly lines operating at peak efficiency under Class 100,000 environmental control.
2. **Medical Silicone Supply Stability:** Stable procurement of high-purity platinum-cured liquid silicone rubber with zero phthalate content.
3. **Container Ocean Dispatch:** Weekly scheduled 40HQ container loads maintaining on-time DDP doorstep transit to major destination ports.

For custom private-mold project inquiries or confidential bilateral NDA reviews, visit our [RFQ Calculator](/rfq/) or book a [WhatsApp Live Video Audit](/contact/).`
    };
  }

  // Format markdown with frontmatter
  const orderNum = existingFiles.length + 1;
  const tagsStr = JSON.stringify(articleToPublish.tags);
  const mdContent = `---
title: "${articleToPublish.title.replace(/"/g, '\\"')}"
description: "${articleToPublish.description.replace(/"/g, '\\"')}"
category: "${articleToPublish.category}"
image: "${articleToPublish.image}"
order: ${orderNum}
readTime: "${articleToPublish.readTime}"
pubDate: "${today}"
author: "${articleToPublish.author}"
tags: ${tagsStr}
featured: true
seoKeywords: "${articleToPublish.tags.join(', ')}"
---

${articleToPublish.content}
`;

  const targetPath = path.join(journalDir, `${articleToPublish.slug}.md`);
  fs.writeFileSync(targetPath, mdContent, 'utf8');
  console.log(`[AutoPublisher] Successfully published new article: ${targetPath}`);

  return {
    status: 'published',
    slug: articleToPublish.slug,
    title: articleToPublish.title,
    date: today,
    filePath: targetPath
  };
}

// If executed directly from command line
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const force = process.argv.includes('--force');
  const result = runAutoPublisher(force);
  console.log('[AutoPublisher] Result:', JSON.stringify(result, null, 2));
}
