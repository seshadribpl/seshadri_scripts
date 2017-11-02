class student
{
  [string]$name
  [int]$age
  [string]$colour
  [string]$gender
}

$trisha =  New-Object student
$trisha.name = "Trisha"
$trisha.age = 14
$trisha.colour = "blue"
$trisha.gender =  "female"

$trisha