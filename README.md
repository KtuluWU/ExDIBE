
#ExDIBE

**Créez un fichier `<config.php>` dans la racine, le format est suivant:**
```php
<?php
    /**
     * Les valeurs par défaut
     */
    $identifiant = "votre identifiant d'Infogreffe"; // exemple: 08500-00000
    $password = "votre mot de passe"; 
    $email = "votre destionation";
    $sftp_address = "adresse du serveur";
    $sftp_login = "identifiant du serveur";
    $sftp_password = "mot de passe du serveur";

    return array(
        'identifiant'   => $identifiant,
        'password'      => $password,
        'email'         => $email,
        'sftp_address'  => $sftp_address,
        'sftp_login'    => $sftp_login,
        'sftp_password' => $sftp_password
    );
?>
```