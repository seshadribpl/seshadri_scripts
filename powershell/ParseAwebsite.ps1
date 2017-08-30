Invoke-WebRequest -Uri "https://www.microsoft.com/en-in/"  -OutFile c:\tmp\microsoft.html 

$fileName =  "C:\tmp\microsoft.html"
$searchString = "Xbox"

$searchStatus = Select-String -Pattern $searchString -path $fileName

if ($searchStatus)
 {
  Send-MailMessage -to kothand@arcesium.com -Subject "Found the string: $searchString" -from kothand@arcesium.com -SmtpServer postmulti-relay.deshaw.com
 }

else
 {
  write-host "String `"$searchString`" not found on the web page"
 }