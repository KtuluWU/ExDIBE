#ExDIBE
**Créez un fichier `<config.php>` dans la racine, le format est suivant:**
```php
<?php
    <?php
    /**
     * Les valeurs par défaut
    */
    $identifiant = "***"; // exemple: 08500-00000
    $password = "***"; 
    $email = "***";

    return array(
        'identifiant'   => $identifiant,
        'password'      => $password,
        'email'         => $email
    );

?>
```