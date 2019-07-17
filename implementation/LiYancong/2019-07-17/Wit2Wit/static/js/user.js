/*$('#zphone').click( function(){ //发送验证码
    $.get('/user/send_message',
    {mobile:$('#mobile').val()},
     function(msg) { alert(jQuery.trim(msg.msg));
     if(msg.msg=='提交成功')
     { RemainTime(); }
     }
     );
     }
     )*/

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // 这些HTTP方法不要求CSRF包含
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
/*$.ajax({

     type: 'POST',

     url: url ,

    data: data ,

    success: success ,

    dataType: dataType

});*/


$(function(){

})


function test(){
    $.ajax({
        type: 'GET',
        url: 'send_message' ,
        data: {
            mobile:$('#mobile').val()
        } ,
        success: function(msg){
            alert(msg.msg)
        },
        dataType: "json"

    });
        //alert('ok')
    }

function delete_address(address_id){
    $.ajax({
        type: 'POST',
        url: 'address',
        data: {
            address_id: address_id,
            mode: 3,
        },
        success: function(msg){},
        dataType: "json"

    });
}

function default_address(address_id){
    $.ajax({
        type: 'POST',
        url: 'address',
        data: {
            address_id: address_id,
            mode: 4,
        },
        success: function(msg){},
        dataType: "json"

    });
}



function update_address(address_id){
    $.ajax({
        type: 'POST',
        url: 'address',
        data: {
            address_id: address_id,
            receiver: '李彦聪',
            addr: '北京市 海淀区 学院路',
            zip_code: '123456',
            phone: '18353115071',
            mode: 2,
        },
        success: function(msg){},
        dataType: "json"

    });
}