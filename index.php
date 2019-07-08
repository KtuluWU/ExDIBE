<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <link rel='stylesheet' href='assets/css/style.css'>
    <link rel='stylesheet' href='assets/css/sweet-alert.css'>
    <title> ExDIBE </title>
</head>

<body>
    <div class="container">
        <form id="form_info" name="form_info" action="" method="POST">
            <div class="content">
                <div class="input_block">
                    <span class="input">
                        <input class="input_field" type="text" name="siren" id="siren" maxlength="15" value=""/>
                        <label class="input_label" for="siren">
                            <span class="input_label-content">Siren</span>
                        </label>
                    </span>

                    <span class="input">
                        <input class="input_field" type="text" name="ident" id="ident" maxlength="30" value=""/>
                        <label class="input_label" for="ident">
                            <span class="input_label-content">Identifiant</span>
                        </label>
                    </span>

                    <span class="input">
                        <input class="input_field" type="password" name="password" id="password" value="98541"
                            autocomplete="off" />
                        <label class="input_label" for="password">
                            <span class="input_label-content">Mot de passe</span>
                        </label>
                    </span>

                    <span class="input">
                        <input class="input_field" type="email" name="email" id="email" value="rbe@infogreffe-siege.fr"
                            autocomplete="off" />
                        <label class="input_label" for="email">
                            <span class="input_label-content">Email</span>
                        </label>
                    </span>

                    <span class="commentaire_block">
                        <textarea class="commentaire" name="commentaire" id="commentaire" maxlength="100" placeholder="Commentaire..."></textarea>
                    </span>

                </div>
                <div class="button_block">
                    <input type="button" class="button_field" name="send" id="send" value="Envoyer" onclick="ajax_send_data()">
                </div>
                <div class="loading">
                    <img class="loading_gif" id="loading_gif" alt="Chargement..." src="assets/loading_gr.gif">
                </div>
            </div>
        </form>
    </div>
</body>
<script src='assets/js/action.js'></script>
<script src='assets/js/classie.js'></script>
<script src='assets/vendor/jquery-3.4.1.min.js'></script>
<script src='assets/vendor/sweet-alert.js'></script>
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

</html>