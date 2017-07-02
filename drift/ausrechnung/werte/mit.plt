set terminal png enhanced font arial 30 size 1600,1200
set encoding utf8



set title "Messung mit Quelle"
#f1(x)=a*x+b
#f2(x)=c*x+d


#set xrange [0:50]
set xlabel "U/kV"
set ylabel "I/A"
unset key

#set grid ytics lt 0 lw 1 lc rgb "#bbbbbb"
#set grid xtics lt 0 lw 1 lc rgb "#bbbbbb"

set output "mit.png"

#fit f1(x) "ver.txt" using 1:4 via a, b 
#fit f2(x) "hor.txt" using 1:4 via c, d

plot "mit.dat" u 1:3:($2/2):($4*3) pt 3 ps 4 lw 2 with xyerrorbars
#"hor.txt" u ($1):4:(0.04)1:(10) pt 1 ps 4 with xyerrorbars, f2(x)
pause 1
