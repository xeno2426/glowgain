/* ═══════════════════════════════════════════════════
   GlowGain v2 — Service Worker
   Offline-first shell caching + AI model passthrough
═══════════════════════════════════════════════════ */

const CACHE_NAME  = 'gg-v2-shell';
const CDN_CACHE   = 'gg-v2-cdn';
const AI_CACHE    = 'gg-v2-model';

/* Shell assets cached on install */
const SHELL = [
  './',
  './index.html',
  './manifest.json',
];

/* CDN assets (fonts, transformers lib) — stale-while-revalidate */
const CDN_PATTERNS = [
  'fonts.googleapis.com',
  'fonts.gstatic.com',
  'cdn.jsdelivr.net',
];

/* ── Install: cache shell ──────────────────────── */
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME)
      .then(c => c.addAll(SHELL))
      .then(() => self.skipWaiting())
  );
});

/* ── Activate: clean up old caches ────────────── */
self.addEventListener('activate', e => {
  const keep = [CACHE_NAME, CDN_CACHE, AI_CACHE];
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(k => !keep.includes(k))
          .map(k => caches.delete(k))
      )
    ).then(() => self.clients.claim())
  );
});

/* ── Fetch strategy ────────────────────────────── */
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  /* 1. HuggingFace model files — cache-first (immutable after download) */
  if (
    url.hostname.includes('huggingface.co') ||
    url.pathname.includes('/resolve/') ||
    url.pathname.includes('.gguf') ||
    url.pathname.includes('.bin') ||
    url.pathname.includes('.onnx') ||
    url.hostname.includes('cdn-lfs')
  ) {
    e.respondWith(
      caches.open(AI_CACHE).then(async cache => {
        const hit = await cache.match(e.request);
        if (hit) return hit;
        const resp = await fetch(e.request);
        if (resp.ok) {
          /* Clone before consuming body */
          cache.put(e.request, resp.clone());
        }
        return resp;
      }).catch(() => fetch(e.request))
    );
    return;
  }

  /* 2. CDN assets (fonts, transformers.js) — stale-while-revalidate */
  if (CDN_PATTERNS.some(p => url.hostname.includes(p))) {
    e.respondWith(
      caches.open(CDN_CACHE).then(async cache => {
        const hit = await cache.match(e.request);
        /* Start background revalidation */
        const fetchPromise = fetch(e.request).then(resp => {
          if (resp.ok) cache.put(e.request, resp.clone());
          return resp;
        }).catch(() => null);
        return hit || fetchPromise;
      })
    );
    return;
  }

  /* 3. Shell — network-first with offline fallback */
  e.respondWith(
    fetch(e.request)
      .then(resp => {
        if (resp.ok) {
          const clone = resp.clone();
          caches.open(CACHE_NAME).then(c => c.put(e.request, clone));
        }
        return resp;
      })
      .catch(() =>
        caches.match(e.request).then(hit => hit || caches.match('./index.html'))
      )
  );
});

/* ── Message handler ───────────────────────────── */
self.addEventListener('message', e => {
  if (e.data?.type === 'SKIP_WAITING') self.skipWaiting();
});
