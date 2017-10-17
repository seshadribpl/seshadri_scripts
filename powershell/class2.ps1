class student{
    [string]$name
    [int]$age
    }

$student1 = [student]::new()
$student1.name =  "Trisha"
$student1.age = 13

$student2 = [student]::new()
$student2.name = "Juhi"
$student2.age = 10

$student1
$student2

$i = 10

do
{
    Write-Host $i
    $i--
}
until ($i -lt 5)
Write-Host "-----------------"

$j = 8
do
{
    Write-Host $j
    $j--
}
while ($j -gt 5)