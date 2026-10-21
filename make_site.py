"""Build the public website (docs/index.html, served by GitHub Pages) from the claude.ai artifact (index.html).

The artifact talks to Claude through the claude.ai runtime. The public site instead calls the
Claude API straight from the browser with the visitor's own API key (official Anthropic SDK,
no server). Everything else - parsing, prompts, deck view, Anki export, quiz - is shared.

Run:  python3 make_site.py
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
src = (HERE / "index.html").read_text(encoding="utf-8")

SDK_VERSION = "0.131.0"
# The same app as a claude.ai artifact; visitors without API credits use it with their Claude plan.
CLAUDE_AI_URL = "https://claude.ai/artifact/AFmAvNHL7PmobSAQskKrmB"
CSP = (
    "default-src 'none'; "
    "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
    "connect-src https://api.anthropic.com; "
    "img-src 'self' data: blob:; "
    "style-src 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src https://fonts.gstatic.com data:; "
    "manifest-src 'self'; "
    "base-uri 'none'; form-action 'none'"
)


def replace(text, old, new, count=1):
    found = text.count(old)
    if found != count:
        sys.exit(f"make_site: expected {count}x, found {found}x:\n{old[:200]}")
    return text.replace(old, new)


def between(text, start, end):
    i = text.index(start)
    j = text.index(end, i)
    return i, j


# ---------- document skeleton ----------
style_start = src.index("<style>")
style_end = src.index("</style>") + len("</style>")
fonts = src[src.index('<link rel="preconnect"'):style_start]
style = src[style_start:style_end]
body = src[style_end:].lstrip("\n")

style = replace(style, "<style>\n", """<style>
html{-webkit-text-size-adjust:100%}
body{margin:0}
img{max-width:100%}
[hidden]{display:none!important}
a{color:var(--accent)}
.keybox{margin-bottom:20px}
.keybox > * + *{margin-top:12px}
.steps{margin:0;padding-left:1.3em;display:grid;gap:4px;max-width:72ch}
.key-row{display:flex;flex-wrap:wrap;gap:10px;align-items:flex-end}
.key-field{flex:1 1 280px;min-width:0}
.key-field input{width:100%;background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:8px 10px;font-family:var(--f-mono);font-size:14px}
.key-ready{display:flex;flex-wrap:wrap;gap:6px 18px;align-items:center;justify-content:space-between}
.foot{margin-top:28px;color:var(--muted);font-size:13px;max-width:80ch}
""")

head = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="no-referrer">
<meta name="description" content="Aus Vorlesungsfolien werden Anki-Karteikarten und Übungsquizze, mit deinem eigenen Claude-API-Schlüssel.">
<title>Vorlesungs-Lernstudio</title>
<meta name="theme-color" content="#2446A6">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<link rel="preconnect" href="https://api.anthropic.com" crossorigin>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
{fonts}{style}
</head>
<body>
"""

# ---------- markup ----------
body = replace(body, '  <div id="env-note" class="notice" role="status" hidden></div>\n', """  <section id="key-panel" class="panel keybox" aria-labelledby="key-h">
    <div id="key-setup">
      <div class="panel-head"><h2 id="key-h">Dein Claude-Zugang</h2></div>
      <p>Das Lernstudio arbeitet mit deinem eigenen API-Schlüssel von Anthropic. Die Seite hat keinen Server: Der Schlüssel bleibt in deinem Browser und wird nur direkt an api.anthropic.com gesendet.</p>
      <ol class="steps">
        <li>Lege ein Konto in der <a href="https://platform.claude.com" target="_blank" rel="noopener noreferrer">Claude Console</a> an.</li>
        <li>Kaufe unter <a href="https://platform.claude.com/settings/billing" target="_blank" rel="noopener noreferrer">Billing</a> Guthaben und setze ein Monatslimit, z. B. 10 $.</li>
        <li>Erstelle unter <a href="https://platform.claude.com/settings/keys" target="_blank" rel="noopener noreferrer">API Keys</a> einen Schlüssel und füge ihn hier ein.</li>
      </ol>
      <div class="key-row">
        <label class="key-field"><span class="lbl">API-Schlüssel</span><input type="password" id="api-key" autocomplete="off" spellcheck="false" placeholder="sk-ant-…"></label>
        <button type="button" id="key-save" class="btn primary">Schlüssel prüfen und nutzen</button>
      </div>
      <label class="choice"><input type="checkbox" id="key-remember"><span>Auf diesem Gerät merken<small>Nur auf deinem eigenen Gerät. Sonst vergisst der Browser den Schlüssel, wenn du den Tab schließt.</small></span></label>
      <p id="key-msg" class="msg" role="status"></p>
      <p class="hint">Kein API-Guthaben? Mit einem Konto bei claude.ai kannst du die <a href="__CLAUDE_AI_URL__" target="_blank" rel="noopener noreferrer">Version für claude.ai</a> nutzen. Sie läuft über dein Claude-Abo statt über einen API-Schlüssel.</p>
      <details class="method">
        <summary>Was kostet das?</summary>
        <p>Anthropic rechnet direkt über dein Konto ab, nach verbrauchten Tokens. Grobe Schätzung für eine Vorlesung mit rund 50 Folien: Karteikarten kosten etwa 0,50–1 $ mit „Gründlich“ (Claude Opus 5.5) und 0,25–0,50 $ mit „Schnell“ (Claude Sonnet 5.5), mit Folienbildern etwas mehr. Ein Quiz mit 15 Fragen kostet etwa 0,15–0,45 $. Nach jedem Durchlauf zeigt das Lernstudio die ungefähren Kosten an. Ein Monatslimit in der Console verhindert, dass mehr ausgegeben wird als geplant.</p>
      </details>
    </div>
    <div id="key-ready" class="key-ready" hidden>
      <span><b>Claude-Zugang aktiv</b> <span id="key-mask" class="mono muted"></span></span>
      <span id="usage-line" class="mono muted"></span>
      <span class="actions"><button type="button" id="key-change" class="btn small ghost">Schlüssel ändern</button><button type="button" id="key-forget" class="btn small ghost">Schlüssel entfernen</button></span>
    </div>
  </section>
""")
body = replace(body, "    </main>\n  </div>\n</div>\n", """    </main>
  </div>
  <footer class="foot">
    <p>Das Lernstudio läuft komplett in deinem Browser. Material, Karten und Quizze bleiben in diesem Browser gespeichert. An Anthropic gehen nur die Inhalte, aus denen Claude Karten und Fragen erstellt (Folientext und auf Wunsch Folienbilder), zusammen mit deinem API-Schlüssel.</p>
  </footer>
</div>
""")
body = replace(body, '<option value="complex">Gründlich (stärkstes Modell)</option>', '<option value="complex">Gründlich (Claude Opus 5.5)</option>', 2)
body = replace(body, '<option value="default">Schnell</option>', '<option value="default">Schnell (Claude Sonnet 5.5, etwa halbe Kosten)</option>', 2)
body = replace(body, "Du bekommst eine .zip mit der .apkg-Datei darin. Entpacke sie per Doppelklick und öffne dann die .apkg. Anki importiert das Deck mit Unterdeck, Schlagwörtern und Folienangabe.",
               "Du bekommst eine .apkg-Datei. Ein Doppelklick öffnet sie in Anki und importiert das Deck mit Unterdeck, Schlagwörtern und Folienangabe.")

# ---------- Claude connection ----------
i, j = between(body, "/* ---------- Claude runtime ---------- */", "async function runPool(")
runtime = body[i:j]
parse_helpers = runtime[runtime.index("function parseLine(line) {"):runtime.index("// Streams a reply written as one JSON object per line")]
new_runtime = """/* ---------- Claude API (eigener Schlüssel, direkt aus dem Browser) ---------- */
const SDK_URL = 'https://cdn.jsdelivr.net/npm/@anthropic-ai/sdk@__SDK_VERSION__/+esm';
const API_BASE = undefined; // undefined: the SDK's default, https://api.anthropic.com
const MODELS = { complex: 'claude-opus-5-5', default: 'claude-sonnet-5-5' };
// US dollars per million tokens (input, output): Claude API list prices, October 2026.
const PRICES = { 'claude-opus-5-5': [4, 20], 'claude-sonnet-5-5': [2, 10], 'claude-opus-5': [5, 25], 'claude-opus-4-8': [5, 25], 'claude-sonnet-5': [2, 10] };
// The API accepts many images per request; slide chunks stay at 6-12 slides anyway.
const caps = { imageMax: 20 };
const usage = { cost: 0 };
// Over the API every section of a typical lecture can run at once; the SDK waits and retries
// on rate limits and overloads by itself (new accounts start with lower limits).
const POOL = 8;
// Card writing is extraction, so little thinking is needed; checks and distractors get a bit more.
const EFFORT = { cards: 'low', coverage: 'medium', quiz: 'medium', grade: 'low' };
const FATAL = new Set(['no_key', 'auth', 'permission', 'spend_cap', 'billing', 'model']);
function errText(e) {
  if (e instanceof Error) return e.message;
  const map = {
    no_key: 'Trage zuerst oben deinen Claude-API-Schlüssel ein.',
    auth: 'Anthropic hat den API-Schlüssel abgelehnt. Prüfe ihn oder erstelle in der Claude Console einen neuen.',
    permission: 'Dieser API-Schlüssel darf die Anfrage nicht ausführen.',
    model: 'Das Modell ist für dein API-Konto nicht verfügbar.',
    spend_cap: 'Das monatliche Ausgabenlimit deines API-Kontos ist erreicht. Du kannst es in der Claude Console unter Billing erhöhen.',
    billing: 'Es gibt ein Problem mit der Abrechnung deines API-Kontos. Prüfe Guthaben und Zahlungsdaten in der Claude Console.',
    bad_request: 'Anthropic hat die Anfrage abgelehnt.',
    rate_limited: 'Zu viele Anfragen in kurzer Zeit. Warte eine Minute und klicke dann auf „Erneut versuchen“.',
    overloaded: 'Claude ist gerade überlastet. Versuche es in ein paar Minuten erneut.',
    network: 'Keine Verbindung zu Claude. Prüfe deine Internetverbindung und klicke auf „Erneut versuchen“.',
    invalid_json: 'Claudes Antwort war unvollständig. Klicke auf „Erneut versuchen“.',
    refused: 'Claude hat diesen Abschnitt nicht bearbeitet. Prüfe den Inhalt und deine Anforderungen.',
    empty_completion: 'Claude hat keine Antwort geliefert. Klicke auf „Erneut versuchen“.',
    upstream_error: 'Die Verbindung zu Claude wurde unterbrochen. Klicke auf „Erneut versuchen“.',
    bad_shape: 'Claudes Antwort hatte nicht das erwartete Format. Klicke auf „Erneut versuchen“.',
  };
  const text = map[e && e.code] || map.upstream_error;
  // Anthropic's own message says what to fix for these (for example a low credit balance).
  return e && e.detail && ['bad_request', 'permission', 'billing'].includes(e.code) ? `${text} ${e.detail}` : text;
}
let Anthropic = null, client = null, clientKey = '', memKey = '';
const KEY_NAME = 'lernstudio.apiKey';
function readKey() {
  let k = memKey;
  try { k = k || sessionStorage.getItem(KEY_NAME) || localStorage.getItem(KEY_NAME) || ''; } catch {}
  return k;
}
function writeKey(k, remember) {
  memKey = k;
  try { sessionStorage.removeItem(KEY_NAME); localStorage.removeItem(KEY_NAME); (remember ? localStorage : sessionStorage).setItem(KEY_NAME, k); } catch {}
}
function forgetKey() {
  memKey = ''; client = null; clientKey = '';
  try { sessionStorage.removeItem(KEY_NAME); localStorage.removeItem(KEY_NAME); } catch {}
}
const hasKey = () => !!readKey();
async function loadSdk() {
  if (!Anthropic) {
    try { Anthropic = (await import(SDK_URL)).default; }
    catch { throw new Error('Die Anthropic-Bibliothek konnte nicht geladen werden. Prüfe deine Internetverbindung.'); }
  }
  return Anthropic;
}
function newClient(apiKey, maxRetries) {
  return new Anthropic({ apiKey, baseURL: API_BASE, dangerouslyAllowBrowser: true, maxRetries });
}
async function getClient() {
  const key = readKey();
  if (!key) throw { code: 'no_key' };
  await loadSdk();
  if (!client || clientKey !== key) { client = newClient(key, 3); clientKey = key; }
  return client;
}
// Maps SDK errors to the codes the page shows; most specific class first.
function apiError(e) {
  const A = Anthropic;
  if (!A || !(e instanceof A.APIError)) return e;
  const body = e.error && e.error.error;
  const detail = (body && body.message) || '';
  if (e instanceof A.APIUserAbortError) return { code: 'cancelled' };
  if (e instanceof A.APIConnectionError) return { code: 'network' };
  if (e instanceof A.AuthenticationError) return { code: 'auth' };
  if (e instanceof A.PermissionDeniedError) return { code: 'permission', detail };
  if (e instanceof A.NotFoundError) return { code: 'model' };
  if (e instanceof A.RateLimitError) return { code: body && body.details && body.details.error_code === 'enforced_spend_limit_reached' ? 'spend_cap' : 'rate_limited' };
  if (e instanceof A.BadRequestError) return { code: 'bad_request', detail };
  if (e instanceof A.InternalServerError) return { code: e.status === 529 ? 'overloaded' : 'upstream_error' };
  return { code: e.status === 402 ? 'billing' : 'upstream_error', detail };
}
const fmtUsd = v => (v < 0.01 ? '< 0,01' : v.toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })) + ' $';
function addUsage(msg) {
  const u = msg && msg.usage;
  if (!u) return;
  // With a server-side fallback, usage.iterations lists every attempt with its own model.
  const parts = Array.isArray(u.iterations) && u.iterations.length ? u.iterations : [u];
  for (const p of parts) {
    const [pin, pout] = PRICES[p.model || msg.model] || PRICES['claude-opus-5-5'];
    const inTok = (p.input_tokens || 0) + (p.cache_creation_input_tokens || 0) * 1.25 + (p.cache_read_input_tokens || 0) * 0.1;
    usage.cost += (inTok * pin + (p.output_tokens || 0) * pout) / 1e6;
  }
  paintUsage();
}
const costNote = since => usage.cost - since > 0 ? ` · ca. ${fmtUsd(usage.cost - since)}` : '';
async function blobToBase64(b) {
  const buf = new Uint8Array(await b.arrayBuffer());
  let s = '';
  for (let i = 0; i < buf.length; i += 0x8000) s += String.fromCharCode.apply(null, buf.subarray(i, i + 0x8000));
  return btoa(s);
}
// One streamed Messages API call. Text arrives at onText piece by piece.
async function callClaude(prompt, { tier = 'complex', effort, signal, images, onText, maxTokens = 64000 } = {}) {
  const c = await getClient();
  const content = [];
  for (const b of images || []) content.push({ type: 'image', source: { type: 'base64', media_type: 'image/jpeg', data: await blobToBase64(b) } });
  content.push({ type: 'text', text: prompt });
  const params = {
    model: MODELS[tier] || MODELS.complex,
    max_tokens: maxTokens,
    messages: [{ role: 'user', content }],
    // If a safety classifier declines, the API retries on the model Anthropic recommends for that case.
    betas: ['server-side-fallback-2026-07-01'],
    fallbacks: 'default',
  };
  if (effort) params.output_config = { effort };
  let msg;
  try {
    const stream = c.beta.messages.stream(params, { signal });
    if (onText) stream.on('text', delta => onText(delta));
    msg = await stream.finalMessage();
  } catch (e) {
    if (signal && signal.aborted) throw { code: 'cancelled' };
    throw apiError(e);
  }
  addUsage(msg);
  if (msg.stop_reason === 'refusal') throw { code: 'refused' };
  const text = msg.content.filter(b => b.type === 'text').map(b => b.text).join('');
  if (!text.trim()) throw { code: 'empty_completion' };
  return { text, truncated: msg.stop_reason === 'max_tokens' };
}
function parseObject(text) {
  for (const t of [text, (text.match(/```(?:json)?\\s*([\\s\\S]*?)```/) || [])[1], text.slice(text.indexOf('{'), text.lastIndexOf('}') + 1)]) {
    if (!t) continue;
    try { const v = JSON.parse(t); if (v && typeof v === 'object' && !Array.isArray(v)) return v; } catch {}
  }
  return null;
}
async function askJSON(prompt, o = {}) {
  const { text } = await callClaude(prompt, Object.assign({ maxTokens: 16000 }, o));
  const v = parseObject(text);
  if (!v) throw { code: 'invalid_json' };
  return v;
}
__PARSE_HELPERS__// Streams a reply written as one JSON object per line and hands each object over as soon as its line is complete.
async function streamItems(prompt, { onItem, ...o }) {
  let pending = '', count = 0;
  // A line may also hold the older single-object form ({"cards":[…]}); unpack it into items.
  const expand = v => {
    for (const k of ['cards', 'add', 'questions']) if (Array.isArray(v[k])) return v[k].filter(x => x && typeof x === 'object').concat(Array.isArray(v.duplicates) ? [{ duplicates: v.duplicates }] : []);
    return [v];
  };
  const take = line => { const v = parseLine(line); if (v) expand(v).forEach(x => { count++; onItem(x); }); };
  let res;
  try {
    res = await callClaude(prompt, Object.assign({}, o, { onText: delta => { pending += delta; const lines = pending.split('\\n'); pending = lines.pop(); lines.forEach(take); } }));
  } catch (e) {
    if (e instanceof Error) throw e;
    throw Object.assign({}, e, { count });
  }
  if (pending.trim()) take(pending);
  if (!count) parseWhole(res.text).forEach(v => { count++; onItem(v); });
  return { truncated: res.truncated, count };
}
async function saveFile(filename, data) {
  const blob = data instanceof Blob ? data : new Blob([data], { type: typeof data === 'string' ? 'application/json' : 'application/octet-stream' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = filename; a.rel = 'noopener';
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 60000);
  return { status: 'saved' };
}
/* ---------- Schlüssel-Verwaltung ---------- */
function maskKey(k) { return k.length > 14 ? k.slice(0, 10) + '…' + k.slice(-4) : '…'; }
function paintUsage() {
  const el = $('#usage-line');
  if (el) el.textContent = usage.cost ? `Verbrauch in dieser Sitzung: ca. ${fmtUsd(usage.cost)}` : 'Noch kein Verbrauch in dieser Sitzung';
}
function paintKey() {
  const k = readKey();
  $('#key-setup').hidden = !!k;
  $('#key-ready').hidden = !k;
  $('#key-mask').textContent = k ? maskKey(k) : '';
  paintUsage();
}
function focusKey() {
  $('#key-setup').hidden = false;
  $('#key-panel').scrollIntoView({ block: 'start' });
  $('#api-key').focus();
}
async function saveKey() {
  const input = $('#api-key'), msg = $('#key-msg'), btn = $('#key-save');
  const k = input.value.trim();
  msg.className = 'msg';
  if (!k) { msg.className = 'msg err'; msg.textContent = 'Füge zuerst deinen API-Schlüssel ein.'; return; }
  if (!/^sk-ant-/.test(k)) { msg.className = 'msg err'; msg.textContent = 'Das sieht nicht nach einem Claude-API-Schlüssel aus. Er beginnt mit „sk-ant-“.'; return; }
  btn.disabled = true; msg.textContent = 'Schlüssel wird geprüft …';
  try {
    await loadSdk();
    // Looking up the model is free and confirms both the key and access to the model.
    await newClient(k, 1).models.retrieve(MODELS.complex);
    writeKey(k, $('#key-remember').checked);
    client = null;
    input.value = ''; msg.textContent = '';
    paintKey();
  } catch (e) {
    msg.className = 'msg err'; msg.textContent = errText(apiError(e));
  } finally { btn.disabled = false; }
}
"""
new_runtime = new_runtime.replace("__SDK_VERSION__", SDK_VERSION).replace("__PARSE_HELPERS__", parse_helpers)
body = body[:i] + new_runtime + body[j:]

body = replace(body, """  const img = $('#opt-images');
  const canSend = caps.imageMax > 0;
  img.disabled = !anyPdf || (caps.ready && !canSend);
  if (img.disabled) img.checked = false;
  $('#opt-images-hint').textContent = caps.ready && !canSend && caps.sample
    ? 'In dieser Ansicht können keine Bilder an Claude gesendet werden.'
    : anyPdf ? 'Liest auch Diagramme, Abbildungen und gescannte Folien. Langsamer und verbraucht mehr Nutzung.' : 'Nur für PDFs, die in dieser Sitzung geladen wurden.';""",
"""  const img = $('#opt-images');
  img.disabled = !anyPdf;
  if (img.disabled) img.checked = false;
  $('#opt-images-hint').textContent = anyPdf ? 'Liest auch Diagramme, Abbildungen und gescannte Folien. Langsamer und etwas teurer.' : 'Nur für PDFs, die in dieser Sitzung geladen wurden.';""")
body = replace(body, "  if (!caps.sample) { msg.textContent = errText({ code: 'unavailable' }); return; }", "  if (!hasKey()) { msg.textContent = errText({ code: 'no_key' }); focusKey(); return; }", 6)
body = replace(body, "  if (!caps.sample) { $('#gen-cards-msg').textContent = errText({ code: 'unavailable' }); return; }", "  if (!hasKey()) { $('#gen-cards-msg').textContent = errText({ code: 'no_key' }); focusKey(); return; }")

# cost after each run
body = replace(body, "  const started = Date.now();\n", "  const started = Date.now(), cost0 = usage.cost;\n")
body = replace(body, "Karten in ${secs < 90 ? secs + ' s' : Math.round(secs / 6) / 10 + ' min'}.`;", "Karten in ${secs < 90 ? secs + ' s' : Math.round(secs / 6) / 10 + ' min'}${costNote(cost0)}.`;")
body = replace(body, "let quizCtl = null, quizJobs = [], pendingQuestions = [];", "let quizCtl = null, quizJobs = [], pendingQuestions = [], quizCost0 = 0;")
body = replace(body, "  quizCtl = new AbortController();\n  setQuizBusy(true); paintQuizProgress();", "  quizCtl = new AbortController(); quizCost0 = usage.cost;\n  setQuizBusy(true); paintQuizProgress();")
body = replace(body, "fehlgeschlagen.` : n ? 'Fertig.' : '';", "fehlgeschlagen.` : n ? `Fertig${costNote(quizCost0)}.` : '';")

# downloads: a real .apkg instead of a .zip wrapper
body = replace(body, """    const base = fileSafe(deckName.split('::').pop());
    const outer = new window.JSZip();
    outer.file(base + '.apkg', apkg);
    const blob = await outer.generateAsync({ type: 'blob', compression: 'STORE' });
    msgEl.textContent = 'Bitte bestätige das Speichern.';
    await saveFile(base + '.zip', blob);
    msgEl.className = 'msg ok';
    msgEl.textContent = `Gespeichert: ${base}.zip mit ${cards.length} Karten. Entpacken und die .apkg mit Anki öffnen.`;""",
"""    const base = fileSafe(deckName.split('::').pop());
    await saveFile(base + '.apkg', new Blob([apkg], { type: 'application/octet-stream' }));
    msgEl.className = 'msg ok';
    msgEl.textContent = `Gespeichert: ${base}.apkg mit ${cards.length} Karten. Ein Doppelklick öffnet sie in Anki.`;""")
body = replace(body, "  msg.className = 'msg'; msg.textContent = 'Bitte bestätige das Speichern.';\n", "  msg.className = 'msg';\n")

# start-up and key controls
body = replace(body, "  initCaps();\n", "  paintKey();\n  idle(() => loadSdk().catch(() => {}));\n")
body = replace(body, "function bind() {\n", """function bind() {
  $('#key-save').addEventListener('click', saveKey);
  $('#api-key').addEventListener('keydown', e => { if (e.key === 'Enter') saveKey(); });
  $('#key-change').addEventListener('click', () => { $('#key-ready').hidden = true; focusKey(); });
  $('#key-forget').addEventListener('click', e => armConfirm(e.currentTarget, 'Wirklich entfernen?', () => { forgetKey(); paintKey(); }));
""")

# Text replacements that change lengths come last, after all position-based splicing.
body = body.replace("__CLAUDE_AI_URL__", CLAUDE_AI_URL)

if any(x in body for x in ("caps.sample", "caps.downloads", "window.claude", "claude.use(", "claude.ai-Link")):
    sys.exit("make_site: claude.ai runtime code left in the site")

# ---------- app icon and manifest (installable on phones) ----------
ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
<rect width="512" height="512" rx="112" fill="#2446A6"/>
<rect x="122" y="150" width="300" height="212" rx="14" fill="#C9D3EC"/>
<rect x="96" y="128" width="300" height="212" rx="14" fill="#FFFFFF"/>
<rect x="96" y="180" width="300" height="8" fill="#CF5547"/>
<g fill="#D3DEF0"><rect x="120" y="222" width="252" height="5"/><rect x="120" y="256" width="252" height="5"/><rect x="120" y="290" width="200" height="5"/></g>
</svg>
"""
MANIFEST = {
    "name": "Vorlesungs-Lernstudio",
    "short_name": "Lernstudio",
    "description": "Aus Vorlesungsfolien werden Anki-Karteikarten und Übungsquizze.",
    "lang": "de",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "background_color": "#EEF1F5",
    "theme_color": "#2446A6",
    "icons": [
        {"src": "icon.svg", "sizes": "any", "type": "image/svg+xml"},
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
    ],
}
import json
(HERE / "docs").mkdir(exist_ok=True)
(HERE / "docs" / "icon.svg").write_text(ICON_SVG, encoding="utf-8")
(HERE / "docs" / "manifest.webmanifest").write_text(json.dumps(MANIFEST, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
# The PNG icons (icon-192.png, icon-512.png, apple-touch-icon.png) are rendered from icon.svg once and kept in docs/.

out = HERE / "docs" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(head + body.rstrip() + "\n</body>\n</html>\n", encoding="utf-8")
print(f"wrote {out.relative_to(HERE)} ({out.stat().st_size // 1024} KB)")
