
const CACHE = "pwabuilder-page";

// TODO: замените следующее на правильную автономную резервную страницу i.e.: const offlineFallbackPage = "offline.html";

// Этап установки устанавливает автономную страницу в кеш и открывает новый кеш
self.addEventListener("install", function (event) {
    console.log("[PWA Builder] Install Event processing");

    event.waitUntil(
        caches.open(CACHE).then(function (cache) {
            console.log("[PWA Builder] Cached offline page during install");

            if (offlineFallbackPage === "pwa-offline.html") {
                return cache.add(new Response("TODO: Update the value of the offlineFallbackPage constant in the serviceworker."));
            }

            return cache.add(offlineFallbackPage);
        })
    );
});

// Если какая-либо загрузка не удалась, она покажет автономную страницу.
self.addEventListener("fetch", function (event) {
    if (event.request.method !== "GET") return;

    event.respondWith(
        fetch(event.request).catch(function (error) {
            // Следующее подтверждает, что запрос был для перехода к новому документу
            if (
                event.request.destination !== "document" ||
                event.request.mode !== "navigate"
            ) {
                return;
            }

            console.error("[PWA Builder] Network request Failed. Serving offline page " + error);
            return caches.open(CACHE).then(function (cache) {
                return cache.match(offlineFallbackPage);
            });
        })
    );
});

// Это событие, которое можно запустить с вашей страницы, чтобы сообщить программному обеспечению обновить автономную страницу.
self.addEventListener("refreshOffline", function () {
    const offlinePageRequest = new Request(offlineFallbackPage);

    return fetch(offlineFallbackPage).then(function (response) {
        return caches.open(CACHE).then(function (cache) {
            console.log("[PWA Builder] Offline page updated from refreshOffline event: " + response.url);
            return cache.put(offlinePageRequest, response);
        });
    });
});
