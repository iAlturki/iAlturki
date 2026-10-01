// Refreshes the release numbers in README.md between <!-- key:Repo --> markers.
// Node 20+, no dependencies. Exits 0 without writing if any API call fails.
import fs from 'node:fs';

const OWNER = 'iAlturki';
const REPOS = ['MicMute', 'Nvidia_Instant_Replay_Fix', 'Look20'];
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
  return { downloads, tag: latest.tag_name, size: exe?.size };
}

const fmt = n => new Intl.NumberFormat('en-US').format(n);
const put = (text, key, value) =>
  text.replace(new RegExp(`(<!-- ${key} -->)[^<]*(<!-- /${key.split(':')[0]} -->)`, 'g'), `$1${value}$2`);

try {
  const file = 'README.md';
  const before = fs.readFileSync(file, 'utf8');
  let text = before;
  for (const repo of REPOS) {
    const s = await stats(repo);
    if (s.tag) text = put(text, `tag:${repo}`, s.tag);
    if (s.size) text = put(text, `size:${repo}`, fmt(s.size));
    text = put(text, `dl:${repo}`, fmt(s.downloads)); // Look20 has no dl marker, so its count is never written
  }
  const changed = text !== before;
  const asof = /<!-- asof -->([^<]*)<!-- \/asof -->/.exec(text)?.[1];
  const stale = !asof || Date.now() - Date.parse(asof) > 28 * 864e5;
  if (changed || stale) {
    const today = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' }).format(new Date());
    text = text.replace(/(<!-- asof -->)[^<]*(<!-- \/asof -->)/, `$1${today}$2`);
  }
  if (text !== before) fs.writeFileSync(file, text);
  console.log(text !== before ? 'README.md updated' : 'no change');
} catch (e) {
  console.log('skipped:', e.message);
}
