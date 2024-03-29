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
define ('DEVICE', '/dev/ttyS0');
clearstatcache();
$fp = fopen(DEVICE,'r');
//stream_set_blocking($fp, 0);

$value = $res = "";
$cnt = 0;
// търсим 2 последователни равни стринга или стабилно състояние /всеки 2-ри 3 празен стринг/
while ($cnt<1) {
    $res = trim(fgets($fp));
    if (!empty(trim($res))) { //echo ($res . "\n");
        if ($value == $res || (true === strpos($res, "ST,GS"))) {
            $cnt++;
        } else {
            $value = $res;
        }
        
    }
}
fclose($fp);

$valueArr = explode (' ', $value);
$err = true;
$weight = 0;

foreach ($valueArr as $value) {

	$value = str_replace('kg', '', $value, $cnt);
	if (is_numeric($value)) {
		$weight = $value; //echo($weight); die;
	}
	if ($cnt > 0) {
		$err = false;
	}
}
if (!$err) {
	$tmpl = str_replace('[#0.000#]', $weight, $tmpl);
} else {
	$tmpl = str_replace('[#0.000#]', 'PORT_BUSSY', $tmpl);
}

