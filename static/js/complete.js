$(function (){
    $(document).on('click','#remove',function(){
        setTimeout(function(){
            var del = document.getElementsByClassName('box');
            for(var i = 0; i< del.length; i++){
                    if(del[i].style.display == "none"){
                        var title = $("#title"+i).text();
                        var contents = $("#contents"+i).text();
                        var name = $("#name").text();
                        $.ajax({
                            type:'POST',
                            url:'/remove',
                            data: JSON.stringify({"title": title,
                                               "contents": contents,
                                               "name": name,
                                               "status": "off"
                                                }),
                            contentType:'application/json',
                            success: function(response){
                                $.ajax({
                                    type:'GET',
                                    url:'/complist',
                                    contentType:'application/json',
                                    success: function(response){
                                        $("#tasklist").empty();
                                        for(var y = 0; y < response.length; y++){
                                            if(response[y][5] == "最重要"){
                                                var level = "box-danger";
                                            }else if(response[y][5] == "重要"){
                                                var level = "box-warning";
                                            }else{
                                                var level = "box-primary";
                                            }
                                            $("#tasklist").append(
                                                "<div class='box "+level+"'><div class='box-header with-border'><label class='box-title' id='title"+y+"'>"+response[y][1]+"</label><div class='box-tools pull-right'>"+response[y][3]+" - "+response[y][4]+"<button id='remove' type='button' class='btn btn-box-tool' data-widget='remove'><i class='fa fa-times'> 削除</i></button></div></div><div class='box-body' id='contents"+y+"'>"+response[y][2]+"</div></div>");
                                        }
                                    },
                                    error: function(response){
                                    }
                                });
                            },
                            error: function(response){
                            }
                        })

                    }
            }
        },800);
    });
});
$(document).ready(function(){
    $.ajax({
            type:'GET',
            url:'/complist',
            contentType:'application/json',
            success: function(response){
                for(var i = 0; i < response.length; i++){
                    if(response[i][5] == "最重要"){
                        var level = "box-danger";
                    }else if(response[i][5] == "重要"){
                        var level = "box-warning";
                    }else{
                        var level = "box-primary";
                    }
                    $("#tasklist").append(
                        "<div class='box "+level+"'><div class='box-header with-border'><label class='box-title' id='title"+i+"'>"+response[i][1]+"</label><div class='box-tools pull-right'>"+response[i][3]+" - "+response[i][4]+"<button id='remove' type='button' class='btn btn-box-tool' data-widget='remove'><i class='fa fa-times'> 削除</i></button></div></div><div class='box-body' id='contents"+i+"'>"+response[i][2]+"</div></div>");
                }
            },
            error: function(response){
            }
    });
});