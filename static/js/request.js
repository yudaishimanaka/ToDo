$(function (){
    $(document).on('click','#remove',function(){
        setTimeout(function(){
            var del = document.getElementsByClassName('box');
            for(var i =0; i<del.length; i++){
                    if(del[i].style.display == "none"){
                        var title = $("#title"+i).text();
                        var contents = $("#contents"+i).text();
                        var name = $("#name").text();
                        $(del[i]).remove();
                        $.ajax({
                            type:'POST',
                            url:'/remove',
                            data: JSON.stringify({"title": title,
                                               "contents": contents,
                                               "name": name
                                                }),
                            contentType:'application/json',
                            success: function(response){
                            },
                            error: function(response){
                            }
                        })

                    }
            }
        },1000);
    });
});
$(document).ready(function(){
    $.ajax({
            type:'GET',
            url:'/request',
            contentType:'application/json',
            success: function(response){
                for(var i = 0; i < response.length; i++){
                    $("#tasklist").append(
                        "<div class='box box-primary'><div class='box-header with-border'><label class='box-title' id='title"+i+"'>"+response[i][1]+"</label><div class='box-tools pull-right'><button id='remove' type='button' class='btn btn-box-tool' data-widget='remove' data-toggle='tooltip' title='削除'><i class='fa fa-times'></i></button></div></div><div class='box-body' id='contents"+i+"'>"+response[i][2]+"</div></div>");
                }

            },
            error: function(response){
            }
    });
});