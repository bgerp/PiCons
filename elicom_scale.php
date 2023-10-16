<?php



/*
 * 000050A - нестабилно 50 гр.
 * 000150B - стабилно 150 гр.
 *
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

$res = "";
$cnt = 0;
$ch = '';
$stable = false;

// Търсим първият стринг с дължина 6 и завършващ на 'B'
while ($stable != true) {
    $ch = fgetc($fp);
    if ($ch != 'B') {;
        $res .= $ch; $cnt++;
    } elseif ($cnt == 6) {
        $stable = true;
    }
}
fclose($fp);

echo ($res);

$weight = substr($res,0,3) . "." . substr($res,3,6);
$weight = substr($res,0,3) . "." . substr($res,3,6);
$weight =  number_format($weight, 3, '.', '');

$err = true;

if (!$err) {
	$tmpl = str_replace('[#0.000#]', $weight, $tmpl);
} else {
	$tmpl = str_replace('[#0.000#]', 'PORT_BUSSY', $tmpl);
}

