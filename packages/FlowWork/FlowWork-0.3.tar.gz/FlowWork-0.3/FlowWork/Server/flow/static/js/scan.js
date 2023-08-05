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
        idv = s.attr('id') ? "#" + s.attr('id') : ""
        clvs = s.attr('class') ? s.attr("class").split(" ") : []
        clv = ''
        
        tv = e.target.tagName
        parent = ''

        if (clvs.length > 0){
            clv = '.' + clvs[0]
            clvl = $(window.frames[0].document).find(clv).length

            for(i =0 ; i< clvs.length ; i++){
                clvt = '.' + clvs[i];
                console.log(clvt)
                if ($(window.frames[0].document).find(clvt).length <= clvl){
                    clv = clvt;
                    clvl = $(window.frames[0].document).find(clv).length;
                }

            }
            if ($(window.frames[0].document).find(clv).length > 1){
                console.log("pp")
                parent = e.target.parentElement.tagName;
            }
        }

         
        
        

        tv = e.target.tagName
        sele_css = tv  + clv + idv
        if (parent != ""){
            sele_css = parent+">" + sele_css;
        }

        

        test_tar = $(window.frames[0].document).find(sele_css);
        if (test_tar.length > 1){
            for (i = 0; i< test_tar.length; i++){
                if (test_tar[i] == e.target){
                    sele_css += ":" + i
                }
            }
        }

        ac = sele_css + "/C";
        
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
        idv = s.attr('id') ? "#" + s.attr('id') : ""
        tv = e.target.tagName
        clvs = s.attr('class') ? s.attr("class").split(" ") : []
        clv = ''
        
        parent = ''

        if (clvs.length > 0){
            clv = '.' + clvs[0]
            clvl = $(window.frames[0].document).find(clv).length

            for(i =0 ; i< clvs.length ; i++){
                clvt = '.' + clvs[i];
                console.log(clvt)
                if ($(window.frames[0].document).find(clvt).length <= clvl){
                    clv = clvt;
                    clvl = $(window.frames[0].document).find(clv).length;
                }

            }
            if ($(window.frames[0].document).find(clv).length > 1){
                console.log("pp")
                parent = e.target.parentElement.tagName;
            }
        }

         
        

        tv = e.target.tagName
        sele_css = tv  + clv + idv
        if (parent != ""){
            sele_css = parent+">" + sele_css;
        }
        
        test_tar = $(window.frames[0].document).find(sele_css);
        if (test_tar.length > 1){
            for (i = 0; i< test_tar.length; i++){
                if (test_tar[i] == e.target){
                    sele_css += ":" + i
                }
            }
        }
        
        ac = sele_css + "/C";
        
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
        // 需要选取最少最特征的 css 
        idv = s.attr('id') ? "#" + s.attr('id') : ""
        clvs = s.attr('class') ? s.attr("class").split(" ") : []
        clv = ''
        parent = ''

        if (clvs.length > 0){
            clv = '.' + clvs[0]
            clvl = $(window.frames[0].document).find(clv).length

            for(i =0 ; i< clvs.length ; i++){
                clvt = '.' + clvs[i];
                console.log(clvt)
                if ($(window.frames[0].document).find(clvt).length <= clvl){
                    clv = clvt;
                    clvl = $(window.frames[0].document).find(clv).length;
                }

            }
            if ($(window.frames[0].document).find(clv).length > 1){
                console.log("pp")
                parent = e.target.parentElement.tagName;
            }
        }

         
        

        tv = e.target.tagName
        sele_css = tv  + clv + idv
        if (parent != ""){
            sele_css = parent+">" + sele_css;
        }

        test_tar = $(window.frames[0].document).find(sele_css);
        if (test_tar.length > 1){
            for (i = 0; i< test_tar.length; i++){
                if (test_tar[i] == e.target){
                    sele_css += ":" + i
                }
            }
        }

        va = s.val()
        
        console.log(va)
        
        ac = sele_css + "/I'"+ va + "'"
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


