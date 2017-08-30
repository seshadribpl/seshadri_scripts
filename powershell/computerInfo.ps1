$a = "<style>"
$a = $a + "BODY{background-color:peachpuff;}"
$a = $a + "TABLE{border-width: 1px;border-style: solid;border-color: black;border-collapse: collapse;}"
$a = $a + "TH{border-width: 1px;padding: 0px;border-style: solid;border-color: black;background-color:grey}"
$a = $a + "TD{border-width: 1px;padding: 0px;border-style: solid;border-color: black;background-color:palegoldenrod}"
$a = $a + "</style>"

# $a = "<style>BODY{background-color:peachpuff;}</style>"
Get-CimInstance win32_operatingsystem | Select-Object BootDevice,Manufacturer,Name,Organization,SerialNumber,CSName,Caption,SystemDrive,InstallDate,TotalVisibleMemorySize | ConvertTo-Html -head $a|
 Out-File H:\scripts\powershell\computerInfo.html

# $b = "<style>BODY{background-color:peachpuff;}</style>"

# $t = @{Expression={$_.Name};Label="Software"}

# Get-WmiObject -class win32_product |Select-Object Name | convertto-html -head $a | Out-File -Append H:\scripts\powershell\computerInfo.html
Get-WmiObject -class win32_product |Select-Object Name | convertto-html | Out-File -Append H:\scripts\powershell\computerInfo.html



Invoke-Expression H:\scripts\powershell\computerInfo.html

