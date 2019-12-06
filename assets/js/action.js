function ajax_send_data() {
    var siren = document.form_info.siren.value;
    var ident = document.form_info.ident.value;
    var pwd = document.form_info.password.value;
    var email = document.form_info.email.value;
    var commentaire = document.form_info.commentaire.value.replace(/\n/g, "<br>");
    var siren_radio = document.form_info.siren_select;
    var file_upload = document.form_info.file_upload.files[0];
    var python_option_entete = document.form_info.python_option_entete;
    var python_option_ref = document.form_info.python_option_ref;
    var format_res_pdf = document.form_info.format_res_pdf;
    var format_res_data = document.form_info.format_res_data;
    var res_zip = document.form_info.res_zip.value;
    var url = "./action.php";
    var data = new FormData();

    if (siren_radio[0].checked) {
        siren = siren_checked(siren);
        data.append('siren', siren);
    } else if (siren_radio[1].checked) {
        file_upload = file_checked(file_upload);
        console.log(file_upload);
        data.append('file_upload', file_upload);
    }

    ident = ident_checked(ident);

    res_zip = res_zip.replace(/\s+/g, "_");

    if ((siren || file_upload) && format_res_checked(format_res_pdf, format_res_data)) {
        document.getElementById("loading_gif").style.display = "block";
        data.append('ident', ident);
        data.append('pwd', pwd);
        data.append('email', email);
        data.append('commentaire', commentaire);
        data.append('python_option_entete', python_option_entete.checked);
        data.append('python_option_ref', python_option_ref.checked);
        data.append('format_res_pdf', format_res_pdf.checked);
        data.append('format_res_data', format_res_data.checked);
        data.append('res_zip', res_zip);
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
        //ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");//HTTP head

        ajax.send(data);
        ajax.onreadystatechange = function () {
            //如果执行状态成功，那么就把返回信息写到指定的层里
            if (ajax.readyState == 4 && ajax.status == 200) {
                if (ajax.responseText == "200") {
                    swal({
                        title: "Bien envoyé!",
                        text: "Fermer automatiquement après 2 secondes",
                        timer: 2000,
                        type: "success"
                    });
                    setTimeout("location.reload()", 2000)
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

    if (len == 0) {
        swal({
            title: "Échoué!",
            text: "Siren ne doit pas être vide!",
            type: "error"
        })
        return false;
    }

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

function file_checked(file) {
    if (!file) {
        swal({
            title: "Échoué!",
            text: "Le fichier ne doit pas être vide!",
            type: "error"
        })
        return false;
    }
    return file;
}

function format_res_checked(pdf, data) {
    if (!pdf.checked && !data.checked) {
        swal({
            title: "Échoué!",
            text: "Veuillez choisir un format du fichier résultat!",
            type: "error"
        })
        return false;
    } else {
        return true;
    }
}

$(document).ready(function () {
    $("input:radio[name='siren_select']").change(function () {
        if (this.checked && this.value == 'siren_multip') {
            $('.input-siren').hide(800);
            $('.checkbox-block').fadeIn(900).css('display', 'flex');
            $('.nodisplay-block').fadeIn(1000).css('display', 'block');
        } else {
            $('.input-siren').show(800);
            $('.checkbox-block').hide(900);
            $('.nodisplay-block').hide(1000);
        }
    });

    $(".file_upload").change(function () {
        var fileName = $("#file_upload").val().split('\\').pop();
        $(".file_label-content").html("Fichier: " + fileName);
    })
});