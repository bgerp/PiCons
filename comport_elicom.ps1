$ports= new-Object System.IO.Ports.SerialPort COM1,9600,None,8,one
$ports.open()
#echo $ports.ReadTo("B")
#echo $ports.ReadExisting()
$ports.close()
