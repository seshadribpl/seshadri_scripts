<# 
  .SYNOPSIS
    Get Arc AD members from Desco
  .DESCRIPTION
    Get Arc AD members from Desco
#>

[CmdletBinding()]
Param()

$groups = Get-DescoADGroup -SearchRoot "dc=deshaw,dc=com" -AdditionalLDAP "(mail=*)" -PropertiesToLoad mail, member, name
$arcrelatedgroups = @()
foreach($group in $groups)
{
  Write-verbose ("Checking {0}..." -f $group.name)
  $isrelated = $false
  foreach($member in $group.member)
  {
    if($member -match "arcesium")
    {
      Write-Verbose ("{0} is a match" -f $member) 
      $isrelated = $true
    }
  }
  if ($isrelated)
    {
    $properties =  @{
      name = $group.name
      mail = $group.mail
      member = $group.member
    }
    $obj = New-Object -TypeName PSObject -Property $properties
    $obj
    }
}