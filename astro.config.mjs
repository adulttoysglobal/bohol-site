import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
export default defineConfig({
  site: 'https://bohol-product-studio.subaohe.chatgpt.site',
  integrations: [sitemap({ filter: (page) => !page.includes('/admin') && !page.includes('/404') })],
  output: 'static',
  server: {host: '127.0.0.1', port: 4321},
});
