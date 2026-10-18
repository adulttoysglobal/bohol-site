import { getCollection } from 'astro:content';

export async function GET(context: any) {
  const articles = (await getCollection('journal')).sort((a, b) => {
    const dateA = new Date(a.data.pubDate || '2026-10-14').getTime();
    const dateB = new Date(b.data.pubDate || '2026-10-14').getTime();
    return dateB - dateA;
  });

  const site = context.site?.toString().replace(/\/$/, '') || 'https://bohol-product-studio.subaohe.chatgpt.site';

  const itemsXml = articles
    .map((article) => {
      const link = `${site}/journal/${article.id}/`;
      const pubDate = new Date(article.data.pubDate || '2026-10-14').toUTCString();
      const title = article.data.title.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      const desc = article.data.description.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      const category = article.data.category.replace(/&/g, '&amp;');

      return `    <item>
      <title>${title}</title>
      <link>${link}</link>
      <guid>${link}</guid>
      <description>${desc}</description>
      <pubDate>${pubDate}</pubDate>
      <category>${category}</category>
    </item>`;
    })
    .join('\n');

  const rssFeed = `<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>BOHOL Adult Wellness &amp; Smart Manufacturing Intelligence</title>
    <link>${site}/journal/</link>
    <description>Latest technical specifications, OEM silicone tooling insights, IPX7 waterproof standards, and commercial intimate wellness trends from BOHOL 35,000 m² cleanroom campus.</description>
    <language>en-US</language>
    <atom:link href="${site}/rss.xml" rel="self" type="application/rss+xml" />
    <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
${itemsXml}
  </channel>
</rss>`;

  return new Response(rssFeed, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=3600'
    }
  });
}
