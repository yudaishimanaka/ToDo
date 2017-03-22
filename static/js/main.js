$(function (){
    $("#register").click(function(){
        if($("#pass").val() == $("#cpass").val()){
            $.ajax({
                    type:'POST',
                    url:'/register',
                    data: JSON.stringify({"name":$("#name").val(),
                                       "email":$("#email").val(),
                                       "pass":$("#pass").val()
                                        }),
                    contentType:'application/json',
                    success: function(response){
                        $("#msg").html(response)
                    },
                    error: function(response){
                    }
            });
            $("#name").val("");
            $("#email").val("");
            $("#pass").val("");
            $("#cpass").val("");
            }else{
                $("#name").val("");
                $("#email").val("");
                $("#pass").val("");
                $("#cpass").val("");
                $("#msg").html("パスワードと確認用パスワードが一致しません")
            }
    });
});
$(function (){
    $("#task").click(function(){
        if($("#title").val().length != 0){
            $.ajax({
                    type:'POST',
                    url:'/taskadd',
                    data: JSON.stringify({"title":$("#title").val(),
                                       "contents":$("#contents").val(),
                                       "period":$("#reservation").val(),
                                       "level":$("#level").val()
                                        }),
                    contentType:'application/json',
                    success: function(response){
                        alert(response)
                    },
                    error: function(response){
                    }
            });
            $("#title").val("");
            $("#contents").val("");
        }else{
            alert("タイトルは必須項目です")
            $("#title").val("");
            $("#contents").val("");
        }
    });
});