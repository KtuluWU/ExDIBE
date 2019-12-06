<?php



use PHPMailer\PHPMailer\Exception;

$data = include 'config.php';

$str_python_param = $data['str_python_param'];

$str_python = $str_python_param . " -i " . "08500-00170";
$str_python .= " -s " . "775573009" . " -d ./files/" . "775573009";

mkdir('./files/' . "775573009", 0777, true);

exec("/Library/Frameworks/Python.framework/Versions/3.7/bin/python3 /Users/yw/Sites/ExDIBE/dibe_datas2.py -i 08500-00170 -s 775573009 -d ./files/775573009 2>&1", $ouput, $code);
print_r($ouput);
