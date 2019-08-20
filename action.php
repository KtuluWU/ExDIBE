<?php
error_reporting(E_ALL ^ E_NOTICE ^ E_WARNING);

use PHPMailer\PHPMailer\Exception;
use PHPMailer\PHPMailer\PHPMailer;

require './assets/vendor/PHPMailer/src/Exception.php';
require './assets/vendor/PHPMailer/src/PHPMailer.php';
require './assets/vendor/PHPMailer/src/SMTP.php';

class SFTPConnection
{
    private $connection;
    private $sftp;

    public function __construct($host, $port = 22)
    {
        $this->connection = @ssh2_connect($host, $port);
        if (!$this->connection) {
            throw new Exception("Could not connect to $host on port $port.");
        }

    }

    public function login($username, $password)
    {
        if (!@ssh2_auth_password($this->connection, $username, $password)) {
            throw new Exception("Could not authenticate with username $username " .
                "and password $password.");
        }

        $this->sftp = @ssh2_sftp($this->connection);
        if (!$this->sftp) {
            throw new Exception("Could not initialize SFTP subsystem.");
        }

    }

    public function uploadFile($local_file, $remote_file)
    {
        $sftp = $this->sftp;
        $stream = @fopen("ssh2.sftp://$sftp$remote_file", 'w');

        if (!$stream) {
            throw new Exception("Could not open file: $remote_file");
        }

        $data_to_send = @file_get_contents($local_file);
        if ($data_to_send === false) {
            throw new Exception("Could not open local file: $local_file.");
        }

        if (@fwrite($stream, $data_to_send) === false) {
            throw new Exception("Could not send data from file: $local_file.");
        }

        @fclose($stream);
    }
}

@$siren = $_POST["siren"];
$ident = $_POST["ident"];
$pwd = $_POST["pwd"];
$email = $_POST["email"];
$commentaire = $_POST["commentaire"];
@$python_option_entete = $_POST["python_option_entete"];
@$python_option_ref = $_POST["python_option_ref"];
@$file_upload = $_FILES["file_upload"];
@$res_zip = $_POST["res_zip"];
$flag = false;
$filename_compl = false;
$filename = false;
$uploaded_filename = explode('.', $file_upload["name"])[0];

$url = "/Users/yw/Sites/ExDIBE/dibe_pdf_v2.py";
$url_windows = "C:/xampp/htdocs/ExDIBE/dibe_pdf_v2.py";
$url_files = "/ExDIBE/files/";

$str_python = "/usr/local/bin/python3 " . $url . " -i " . $ident . " -p " . $pwd;
// $str_python = "python ".$url_windows." -i ".$ident." -p ".$pwd;

$v = ($file_upload ? true : false);
clean_up($siren, $v, $uploaded_filename);

if ($siren && !$file_upload) {
    mkdir('./files/' . $siren, 0777, true);
    $str_python .= " -s " . $siren . " -d ./files/" . $siren;
} else if ($file_upload && !$siren) {
    mkdir('./files/' . $uploaded_filename, 0777, true);
    mkdir('./upload/' . $uploaded_filename, 0777, true);
    mkdir('./zip/' . $uploaded_filename, 0777, true);
    move_uploaded_file($file_upload["tmp_name"], "./upload/" . $uploaded_filename . "/" . $file_upload["name"]);
    $str_python .= " -f " . "./upload/" . $uploaded_filename . "/" . $file_upload["name"] . " -d ./files/" . $uploaded_filename . "/";

    if ($python_option_entete == "true") {
        $str_python .= " -e";
    }

    if ($python_option_ref == "true") {
        $str_python .= " -r";
    }
}

exec($str_python, $output, $code);
$files_siren = scandir("./files/" . $siren . "/");
$files_multisirens = scandir("./files/" . $uploaded_filename . "/");

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
        $mail->addCC('test.infogreffe@gmail.com');

        if (!$file_upload) {
            foreach ($files_siren as $file) {
                if ($file != '.' && $file != '..' && $file != '.DS_Store' && $file != '.gitkeep') {
                    $mail->addAttachment("./files/" . $siren . "/" . $file);
                }
            }
        } else {
            foreach ($files_multisirens as $file) {
                if (pathinfo($file, PATHINFO_EXTENSION) == 'csv') {
                    $mail->addAttachment("./files/" . $uploaded_filename . "/" . $file);
                }
            }
        }

        if ($file_upload) {
            foreach ($files_multisirens as $file) {
                if (pathinfo($file, PATHINFO_EXTENSION) == 'pdf') {
                    $zip = new ZipArchive();
                    if ($res_zip != "") {
                        $filename = $res_zip . ".zip";
                    } else {
                        $filename = $uploaded_filename . ".zip";
                    }
                    $filename_compl = "./zip/" . $uploaded_filename . "/" . $filename;
                    $zip->open($filename_compl, ZIPARCHIVE::CREATE);
                    addFileToZip("./files/" . $uploaded_filename . "/", $zip);
                    $zip->close();
                }
            }

            if (!$filename_compl) {
                echo "\n Erreur de format des donnnées du fichier (ou il n'y a aucun siren qui peut générer un pdf): " . $output . " (vient du Python)\n";
            } else {
                /**
                 * Send zip to the server by sftp
                 */
                try
                {
                    $sftp = new SFTPConnection("10.168.128.120", 22);
                    $sftp->login("rbe", "Rbe2019");
                    $sftp->uploadFile($filename_compl, "/home/rbe/" . $filename);
                } catch (Exception $e) {
                    echo "Erreur de SFTP: " . $e->getMessage() . "\n";
                }
            }
        }

        $mail->isHTML(true);
        $mail->Subject = 'ExDIBE - ' . $ident;
        $mail->Body = email_body_html($ident, $commentaire);
        $mail->AltBody = "IDENTIFIANT: " . $ident . " COMMENTAIRE: " . $commentaire;
        $mail->send();

        /**
         *  Clean up
         */
        clean_up($siren, $v, $uploaded_filename);
        /******************************/

        echo "200";

    } catch (Exception $e) {
        echo $mail->ErrorInfo;
    }
} else {
    echo "Erreur du programme Python.";
}

function addFileToZip($path, $zip)
{
    $handler = opendir($path); //打开当前文件夹由$path指定。
    while (($filename_compl = readdir($handler)) !== false) {
        if ($filename_compl != "." && $filename_compl != ".." && $filename_compl != ".DS_Store" && pathinfo($filename_compl, PATHINFO_EXTENSION) == 'pdf') { //文件夹文件名字为'.'和‘..’，不要对他们进行操作
            if (is_dir($path . "/" . $filename_compl)) { // 如果读取的某个对象是文件夹，则递归
                addFileToZip($path . "/" . $filename_compl, $zip);
            } else { //将文件加入zip对象
                $zip->addFile($path . "/" . $filename_compl);
            }
        }
    }
    @closedir($path);
}

function email_body_html($ident, $commentaire)
{
    return "
        <div style=\"background: #ebe4e0;font-size:1.2em;\">
            <div style=\"margin: 0 auto;text-align: center;font-size: 150%;padding: 3em 0;\">
                <div style=\"max-width: 500px;width: calc(100% - 2em);margin: 1em auto;color: #fff;background: #A2C616;line-height: normal;border-radius: 20px;padding: 1.2em;font-weight: bold;\">
                    <span style=\"font-size: 100%;\">ExDIBE</span>
                </div>
                <div style=\"max-width: 500px;width: calc(100% - 2em);margin: 1em auto;color: #fff;background: #A2C616;line-height: normal;border-radius: 20px;padding: 1.2em;\">
                    <span style=\"font-size: 90%;font-weight: bold;\">Identifiant</span>
                    <br>
                    <span style=\"font-size: 70%;\">$ident</span>
                </div>
                <div style=\"max-width: 500px;width: calc(100% - 2em);margin: 1em auto;color: #6a7f95;background: #fff;line-height: normal;border-radius: 20px;padding: 1.2em;\">
                    <span style=\"font-size: 90%;font-weight: bold;\">Commentaire</span>
                    <br>
                    <span style=\"font-size: 70%;color:#798ca0\">$commentaire</span>
                </div>
            </div>
        </div>
    ";
}

function clean_up($siren, $multisirens, $file_upload)
{
    $url_cp = ($multisirens ? $file_upload : $siren);

    $files = scandir("./files/" . $url_cp . "/");
    $zips = scandir("./zip/" . $url_cp . "/");
    $upload = scandir("./upload/" . $url_cp . "/");

    foreach ($files as $file) {
        if ($file != '.gitkeep') {
            @unlink("./files/" . $url_cp . "/" . $file);
        }

    }
    foreach ($zips as $zip_f) {
        if ($zip_f != '.gitkeep') {
            @unlink("./zip/" . $url_cp . "/" . $zip_f);
        }

    }
    foreach ($upload as $upload_f) {
        if ($upload_f != '.gitkeep') {
            @unlink("./upload/" . $url_cp . "/" . $upload_f);
        }

    }

    rmdir('./files/' . $url_cp);
    rmdir('./zip/' . $url_cp);
    rmdir('./upload/' . $url_cp);
}
