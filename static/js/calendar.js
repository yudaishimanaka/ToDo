$(document).ready(function(){
    $.ajax({
            type:'GET',
            url:'/tasklist',
            contentType:'application/json',
            success: function(response){
                $('#calendar').fullCalendar({
                    header: {
                        left: 'prev,next today',
                        center: 'title',
                        right: 'month,agendaWeek,agendaDay'
                    },
                    buttonText: {
                        today: '今日',
                        month: '月',
                        week: '週',
                        day: '日'
                    },
                    //Random default events
                    events: {url: 'tasklist'},
                    editable: true,
                    droppable: true
                });
                //$('#calendar').fullCalendar('addEvent', value);

            },
            error: function(start){
            }
    });
});