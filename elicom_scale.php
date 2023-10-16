<?php

/*
 * US,GS,+ 7.14 kg
 *US,GS,+  27.26kg
 *ST,GS,+      0 g
 *US,GS,+  23550 g
 *ST,GS,+   0.00lb
 *US,GS,+  61.36lb
 *ST,GS,+    0.0oz
 *US,GS,+ 1071.0oz
 
**/

$tmpl = "<?xml version='1.0' encoding='UTF-8' ?>" . 
	"<monitor>" . 
	"<Devices>" .
	"<item>" . 
	"<Name>D19</Name>" .
	"<Entries>" .
	"<item>" . 
		"<Unit>KG</Unit>" .
		"<ID>20</ID>" .
		"<Value>[#0.000#]</Value>" . // UNSTABLE, NO_CONNECTION, PORT_BUSSY
		"<Name>ElectronicScale1</Name>" .
		"</item>" .
	"</Entries>" .
	"</item>" .
        "</Devices>" .	
	"</monitor>";

//define ('DEVICE', '/dev/ttyUSB0');
//define ('DEVICE', '/dev/ttyS0');
define ('DEVICE', 'COM1');
clearstatcache();
$fp = fopen(DEVICE,'r');
//stream_set_blocking($fp, 0);

$value = $res = "";
$cnt = 0;
$ch = '';

// търсим 2 последователни равни стринга или стабилно състояние /всеки 2-ри 3 празен стринг/
while ($ch!='B') {
    $ch = fgetc($fp);
    if (!empty($ch)) { echo ($ch . "\n");
        $res .= $ch;
    }
}
fclose($fp);
echo ($res);



if (!$err) {
	$tmpl = str_replace('[#0.000#]', $weight, $tmpl);
} else {
	$tmpl = str_replace('[#0.000#]', 'PORT_BUSSY', $tmpl);
}

