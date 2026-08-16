const fs = require('fs');
const path = require('path');
const { createRequire } = require('module');

const requireFromProfile = createRequire('C:/Users/23600/.dsh/profiles/package.json');
const sharp = requireFromProfile('sharp');

const dir = 'C:/Users/23600/Desktop/自迭代模型/ppt素材';
const svg = fs.readFileSync(path.join(dir, 'rlhf_flow.svg'), 'utf8');

(async () => {
  const rendered = sharp(Buffer.from(svg), { density: 144 });
  const meta = await rendered.metadata();
  console.log('Rendered dimensions:', meta.width, 'x', meta.height);
  const png = await rendered.resize(3200, 1800, { fit: 'fill' }).png().toBuffer();
  const out = path.join(dir, 'figures', 'rlhf_flow.png');
  fs.writeFileSync(out, png);
  const outMeta = await sharp(png).metadata();
  console.log('SAVED', out, '|', png.length, 'bytes |', outMeta.width + 'x' + outMeta.height);
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
