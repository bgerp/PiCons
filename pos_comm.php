<?php
// exec ('powershell C:\Users\epuser\Documents\GitHub\PiCons\pos_comport.ps1');

function cmdWrite ($fp, $cmd)
{
	foreach ($cmd as $b) {
		if (fputs($fp, chr($b)) === false) {
			
			return false;
		}
	}
	
	return true;
}

function cmdRead($fp)
{
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
	
	return $res;
}

function parityCheck(array $arr) 
{
	// Махаме първия байт 06 - ACK - Acknowledge
	if ($arr[0] == 0x6 || $arr[0] == 0x2) unset($arr[0]);
	// Махаме втория байт 02 - STX - Start of Text
	if ($arr[1] == 0x2) unset($arr[1]);

	// Изчисляваме сумата по четност
	$PCheck = 0;
	foreach ($arr as $byte) {
		$PCheck ^= $byte; 
	}
	
	return ([$PCheck]);
}

define ('DEVICE', 'COM1');
clearstatcache();
$fp = fopen(DEVICE,'r+');
//stream_set_blocking($fp, 0);

$STX = [0x02]; // STX - Start of Text
$ETX = [0x03]; // ETX - End of Text
$АСК = [0x06]; // ACK - Acknowledge

// Request approval
$rApproval = array(0x02, 0x31, 0x30, 0x31, 0x03, 0x33);
if (!cmdWrite($fp,$rApproval)) die('Write error!');
$res = cmdRead($fp);
var_dump($res);

//------------ Пращаме сума 12 байта
$amount = '423.78';
$amount = intval((100*floatval($amount)));
$amount = str_pad("$amount", 12, "0", STR_PAD_LEFT);
$amountArr = unpack('C*', $amount);
    //$cmd = "06 02 34 30 31 31    30 30 30 30 30 30 30 30 30 31 35 38      39 37 35 39 39 39 39 03 30"
	//$amountCmd = array(0x06,0x02,0x34,0x30,0x31,0x31,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x31,0x35,0x38,0x39,0x37,0x35,0x39,0x39,0x39,0x39,0x03,0x30);
	
$amountCmd = array_merge([0x06,0x02,0x34,0x30,0x31,0x31], $amountArr, [0x39,0x37,0x35], [0x39,0x39,0x39,0x39], $ETX);
$amountCmd = array_merge($amountCmd, parityCheck($amountCmd));

if (!cmdWrite($fp,$amountCmd)) die('Write error!');

$res = cmdRead($fp);

var_dump($res);

fclose($fp);
