/* Offline support: keeps the app on the device so practice works without internet.
   Change VERSION whenever you upload a new index.html, so phones pick up the update. */
const VERSION = "mtg-2026-11-26c";
const FILES = ["./", "index.html", "config.js", "manifest.webmanifest", "icon-192.png", "icon-512.png", "source/questions-cem.js", "source/figures-more.js"];
self.addEventListener("install", e => { e.waitUntil(caches.open(VERSION).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  const u = new URL(e.request.url);
  if (e.request.method !== "GET" || u.origin !== location.origin) return;   /* sign-in, sync and payments always go online */
  /* the app itself: newest copy when online, saved copy when offline */
  e.respondWith(fetch(e.request).then(r => { const copy = r.clone(); caches.open(VERSION).then(c => c.put(e.request, copy)); return r; })
    .catch(() => caches.match(e.request, { ignoreSearch: true }).then(r => r || caches.match("index.html"))));
});
