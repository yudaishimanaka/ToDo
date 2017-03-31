window.addEventListener('load', function() {
  register();

  navigator.serviceWorker.ready.then(checkPush);
}, false);
$('#pushEnableButton').on('click', function() {
    var pushButton = document.getElementById('pushEnableButton').addEventListener('click', setPush , false);
    //var pushButton = setPush();
    alert(pushButton);
});

function register() {
  navigator.serviceWorker.register('/static/push.js').then(checkNotification);
}

function checkNotification() {
  Notification.requestPermission(function(permission) {
    if(permission !== 'denied')
      document.getElementById('pushEnableButton').disabled = false;
    else
      alert('プッシュ通知を有効にできません。ブラウザの設定を確認して下さい。');
  });
}
var subscription = null;

function checkPush(sw) {
  sw.pushManager.getSubscription().then(setSubscription, resetSubscription);
}

function setSubscription(s) {
  if(!s)
    resetSubscription();
  else {
    subscription = s;
    var p = document.getElementById('pushEnableButton');
    p.textContent = 'プッシュ通知を解除する';
    p.disabled = false;
    registerNotification(s);
    console.log(subscription.endpoint);
  }
}

function resetSubscription() {
  subscription = null;
  var p = document.getElementById('pushEnableButton');
  p.textContent = 'プッシュ通知を有効にする';
  p.disabled = false;
}

function setPush() {
  if(!subscription) {
    if(Notification.permission == 'denied') {
      alert('プッシュ通知を有効にできません。ブラウザの設定を確認して下さい。');
      return;
    }

    navigator.serviceWorker.ready.then(subscribe);
  }

  else
    navigator.serviceWorker.ready.then(unsubscribe);
}

function subscribe(sw) {
  sw.pushManager.subscribe({
    userVisibleOnly: true
  }).then(setSubscription, resetSubscription);
}

function unsubscribe() {
  if(subscription) {
    // 自分のWebアプリサーバ等にプッシュ通知の解除を通知する処理をここに実装
    subscription.unsubscribe();
  }
  resetSubscription();
}

function registerNotification(s) {
  var endpoint = s.endpoint;
  // Chrome 43以前への対処
  if(('subscriptionId' in s) && !s.endpoint.match(s.subscriptionId))
    endpoint += '/' + s.subscriptionId;
  // 自分のWebアプリサーバ等にプッシュ通知を登録する処理をここに実装
  // endpointにプッシュサービスのエンドポイントのURLが格納される
}
