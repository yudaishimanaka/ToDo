'use strict';

self.addEventListener('push', function(event) {
  console.log('Received a push message', event);

  // サンプルでは固定のメッセージを通知するようにしています。
  // 動的にユーザーごとにメッセージを変えたい場合は、
  // ペイロードの暗号化を行うか、FetchAPIで動的に情報を取得する必要があります。
  var title = '僕だけのToDo管理';
  var body = '4件の未完了タスクがあります。ログインして確認しましょう';
  var icon = 'img/yohane.png';
  var tag = 'simple-push-demo-notification-tag';
  var url = 'localhost:5000/login';

  event.waitUntil(
    self.registration.showNotification(title, {
      body: body,
      icon: icon,
      tag: tag,
      data: {
        url: url
      }
    })
  );
});

self.addEventListener('notificationclick', function(event) {
  console.log('On notification click: ', event.notification.tag);
  event.notification.close();

 var notoficationURL = "/"
  if (event.notification.data.url) {
    notoficationURL = event.notification.data.url
  }

  event.waitUntil(clients.matchAll({
    type: 'window'
  }).then(function(clientList) {
    for (var i = 0; i < clientList.length; i++) {
      var client = clientList[i];
      if (client.url === '/' && 'focus' in client) {
        return client.focus();
      }
    }
    if (clients.openWindow) {
      return clients.openWindow(notoficationURL);
    }
  }));
});
