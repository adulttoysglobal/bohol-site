/**
 * Automated IndexNow Submitter for adulttoysglobal.com
 * Immediately notifies Bing, Yandex, Naver, Seznam, and search engine crawlers of all 116+ site URLs.
 */
import fs from 'node:fs';
import path from 'node:path';

const HOST = 'adulttoysglobal.com';
const KEY = 'b8f4e29c017d45ba8933e9b08f4c21a5';
const KEY_LOCATION = `https://${HOST}/${KEY}.txt`;

// Extract URLs from built sitemap or generate from static list
async function getUrlList() {
  const sitemapPath = path.resolve('dist/sitemap-0.xml');
  if (fs.existsSync(sitemapPath)) {
    const xml = fs.readFileSync(sitemapPath, 'utf-8');
    const matches = [...xml.matchAll(/<loc>(https:\/\/adulttoysglobal\.com[^<]+)<\/loc>/g)];
    const urls = matches.map(m => m[1]);
    if (urls.length > 0) return urls;
  }
  
  // Fallback core list
  return [
    `https://${HOST}/`,
    `https://${HOST}/products/`,
    `https://${HOST}/manufacturing/`,
    `https://${HOST}/about/`,
    `https://${HOST}/partners/`,
    `https://${HOST}/contact/`,
    `https://${HOST}/rfq/`,
    `https://${HOST}/technology/`,
    `https://${HOST}/catalogue/`,
    `https://${HOST}/privacy/`,
    `https://${HOST}/support/`,
    `https://${HOST}/support/documentation/`,
    `https://${HOST}/journal/`,
    `https://${HOST}/guide/`
  ];
}

async function submitToIndexNow() {
  const urlList = await getUrlList();
  console.log(`Found ${urlList.length} URLs to submit to IndexNow...`);

  const payload = {
    host: HOST,
    key: KEY,
    keyLocation: KEY_LOCATION,
    urlList: urlList
  };

  const endpoints = [
    'https://api.indexnow.org/indexnow',
    'https://www.bing.com/indexnow'
  ];

  for (const endpoint of endpoints) {
    try {
      console.log(`Submitting to ${endpoint}...`);
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json; charset=utf-8'
        },
        body: JSON.stringify(payload)
      });
      console.log(`Endpoint ${endpoint} response: ${res.status} ${res.statusText}`);
    } catch (err) {
      console.error(`Error submitting to ${endpoint}:`, err.message);
    }
  }
}

submitToIndexNow();
