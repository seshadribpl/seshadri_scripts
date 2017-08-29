function getinfo 
{

  [cmdletbinding()]
  param($computername)
  
  $sysinfo = Get-WmiObject -class win32_computersystem -ComputerName $computername
  $osinfo = Get-WmiObject -class win32_operatingsystem -ComputerName $computername
  $biosinfo = Get-WmiObject -class win32_bios -ComputerName $computername

  $properties = @{
    computerName = $sysinfo
    manufacturer = $sysinfo.manufacturer
    model = $sysinfo.model
    OS = $osinfo.caption
    operatingSystemVersion = $osinfo.version
    serialNumber = $biosinfo.serialnumber
    }

    New-Object -TypeName PSobject -Property $properties



}

getinfo -computername tuberose