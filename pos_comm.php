<?php
exec ('powershell C:\Users\1064\PiCons\comport_pos.ps1');

define ('DEVICE', 'COM1');
clearstatcache();
$fp = fopen(DEVICE,'r+');
//stream_set_blocking($fp, 0);

// Request approval
$rApproval = array(0x02, 0x31, 0x30, 0x31, 0x03, 0x33);
foreach ($rApproval as $b) {
	if (fputs($fp, chr($b)) === false) {
		die("Can`t write to port.");
	}
}
echo "writed ...\n\r";
$end = false;
$res ="";
while ($end != true) {
   $res .= ord(fgetc($fp)) . " ";
   if (strlen($res) == 7) {
	   $end = true;
   }
}
echo ($res);

// Търсим първият стринг с дължина 6 и завършващ на 'B'
