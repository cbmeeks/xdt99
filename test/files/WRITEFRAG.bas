100 REM CREATE FRAGMENTED DISK

110 FOR F=1 TO 16
120 OPEN #1:"DSK2.F"&STR$(F),DISPLAY,OUTPUT,VARIABLE 127
130 CLOSE #1
140 NEXT F

200 FOR R=1 TO 20
210 FOR F=1 TO 16
220 PRINT R;F;"OF 20, 16"

300 D$=CHR$(64+R)&CHR$(96+F)
310 FOR I=1 TO 5 :: D$=D$&D$ :: NEXT I  ! LEN == 64
320 OPEN #1:"DSK2.F"&STR$(F),DISPLAY,APPEND,VARIABLE 127
330 PRINT #1:">";D$;"<"
340 CLOSE #1

400 NEXT F
410 NEXT R

999 END
