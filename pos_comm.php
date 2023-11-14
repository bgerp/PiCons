<?php
// exec ('powershell C:\Users\epuser\Documents\GitHub\PiCons\pos_comport.ps1');

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
$res = [];
do {
   $res[] = ord(fgetc($fp));
   if (end($res) == 3) {
	   $end = true;
	   // Четем кода по четност
	   $resPCheck = ord(fgetc($fp));
   }

} while ($end != true);

//fclose($fp);
// Махаме първия байт 06 - ACK - Acknowledge
unset($res[0]);
// Махаме втория байт 02 - STX - Start of Text
unset($res[1]);

// Проверяваме сумата по четност
$PCheck = 0;
foreach ($res as $byte) {
	$PCheck ^= $byte; 
}
if ($PCheck != $resPCheck) die ("Parity Check ERROR!");

var_dump ($res, $PCheck, $resPCheck);


//------------ Пращаме сума

     // $cmd = "06    02    34    30    31    31    30 30 30 30 30 30 30 30 30 31 35 38 39 37 35 39 39 39 39 03 30"

$rSum = array(0x06,0x02,0x34,0x30,0x31,0x31,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x31,0x35,0x38,0x39,0x37,0x35,0x39,0x39,0x39,0x39,0x03,0x30);

foreach ($rSum as $b) {
	if (fputs($fp, chr($b)) === false) {
		die("Can`t write to port.");
	}
}
echo "writed SUM...\n\r";
$end = false;
$res = [];
do {
   $res[] = ord(fgetc($fp));
   if (end($res) == 3) {
	   $end = true;
	   // Четем кода по четност
	   $resPCheck = ord(fgetc($fp));
   }

} while ($end != true);

fclose($fp);
// Махаме първия байт 06 - ACK - Acknowledge
unset($res[0]);
// Махаме втория байт 02 - STX - Start of Text
unset($res[1]);

// Проверяваме сумата по четност
$PCheck = 0;
foreach ($res as $byte) {
	$PCheck ^= $byte; 
}
if ($PCheck != $resPCheck) die ("Parity Check ERROR!");

var_dump ($res, $PCheck, $resPCheck);
