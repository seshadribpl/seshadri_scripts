function echoname()

{

  [cmdletbinding()]
  param($name)
  

  write-host "Checking whether $name exists in the AD..."

}

function checkADuser()
{
  [cmdletbinding()]
  param($name)
  try
    {
      get-aduser -Identity $name |Out-Null
      Write-Output "User `"$name`" exists in the AD"
    }
  catch
    {
      Write-Output "No such user `"$name`" in the AD"
    }
}


$users = @("kothand", "foobar", "trucks", "hughesd")
cls
foreach($name in $users)
{
  echoname($name)
  checkADuser($name)
}

