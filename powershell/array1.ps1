# get-service |Select-Object -first 10 | Where-Object {$_.Status -eq "Running"}
# get-psprovider|select-object Implementingtype,Name
# get-service |Select-Object -first 10 | Where-Object {$_.Canshutdown-eq "yes"}
# get-service |select-object -last 5 |where-object {$_.status -ne "stopped"}
# Get-psdrive |sort Provider, Name,Used
# Get-psdrive  | Format-List 
# cd env:
# dir u:\ |Get-Member
# dir u:\ |Where-Object {$_.Name -like "*hy*"}
$myarray = @("aa", "bb")
$myarray
foreach($item in $myarray) {Write-Host "The item is now: $item"}