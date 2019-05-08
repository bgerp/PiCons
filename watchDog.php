<?php
function value_in($element_name, $xml, $content_only = true)
{
	if ($xml == false) {
		return false;
	}
	$found = preg_match('#<'.$element_name.'(?:\s+[^>]+)?>(.*?)'.
		            '</'.$element_name.'>#s', $xml, $matches);
	if ($found != false) {
		if ($content_only) {
			return $matches[1];  //ignore the enclosing tags
		} else {
			return $matches[0];  //return the full pattern match
	        }
	}
        // No match found: return false.
	return false;
}

$xml = exec('curl -s --connect-timeout 3 --max-time 3 http://localhost/?ElectronicScales=1');
$value = value_in('Value',$xml); //var_dump(is_float($value)); die;
if (strlen($value)<2) {
	`sudo pkill python`;
	`git --work-tree="/home/pi/PiCons/" checkout settings.ini`;
	`sudo python /home/pi/PiCons/main.py > /dev/null 2>&1 &`;
	file_put_contents('/home/pi/PiCons/watchDog.log',date("Y-m-d H:i:s") . " - restarted ... \n", FILE_APPEND);

	exit;
}

// на всеки 5 мин рестартираме PiCons сървъра, защото по незнайни причини се губи теглото.
if ( time()%300 == 0 ) {
    `sudo pkill python`;
    `sudo python /home/pi/PiCons/main.py > /dev/null 2>&1 &`;
}

// file_put_contents('/home/pi/PiCons/watchDog.log',date("Y-m-d H:i:s") . " - OK ... \n", FILE_APPEND);
