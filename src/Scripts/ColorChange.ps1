function sendColor($colorName)
{
    $portInfo = ( Get-WmiObject Win32_SerialPort | Where { $_.PNPDeviceID -like '*VID_239A*' } | select -last 1 )
    $port = new-Object System.IO.Ports.SerialPort $portInfo.DeviceID,9600,None,8,one
    $port.open()
    $text = $colorName + "`r"
    $port.Write($text)
    start-sleep -m 50
    $port.ReadExisting()
    $port.Close()
}
if ($args.Length -eq 0)
{
    echo "Usage: ColorChange <color>"
}
else
{
    sendColor($args[0])
}