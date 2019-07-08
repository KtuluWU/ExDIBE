<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require './assets/vendor/PHPMailer/src/Exception.php';
require './assets/vendor/PHPMailer/src/PHPMailer.php';
require './assets/vendor/PHPMailer/src/SMTP.php';

$siren = $_POST["siren"];
$ident = $_POST["ident"];
$pwd = $_POST["pwd"];
$email = $_POST["email"];
$commentaire = $_POST["commentaire"];

$url = "/Users/yw/Sites/ExDIBE/dibe_pdf_new2.py";
$url_windows = "C:/xampp/htdocs/ExDIBE/dibe_pdf_new2.py";
$url_files = "/ExDIBE/files/";

$str_python = "/usr/local/bin/python3 ".$url." -s ".$siren." -i ".$ident." -p ".$pwd." -d ./files";
/*$str_python = "python ".$url_windows." -s ".$siren." -i ".$ident." -p ".$pwd." -d ./files";*/
exec($str_python, $output, $code);

if ($code == 0) {
    $mail = new PHPMailer(true);
    try {
        $mail->CharSet = "UTF-8";
        $mail->SMTPDebug = 0;
        $mail->isSMTP();
        $mail->Host = 'smtp.gmail.com';
        $mail->SMTPAuth = true;
        $mail->Username = 'test.infogreffe@gmail.com';
        $mail->Password = 'Infogreffe2019';
        $mail->SMTPSecure = 'ssl';
        $mail->Port = 465;

        $mail->setFrom('test.infogreffe@gmail.com', 'DataInfogreffe');
        $mail->addAddress($email);

        $files = scandir("./files/");
        foreach( $files as $file) {
            if ($file != '.' && $file != '..' && $file != '.DS_Store') {
                $mail->addAttachment("./files/".$file);
            }
        }

        $mail->isHTML(true);  
        $mail->Subject = 'ExDIBE - '.$ident;
        $mail->Body = "<h1>IDENTIFIANT: ".$ident."</h1><br><h2>COMMENTAIRE: </h2><br>".$commentaire;
        $mail->AltBody = "IDENTIFIANT: ".$ident." COMMENTAIRE: ".$commentaire;

        $mail->send(); 

        foreach( $files as $file) {
            @unlink("./files/".$file);
        }

        echo "200";

    } catch (Exception $e) {
        echo $mail->ErrorInfo;
    }
} else {
    echo "Échec du programme Python.";
}


