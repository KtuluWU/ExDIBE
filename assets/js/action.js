function ajax_send_data() {
    var siren = document.form_info.siren.value;
    var ident = document.form_info.ident.value;
    var pwd = document.form_info.password.value;
    var email = document.form_info.email.value;
    var url = "./action.php";

    siren = siren_checked(siren);
    ident = ident_checked(ident);

    if (siren && ident) {
        document.getElementById("loading_gif").style.display = "block";
        var data = "siren=" + siren + "&ident=" + ident + "&pwd=" + pwd + "&email=" + email;
        var ajax = false;
        //初始化XMLHttpRequest对象
        if (window.XMLHttpRequest) { //Mozilla 浏览器
            ajax = new XMLHttpRequest();
            if (ajax.overrideMimeType) {//设置MiME类别
                ajax.overrideMimeType("text/xml");
            }
        }
        else if (window.ActiveXObject) { // IE浏览器
            try {
                ajax = new ActiveXObject("Msxml2.XMLHTTP");
            } catch (e) {
                try {
                    ajax = new ActiveXObject("Microsoft.XMLHTTP");
                } catch (e) { }
            }
        }
        if (!ajax) { // 异常，创建对象实例失败
            window.alert("不能创建XMLHttpRequest对象实例.");
            return false;
        }

        //开始发送
        ajax.open("POST", url, true);
        ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");//HTTP head

        ajax.send(data);
        ajax.onreadystatechange = function () {
            //如果执行状态成功，那么就把返回信息写到指定的层里
            if (ajax.readyState == 4 && ajax.status == 200) {
                if (ajax.responseText == "200") {
                    swal({
                        title: "Bien envoyé!",
                        text: "Fermer automatiquement après 5 secondes",
                        timer: 5000,
                        type: "success"
                    })                
                } else {
                    swal({
                        title: "Échoué!",
                        text: ajax.responseText,
                        type: "error"
                    })
                
                }
                document.getElementById("loading_gif").style.display = "none";
            }
        }
    }
}

function siren_checked(siren) {
    siren = siren.replace(/\s+/g, "");
    var len = siren.length;

    if (siren.length > 9) {
        swal({
            title: "Échoué!",
            text: "Siren non disponible!",
            type: "error"
        })
        return false;
    } else {
        for (let i = 0; i < (9 - len); i++) {
            siren = "0" + siren;
        }
    }
    return siren;
}

function ident_checked(ident) {
    if (ident.length > 11) {
        swal({
            title: "Échoué!",
            text: "L'identifiant non disponible!",
            type: "error"
        })
        return false;
    } else {
        let res = ident.substr(5, 1);
        if (res != "-") {
            swal({
                title: "Échoué!",
                text: "Le format de l'identifiant doit être 'XXXXX-YYYYY'!",
                type: "error"
            })
            return false;
        }
    }
    return ident;
}