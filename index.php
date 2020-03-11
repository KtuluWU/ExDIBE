<?php
$data = include 'config.php';
$identifiant = $data['identifiant'];
$password = $data['password'];
$email = $data['email'];
?>
<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <link rel='stylesheet' href='assets/css/style.css'>
    <link rel='stylesheet' href='assets/css/sweet-alert.css'>
    <link rel='shortcut icon' href='assets/data_favicon.png' />
    <title> ExDIBE </title>
</head>

<body>
    <div class="container">
        <form id="form_info" name="form_info" action="" method="POST" enctype="multipart/form-data">
            <div class="content">
                <div class="">
                    <div class="checkbox2-block">
                        <div class="format_res_label">
                            Format du fichier résultat:
                        </div>
                        <div class="format_res_block">
                            <span class="checkbox format_res">
                                <input type="checkbox" name="format_res" id="format_res_pdf" value="format_res_pdf">
                                <label for="format_res_pdf" class="checkbox_label">PDF</label>
                            </span>
                            <span class="checkbox format_res">
                                <input type="checkbox" name="format_res" id="format_res_data" value="format_res_data">
                                <label for="format_res_data" class="checkbox_label">DATA</label>
                            </span>
                        </div>
                    </div>

                    <div class="radio-block">
                        <span class="radio">
                            <input type="radio" name="siren_select" id="siren_single" value="siren_single" checked>
                            <label for="siren_single" class="radio_label">Siren</label>
                        </span>
                        <span class="radio">
                            <input type="radio" name="siren_select" id="siren_multip" value="siren_multip">
                            <label for="siren_multip" class="radio_label">Fichier</label>
                        </span>
                    </div>

                    <div class="input-block input-siren">
                        <span class="input">
                            <input class="input_field" type="text" name="siren" id="siren" maxlength="15" value="" />
                            <label class="input_label" for="siren">
                                <span class="input_label-content">Siren</span>
                            </label>
                        </span>
                    </div>

                    <div class="checkbox-block">
                        <span class="checkbox">
                            <input type="checkbox" name="python_option" id="python_option_entete"
                                value="python_option_entete">
                            <label for="python_option_entete" class="checkbox_label">Il existe une entête en première
                                ligne?</label>
                        </span>
                        <span class="checkbox">
                            <input type="checkbox" name="python_option" id="python_option_ref"
                                value="python_option_ref">
                            <label for="python_option_ref" class="checkbox_label">Il existe des références dans la
                                colonne 2?</label>
                        </span>
                    </div>

                    <div class="input-block nodisplay-block">
                        <span class="input file-upload">
                            <input class="file_upload" type="file" name="file_upload" id="file_upload"
                                accept="text/csv, application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">
                            <label class="file_label" for="file_upload">
                                <span class="file_label-content">Uploadez un ficher</span>
                            </label>
                        </span>
                        <span class="exemple">
                            Formats acceptés: csv(non UTF-8), xls, xlsx
                        </span>
                    </div>

                    <div class="input-block nodisplay-block">
                        <span class="input">
                            <input class="input_field" type="text" name="res_zip" id="res_zip" maxlength="30"
                                value="" />
                            <label class="input_label" for="res_zip">
                                <span class="input_label-content">.zip</span>
                            </label>
                        </span>
                        <span class="exemple">
                            Nommez le fichier de résultat (.zip)
                        </span>
                    </div>

                    <div class="input-block">
                        <span class="input">
                            <input class="input_field" type="text" name="ident" id="ident" maxlength="30"
                                value="<?php echo $identifiant ?>" />
                            <label class="input_label" for="ident">
                                <span class="input_label-content">Identifiant</span>
                            </label>
                        </span>
                        <span class="exemple">
                            Exemple: 08500-00000
                        </span>
                    </div>

                    <div class="input-block">
                        <span class="input">
                            <input class="input_field" type="password" name="password" id="password"
                                value="<?php echo $password ?>" autocomplete="off" />
                            <label class="input_label" for="password">
                                <span class="input_label-content">Mot de passe</span>
                            </label>
                        </span>
                    </div>

                    <div class="input-block">
                        <span class="input">
                            <input class="input_field" type="email" name="email" id="email" value="<?php echo $email ?>"
                                autocomplete="off" />
                            <label class="input_label" for="email">
                                <span class="input_label-content">Email</span>
                            </label>
                        </span>
                    </div>


                    <div class="commentaire_block">
                        <textarea class="commentaire" name="commentaire" id="commentaire" maxlength="100"
                            placeholder="Commentaire..."></textarea>
                    </div>

                </div>
                <div class="button_block">
                    <input type="button" class="button_field" name="send" id="send" value="Envoyer"
                        onclick="ajax_send_data()">
                </div>
                <div class="loading">
                    <img class="loading_gif" id="loading_gif" alt="Chargement..." src="assets/loading_gr.gif">
                </div>
            </div>
        </form>
    </div>

    <script src='assets/vendor/jquery-3.4.1.min.js'></script>
    <script src='assets/vendor/sweet-alert.js'></script>
    <script src='assets/js/action.js'></script>
    <script src='assets/js/classie.js'></script>
    <script>
        (function () {
            [].slice.call(document.querySelectorAll('input.input_field')).forEach(function (inputEl) {
                if (inputEl.value.trim() !== '') {
                    classie.add(inputEl.parentNode, 'input-filled');
                }

                // events:
                inputEl.addEventListener('focus', onInputFocus);
                inputEl.addEventListener('blur', onInputBlur);
            });

            function onInputFocus(ev) {
                classie.add(ev.target.parentNode, 'input-filled');
            }

            function onInputBlur(ev) {
                if (ev.target.value.trim() === '') {
                    classie.remove(ev.target.parentNode, 'input-filled');
                }
            }
        })();
    </script>
</body>

</html>