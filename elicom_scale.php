<?php

// За Windows
if (substr(php_uname(), 0, 7) === "Windows") {
    exec("mode COM1 96,n,8");
}
/*
 * 000050A - нестабилно 50 гр.
 * 000150B - стабилно 150 гр.
 *
**/
$tmpl = "<?xml version='1.0' encoding='UTF-8' ?>" . 
	"<monitor>" .
    	"<item>" . 
    		"<Unit>KG</Unit>" .
    		"<Value>[#0.000#]</Value>" . // UNSTABLE, NO_CONNECTION, PORT_BUSSY
            "<Name>ElicomScale1</Name>" .
         "</item>" .
	"</monitor>";

//define ('DEVICE', '/dev/ttyUSB0');
define ('DEVICE', '/dev/ttyS0');
//define ('DEVICE', 'COM1');
clearstatcache();
$fp = fopen(DEVICE,'r');
//stream_set_blocking($fp, 0);
//stream_set_timeout($fp, 2);
$res = "";
$stable = false;

$startTime = time();

// Търсим първият стринг с дължина 6 и завършващ на 'B'
while ((time() - $startTime) < 3 && !$stable) {
    $res .= fgetc($fp);
    if (strlen($res)>6 && (false !== strpos($res, "B"))) {
		$stable = true;
    }
}
fclose($fp);
$weight = substr($res,strlen($res)-7,3) . "." . substr($res,strlen($res)-4,3);
$weight =  number_format($weight, 3, '.', '');

$err = false;

if (!$err) {
	$tmpl = str_replace('[#0.000#]', $weight, $tmpl);
} else {
	$tmpl = str_replace('[#0.000#]', 'PORT_BUSSY', $tmpl);
}
echo $tmpl;
