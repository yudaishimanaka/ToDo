var pushButton = document.getElementById('pushEnableButton');
function initialize(){
    $.ajax({
            type:'GET',
            url:'/user_state',
            contentType:'application/json',
            success: function(response){
                if (response[0][4] == "True"){
                    pushButton.checked = true;
                }else{
                    pushButton.checked = false;
                }
            },
            error: function(response){
            }
    });
}
$(document).ready(function(){
    initialize();
});
pushButton.addEventListener('click', function() {
var pushButton = document.getElementById('pushEnableButton');
if (pushButton.checked == true){
  var state = pushButton.checked;
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/push.js')
      .then(function(registration) {
        console.log(registration);
        return registration.pushManager.getSubscription().then(function(subscription) {
          if (subscription) {
            return subscription
          }
          return registration.pushManager.subscribe({
            userVisibleOnly: true
          })
        })
      }).then(function(subscription) {
        var endpoint = subscription.endpoint
        console.log("pushManager endpoint:", endpoint)
        var name = $("#name").text();
        $.ajax({
            type:'POST',
            url:'/register_endpoint',
            data: JSON.stringify({"name": name,
                                  "endpoint": endpoint,
                                  "state": state
            }),
            contentType:'application/json',
            success: function(response){
                initialize();
            },
            error: function(start){
            }
        });
      }).catch(function(error) {
        console.warn("serviceWorker error:", error)
      })
  }
}else{
  var state = pushButton.checked;
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/push.js')
      .then(function(registration) {
        console.log(registration);
        return registration.pushManager.getSubscription().then(function(subscription) {
          if (subscription) {
            return subscription.unsubscribe();
          }
          return registration.pushManager.subscribe({
            userVisibleOnly: true
          })
        })
      }).then(function(subscription) {
        var name = $("#name").text();
        $.ajax({
            type:'POST',
            url:'/update_state',
            data: JSON.stringify({"name": name,
                                  "state": state
            }),
            contentType:'application/json',
            success: function(response){
                initialize();
            },
            error: function(start){
            }
        });
      }).catch(function(error) {
        console.warn("serviceWorker error:", error)
      })
  }
}
})