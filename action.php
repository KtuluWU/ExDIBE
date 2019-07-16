<?php
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

$url = "/Users/yw/Sites/ExDIBE/dibe_pdf_v2.py";
$url_windows = "C:/xampp/htdocs/ExDIBE/dibe_pdf_v2.py";
$url_files = "/ExDIBE/files/";

$str_python = "/usr/local/bin/python3 " . $url . " -i " . $ident . " -p " . $pwd . " -d ./files";
// $str_python = "python ".$url_windows." -i ".$ident." -p ".$pwd." -d ./files";

if ($siren && !$file_upload) {
    $str_python .= " -s " . $siren;
} else if ($file_upload && !$siren) {
    move_uploaded_file($file_upload["tmp_name"], "./upload/" . $file_upload["name"]);
    $str_python .= " -f " . "./upload/" . $file_upload["name"];

    if ($python_option_entete == "true") {
        $str_python .= " -e";
    }

    if ($python_option_ref == "true") {
        $str_python .= " -r";
    }
}

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

        foreach ($files as $file) {
            if ($file != '.' && $file != '..' && $file != '.DS_Store') {
                if (!$file_upload) {
                    $mail->addAttachment("./files/" . $file);
                } else {
                    if (pathinfo($file, PATHINFO_EXTENSION) == 'csv') {
                        $mail->addAttachment("./files/" . $file);
                    }
                }
            }
        }

        $mail->isHTML(true);
        $mail->Subject = 'ExDIBE - ' . $ident;
        $mail->Body = "<h2>IDENTIFIANT: " . $ident . "</h2><br><h2>COMMENTAIRE: </h2><br>" . $commentaire;
        $mail->AltBody = "IDENTIFIANT: " . $ident . " COMMENTAIRE: " . $commentaire;

        $mail->send();

        if ($file_upload) {
            foreach ($files as $file) {
                if (pathinfo($file, PATHINFO_EXTENSION) == 'pdf') {
                    $zip = new ZipArchive();
                    $filename = "./zip/" . $res_zip . ".zip";
                    $zip->open($filename, ZIPARCHIVE::CREATE);
                    addFileToZip("./files/", $zip);
                    $zip->close();
                }
                @unlink("./files/" . $file);
            }

            /**
             * Send zip to the server by ssh
             */
            try
            {
                $sftp = new SFTPConnection("10.168.128.120", 22);
                $sftp->login("rbe", "Rbe2019");
                $sftp->uploadFile("./zip/" . $res_zip . ".zip", "/home/rbe/" . $res_zip . ".zip");
            } catch (Exception $e) {
                echo $e->getMessage() . "\n";
            }

            @unlink("./zip/" . $res_zip . ".zip");

            /******************************/

            @unlink("./upload/" . $file_upload["name"]);
        } else {
            foreach ($files as $file) {
                @unlink("./files/" . $file);
            }
        }

        echo "200";

    } catch (Exception $e) {
        echo $mail->ErrorInfo;
    }
} else {
    echo "Échec du programme Python.";
}

function addFileToZip($path, $zip)
{
    $handler = opendir($path); //打开当前文件夹由$path指定。
    while (($filename = readdir($handler)) !== false) {
        if ($filename != "." && $filename != ".." && $filename != ".DS_Store" && pathinfo($filename, PATHINFO_EXTENSION) == 'pdf') { //文件夹文件名字为'.'和‘..’，不要对他们进行操作
            if (is_dir($path . "/" . $filename)) { // 如果读取的某个对象是文件夹，则递归
                addFileToZip($path . "/" . $filename, $zip);
            } else { //将文件加入zip对象
                $zip->addFile($path . "/" . $filename);
            }
        }
    }
    @closedir($path);
}
