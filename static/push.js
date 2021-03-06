'use strict';

self.addEventListener('push', function(event) {
  console.log('Received a push message', event);
  function getEndpoint() {
    return self.registration.pushManager.getSubscription().then(function(subscription) {
                if (subscription) {
                    return subscription.endpoint
                }
            })
  }
  var icon = 'img/yohane.png';
  var url = 'http://localhost:5000/index';
  event.waitUntil(
    getEndpoint().then(function(endpoint) {
        return fetch("http://localhost:5000/fetch", {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                end_point: endpoint
            })
        }).then(function(response) {
            if (response.status === 200) {
                return response.json()
            }
        }).then(function(response) {
            console.log(response.action)
            return self.registration.showNotification(response.title, {
                icon: icon,
                body: response.body,
                actions: [{
                    "action": "setting",
                    "title": "設定"
                }],
                data: {
                    url: url
                },
                vibrate: [200, 100, 200, 100, 200, 100, 200]
            })
        }).catch(err => {
            return;
        })
    })
  );
});
self.addEventListener('notificationclick', function(event) {
  event.notification.close()
  if (event.action === 'setting'){
    clients.openWindow('/setting');
  }
  var url = "/"
  if (event.notification.data.url) {
    url = event.notification.data.url
  }

  event.waitUntil(
    clients.matchAll({type: 'window'}).then(function() {
      if(clients.openWindow) {
        return clients.openWindow(url)
      }
    })
  )
})
