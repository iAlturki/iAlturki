// Refreshes the numbers baked into the README art: <!-- dl:Repo -->n<!-- /dl -->
// (total release downloads) and <!-- kb:Repo -->n<!-- /kb --> (latest .exe size).
// Node 20+, no dependencies. Exits 0 without writing if any API call fails.
import fs from 'node:fs';

const OWNER = 'iAlturki';
const REPOS = ['MicMute', 'Nvidia_Instant_Replay_Fix', 'Look20', 'ytr-music'];
const FILES = ['README.md', ...fs.readdirSync('assets').filter(f => f.endsWith('.svg')).map(f => `assets/${f}`)];
const headers = { Accept: 'application/vnd.github+json', 'User-Agent': 'iAlturki-readme' };
if (process.env.GH_TOKEN) headers.Authorization = `Bearer ${process.env.GH_TOKEN}`;

async function get(url) {
  const r = await fetch(url, { headers });
  if (!r.ok) throw new Error(`${r.status} ${url}`);
  return r;
}
async function stats(repo) {
  let url = `https://api.github.com/repos/${OWNER}/${repo}/releases?per_page=100`, downloads = 0;
  while (url) {
    const r = await get(url);
    for (const rel of await r.json()) for (const a of rel.assets || []) downloads += a.download_count || 0;
    url = /<([^>]+)>;\s*rel="next"/.exec(r.headers.get('link') || '')?.[1];
  }
  const latest = await (await get(`https://api.github.com/repos/${OWNER}/${repo}/releases/latest`)).json();
  const exe = (latest.assets || []).find(a => a.name.toLowerCase().endsWith('.exe'));
  return { downloads, kb: exe ? Math.round(exe.size / 1000) : null };
}
const put = (text, key, value) =>
  text.replace(new RegExp(`(<!-- ${key} -->)[^<]*(<!-- /${key.split(':')[0]} -->)`, 'g'), `$1${value}$2`);

try {
  const all = {};
  for (const repo of REPOS) all[repo] = await stats(repo);
  let changed = 0;
  for (const file of FILES) {
    const before = fs.readFileSync(file, 'utf8');
    let text = before;
    for (const [repo, s] of Object.entries(all)) {
      text = put(text, `dl:${repo}`, new Intl.NumberFormat('en-US').format(s.downloads));
      if (s.kb) text = put(text, `kb:${repo}`, String(s.kb));
    }
    if (text !== before) { fs.writeFileSync(file, text); changed++; }
  }
  console.log(changed ? `${changed} file(s) updated` : 'no change');
} catch (e) {
  console.log('skipped:', e.message);
}
