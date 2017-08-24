 awk ' {pay = pay + $2*$3};  $2 > maxpay { maxpay = $2}; $3 > maxhr {maxhr = $3; maxp = $1}; $2 < minpay {minpay = $2; minemp = $1} END {print "total pay is: " pay " total employees is: " NR " } average pay is " pay/NR " and the maximum pay is " maxpay " Max hrs is " maxhr " by " maxp   \ 
" and min pay is " minpay " for " minemp"}'
