<?php
if (!empty($_GET['err'])) {
    $err = $_GET['err'];
}
echo ("
<form name='bgERP' method=get action='redirect.php'>
" . (empty($err)?'':"<div><font style='color: red;'>" . $err . "</font></div>") .  
	"<span style='1color: green; font-size: 12pt'>Въведете баркода от работната карта: </span><input name=redirectUrl type=text autofocus></input>
</form>

");
?>
