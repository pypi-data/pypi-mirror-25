function post(url, data, callback){
    $.ajax({
        url:  url,
        type: 'POST',
        // contentType: "application/json;charset=utf-8",
        data: {data: JSON.stringify({data: data, url: $("iframe").attr("src")})},
        dataType: 'json',
        success:function(res){
            callback(res);
        }
        // processData: false,
        // contentType: false,
//         xhr: function(){
// 　　　　　　var xhr = $.ajaxSettings.xhr();
// 　　　　　　if(onprogress && xhr.upload) {
// 　　　　　　　　xhr.upload.addEventListener("progress" , onprogress, false);
// 　　　　　　　　return xhr;
// 　　　　　　}
// 　　　　}
    }).done(function(res) {
        
            alert(res);

    })    
}
