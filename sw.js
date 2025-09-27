// Service Worker for Insaka Conference PWA
const CACHE_NAME = 'insaka-conference-v1.0.2-' + Date.now();
const urlsToCache = [
  '/',
  '/pages/1_Delegate_Dashboard.py',
  '/pages/0_Landing.py',
  '/assets/logos/insaka.jpg',
  '/assets/pwa/icon-48x48.png',
  '/assets/pwa/icon-72x72.png',
  '/assets/pwa/icon-96x96.png',
  '/assets/pwa/icon-144x144.png',
  '/assets/pwa/icon-152x152.png',
  '/assets/pwa/icon-167x167.png',
  '/assets/pwa/icon-180x180.png',
  '/assets/pwa/icon-192x192.png',
  '/assets/pwa/icon-512x512.png',
  '/manifest.json'
];

// Install event - cache resources
self.addEventListener('install', (event) => {
  console.log('🔧 Insaka PWA: Service Worker installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('📦 Insaka PWA: Caching app shell');
        return cache.addAll(urlsToCache);
      })
      .then(() => {
        console.log('✅ Insaka PWA: Service Worker installed');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('❌ Insaka PWA: Cache installation failed:', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('🚀 Insaka PWA: Service Worker activating...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('🗑️ Insaka PWA: Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('✅ Insaka PWA: Service Worker activated');
      return self.clients.claim();
    })
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') {
    return;
  }

  // Skip Streamlit internal requests
  if (event.request.url.includes('/_stcore/') || 
      event.request.url.includes('/static/') ||
      event.request.url.includes('/health')) {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Return cached version or fetch from network
        if (response) {
          console.log('📱 Insaka PWA: Serving from cache:', event.request.url);
          return response;
        }

        console.log('🌐 Insaka PWA: Fetching from network:', event.request.url);
        return fetch(event.request).then((response) => {
          // Don't cache non-successful responses
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }

          // Clone the response
          const responseToCache = response.clone();

          caches.open(CACHE_NAME)
            .then((cache) => {
              cache.put(event.request, responseToCache);
            });

          return response;
        }).catch((error) => {
          console.error('❌ Insaka PWA: Network fetch failed:', error);
          // Return offline page or cached fallback
          if (event.request.destination === 'document') {
            return caches.match('/pages/0_Landing.py');
          }
        });
      })
  );
});

// Background sync for offline functionality
self.addEventListener('sync', (event) => {
  console.log('🔄 Insaka PWA: Background sync triggered:', event.tag);
  
  if (event.tag === 'background-sync') {
    event.waitUntil(
      // Handle offline actions when connection is restored
      handleBackgroundSync()
    );
  }
});

// Push notification handling
self.addEventListener('push', (event) => {
  console.log('📲 Insaka PWA: Push notification received');
  
  const options = {
    body: event.data ? event.data.text() : 'New conference update available!',
    icon: '/assets/logos/insaka.jpg',
    badge: '/assets/logos/insaka.jpg',
    vibrate: [200, 100, 200],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'View Details',
        icon: '/assets/logos/insaka.jpg'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/assets/logos/insaka.jpg'
      }
    ],
    tag: 'insaka-notification'
  };

  event.waitUntil(
    self.registration.showNotification('Insaka Conference', options)
  );
});

// Notification click handling
self.addEventListener('notificationclick', (event) => {
  console.log('👆 Insaka PWA: Notification clicked');
  
  event.notification.close();

  if (event.action === 'explore') {
    // Open the app to the dashboard
    event.waitUntil(
      clients.openWindow('/pages/1_Delegate_Dashboard.py')
    );
  } else if (event.action === 'close') {
    // Just close the notification
    return;
  } else {
    // Default action - open the app
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Helper function for background sync
async function handleBackgroundSync() {
  try {
    console.log('🔄 Insaka PWA: Handling background sync...');
    
    // Here you could sync offline data, upload cached interactions, etc.
    // For now, just log that sync occurred
    console.log('✅ Insaka PWA: Background sync completed');
  } catch (error) {
    console.error('❌ Insaka PWA: Background sync failed:', error);
  }
}
