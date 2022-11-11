<?php
if ($_SERVER["REQUEST_METHOD"] != 'GET') {
    
    exit;
}

#include ('vedicom600_1000.php');
include ('standard_scale.php');

//header("Content-type: text/xml");
header("Access-Control-Allow-Origin: * ");
echo ($tmpl);

