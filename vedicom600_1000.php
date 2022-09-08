<?php

/*
 *
 *p-0000.2
 *p-0000.2
 *p-0000.2
 *P+0108.6
 *P+0108.6
 *P+0108.6

 
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

define ('DEVICE', '/dev/ttyUSB0');
//define ('DEVICE', '/dev/ttyS0');
clearstatcache();
$fp = fopen(DEVICE,'r');
//stream_set_blocking($fp, 0);
$res = [];
$value = "";
$cnt = 0;
// четем 4 пъти, търсим 2 последователни равни стринга за стабилно състояние /всеки 2-ри 3 празен стринг/
for ($i=1; $i<=4; $i++ ) {
	$res = trim(fgets($fp));
	if (!empty($res)) {
		preg_match_all("/[+-]?([0-9]*[.])?[0-9]+/", $res, $resV);
		if ($value == $resV[0][0] && is_numeric($value)) {
		    $value = str_replace("+", "", $value);
		    $value = str_replace("-", "", $value);
		    break; 
		} else {
			$value = $resV[0][0];
		}

	}
}
fclose($fp);

$weight = 0;
if (is_numeric($value)) {
	$weight = $value;
} else {
	$err = true;
}
if (!$err) {
	$tmpl = str_replace('[#0.000#]', $weight, $tmpl);
} else {
	$tmpl = str_replace('[#0.000#]', 'PORT_BUSSY', $tmpl);
}
