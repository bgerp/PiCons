<?php 
if (strpos($_GET['redirectUrl'], 'https://bags.bg') !== false ) {
    header("Location: " . $_GET['redirectUrl']);
} else {
    header("Location: http://localhost:8181/?err=Грешен баркод!");
}
exit();
?>