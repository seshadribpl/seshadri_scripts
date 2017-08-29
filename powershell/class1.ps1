class animal
{
  
  [string]$name
  [int]$maxAge
  
}

$tommy = New-Object animal
$tommy.name = "dog"
$tommy.maxAge = 14

$tommy

$pihu = New-Object animal
$pihu.name = "bird"
$pihu.maxAge = 4

$pihu
