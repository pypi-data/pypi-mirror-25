// $('#iframe-content').load(function(){

//     after_load();

// });
var actions_chains = []

function get_path(e){
    s = $(e)
    vid = s.attr("id");
    vclass = s.attr("class");
    vname = s.tagName

}

function after_load(){
    $(".process-bar-load").modal();
    $(window.frames[0].document).click(function(e){
        console.log(e.target)
        s = $(e.target)
        idv = "#" + s.attr('id') ? "#" + s.attr('id') : ""
        clv = "." + s.attr('class') ? "." + s.attr("class").split(" ")[0] : ""
        tv = e.target.tagName
        ac = tv  + clv + idv + "/C";
        
        tmp = false
        actions_chains.forEach(function(e){
            if (e == ac){
                tmp = true
            }
        })

        if (tmp == false){
            actions_chains.push(ac)
            $("#attrs").append("<li>" + ac  + "</li>");
        }
    })

    $(window.frames[0].document).find("a").click(function(e){
        console.log(e.target)
        s = $(e.target)
        idv = "#" + s.attr('id') ? "#" + s.attr('id') : ""
        clv = "." + s.attr('class') ? "." + s.attr("class").split(" ")[0] : ""
        tv = e.target.tagName
        ac = tv  + clv + idv + "/C";
        
        tmp = false
        actions_chains.forEach(function(e){
            if (e == ac){
                tmp = true
            }
        })

        if (tmp == false){
            actions_chains.push(ac)
            $("#attrs").append("<li>" + ac  + "</li>");
        }
    })
    // $(window.frames[0].document).find("input")

    $(window.frames[0].document).find("input").change(function (e){
        s = $(e.target)

        idv = "#" + s.attr('id') ? "#" + s.attr('id') : ""
        clv = "." + s.attr('class') ? "." + s.attr("class").split(" ")[0] : ""
        tv = e.target.tagName
        va = s.val()
        
        console.log(va)
        
        ac = tv  + clv + idv + "/I'"+ va + "'"
        tmp = false
        actions_chains.forEach(function(e){
            if (e == ac){
                tmp = true
            }
        })

        if (tmp == false){
            actions_chains.push(ac)
            $("#attrs").append("<li>" + ac  + "</li>");

        }
    })
    // }).focus(function(e){
    //     console.log('in:',e.target)
    //     s = $(e.target)
    //     idv = s.attr('id')
    //     clv = s.attr('class')
    //     tv = e.target.tagName
    //     $("#attrs").append("<li>"+tv + "." + clv+"#"+idv);


    // });
}


