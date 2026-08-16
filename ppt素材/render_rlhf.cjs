const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// 子进程渲染器：sharp 的 fontconfig 只认进程启动时的环境块，
// 因此在 spawn 时注入 FONTCONFIG_FILE（纯 ASCII 路径），
// 使 librsvg 能解析到思源黑体 CN（字体已复制到 Temp\dsh-shfonts）。
const worker = path.join(__dirname, 'render_rlhf_worker.cjs');
const env = {
  ...process.env,
  FONTCONFIG_FILE: 'C:\\Users\\23600\\AppData\\Local\\Temp\\dsh-shfonts\\fonts.conf',
  HOME: 'C:\\Users\\23600\\AppData\\Local\\Temp',
};

if (!fs.existsSync('C:\\Users\\23600\\AppData\\Local\\Temp\\dsh-shfonts\\fonts.conf')) {
  fs.copyFileSync(path.join(__dirname, 'fonts.conf'), 'C:\\Users\\23600\\AppData\\Local\\Temp\\dsh-shfonts\\fonts.conf');
}

const r = spawnSync(process.execPath, [worker], { env, stdio: 'inherit' });
if (r.status !== 0) process.exit(r.status ?? 1);
