import fs from 'fs';
import path from 'path';

const distDir = 'dist';
let htmlFiles = [];

function getHtmlFiles(dir) {
  if (!fs.existsSync(dir)) return;
  const list = fs.readdirSync(dir);
  for (const file of list) {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    if (stat && stat.isDirectory()) {
      getHtmlFiles(fullPath);
    } else if (file.endsWith('.html')) {
      htmlFiles.push(fullPath);
    }
  }
}

getHtmlFiles(distDir);
console.log(`[Audit] Total HTML pages in dist: ${htmlFiles.length}`);

let brokenLinks = [];
let totalLinks = 0;
let missingAltImages = 0;
let totalImages = 0;
let schemaCount = 0;
let canonicalCount = 0;
let openGraphCount = 0;

for (const file of htmlFiles) {
  const content = fs.readFileSync(file, 'utf8');
  
  // Check Canonical
  if (content.includes('rel="canonical"')) {
    canonicalCount++;
  }
  
  // Check OpenGraph
  if (content.includes('property="og:title"')) {
    openGraphCount++;
  }
  
  // Check Schema JSON-LD
  if (content.includes('application/ld+json')) {
    schemaCount++;
  }

  // Check Images & Alt text
  const imgMatches = content.match(/<img[^>]+>/g) || [];
  totalImages += imgMatches.length;
  for (const img of imgMatches) {
    if (!img.includes('alt="') || img.includes('alt=""')) {
      missingAltImages++;
    }
  }

  // Check Internal Links
  const linkMatches = content.match(/href="(\/[^"#?]+)"/g) || [];
  for (const l of linkMatches) {
    const raw = l.replace('href="', '').replace('"', '');
    if (raw.startsWith('/api') || raw.startsWith('//')) continue;
    totalLinks++;

    let target = raw;
    if (target.endsWith('/')) {
      target = path.join(target, 'index.html');
    } else if (!path.extname(target)) {
      target = path.join(target, 'index.html');
    }
    
    // Normalize target relative to dist
    const cleanTarget = target.startsWith('/') ? target.slice(1) : target;
    const targetFile = path.join(distDir, cleanTarget);
    
    if (!fs.existsSync(targetFile)) {
      brokenLinks.push({ source: path.relative(distDir, file), href: raw });
    }
  }
}

console.log(`[Audit] Total Internal Links: ${totalLinks}`);
console.log(`[Audit] Broken Links: ${brokenLinks.length}`);
if (brokenLinks.length > 0) {
  console.log(`[Audit] First 5 Broken Links:`, brokenLinks.slice(0, 5));
}
console.log(`[Audit] Pages with Canonical: ${canonicalCount} / ${htmlFiles.length}`);
console.log(`[Audit] Pages with OpenGraph: ${openGraphCount} / ${htmlFiles.length}`);
console.log(`[Audit] Pages with Schema JSON-LD: ${schemaCount} / ${htmlFiles.length}`);
console.log(`[Audit] Total Images: ${totalImages}, Missing Alt: ${missingAltImages}`);

// Test SSL and Response of live domain
console.log('\n[Audit] Testing Live Domain Response...');
try {
  const resp = await fetch('https://adulttoysglobal.com/', { headers: { 'User-Agent': 'Mozilla/5.0' } });
  console.log(`[Audit] Live Domain Status: ${resp.status} ${resp.statusText}`);
  const headers = Object.fromEntries(resp.headers.entries());
  console.log(`[Audit] Server: ${headers['server'] || 'Unknown'}`);
  console.log(`[Audit] Content-Type: ${headers['content-type']}`);
  console.log(`[Audit] Content-Encoding: ${headers['content-encoding'] || 'identity'}`);
  console.log(`[Audit] Cache-Control: ${headers['cache-control'] || 'none'}`);
} catch (e) {
  console.log(`[Audit] Live Domain Error: ${e.message}`);
}
