import { dev } from 'astro';

async function start() {
  const server = await dev({
    server: {
      host: '0.0.0.0',
      port: 4321
    }
  });
  console.log(`BOHOL Astro dev server running at http://localhost:${server.address.port}`);
}

start().catch(err => {
  console.error('Failed to start dev server:', err);
  process.exit(1);
});
