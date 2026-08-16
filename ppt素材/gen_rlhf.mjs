import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const prompt = readFileSync(join(__dirname, 'rlhf_prompt.txt'), 'utf8').trim();

const seed = process.argv[2] ?? '1';
const width = 1536;
const height = 864;
const model = 'flux';

const url =
  'https://image.pollinations.ai/prompt/' +
  encodeURIComponent(prompt) +
  `?width=${width}&height=${height}&model=${model}&nologo=true&seed=${seed}`;

console.log('Model:', model, '| size:', `${width}x${height}`, '| seed:', seed);
console.log('Encoded URL length:', url.length);

const controller = new AbortController();
const timer = setTimeout(() => controller.abort(), 240000);
let res;
try {
  res = await fetch(url, { signal: controller.signal, headers: { 'User-Agent': 'dsh-image-gen/1.0' } });
} finally {
  clearTimeout(timer);
}

if (!res.ok) {
  console.error('HTTP', res.status, res.statusText);
  const body = await res.text().catch(() => '');
  console.error('Body (first 500):', body.slice(0, 500));
  process.exit(1);
}

const ct = res.headers.get('content-type') ?? '';
console.log('Content-Type:', ct);
const ext = ct.includes('jpeg') || ct.includes('jpg') ? 'jpg' : ct.includes('webp') ? 'webp' : 'png';

const buf = Buffer.from(await res.arrayBuffer());
if (buf.length < 1000) {
  console.error('Suspiciously small payload:', buf.length, 'bytes');
  console.error(buf.toString('utf8').slice(0, 500));
  process.exit(1);
}

const outDir = join(__dirname, 'figures');
mkdirSync(outDir, { recursive: true });
const out = join(outDir, `rlhf_flow_seed${seed}.${ext}`);
writeFileSync(out, buf);
console.log('SAVED', out, '|', buf.length, 'bytes');
