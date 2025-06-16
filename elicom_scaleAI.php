<?php
// --- Начални настройки ---
header("Content-Type: application/xml; charset=utf-8");

$tmpl = "<?xml version='1.0' encoding='UTF-8' ?>" . 
	"<monitor>" .
    	"<item>" . 
    		"<Unit>KG</Unit>" .
    		"<Value>[#VALUE#]</Value>" . // Грешки: UNSTABLE, NO_CONNECTION
            "<Name>ElicomScale1</Name>" .
         "</item>" .
	"</monitor>";

// --- Конфигурация на порта ---
//define ('DEVICE', '/dev/ttyUSB0');
define ('DEVICE', '/dev/ttyS0');
//define ('DEVICE', 'COM1');

// --- Логика ---
$error_message = null;
$weight_formatted = '0.000'; // Форматирано тегло в кг

// Потискаме грешките при отваряне с @, за да ги обработим ръчно
$fp = @fopen(DEVICE, 'r');

if ($fp === false) {
    // Грешка: Портът не може да бъде отворен (зает, не съществува, няма права)
    $error_message = 'NO_CONNECTION';
} else {
    // НОВО: Превключваме порта в НЕБЛОКИРАЩ режим.
    // Това е ключово, за да може нашият цикъл с таймер да работи коректно.
    stream_set_blocking($fp, false);

    $stable = false;
    $startTime = time(); // Вземаме началното време за нашия 3-секунден таймер

    // Цикълът се изпълнява, докато не минат 3 секунди ИЛИ докато не намерим стабилно тегло
    while ((time() - $startTime) < 3 && !$stable) {
        
        // НОВО: Опитваме се да прочетем точно 7 байта (един цял пакет)
        $packet = fread($fp, 7);

        // Проверяваме дали сме получили пълен пакет от 7 байта
        if ($packet && strlen($packet) === 7) {
            
            // Проверяваме последния символ за стабилност ('B')
            if (substr($packet, -1) === 'B') {
                
                // Намерено е стабилно тегло!
                // Вземаме първите 6 символа и ги преобразуваме в число (грамове)
                $weight_grams = (int)substr($packet, 0, 6);
                
                // Преобразуваме грамовете в килограми
                $weight_kg = $weight_grams / 1000;
                
                // Форматираме до 3 знака след запетаята
                $weight_formatted = number_format($weight_kg, 3, '.', '');
                
                $stable = true; // Маркираме, че сме намерили стабилно тегло, за да спрем цикъла
            }
            // Ако последният символ е 'A' или друг, просто игнорираме пакета и продължаваме да четем
        }
        
        // Малка пауза, за да не натоварваме процесора на 100%
        usleep(50000); // 50 милисекунди
    }

    // Затваряме връзката с порта
    fclose($fp);

    // НОВО: Проверяваме защо е приключил цикълът.
    // Ако е приключил заради изтичане на времето ($stable все още е false), значи имаме грешка.
    if (!$stable) {
        $error_message = 'UNSTABLE';
    }
}

// --- Генериране на финалния XML ---
$final_value = $error_message ? $error_message : $weight_formatted;
$tmpl = str_replace('[#VALUE#]', $final_value, $tmpl);

echo $tmpl;
?>