
      program digest2

******************************************************************
*
* Digest2 is a Fortran code that determines the probability that 
* an asteroid is of a particular dynamic class based on the sky
* motion of the asteroid. The digest2 code is an amalgamation of
* a Rob McNaught/David Asher code named Pangloss that determines
* orbital elements for two astrometric positions and a bunch of
* code by Carl Hergenrother that determines the probabilities that
* an object is unusual and other assorted stuff. CWH 2002-03-19
*
******************************************************************

******************************************************************
* NOTE: Code in caps are McNaught/Asher code while lower case 
*       lines are Hergenrother.
******************************************************************

      IMPLICIT NONE

      LOGICAL FLAG
      REAL*8 DAY,Q,E,JD1,DT,R
      REAL*8 RA,W,N,I,XS,YS,ZS,ELONG,PSI,K,W1,N1,I1,W2,N2,I2
      REAL*8 M1,TH,N0,mb_count,neo_count,h18n,score
      REAL*8 LONG,DXY,DZ,A
      REAL*8 RD,RSUN(2)
      REAL*8 MEAN
      REAL*8 EE(2,3),DD(0:2,3),DE,T(2)
      REAL*8 O(3),V(3),D1,D2,TZ,DP,AL,T0,AA,BB,CC,U,SA,CA,ANG(2),AN
      REAL*8 MAGOBS(2),HMAG,G,AET2M
      REAL OBS(999,3),ET
      INTEGER YEAR,MONTH,NUMBER,OBSCODE,IUNIT,IUOUT
      INTEGER EPOCH,II,PARAB,ARC,NUMOBS,l,i3,i4
      real semi1(20000),ecc1(20000),ncl1(20000)
      real h6(20000),h7(20000),h8(20000),h9(20000),h10(20000)
      real h11(20000),h12(20000),h13(20000),h14(20000),h15(20000)
      real h16(20000),h17(20000),h18(20000),h19(20000),h20(20000)
      real h21(20000),h22(20000),h23(20000),h24(20000),h25(20000)
      real h26(20000),h27(20000),h28(20000),h29(20000),h30(20000)
      integer az,ez,nz,aaa,i5
      integer year8,year9,month8,month9,rahr8,rahr9,ramin8,ramin9
      integer deg8,deg9,decmin8,decmin9,obscode8,obscode9
      double precision rasec8,rasec9,decsec8,decsec9,day8,day9
      real ncl,ecc,semi,semiadd,eccadd,ncladd,magn8,magn9
      real dddd1,dddd2,aaa1,aaa2,bbb1,bbb2,rate,bcd,lcd
      real pi,drad,lc1,lc2,magobs2,score2

      character    desig2*13,desig8*13,desig9*13
      character    sign8,sign9,magtype8,magtype9
      CHARACTER    DESIG*7,OBSN*80,neoflag*3
      CHARACTER*1  COMPUTER,MONSTR,DAYSTR,MAGTYPE(2),CDUM1(3)
      CHARACTER*3  MONTHNAME(12),YRSTR
      CHARACTER*99 INPUTFILE,FLNM
      CHARACTER*50 OBSNAME(999)
      open(31,file='test8.out')
      open(32,file='AST.BIAS.POP')
      open(33,file='digest.hold',status='unknown')

59    FORMAT(1X,F5.3,1X,F5.1,1X,F4.0,1X,F6.3,1X,F6.3,1X,
     /       F7.3,1X,F7.3,1X,F7.3,1X,F6.3)

* Format statement for reading in asteroid population

102   format(F5.2,1X,F4.2,1X,F4.1,1X,F13.2,1X,F13.2,1X,F13.2,
     &       1X,F13.2,1X,F13.2,1X,F13.2,1X,F13.2,1X,F13.2,1X,F13.2,
     &       1X,F13.2,1X,F13.2,1X,F13.2,1X,F13.2,1X,F13.2,1X,F13.2,
     &       1X,F13.2,1X,F13.2,1X,F13.2,1X,F13.2,1X,F13.2,1X,F13.2,
     &       1X,F13.2,1X,F13.2,1X,F13.2,1X,F13.2)

* Format statement for reading and writing MPC format astrometry

120   FORMAT (A12,3X,I4,1X,I2,1X,F8.5,1X,I2,1X,I2,1X,F5.2,1X,
     &        A1,I2,1X,I2,1X,F4.1,10X,F4.1,1X,A1,6X,I3)

* Format statement for writing output

122   format(i4,3x,a12,3x,F5.1,3x,a3,3x,F6.1,1X,F5.1,1X,F7.3,1X,F7.3,
     &       1X,F7.3,2X,F4.1)

* Format statement for writing column header for output

123   format('   #        Design    Score   NEO?   Elong  Elat  ElongR
     & ElatR  TotalR   Mag')

* Ask user for file containing asteroid photometry

      PRINT *, 'INPUTFILE (J2000 OBSERVATIONS)'
      READ '(A)', INPUTFILE
      open(34,file=inputfile,status='old')

      G=0.15
      NUMOBS=2
      COMPUTER='M'
      K=0.01720209895
      RD=57.2957795131
      MONTHNAME(1)='Jan'
      MONTHNAME(2)='Feb'
      MONTHNAME(3)='Mar'
      MONTHNAME(4)='Apr'
      MONTHNAME(5)='May'
      MONTHNAME(6)='Jun'
      MONTHNAME(7)='Jul'
      MONTHNAME(8)='Aug'
      MONTHNAME(9)='Sep'
      MONTHNAME(10)='Oct'
      MONTHNAME(11)='Nov'
      MONTHNAME(12)='Dec'
      pi  = 3.14159265358979323846
      drad = pi/180.0D0

* Set counters to zero

      i5 = 0
      mb_count = 0.0D0
      neo_count = 0.0D0
      desig9 = '           '

* Write column header to output

      write(*,123) 

* Read asteroid population into array

      do i3 = 1 , 9001

         read(32,102) semi1(i3),ecc1(i3),ncl1(i3),h6(i3),
     &                 h7(i3),h8(i3),h9(i3),h10(i3),h11(i3),
     &                 h12(i3),h13(i3),h14(i3),h15(i3),
     &                 h16(i3),h17(i3),h18(i3),h19(i3),
     &                 h20(i3),h21(i3),h22(i3),h23(i3),
     &                 h24(i3),h25(i3),h26(i3),h27(i3),
     &                 h28(i3),h29(i3),h30(i3)

      end do

* Calls Observatory subroutine which extracts observatory topocentric params

      CALL OBSERVATORY(OBS,OBSNAME)

* Start 'do loop' that will read in astrometry, produce orbital solutions,
* determine probabilities and write the output to the command line

      do i4 = 1, 777000

      desig8 = desig9
      year8 = year9
      month8 = month9
      day8 = day9
      rahr8 = rahr9
      ramin8 = ramin9
      rasec8 = rasec9
      sign8 = sign9
      deg8 = deg9
      decmin8 = decmin9
      decsec8 = decsec9
      magn8 = magn9 
      magtype8 = magtype9
      obscode8 = obscode9

* Read in astrometric positions, one line at a time

      read(34,120,end=888) desig9,
     &             year9,month9,day9,rahr9,ramin9,rasec9,
     &             sign9,deg9,decmin9,decsec9,magn9,
     &             magtype9,obscode9

      if (desig9 .NE. desig8 .AND. desig8 .EQ. '           ') then

           write(33,120) desig9,
     &                   year9,month9,day9,rahr9,ramin9,rasec9,
     &                   sign9,deg9,decmin9,decsec9,magn9,
     &                   magtype9,obscode9   

           dddd1 = day9

           call astromrates(year9,month9,day9,rahr9,ramin9,rasec9,
     &                      sign9,deg9,decmin9,decsec9,aaa1,bbb1,lc1)

      end if

      if (desig9 .NE. desig8 .AND. desig8 .NE. '           ') then

           write(33,120) desig8,
     &                   year8,month8,day8,rahr8,ramin8,rasec8,
     &                   sign8,deg8,decmin8,decsec8,magn8,
     &                   magtype8,obscode8

           dddd2 = day8

           call astromrates(year8,month8,day8,rahr8,ramin8,rasec8,
     &                      sign8,deg8,decmin8,decsec8,aaa2,bbb2,lc2)

           rewind(33)

      DO 30 II=1,2

      READ (33, '(A)') OBSN
      CALL READOBS2000 (OBSN, NUMBER,DESIG,CDUM1(1),CDUM1(2),CDUM1(3),
     $ YEAR,MONTH,DAY,RA,DE,MAGOBS(II),MAGTYPE(II),OBSCODE)

      if (ii .eq. 2 .and. magobs(1) .ge. 1 .and. magobs(2) .ge. 1) then
        magobs2 = (magobs(1) + magobs(2)) * 0.5
      else if (ii .eq. 2 .and. magobs(1) .le. 1) then
        magobs2 = magobs(2)
      else if (ii .eq. 2 .and. magobs(2) .le. 1) then
        magobs2 = magobs(1)
      else if (ii.eq.2.and.magobs(1).le.1.and.magobs(2).le.1) then
	    magobs2 = 19.0 
	  end if

      if (magtype(2) .eq. 'B' .or. magtype(2) .eq. ' ') then
        magobs2 = magobs2 - 0.8
      else if (magtype(2) .eq. 'R') then
        magobs2 = magobs2 + 0.4
      else
        magobs2 = magobs2
      end if
        
      CALL JDATE(YEAR,MONTH,DAY,T(II))
      CALL FINDET(YEAR,ET)
      T(II)=T(II)+ET

      IF (OBSCODE.LT.0.OR.OBSCODE.GT.999) OBSCODE=500
      LONG=OBS(OBSCODE,1)/360
      DXY =OBS(OBSCODE,2)
      DZ  =OBS(OBSCODE,3)
*     WRITE (*,*) OBSNAME(OBSCODE)

      CALL SE2000 (T(II), RSUN(II),XS,YS,ZS)
      
      CALL LST(T(II)-ET,LONG,TH)
      EE(II,1)=-(XS+DXY*COS(TH)*1E-7)
      EE(II,2)=-(YS+DXY*SIN(TH)*1E-7)
      EE(II,3)=-(ZS+DZ*1E-7)

      DD(II,1)=COS(RA)*COS(DE)
      DD(II,2)=SIN(RA)*COS(DE)
      DD(II,3)=SIN(DE)

30    CONTINUE

      OPEN(UNIT=9,FILE='PANGLO.MPC')
      OPEN(UNIT=10,FILE='PANGLO.EMP')

C     CALCULATE POSITION AND VELOCITY VECTOR OF OBJECT
      DT=T(2)-T(1)
      ARC=INT(DT)

      D1 = 0.025D0

      do l = 1 , 280 


31    FLAG=D1.LT.0
      D1=ABS(D1)
      IF (D1.EQ.0) GOTO 999

      DP=0
      O(1)=EE(1,1)+D1*DD(1,1)
      DD(0,1)=O(1)-EE(2,1)
      O(2)=EE(1,2)+D1*DD(1,2)
      DD(0,2)=O(2)-EE(2,2)
      O(3)=EE(1,3)+D1*DD(1,3)
      DD(0,3)=O(3)-EE(2,3)

      DP=SQRT(DD(0,1)**2+DD(0,2)**2+DD(0,3)**2)
      R=SQRT(O(1)**2+O(2)**2+O(3)**2)

      CALL MAG (RSUN(1),R,D1,0D0,G, ELONG,PSI,M1)
      HMAG=MAGOBS(1)-M1
      IF (MAGTYPE(1).EQ.'B') HMAG=HMAG-0.8
      if (magtype(1).eq.'R') hmag=hmag+0.4

      TH=(DD(0,1)*DD(2,1)+DD(0,2)*DD(2,2)+DD(0,3)*DD(2,3))/DP
      TZ=ATAN(SQRT(1-TH**2)/TH)

      U=2.95912208E-4
      AA=1/(DT**2)
      BB=(-2*DP*TH)/(DT**2)
      CC=DP**2/DT**2-2*U/R

C     For 1st parabloic solution
      D2=(-BB-SQRT(BB*BB-4*AA*CC))/(2*AA)
      N=SQRT(D2*D2+DP*DP-2*D2*DP*COS(TZ))
      CA=(N*N+DP*DP-D2*D2)/(2*N*DP)
      SA=D2*SIN(TZ)/N
      ANG(1)=2*ATAN(SA/(1+CA))*RD

C     For 2nd parabloic solution
      D2=(-BB+SQRT(BB*BB-4*AA*CC))/(2*AA)
      N=SQRT(D2*D2+DP*DP-2*D2*DP*COS(TZ))
      CA=(N*N+DP*DP-D2*D2)/(2*N*DP)
      SA=D2*SIN(TZ)/N
      ANG(2)=2*ATAN(SA/(1+CA))*RD

      PARAB=1

      DO 50 AL= 0 ,170, 2

      IF (FLAG .AND. AL.GT.15) GOTO 50
      IF (FLAG) GOTO 45

      IF (PARAB.EQ.4) GOTO 50
      AN=AL

      IF (PARAB.EQ.1.AND.ANG(1).LT.AL) THEN
          PARAB=2
          AN=ANG(1)
      END IF

48    IF (PARAB.EQ.3.AND.ANG(2).LT.AL) THEN
          PARAB=4
          AN=ANG(2)
      END IF

45    CONTINUE

      D2=DP*SIN(AN/RD)/SIN((180-AN)/RD-TZ)

      V(1)=(D2*DD(2,1)-DD(0,1))/DT
      V(2)=(D2*DD(2,2)-DD(0,2))/DT
      V(3)=(D2*DD(2,3)-DD(0,3))/DT

*  (The following is all easily visualised by drawing a rough sketch)
*  If i=1,2 is the obsn & j=1,2,3 the coord (ref frame equatorial J2000)
*  then T(i) is JDE
*  EE(i,j) is vector Sun -> observer
*  DD(i,j) is unit vector observer -> object (apparent; will subtract
*   light travel time from perihelion passage time)
*  O(j) is Sun -> object at T(1)
*  DD(0,j) is observer at T(2) -> object at T(1)
*  TZ is angle between object at T1 & T2 as viewed by observer at T2
*  TH is cos(TZ), calculated using scalar product
*  D2 is object-observer dist at T2, calculated using sine rule
*  V(j) is velocity, assuming obsns are close enough in time that the
*   object's motion can be approximated as uniform
*  Now use METEORORBIT to calc orb els from position & velocity

      CALL METEORORBIT(T(1),O,V,T0,Q,E,W,N,I)

      IF (W.EQ.0.0.AND.N.EQ.0.0.AND.I.EQ.0.0) GOTO 50

      W=W*RD
      N=N*RD
      I=I*RD

      T0=T0-0.005775518*D1
      CALL CIVILDATE(T0,YEAR,MONTH,DAY)

      A=0.0
      IF (E.NE.1.0) A=Q/(1-E)
      IF (A.GE.100.0) A=0.0






********************************************************************
* Getting bias numbers from asteroid pops
********************************************************************

*     WRITE(31,59) D1,HMAG,AN,A,E,I,W,N,Q

      if (i .GE. 90.0D0) then

          i = 89.0D0

      end if

      if (A .GE. 6.0D0) then

          a = 6.0D0

      end if

           semiadd = 0.25D0
           eccadd  = 0.20D0
           ncladd  = 5.00D0

           nz = aint(i/ncladd) 
           ez = aint(e/eccadd) 
           az = aint(a/semiadd) 

           i3 = (az * 90) + (ez * 18) + (nz) + 1

      if (Q .GE. 1.30D0 .AND. I .LE. 50.0D0 .AND. E .LT.
     &    0.40D0) then

          if (hmag .LT. 6.5D0) then

             mb_count = mb_count + h6(i3)

          else if (hmag .GE. 6.5D0 .AND. hmag .LT. 7.5D0) then

             mb_count = mb_count + h7(i3)

          else if (hmag .GE. 7.5D0 .AND. hmag .LT. 8.5D0) then
  
             mb_count = mb_count + h8(i3)

          else if (hmag .GE. 8.5D0 .AND. hmag .LT. 9.5D0) then

             mb_count = mb_count + h9(i3)

          else if (hmag .GE. 9.5D0 .AND. hmag .LT. 10.5D0) then

             mb_count = mb_count + h10(i3)

          else if (hmag .GE. 10.5D0 .AND. hmag .LT. 11.5D0) then

             mb_count = mb_count + h11(i3)

          else if (hmag .GE. 11.5D0 .AND. hmag .LT. 12.5D0) then

             mb_count = mb_count + h12(i3)

          else if (hmag .GE. 12.5D0 .AND. hmag .LT. 13.5D0) then

             mb_count = mb_count + h13(i3)

          else if (hmag .GE. 13.5D0 .AND. hmag .LT. 14.5D0) then

             mb_count = mb_count + h14(i3)

          else if (hmag .GE. 14.5D0 .AND. hmag .LT. 15.5D0) then

             mb_count = mb_count + h15(i3)

          else if (hmag .GE. 15.5D0 .AND. hmag .LT. 16.5D0) then

             mb_count = mb_count + h16(i3)

          else if (hmag .GE. 16.5D0 .AND. hmag .LT. 17.5D0) then

             mb_count = mb_count + h17(i3)

          else if (hmag .GE. 17.5D0 .AND. hmag .LT. 18.5D0) then

             mb_count = mb_count + h18(i3)

          else if (hmag .GE. 18.5D0 .AND. hmag .LT. 19.5D0) then

             mb_count = mb_count + h19(i3)

          else if (hmag .GE. 19.5D0 .AND. hmag .LT. 20.5D0) then

             mb_count = mb_count + h20(i3)

          else if (hmag .GE. 20.5D0 .AND. hmag .LT. 21.5D0) then

             mb_count = mb_count + h21(i3)

          else if (hmag .GE. 21.5D0 .AND. hmag .LT. 22.5D0) then

             mb_count = mb_count + h22(i3)

          else if (hmag .GE. 22.5D0 .AND. hmag .LT. 23.5D0) then

             mb_count = mb_count + h23(i3)

          else if (hmag .GE. 23.5D0 .AND. hmag .LT. 24.5D0) then

             mb_count = mb_count + h24(i3)

          else if (hmag .GE. 24.5D0 .AND. hmag .LT. 25.5D0) then

             mb_count = mb_count + h25(i3)

          else if (hmag .GE. 25.5D0 .AND. hmag .LT. 26.5D0) then

             mb_count = mb_count + h26(i3)

          else if (hmag .GE. 26.5D0 .AND. hmag .LT. 27.5D0) then

             mb_count = mb_count + h27(i3)

          else if (hmag .GE. 27.5D0 .AND. hmag .LT. 28.5D0) then

             mb_count = mb_count + h28(i3)

          else if (hmag .GE. 28.5D0 .AND. hmag .LT. 29.5D0) then

             mb_count = mb_count + h29(i3)

          else

             mb_count = mb_count + h30(i3)

          end if

      else

          if (hmag .LT. 6.5D0) then

             neo_count = neo_count + h6(i3)

          else if (hmag .GE. 6.5D0 .AND. hmag .LT. 7.5D0) then

             neo_count = neo_count + h7(i3)

          else if (hmag .GE. 7.5D0 .AND. hmag .LT. 8.5D0) then

             neo_count = neo_count + h8(i3)

          else if (hmag .GE. 8.5D0 .AND. hmag .LT. 9.5D0) then

             neo_count = neo_count + h9(i3)

          else if (hmag .GE. 9.5D0 .AND. hmag .LT. 10.5D0) then

             neo_count = neo_count + h10(i3)

          else if (hmag .GE. 10.5D0 .AND. hmag .LT. 11.5D0) then

             neo_count = neo_count + h11(i3)

          else if (hmag .GE. 11.5D0 .AND. hmag .LT. 12.5D0) then

             neo_count = neo_count + h12(i3)

          else if (hmag .GE. 12.5D0 .AND. hmag .LT. 13.5D0) then

             neo_count = neo_count + h13(i3)

          else if (hmag .GE. 13.5D0 .AND. hmag .LT. 14.5D0) then

             neo_count = neo_count + h14(i3)

          else if (hmag .GE. 14.5D0 .AND. hmag .LT. 15.5D0) then

             neo_count = neo_count + h15(i3)
 
          else if (hmag .GE. 15.5D0 .AND. hmag .LT. 16.5D0) then
 
             neo_count = neo_count + h16(i3)
 
          else if (hmag .GE. 16.5D0 .AND. hmag .LT. 17.5D0) then
 
             neo_count = neo_count + h17(i3)

          else if (hmag .GE. 17.5D0 .AND. hmag .LT. 18.5D0) then
 
             neo_count = neo_count + h18(i3)
 
          else if (hmag .GE. 18.5D0 .AND. hmag .LT. 19.5D0) then
 
             neo_count = neo_count + h19(i3)
 
          else if (hmag .GE. 19.5D0 .AND. hmag .LT. 20.5D0) then
 
             neo_count = neo_count + h20(i3)

          else if (hmag .GE. 20.5D0 .AND. hmag .LT. 21.5D0) then

             neo_count = neo_count + h21(i3)

          else if (hmag .GE. 21.5D0 .AND. hmag .LT. 22.5D0) then

             neo_count = neo_count + h22(i3)

          else if (hmag .GE. 22.5D0 .AND. hmag .LT. 23.5D0) then

             neo_count = neo_count + h23(i3)

          else if (hmag .GE. 23.5D0 .AND. hmag .LT. 24.5D0) then

             neo_count = neo_count + h24(i3)

          else if (hmag .GE. 24.5D0 .AND. hmag .LT. 25.5D0) then

             neo_count = neo_count + h25(i3)

          else if (hmag .GE. 25.5D0 .AND. hmag .LT. 26.5D0) then

             neo_count = neo_count + h26(i3)

          else if (hmag .GE. 26.5D0 .AND. hmag .LT. 27.5D0) then

             neo_count = neo_count + h27(i3)

          else if (hmag .GE. 27.5D0 .AND. hmag .LT. 28.5D0) then

             neo_count = neo_count + h28(i3)

          else if (hmag .GE. 28.5D0 .AND. hmag .LT. 29.5D0) then

             neo_count = neo_count + h29(i3)

          else
 
             neo_count = neo_count + h30(i3)

          end if

*          score2 = (neo_count / (neo_count + mb_count))*100.0D0
*          write(31,*) neo_count, mb_count, score2

      end if

 
********************************************************************
********************************************************************

50    CONTINUE

      D1 = D1 + 0.025D0

      end do

         if (neo_count .LE. 0.95D0) then

           neo_count = 1.0D0

         end if

           score = (neo_count / (neo_count + mb_count))*100.0D0
           i5 = i5 + 1
           if (score .GE. 25) then

               neoflag = 'NEO'

           else 

               neoflag = '   '

           end if

      lcd = (lc2 - lc1)/(dddd2 - dddd1)
  
      if (lcd .GE. 180) then
        
        lcd = lcd - 360.0D0

      else if (lcd .LE. -180) then

        lcd = lcd + 360.0D0

      else

        lcd = lcd

      end if

      bcd = (bbb2 - bbb1)/(dddd2 - dddd1)

      lcd = lcd * cos(bbb1*drad)

      rate = (bcd**2 + lcd**2)**0.5

      if ((aaa1 .GE. 150 .OR. aaa1 .LE. -150) .AND. (lcd .LE. 
     &     -0.01D0 .AND. lcd .GE. -0.08D0) .AND. (bcd .LE. 0.02D0
     &     .AND. bcd .GE. -0.02D0)) then

         neoflag = 'OSS'

      end if

	  if (score .GE. 00.0D0) then

         write(*,122) i5,desig8,score,neoflag,aaa1,bbb1,
     &                lcd,bcd,rate,magobs2

	  end if

         mb_count = 0.0D0
         neo_count = 0.0D0

           rewind(33)
           write(33,120) desig9,
     &                   year9,month9,day9,rahr9,ramin9,rasec9,
     &                   sign9,deg9,decmin9,decsec9,magn9,
     &                   magtype9,obscode9

           dddd1 = day9
           call astromrates(year9,month9,day9,rahr9,ramin9,rasec9,
     &                      sign9,deg9,decmin9,decsec9,aaa1,bbb1,lc1)

      end if

      end do

888   close(33)

999   CLOSE(UNIT=9)

      END

      SUBROUTINE METEORORBIT(T1,O,VD,T0,Q,E,W,OM,I)

C     T1=TIME AT POSITION O=(X,Y,Z) WITH VELOCITY VD=(XD,YD,ZD)
C        WITH (1950) EQUATORIAL COORDINATES
C     T0=TIME OR PERIHELION IN JD, 'A' IS IN AU
C     W,OM,I ARE IN RADIANS, EQUINOX 1950

*  Changed the value of EPS in the hope that this makes it work in J2000
*  instead of B1950   - DJA, 950320

      IMPLICIT NONE
      REAL*8 T1,X,Y,Z,XD,YD,ZD,T0,A,E,W,OM,I,H,HH,HX,HY,HZ,R
      REAL*8 U,P,C,V,CI,CWF,SWF,WF,CF,CT,F,EC,GAP,PI,N,PI2
      REAL*8 O(3),VD(3),EPS,RR,TH,VEL,RD,S,WW,Q

      T0=0
      A=0
      E=0
      W=0
      OM=0
      I=0

      PI=3.14159265
      PI2=PI*2
      RD=57.2957795131
      EPS=23.4393/RD
*   (Changed from
*      EPS=23.4457889/RD
*   - DJA)
C     EQUINOX OF 1950
      U=2.95912208E-4
C     U=(.985607669/RD)**2   VALUE OF CONSTANT FROM AE 1984

      X=O(1)
      Y=O(2)
      Z=O(3)

      RR=SQRT(Y*Y+Z*Z)
      TH=2*ATAN(Z/(RR+Y))
      Y=COS(TH-EPS)*RR
      Z=SIN(TH-EPS)*RR

      XD=VD(1)
      YD=VD(2)
      ZD=VD(3)

      VEL=SQRT(XD*XD+YD*YD+ZD*ZD)
      RR=SQRT(YD*YD+ZD*ZD)
      TH=2*ATAN(ZD/(RR+YD))
      YD=COS(TH-EPS)*RR
      ZD=SIN(TH-EPS)*RR

C     WRITE(*,*) 'HELIOCENTRIC VEL=',VEL/5.7754833E-4,'KM/SEC'

      R=SQRT(X*X+Y*Y+Z*Z)
      V=SQRT(XD*XD+YD*YD+ZD*ZD)

      HX=Y*ZD-Z*YD
      HY=Z*XD-X*ZD
      HZ=X*YD-Y*XD

      HH=HX*HX+HY*HY+HZ*HZ
      H=SQRT(HH)

      P=HH/U
      C=V*V/2-U/R

      IF (ABS(C).LT.1.0E-12) THEN
C       FOR A PARABOLIC ORBIT
        E=1.0
        GOTO 58
      END IF

C     IF (C.GT.0.0) WRITE(*,*) 'HYPERBOLIC ORBIT, C=',C
      IF (C.GT.0.0) GOTO 60

C     CALCULATION FOR ELLIPSE
      A=1/(2/R-V*V/U)
      E=SQRT(1-P/A)
      Q=A*(1-E)

58    CI=HZ/H
      I=ATAN(SQRT(1-CI*CI)/CI)
      IF (I.LT.0.0) I=PI+I

      OM=2*ATAN(HX/(H*SIN(I)-HY))
      IF (OM.LT.0.0) OM=PI2+OM

      CWF=(X*COS(OM)+Y*SIN(OM))/R
      IF (I.EQ.0.0) SWF=(Y*COS(OM)-X*SIN(OM))/R
      IF (I.NE.0.0) SWF=Z/(R*SIN(I))
      IF (ABS(CWF).GT.0.99999) CWF=ABS(CWF)/CWF*SQRT(1-SWF*SWF)

C     CHECK NEXT LINE

      IF (CWF.LT.-0.9999999) WF=-PI*ABS(CWF)/CWF

      WF=2*ATAN(SWF/(1+CWF))
      CF=(P/R-1)/E
      CT=(-X*XD-Y*YD-Z*ZD)/(R*V)

      F=2*ATAN(SQRT(1-CF*CF)/(1+CF))
      IF (CT.GT.0.0) F=2*PI-F
      W=WF-F
      W=(W/(PI2)-INT(W/PI2))*PI2
      IF (W.LT.0.0) W=PI2+W

      IF (ABS(C).LT.1E-12) THEN
C     DEL TIME TO PERIHELION FOR A PARABOLA
         S=TAN(F/2)
         WW=S**3+3*S
         Q=P/2
         GAP=WW*Q**(1.5)/0.0364911624
         GOTO 59
      END IF


      N=SQRT(U)*A**(-1.5)
      EC=2*ATAN(SQRT((1-E)/(1+E))*TAN(F/2))
      GAP=(EC-E*SIN(EC))/N

59    T0=T1-GAP

60    END

      SUBROUTINE sla_EVP (DATE, DEQX, DVB, DPB, DVH, DPH)
*+
*     - - - -
*      E V P
*     - - - -
*
*  Barycentric and heliocentric velocity and position of the Earth
*
*  All arguments are double precision
*
*  Given:
*
*     DATE          TDB (loosely ET) as a Modified Julian Date
*                                         (JD-2400000.5)
*
*     DEQX          Julian Epoch (e.g. 2000.0D0) of mean equator and
*                   equinox of the vectors returned.  If DEQX .LE. 0D0,
*                   all vectors are referred to the mean equator and
*                   equinox (FK5) of epoch DATE.
*
*  Returned (all 3D Cartesian vectors):
*
*     DVB,DPB       barycentric velocity, position
*
*     DVH,DPH       heliocentric velocity, position
*
*  (Units are AU/s for velocity and AU for position)
*
*  Called:  sla_EPJ, sla_PREC
*
*  Accuracy:
*
*     The maximum deviations from the JPL DE96 ephemeris are as
*     follows:
*
*     barycentric velocity         0.42  m/s
*     barycentric position         6900  km
*
*     heliocentric velocity        0.42  m/s
*     heliocentric position        1600  km
*
*  This routine is adapted from the BARVEL and BARCOR
*  subroutines of P.Stumpff, which are described in
*  Astron. Astrophys. Suppl. Ser. 41, 1-8 (1980).  Most of the
*  changes are merely cosmetic and do not affect the results at
*  all.  However, some adjustments have been made so as to give
*  results that refer to the new (IAU 1976 'FK5') equinox
*  and precession, although the differences these changes make
*  relative to the results from Stumpff's original 'FK4' version
*  are smaller than the inherent accuracy of the algorithm.  One
*  minor shortcoming in the original routines that has NOT been
*  corrected is that better numerical accuracy could be achieved
*  if the various polynomial evaluations were nested.  Note also
*  that one of Stumpff's precession constants differs by 0.001 arcsec
*  from the value given in the Explanatory Supplement to the A.E.
*
*  P.T.Wallace   Starlink   21 March 1999
*
*  Copyright (C) 1999 Rutherford Appleton Laboratory
*-

      IMPLICIT NONE

      DOUBLE PRECISION DATE,DEQX,DVB(3),DPB(3),DVH(3),DPH(3)

      INTEGER IDEQ,I,J,K

      REAL CC2PI,CCSEC3,CCSGD,CCKM,CCMLD,CCFDI,CCIM,T,TSQ,A,PERTL,
     :     PERTLD,PERTR,PERTRD,COSA,SINA,ESQ,E,PARAM,TWOE,TWOG,G,
     :     PHI,F,SINF,COSF,PHID,PSID,PERTP,PERTPD,TL,SINLM,COSLM,
     :     SIGMA,B,PLON,POMG,PECC,FLATM,FLAT

      DOUBLE PRECISION DC2PI,DS2R,DCSLD,DC1MME,DT,DTSQ,DLOCAL,DML,
     :                 DEPS,DPARAM,DPSI,D1PDRO,DRD,DRLD,DTL,DSINLS,
     :                 DCOSLS,DXHD,DYHD,DZHD,DXBD,DYBD,DZBD,DCOSEP,
     :                 DSINEP,DYAHD,DZAHD,DYABD,DZABD,DR,
     :                 DXH,DYH,DZH,DXB,DYB,DZB,DYAH,DZAH,DYAB,
     :                 DZAB,DEPJ,DEQCOR,B1950

      REAL SN(4),CCSEL(3,17),CCAMPS(5,15),CCSEC(3,4),CCAMPM(4,3),
     :     CCPAMV(4),CCPAM(4),FORBEL(7),SORBEL(17),SINLP(4),COSLP(4)
      EQUIVALENCE (SORBEL(1),E),(FORBEL(1),G)

      DOUBLE PRECISION DCFEL(3,8),DCEPS(3),DCARGS(2,15),DCARGM(2,3),
     :                 DPREMA(3,3),W,VW(3)

      DOUBLE PRECISION sla_EPJ

      PARAMETER (DC2PI=6.2831853071796D0,CC2PI=6.283185)
      PARAMETER (DS2R=0.7272205216643D-4)
      PARAMETER (B1950=1949.9997904423D0)

*
*   Constants DCFEL(I,K) of fast changing elements
*                     I=1                I=2              I=3
      DATA DCFEL/ 1.7400353D+00, 6.2833195099091D+02, 5.2796D-06,
     :            6.2565836D+00, 6.2830194572674D+02,-2.6180D-06,
     :            4.7199666D+00, 8.3997091449254D+03,-1.9780D-05,
     :            1.9636505D-01, 8.4334662911720D+03,-5.6044D-05,
     :            4.1547339D+00, 5.2993466764997D+01, 5.8845D-06,
     :            4.6524223D+00, 2.1354275911213D+01, 5.6797D-06,
     :            4.2620486D+00, 7.5025342197656D+00, 5.5317D-06,
     :            1.4740694D+00, 3.8377331909193D+00, 5.6093D-06/

*
*   Constants DCEPS and CCSEL(I,K) of slowly changing elements
*                      I=1           I=2           I=3
      DATA DCEPS/  4.093198D-01,-2.271110D-04,-2.860401D-08 /
      DATA CCSEL/  1.675104E-02,-4.179579E-05,-1.260516E-07,
     :             2.220221E-01, 2.809917E-02, 1.852532E-05,
     :             1.589963E+00, 3.418075E-02, 1.430200E-05,
     :             2.994089E+00, 2.590824E-02, 4.155840E-06,
     :             8.155457E-01, 2.486352E-02, 6.836840E-06,
     :             1.735614E+00, 1.763719E-02, 6.370440E-06,
     :             1.968564E+00, 1.524020E-02,-2.517152E-06,
     :             1.282417E+00, 8.703393E-03, 2.289292E-05,
     :             2.280820E+00, 1.918010E-02, 4.484520E-06,
     :             4.833473E-02, 1.641773E-04,-4.654200E-07,
     :             5.589232E-02,-3.455092E-04,-7.388560E-07,
     :             4.634443E-02,-2.658234E-05, 7.757000E-08,
     :             8.997041E-03, 6.329728E-06,-1.939256E-09,
     :             2.284178E-02,-9.941590E-05, 6.787400E-08,
     :             4.350267E-02,-6.839749E-05,-2.714956E-07,
     :             1.348204E-02, 1.091504E-05, 6.903760E-07,
     :             3.106570E-02,-1.665665E-04,-1.590188E-07/

*
*   Constants of the arguments of the short-period perturbations
*   by the planets:   DCARGS(I,K)
*                       I=1               I=2
      DATA DCARGS/ 5.0974222D+00,-7.8604195454652D+02,
     :             3.9584962D+00,-5.7533848094674D+02,
     :             1.6338070D+00,-1.1506769618935D+03,
     :             2.5487111D+00,-3.9302097727326D+02,
     :             4.9255514D+00,-5.8849265665348D+02,
     :             1.3363463D+00,-5.5076098609303D+02,
     :             1.6072053D+00,-5.2237501616674D+02,
     :             1.3629480D+00,-1.1790629318198D+03,
     :             5.5657014D+00,-1.0977134971135D+03,
     :             5.0708205D+00,-1.5774000881978D+02,
     :             3.9318944D+00, 5.2963464780000D+01,
     :             4.8989497D+00, 3.9809289073258D+01,
     :             1.3097446D+00, 7.7540959633708D+01,
     :             3.5147141D+00, 7.9618578146517D+01,
     :             3.5413158D+00,-5.4868336758022D+02/

*
*   Amplitudes CCAMPS(N,K) of the short-period perturbations
*           N=1          N=2          N=3          N=4          N=5
      DATA CCAMPS/
     : -2.279594E-5, 1.407414E-5, 8.273188E-6, 1.340565E-5,-2.490817E-7,
     : -3.494537E-5, 2.860401E-7, 1.289448E-7, 1.627237E-5,-1.823138E-7,
     :  6.593466E-7, 1.322572E-5, 9.258695E-6,-4.674248E-7,-3.646275E-7,
     :  1.140767E-5,-2.049792E-5,-4.747930E-6,-2.638763E-6,-1.245408E-7,
     :  9.516893E-6,-2.748894E-6,-1.319381E-6,-4.549908E-6,-1.864821E-7,
     :  7.310990E-6,-1.924710E-6,-8.772849E-7,-3.334143E-6,-1.745256E-7,
     : -2.603449E-6, 7.359472E-6, 3.168357E-6, 1.119056E-6,-1.655307E-7,
     : -3.228859E-6, 1.308997E-7, 1.013137E-7, 2.403899E-6,-3.736225E-7,
     :  3.442177E-7, 2.671323E-6, 1.832858E-6,-2.394688E-7,-3.478444E-7,
     :  8.702406E-6,-8.421214E-6,-1.372341E-6,-1.455234E-6,-4.998479E-8,
     : -1.488378E-6,-1.251789E-5, 5.226868E-7,-2.049301E-7, 0.0E0,
     : -8.043059E-6,-2.991300E-6, 1.473654E-7,-3.154542E-7, 0.0E0,
     :  3.699128E-6,-3.316126E-6, 2.901257E-7, 3.407826E-7, 0.0E0,
     :  2.550120E-6,-1.241123E-6, 9.901116E-8, 2.210482E-7, 0.0E0,
     : -6.351059E-7, 2.341650E-6, 1.061492E-6, 2.878231E-7, 0.0E0/

*
*   Constants of the secular perturbations in longitude
*   CCSEC3 and CCSEC(N,K)
*                      N=1           N=2           N=3
      DATA CCSEC3/-7.757020E-08/,
     :     CCSEC/  1.289600E-06, 5.550147E-01, 2.076942E+00,
     :             3.102810E-05, 4.035027E+00, 3.525565E-01,
     :             9.124190E-06, 9.990265E-01, 2.622706E+00,
     :             9.793240E-07, 5.508259E+00, 1.559103E+01/

*   Sidereal rate DCSLD in longitude, rate CCSGD in mean anomaly
      DATA DCSLD/1.990987D-07/,
     :     CCSGD/1.990969E-07/

*   Some constants used in the calculation of the lunar contribution
      DATA CCKM/3.122140E-05/,
     :     CCMLD/2.661699E-06/,
     :     CCFDI/2.399485E-07/

*
*   Constants DCARGM(I,K) of the arguments of the perturbations
*   of the motion of the Moon
*                       I=1               I=2
      DATA DCARGM/  5.1679830D+00, 8.3286911095275D+03,
     :              5.4913150D+00,-7.2140632838100D+03,
     :              5.9598530D+00, 1.5542754389685D+04/

*
*   Amplitudes CCAMPM(N,K) of the perturbations of the Moon
*            N=1          N=2           N=3           N=4
      DATA CCAMPM/
     :  1.097594E-01, 2.896773E-07, 5.450474E-02, 1.438491E-07,
     : -2.223581E-02, 5.083103E-08, 1.002548E-02,-2.291823E-08,
     :  1.148966E-02, 5.658888E-08, 8.249439E-03, 4.063015E-08/

*
*   CCPAMV(K)=A*M*DL/DT (planets), DC1MME=1-MASS(Earth+Moon)
      DATA CCPAMV/8.326827E-11,1.843484E-11,1.988712E-12,1.881276E-12/
      DATA DC1MME/0.99999696D0/

*   CCPAM(K)=A*M(planets), CCIM=INCLINATION(Moon)
      DATA CCPAM/4.960906E-3,2.727436E-3,8.392311E-4,1.556861E-3/
      DATA CCIM/8.978749E-2/




*
*   EXECUTION
*   ---------

*   Control parameter IDEQ, and time arguments
      IDEQ = 0
      IF (DEQX.GT.0D0) IDEQ=1
      DT = (DATE-15019.5D0)/36525D0
      T = REAL(DT)
      DTSQ = DT*DT
      TSQ = REAL(DTSQ)

*   Values of all elements for the instant DATE
      DO K=1,8
         DLOCAL = MOD(DCFEL(1,K)+DT*DCFEL(2,K)+DTSQ*DCFEL(3,K), DC2PI)
         IF (K.EQ.1) THEN
            DML = DLOCAL
         ELSE
            FORBEL(K-1) = REAL(DLOCAL)
         END IF
      END DO
      DEPS = MOD(DCEPS(1)+DT*DCEPS(2)+DTSQ*DCEPS(3), DC2PI)
      DO K=1,17
         SORBEL(K) = MOD(CCSEL(1,K)+T*CCSEL(2,K)+TSQ*CCSEL(3,K),
     :                   CC2PI)
      END DO

*   Secular perturbations in longitude
      DO K=1,4
         A = MOD(CCSEC(2,K)+T*CCSEC(3,K), CC2PI)
         SN(K) = SIN(A)
      END DO

*   Periodic perturbations of the EMB (Earth-Moon barycentre)
      PERTL =  CCSEC(1,1)          *SN(1) +CCSEC(1,2)*SN(2)+
     :        (CCSEC(1,3)+T*CCSEC3)*SN(3) +CCSEC(1,4)*SN(4)
      PERTLD = 0.0
      PERTR = 0.0
      PERTRD = 0.0
      DO K=1,15
         A = SNGL(MOD(DCARGS(1,K)+DT*DCARGS(2,K), DC2PI))
         COSA = COS(A)
         SINA = SIN(A)
         PERTL = PERTL + CCAMPS(1,K)*COSA+CCAMPS(2,K)*SINA
         PERTR = PERTR + CCAMPS(3,K)*COSA+CCAMPS(4,K)*SINA
         IF (K.LT.11) THEN
            PERTLD = PERTLD+
     :               (CCAMPS(2,K)*COSA-CCAMPS(1,K)*SINA)*CCAMPS(5,K)
            PERTRD = PERTRD+
     :               (CCAMPS(4,K)*COSA-CCAMPS(3,K)*SINA)*CCAMPS(5,K)
         END IF
      END DO

*   Elliptic part of the motion of the EMB
      ESQ = E*E
      DPARAM = 1D0-DBLE(ESQ)
      PARAM = REAL(DPARAM)
      TWOE = E+E
      TWOG = G+G
      PHI = TWOE*((1.0-ESQ*0.125)*SIN(G)+E*0.625*SIN(TWOG)
     :          +ESQ*0.54166667*SIN(G+TWOG) )
      F = G+PHI
      SINF = SIN(F)
      COSF = COS(F)
      DPSI = DPARAM/(1D0+DBLE(E*COSF))
      PHID = TWOE*CCSGD*((1.0+ESQ*1.5)*COSF+E*(1.25-SINF*SINF*0.5))
      PSID = CCSGD*E*SINF/SQRT(PARAM)

*   Perturbed heliocentric motion of the EMB
      D1PDRO = 1D0+DBLE(PERTR)
      DRD = D1PDRO*(DBLE(PSID)+DPSI*DBLE(PERTRD))
      DRLD = D1PDRO*DPSI*(DCSLD+DBLE(PHID)+DBLE(PERTLD))
      DTL = MOD(DML+DBLE(PHI)+DBLE(PERTL), DC2PI)
      DSINLS = SIN(DTL)
      DCOSLS = COS(DTL)
      DXHD = DRD*DCOSLS-DRLD*DSINLS
      DYHD = DRD*DSINLS+DRLD*DCOSLS

*   Influence of eccentricity, evection and variation on the
*   geocentric motion of the Moon
      PERTL = 0.0
      PERTLD = 0.0
      PERTP = 0.0
      PERTPD = 0.0
      DO K=1,3
         A = SNGL(MOD(DCARGM(1,K)+DT*DCARGM(2,K), DC2PI))
         SINA = SIN(A)
         COSA = COS(A)
         PERTL = PERTL +CCAMPM(1,K)*SINA
         PERTLD = PERTLD+CCAMPM(2,K)*COSA
         PERTP = PERTP +CCAMPM(3,K)*COSA
         PERTPD = PERTPD-CCAMPM(4,K)*SINA
      END DO

*   Heliocentric motion of the Earth
      TL = FORBEL(2)+PERTL
      SINLM = SIN(TL)
      COSLM = COS(TL)
      SIGMA = CCKM/(1.0+PERTP)
      A = SIGMA*(CCMLD+PERTLD)
      B = SIGMA*PERTPD
      DXHD = DXHD+DBLE(A*SINLM)+DBLE(B*COSLM)
      DYHD = DYHD-DBLE(A*COSLM)+DBLE(B*SINLM)
      DZHD =     -DBLE(SIGMA*CCFDI*COS(FORBEL(3)))

*   Barycentric motion of the Earth
      DXBD = DXHD*DC1MME
      DYBD = DYHD*DC1MME
      DZBD = DZHD*DC1MME
      DO K=1,4
         PLON = FORBEL(K+3)
         POMG = SORBEL(K+1)
         PECC = SORBEL(K+9)
         TL = MOD(PLON+2.0*PECC*SIN(PLON-POMG), CC2PI)
         SINLP(K) = SIN(TL)
         COSLP(K) = COS(TL)
         DXBD = DXBD+DBLE(CCPAMV(K)*(SINLP(K)+PECC*SIN(POMG)))
         DYBD = DYBD-DBLE(CCPAMV(K)*(COSLP(K)+PECC*COS(POMG)))
         DZBD = DZBD-DBLE(CCPAMV(K)*SORBEL(K+13)*COS(PLON-SORBEL(K+5)))
      END DO

*   Transition to mean equator of date
      DCOSEP = COS(DEPS)
      DSINEP = SIN(DEPS)
      DYAHD = DCOSEP*DYHD-DSINEP*DZHD
      DZAHD = DSINEP*DYHD+DCOSEP*DZHD
      DYABD = DCOSEP*DYBD-DSINEP*DZBD
      DZABD = DSINEP*DYBD+DCOSEP*DZBD

*   Heliocentric coordinates of the Earth
      DR = DPSI*D1PDRO
      FLATM = CCIM*SIN(FORBEL(3))
      A = SIGMA*COS(FLATM)
      DXH = DR*DCOSLS-DBLE(A*COSLM)
      DYH = DR*DSINLS-DBLE(A*SINLM)
      DZH =          -DBLE(SIGMA*SIN(FLATM))

*   Barycentric coordinates of the Earth
      DXB = DXH*DC1MME
      DYB = DYH*DC1MME
      DZB = DZH*DC1MME
      DO K=1,4
         FLAT = SORBEL(K+13)*SIN(FORBEL(K+3)-SORBEL(K+5))
         A = CCPAM(K)*(1.0-SORBEL(K+9)*COS(FORBEL(K+3)-SORBEL(K+1)))
         B = A*COS(FLAT)
         DXB = DXB-DBLE(B*COSLP(K))
         DYB = DYB-DBLE(B*SINLP(K))
         DZB = DZB-DBLE(A*SIN(FLAT))
      END DO

*   Transition to mean equator of date
      DYAH = DCOSEP*DYH-DSINEP*DZH
      DZAH = DSINEP*DYH+DCOSEP*DZH
      DYAB = DCOSEP*DYB-DSINEP*DZB
      DZAB = DSINEP*DYB+DCOSEP*DZB

*   Copy result components into vectors, correcting for FK4 equinox
      DEPJ=sla_EPJ(DATE)
      DEQCOR = DS2R*(0.035D0+0.00085D0*(DEPJ-B1950))
      DVH(1) = DXHD-DEQCOR*DYAHD
      DVH(2) = DYAHD+DEQCOR*DXHD
      DVH(3) = DZAHD
      DVB(1) = DXBD-DEQCOR*DYABD
      DVB(2) = DYABD+DEQCOR*DXBD
      DVB(3) = DZABD
      DPH(1) = DXH-DEQCOR*DYAH
      DPH(2) = DYAH+DEQCOR*DXH
      DPH(3) = DZAH
      DPB(1) = DXB-DEQCOR*DYAB
      DPB(2) = DYAB+DEQCOR*DXB
      DPB(3) = DZAB

*   Was precession to another equinox requested?
      IF (IDEQ.NE.0) THEN

*     Yes: compute precession matrix from MJD DATE to Julian epoch DEQX
         CALL sla_PREC(DEPJ,DEQX,DPREMA)

*     Rotate DVH
         DO J=1,3
            W=0D0
            DO I=1,3
               W=W+DPREMA(J,I)*DVH(I)
            END DO
            VW(J)=W
         END DO
         DO J=1,3
            DVH(J)=VW(J)
         END DO

*     Rotate DVB
         DO J=1,3
            W=0D0
            DO I=1,3
               W=W+DPREMA(J,I)*DVB(I)
            END DO
            VW(J)=W
         END DO
         DO J=1,3
            DVB(J)=VW(J)
         END DO

*     Rotate DPH
         DO J=1,3
            W=0D0
            DO I=1,3
               W=W+DPREMA(J,I)*DPH(I)
            END DO
            VW(J)=W
         END DO
         DO J=1,3
            DPH(J)=VW(J)
         END DO

*     Rotate DPB
         DO J=1,3
            W=0D0
            DO I=1,3
               W=W+DPREMA(J,I)*DPB(I)
            END DO
            VW(J)=W
         END DO
         DO J=1,3
            DPB(J)=VW(J)
         END DO
      END IF

      END
      DOUBLE PRECISION FUNCTION sla_EPJ (DATE)
*+
*     - - - -
*      E P J
*     - - - -
*
*  Conversion of Modified Julian Date to Julian Epoch (double precision)
*
*  Given:
*     DATE     dp       Modified Julian Date (JD - 2400000.5)
*
*  The result is the Julian Epoch.
*
*  Reference:
*     Lieske,J.H., 1979. Astron.Astrophys.,73,282.
*
*  P.T.Wallace   Starlink   February 1984
*
*  Copyright (C) 1995 Rutherford Appleton Laboratory
*-

      IMPLICIT NONE

      DOUBLE PRECISION DATE


      sla_EPJ = 2000D0 + (DATE-51544.5D0)/365.25D0

      END
      SUBROUTINE sla_PREC (EP0, EP1, RMATP)
*+
*     - - - - -
*      P R E C
*     - - - - -
*
*  Form the matrix of precession between two epochs (IAU 1976, FK5)
*  (double precision)
*
*  Given:
*     EP0    dp         beginning epoch
*     EP1    dp         ending epoch
*
*  Returned:
*     RMATP  dp(3,3)    precession matrix
*
*  Notes:
*
*     1)  The epochs are TDB (loosely ET) Julian epochs.
*
*     2)  The matrix is in the sense   V(EP1)  =  RMATP * V(EP0)
*
*     3)  Though the matrix method itself is rigorous, the precession
*         angles are expressed through canonical polynomials which are
*         valid only for a limited time span.  There are also known
*         errors in the IAU precession rate.  The absolute accuracy
*         of the present formulation is better than 0.1 arcsec from
*         1960AD to 2040AD, better than 1 arcsec from 1640AD to 2360AD,
*         and remains below 3 arcsec for the whole of the period
*         500BC to 3000AD.  The errors exceed 10 arcsec outside the
*         range 1200BC to 3900AD, exceed 100 arcsec outside 4200BC to
*         5600AD and exceed 1000 arcsec outside 6800BC to 8200AD.
*         The SLALIB routine sla_PRECL implements a more elaborate
*         model which is suitable for problems spanning several
*         thousand years.
*
*  References:
*     Lieske,J.H., 1979. Astron.Astrophys.,73,282.
*      equations (6) & (7), p283.
*     Kaplan,G.H., 1981. USNO circular no. 163, pA2.
*
*  Called:  sla_DEULER
*
*  P.T.Wallace   Starlink   23 August 1996
*
*  Copyright (C) 1996 Rutherford Appleton Laboratory
*-

      IMPLICIT NONE

      DOUBLE PRECISION EP0,EP1,RMATP(3,3)

*  Arc seconds to radians
      DOUBLE PRECISION AS2R
      PARAMETER (AS2R=0.484813681109535994D-5)

      DOUBLE PRECISION T0,T,TAS2R,W,ZETA,Z,THETA



*  Interval between basic epoch J2000.0 and beginning epoch (JC)
      T0 = (EP0-2000D0)/100D0

*  Interval over which precession required (JC)
      T = (EP1-EP0)/100D0

*  Euler angles
      TAS2R = T*AS2R
      W = 2306.2181D0+(1.39656D0-0.000139D0*T0)*T0

      ZETA = (W+((0.30188D0-0.000344D0*T0)+0.017998D0*T)*T)*TAS2R
      Z = (W+((1.09468D0+0.000066D0*T0)+0.018203D0*T)*T)*TAS2R
      THETA = ((2004.3109D0+(-0.85330D0-0.000217D0*T0)*T0)
     :        +((-0.42665D0-0.000217D0*T0)-0.041833D0*T)*T)*TAS2R

*  Rotation matrix
      CALL sla_DEULER('ZYZ',-ZETA,THETA,-Z,RMATP)

      END
      SUBROUTINE sla_DEULER (ORDER, PHI, THETA, PSI, RMAT)
*+
*     - - - - - - -
*      D E U L E R
*     - - - - - - -
*
*  Form a rotation matrix from the Euler angles - three successive
*  rotations about specified Cartesian axes (double precision)
*
*  Given:
*    ORDER   c*(*)   specifies about which axes the rotations occur
*    PHI     d       1st rotation (radians)
*    THETA   d       2nd rotation (   "   )
*    PSI     d       3rd rotation (   "   )
*
*  Returned:
*    RMAT    d(3,3)  rotation matrix
*
*  A rotation is positive when the reference frame rotates
*  anticlockwise as seen looking towards the origin from the
*  positive region of the specified axis.
*
*  The characters of ORDER define which axes the three successive
*  rotations are about.  A typical value is 'ZXZ', indicating that
*  RMAT is to become the direction cosine matrix corresponding to
*  rotations of the reference frame through PHI radians about the
*  old Z-axis, followed by THETA radians about the resulting X-axis,
*  then PSI radians about the resulting Z-axis.
*
*  The axis names can be any of the following, in any order or
*  combination:  X, Y, Z, uppercase or lowercase, 1, 2, 3.  Normal
*  axis labelling/numbering conventions apply;  the xyz (=123)
*  triad is right-handed.  Thus, the 'ZXZ' example given above
*  could be written 'zxz' or '313' (or even 'ZxZ' or '3xZ').  ORDER
*  is terminated by length or by the first unrecognized character.
*
*  Fewer than three rotations are acceptable, in which case the later
*  angle arguments are ignored.  If all rotations are zero, the
*  identity matrix is produced.
*
*  P.T.Wallace   Starlink   23 May 1997
*
*  P.T.Wallace   Starlink   23 May 1997
*
*  Copyright (C) 1997 Rutherford Appleton Laboratory
*-

      IMPLICIT NONE

      CHARACTER*(*) ORDER
      DOUBLE PRECISION PHI,THETA,PSI,RMAT(3,3)

      INTEGER J,I,L,N,K
      DOUBLE PRECISION RESULT(3,3),ROTN(3,3),ANGLE,S,C,W,WM(3,3)
      CHARACTER AXIS



*  Initialize result matrix
      DO J=1,3
         DO I=1,3
            IF (I.NE.J) THEN
               RESULT(I,J) = 0D0
            ELSE
               RESULT(I,J) = 1D0
            END IF
         END DO
      END DO

*  Establish length of axis string
      L = LEN(ORDER)

*  Look at each character of axis string until finished
      DO N=1,3
         IF (N.LE.L) THEN

*        Initialize rotation matrix for the current rotation
            DO J=1,3
               DO I=1,3
                  IF (I.NE.J) THEN
                     ROTN(I,J) = 0D0
                  ELSE
                     ROTN(I,J) = 1D0
                  END IF
               END DO
            END DO

*        Pick up the appropriate Euler angle and take sine & cosine
            IF (N.EQ.1) THEN
               ANGLE = PHI
            ELSE IF (N.EQ.2) THEN
               ANGLE = THETA
            ELSE
               ANGLE = PSI
            END IF
            S = SIN(ANGLE)
            C = COS(ANGLE)

*        Identify the axis
            AXIS = ORDER(N:N)
            IF (AXIS.EQ.'X'.OR.
     :          AXIS.EQ.'x'.OR.
     :          AXIS.EQ.'1') THEN

*           Matrix for x-rotation
               ROTN(2,2) = C
               ROTN(2,3) = S
               ROTN(3,2) = -S
               ROTN(3,3) = C

            ELSE IF (AXIS.EQ.'Y'.OR.
     :               AXIS.EQ.'y'.OR.
     :               AXIS.EQ.'2') THEN

*           Matrix for y-rotation
               ROTN(1,1) = C
               ROTN(1,3) = -S
               ROTN(3,1) = S
               ROTN(3,3) = C

            ELSE IF (AXIS.EQ.'Z'.OR.
     :               AXIS.EQ.'z'.OR.
     :               AXIS.EQ.'3') THEN

*           Matrix for z-rotation
               ROTN(1,1) = C
               ROTN(1,2) = S
               ROTN(2,1) = -S
               ROTN(2,2) = C

            ELSE

*           Unrecognized character - fake end of string
               L = 0

            END IF

*        Apply the current rotation (matrix ROTN x matrix RESULT)
            DO I=1,3
               DO J=1,3
                  W = 0D0
                  DO K=1,3
                     W = W+ROTN(I,K)*RESULT(K,J)
                  END DO
                  WM(I,J) = W
               END DO
            END DO
            DO J=1,3
               DO I=1,3
                  RESULT(I,J) = WM(I,J)
               END DO
            END DO

         END IF

      END DO

*  Copy the result
      DO J=1,3
         DO I=1,3
            RMAT(I,J) = RESULT(I,J)
         END DO
      END DO

      END



      SUBROUTINE OPFLRD (FLNM, IUNIT)
*+
*  FLNM should be the name of an existing file; then OPFLRD looks for
*  the 1st unopened unit numbered in the range 50-99, connects FLNM to
*  that unit for reading & returns the unit number.
*  Stops program execution if no unopened unit can be found.
*
*  960323:  Removed READONLY from OPEN statement (only needed on Vax)
*-
      PARAMETER (MINU=50,MAXU=99)
      CHARACTER FLNM*(*)
      LOGICAL L
      IUNIT=MINU-1
    5 IUNIT=IUNIT+1
      INQUIRE (IUNIT, OPENED=L)
      IF (L) THEN
         IF (IUNIT.LT.MAXU) GOTO 5
         STOP 'Program execution terminated in routine OPFLRD'
      ELSE
         OPEN (IUNIT, FILE=FLNM, STATUS='OLD')
      ENDIF
      END
      SUBROUTINE OBSERVATORY(OBS,OBSNAME)
C     READS THE OBSERVATORY CODES FROM OBSERVATORY.DAT

      IMPLICIT NONE
      REAL LONG,OBS(999,3)
      INTEGER OBSCODE,DDXY,DDZ,IUNIT
      CHARACTER*50 NAME,OBSNAME(999)

      CALL OPFLRD ('OBSERVATORY', IUNIT)

410   READ (IUNIT,420) OBSCODE,LONG,DDXY,DDZ,NAME
420   FORMAT(I3,3X,F6.2,2X,I4,2X,I4,6X,A50)

      IF (OBSCODE.LT.0) GOTO 440

      OBS(OBSCODE,1)=LONG
      OBS(OBSCODE,2)=DDXY
      OBS(OBSCODE,3)=DDZ
      OBSNAME(OBSCODE)=NAME

      GOTO 410

440   CLOSE(IUNIT)

      END
      SUBROUTINE READOBS2000 (OBS, NUMBER,DESIG,DISC,COMMENT1,COMMENT2,
     /                        YEAR,MONTH,DAY,RA,DEC,MAG,MAGTYPE,OBSCODE)
*+
*  Given:
*    OBS      [CHARACTER*80, an observation in MPC J2000 format]
*
*  Returned:
*    NUMBER   [INTEGER]
*    DESIG    [CHARACTER*7]
*    DISC     [CHARACTER*1]
*    COMMENT1 [CHARACTER*1]
*    COMMENT2 [CHARACTER*1]
*    YEAR     [INTEGER]
*    MONTH    [INTEGER]
*    DAY      [DOUBLE PRECISION]
*    RA       [DOUBLE PRECISION, in radians]
*    DEC      [DOUBLE PRECISION, in radians]
*    MAG      [DOUBLE PRECISION]
*    MAGTYPE  [CHARACTER*1]
*    OBSCODE  [INTEGER]
*
*  Last update 971222 (changed format X to 1X as some compilers require)
*-
      CHARACTER OBS*80,DESIG*7,DISC,COMMENT1,COMMENT2,SIGN,MAGTYPE,C5*5
      INTEGER YEAR,MONTH,RAHR,RAMIN,DEG,DECMIN,OBSCODE
      DOUBLE PRECISION RA,DEC,DAY,RASEC,DECSEC,MAG,RD
      PARAMETER (RD=57.295779513082321D0)

      READ (OBS,920) C5,DESIG,DISC,COMMENT1,COMMENT2,
     / YEAR,MONTH,DAY, RAHR,RAMIN,RASEC, SIGN,DEG,DECMIN,DECSEC,
     / IM1,IM2,IM3,MAGTYPE, OBSCODE
*   Possible problems (depending on compiler) with trailing blanks:
      MAG=IM1+IM2/10D0+IM3/100D0

920   FORMAT (5A,
     / I4,I3,F10.7, I2,I3,F6.3, 1X,A,I2,I3,F5.2, 10X,I2,1X,2I1,A, 6X,I3)

      READ (C5,'(I5)',ERR=50) NUMBER
*   (Comet will have letter as 5th character & so give error)
      GOTO 55
   50 READ (C5,'(I4)') NUMBER
   55 CONTINUE

      RA=(RAHR+RAMIN/60.0D0+RASEC/3600)*15/RD
      DEC=(DEG+DECMIN/60.0D0+DECSEC/3600)/RD
      IF (SIGN.EQ.'-') DEC=-DEC

*   Default is that mag is a B mag
      IF (MAGTYPE.EQ.' ') MAGTYPE='B'

      END
      SUBROUTINE JDATE(Y,M,DAY,JDAY)
*+
*  991201:  Added IF block so as to use Julian not Gregorian calendar
*           before 1582 Oct 15
*-
      REAL*8 JDAY,DAY
      INTEGER Y,M,JD,YD,MD,C,D
      JD=367*Y-7*(Y+(M+9)/12)/4-3*((Y+(M-9)/7)/100+1)/4+275*M/9
     1+1721029
      JDAY=JD+DAY-0.5
      IF (Y.LE.1581 .OR.
     $   (Y.EQ.1582 .AND. (M.LE.9 .OR. (M.EQ.10.AND.DAY.LT.15D0)))) THEN
         IF (Y.EQ.1582.AND.M.EQ.10.AND.DAY.GE.5D0.AND.DAY.LT.15D0)
     $    PRINT *, '***  WARNING:  Non-existent day  ***'
         YD=Y
         MD=M
         IF (M.LT.3) THEN
            YD=Y-1
            MD=M+12
         ENDIF
         C=INT(365.25*YD)
         D=INT(30.6001*(MD+1))
         JDAY=C+D+DAY+1720994.5D0
      ENDIF
      END
      SUBROUTINE FINDET(YEAR,ET)
      INTEGER YEAR,YEAR2
      REAL ET

      CALL OPFLRD ('ET', IUNIT)
11    READ(IUNIT,*) YEAR2,ET
      IF (YEAR.GE.YEAR2) GOTO 12
      IF (YEAR2.EQ.-999) GOTO 12
      GOTO 11
12    ET=ET/86400

      CLOSE(IUNIT)

      END
      SUBROUTINE SE2000 (JDE, RS,XS,YS,ZS)
*+
*  J2000 solar ephemeris
*  ---------------------
*
*  Given:
*     JDE
*
*  Returned:
*     Geocentric dist. & x, y, z coords (equatorial J2000) of Sun in AU
*
*  Link with JPL ephemeris software & SLALIB subroutine library
*
*  Input binary file (JPL format) needed:  JPLEPH
*
*  JPL subprograms called:  PLEPH, CONST, STATE, FSIZER3, SPLIT, INTERP
*  COMMON block names in JPL subprograms:  CHRHDR, EPHHDR, STCOMX
*  Fortran i/o unit no. used in JPL subprograms:  12
*
*  Last update 980917
*-
      DOUBLE PRECISION JDE,RS,XS,YS,ZS,VB(3),PB(3),VH(3),PH(3),R(6),
     $ VALS(400),SS(3)
*     CHARACTER*6 NAMS(400)
*     LOGICAL WITHIN

*   Check if date within range
*     CALL CONST (NAMS,VALS,SS,NVS)
*     WITHIN=SS(1).LT.JDE.AND.JDE.LT.SS(2)

*     IF (WITHIN) THEN
*      JPL routine (3 is code for Earth, 11 for Sun)
*        CALL PLEPH (JDE,3,11, R)
*        XS=-R(1)
*        YS=-R(2)
*        ZS=-R(3)
*     ELSE
*      JPL data unavailable; use SLALIB routine
         CALL SLA_EVP (JDE-2400000.5D0,2000D0, VB,PB,VH,PH)
         XS=-PH(1)
         YS=-PH(2)
         ZS=-PH(3)
*     ENDIF

      RS=SQRT(XS*XS+YS*YS+ZS*ZS)

* --------------------- End of subroutine SE2000 --------------------- *
      END
      SUBROUTINE LST(J,LONG,TH)

      IMPLICIT NONE
      DOUBLE PRECISION J,J1,T,TH,UT,LONG

      T=(J-2415020)/36525

      TH=(6.6460656+2400.051262*T+0.00002581*T*T)/24

      J1=J-.5
      UT=(J1-INT(J1))

      TH=TH+UT+LONG
      TH=(TH-INT(TH))*6.28318530

      END
      SUBROUTINE MAG(RSUN,R,DELTA,H,G,ELONG,PSI,M1)

      REAL*8 DELTA,R,RSUN,H,G,M1,ELONG,PSI,PHI1,PHI2,RD
      RD=57.2957795131

      ELONG=ACOS((RSUN*RSUN+DELTA*DELTA-R*R)/(2*RSUN*DELTA))*RD
      PSI  =ACOS((R*R+DELTA*DELTA-RSUN*RSUN)/(2*R*DELTA))

      IF (G.LT.1) THEN
      PHI1=EXP(-3.33*(TAN(PSI/2))**0.63)
      PHI2=EXP(-1.87*(TAN(PSI/2))**1.22)
      M1=H+5*LOG10(R*DELTA)-2.5*LOG10((1-G)*PHI1+G*PHI2)
            ELSE
            M1=H+5*LOG10(DELTA)+G*LOG10(R)
      END IF

      PSI=PSI*RD
      END
      SUBROUTINE CIVILDATE(JD,YEAR,MONTH,DAY)
*+
*  991202:  Added IF block so as to use Julian not Gregorian calendar
*           before 1582 Oct 15
*-
      IMPLICIT NONE
      REAL*8 JD,DAY,F,J
      INTEGER YEAR,MONTH,Z,ALPHA,A,B,C,D,E

      J=JD+5D-1
      Z=INT(J)
      F=J-Z

      IF (Z.GT.2299160) THEN
       ALPHA=INT((Z-1867216.25)/36524.25)
       A=Z+1+ALPHA-INT(ALPHA/4)
      ELSE
       A=Z
      ENDIF
      B=A+1524
      C=INT((B-122.1)/365.25)
      D=INT(365.25*C)
      E=INT((B-D)/30.6001)

      DAY=B-D-INT(30.6001*E)+F

      IF (E.LT.14) THEN
      MONTH=E-1
          ELSE
          MONTH=E-13
          END IF

      IF (MONTH.GT.2) THEN
      YEAR=C-4716
          ELSE
          YEAR=C-4715
          END IF
      END
      SUBROUTINE EL2050(WP,NP,IP,W,N,I)
C     Subroutine EL2050 computes the angular elements (inclination,
C     longitude of the ascending node, and argument of perihelion) of a
C     minor planet or comet at B1950.0 on the FK4 system from the angular
C     elements at J2000.0 on the FK5 system using formula derived from
C     E.M. Standish's diagram.
C
C     External References: None
C
      IMPLICIT NONE
      DOUBLE PRECISION I, IP, N, NP, W, WP
C
C     Input: Angle elements (IP, NP, WP) wrt mean ecliptic and equinox of
C            J2000.0 on the FK5 system, where:
C                    IP = Inclination (deg).
C                    NP = Longitude of the ascending node (deg).
C                    WP = Argument of perihelion (deg).
C
C     Output: Angle elements (I, N, W) wrt mean ecliptic and equinox of
C             B1950.0 on the FK4 system, where:
C                    I = Inclination (deg).
C                    N = Longitude of the ascending node (deg).
C                    W = Argument of perihelion (deg).
C
      DOUBLE PRECISION J, L, LP, JD, LD, LPD
      DOUBLE PRECISION SS, CS, LPN, LPPNP, WPMW, CI
      DOUBLE PRECISION TWOPI, DPR
C
      DATA JD, LD, LPD /0.00651966D0, 5.19856209D0, 4.50001688D0/
      DATA TWOPI  /6.283185307179586D0/
C
      DPR = 360.D0 / TWOPI
C
      J  = JD  / DPR
      L  = LD  / DPR
      LP = LPD / DPR
      WP  = WP  / DPR
      NP  = NP  / DPR
      IP  = IP  / DPR
C
      LPPNP = LP + NP
      SS  = DSIN(J) * DSIN(LPPNP)
      CS  = DSIN(IP) * DCOS(J) - DCOS(IP) * DSIN(J) * DCOS(LPPNP)
      WPMW = DATAN2(SS,CS)
      W  = (WP - WPMW) * DPR
C
      CI = DCOS(IP) * DCOS(J) + DSIN(IP) * DSIN(J) * DCOS(LPPNP)
      I  = DACOS(CI) * DPR
C
      SS  = DSIN(IP) * DSIN(LPPNP)
      CS  = -DCOS(IP) * DSIN(J) + DSIN(IP) * DCOS(J) * DCOS(LPPNP)
      LPN = DATAN2(SS,CS)
      N = (LPN - L) * DPR
C
      W = DMOD(W,360.D0)
      N = DMOD(N,360.D0)
      I = DMOD(I,360.D0)
      IF  (W .LT. 0.D0) W = W + 360.D0
      IF  (I .LT. 0.D0) I = I + 360.D0
      IF  (N .LT. 0.D0) N = N + 360.D0
C

      END
      DOUBLE PRECISION FUNCTION AET2M (A,EPOCH,T)
*+
*  M (dbl) from a (dbl), epoch (int), T (dbl), where
*    a is semi-major axis in AU,
*    epoch (TT) is in form YYMMDD,
*    T is JD (TT) of perihelion passage,
*  & M is mean anomaly at epoch (0-360)
*
*  Called:  JDATE, POSMOD
*-
      IMPLICIT DOUBLE PRECISION (A-Z)
      INTEGER EPOCH
      PARAMETER (PI=3.14159265358979323846D0,K=0.01720209895D0)
      CALL JDATE (1900+EPOCH/10000,MOD(EPOCH,10000)/100,
     $ DBLE(MOD(EPOCH,100)), JDEP)
      AET2M=POSMOD(180*K*(JDEP-T)/(PI*A**1.5D0),360D0)
      END
      SUBROUTINE OPFLWR (FLNM, IUNIT)
*+
*  FLNM should be the name of a desired new file; then OPFLWR looks for
*  the 1st unopened unit numbered in the range 50-99, connects FLNM to
*  that unit with sensible (i.e. not Fortran) carriage control & returns
*  the unit number.
*  Stops program execution if no unopened unit can be found.
*
*  960323:  Removed CARRIAGECONTROL='LIST' from CLOSE statement (only
*  needed on Vax)
*-
      PARAMETER (MINU=50,MAXU=99)
      CHARACTER FLNM*(*)
      LOGICAL L
      IUNIT=MINU-1
    5 IUNIT=IUNIT+1
      INQUIRE (IUNIT, OPENED=L)
      IF (L) THEN
         IF (IUNIT.LT.MAXU) GOTO 5
         STOP 'Program execution terminated in routine OPFLWR'
      ELSE
         OPEN (IUNIT, FILE=FLNM, STATUS='NEW')
      ENDIF
      END
      DOUBLE PRECISION FUNCTION POSMOD (A,B)
*+
*  Same as MOD except always positive
*-
      IMPLICIT DOUBLE PRECISION (A-Z)
      P=MOD(A,B)
      IF (P.LT.0) P=P+B
      POSMOD=P
      END

C+++++++++++++++++++++++++++++
C
      SUBROUTINE CONST(NAM,VAL,SSS,N)
C
C+++++++++++++++++++++++++++++
C
C     THIS ENTRY OBTAINS THE CONSTANTS FROM THE EPHEMERIS FILE
C
C     CALLING SEQEUNCE PARAMETERS (ALL OUTPUT):
C
C       NAM = CHARACTER*6 ARRAY OF CONSTANT NAMES
C
C       VAL = D.P. ARRAY OF VALUES OF CONSTANTS
C
C       SSS = D.P. JD START, JD STOP, STEP OF EPHEMERIS
C
C         N = INTEGER NUMBER OF ENTRIES IN 'NAM' AND 'VAL' ARRAYS
C
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
C
      SAVE

      CHARACTER*6 NAM(*),TTL(14,3),CNAM(400)

      DOUBLE PRECISION VAL(*),SSS(3),SS(3),CVAL(400)
      DOUBLE PRECISION ET2(2),PV(6,12),PNUT(4)

      INTEGER IPT(3,13),DENUM,LIST(12)

      COMMON/EPHHDR/CVAL,SS,AU,EMRAT,DENUM,NCON,IPT
      COMMON/CHRHDR/CNAM,TTL

      ET2(1)=0D0
      ET2(2)=0D0
      DO I=1,12
      LIST(I)=0
      ENDDO

C  CALL STATE TO INITIALIZE THE EPHEMERIS AND READ IN THE CONSTANTS

      CALL STATE (ET2,LIST, PV,PNUT)

      N=NCON

      DO I=1,3
      SSS(I)=SS(I)
      ENDDO

      DO I=1,N
      NAM(I)=CNAM(I)
      VAL(I)=CVAL(I)
      ENDDO

      RETURN

      END
C++++++++++++++++++++++++++
C
      SUBROUTINE PLEPH ( ET, NTARG, NCENT, RRD )
C
C++++++++++++++++++++++++++
C  NOTE : Over the years, different versions of PLEPH have had a fifth argument:
C  sometimes, an error return statement number; sometimes, a logical denoting
C  whether or not the requested date is covered by the ephemeris.  We apologize
C  for this inconsistency; in this present version, we use only the four necessary 
C  arguments and do the testing outside of the subroutine.
C
C
C
C     THIS SUBROUTINE READS THE JPL PLANETARY EPHEMERIS
C     AND GIVES THE POSITION AND VELOCITY OF THE POINT 'NTARG'
C     WITH RESPECT TO 'NCENT'.
C
C     CALLING SEQUENCE PARAMETERS:
C
C       ET = D.P. JULIAN EPHEMERIS DATE AT WHICH INTERPOLATION
C            IS WANTED.
C
C       ** NOTE THE ENTRY DPLEPH FOR A DOUBLY-DIMENSIONED TIME **
C          THE REASON FOR THIS OPTION IS DISCUSSED IN THE 
C          SUBROUTINE STATE
C
C     NTARG = INTEGER NUMBER OF 'TARGET' POINT.
C
C     NCENT = INTEGER NUMBER OF CENTER POINT.
C
C            THE NUMBERING CONVENTION FOR 'NTARG' AND 'NCENT' IS:
C
C                1 = MERCURY           8 = NEPTUNE
C                2 = VENUS             9 = PLUTO
C                3 = EARTH            10 = MOON
C                4 = MARS             11 = SUN
C                5 = JUPITER          12 = SOLAR-SYSTEM BARYCENTER
C                6 = SATURN           13 = EARTH-MOON BARYCENTER
C                7 = URANUS           14 = NUTATIONS (LONGITUDE AND OBLIQ)
C                            15 = LIBRATIONS, IF ON EPH FILE
C
C             (IF NUTATIONS ARE WANTED, SET NTARG = 14. FOR LIBRATIONS,
C              SET NTARG = 15. SET NCENT=0.)
C
C      RRD = OUTPUT 6-WORD D.P. ARRAY CONTAINING POSITION AND VELOCITY
C            OF POINT 'NTARG' RELATIVE TO 'NCENT'. THE UNITS ARE AU AND
C            AU/DAY. FOR LIBRATIONS THE UNITS ARE RADIANS AND RADIANS
C            PER DAY. IN THE CASE OF NUTATIONS THE FIRST FOUR WORDS OF
C            RRD WILL BE SET TO NUTATIONS AND RATES, HAVING UNITS OF
C            RADIANS AND RADIANS/DAY.
C
C            The option is available to have the units in km and km/sec.
C            For this, set km=.true. in the STCOMX common block.
C

      IMPLICIT DOUBLE PRECISION (A-H,O-Z)

      DIMENSION RRD(6),ET2Z(2),ET2(2),PV(6,13)
      DIMENSION SS(3),CVAL(400),PVSUN(6)

      LOGICAL BSAVE,KM,BARY

      INTEGER LIST(12),IPT(36),LPT(3),DENUM


      COMMON/EPHHDR/CVAL,SS,AU,EMRAT,DENUM,NCON,IPT,LPT

      COMMON/STCOMX/KM,BARY,PVSUN

C     INITIALIZE ET2 FOR 'STATE' AND SET UP COMPONENT COUNT
C
      ET2(1)=ET
      ET2(2)=0.D0
      GO TO 11

C     ENTRY POINT 'DPLEPH' FOR DOUBLY-DIMENSIONED TIME ARGUMENT 
C          (SEE THE DISCUSSION IN THE SUBROUTINE STATE)

      ENTRY DPLEPH(ET2Z,NTARG,NCENT,RRD)

      ET2(1)=ET2Z(1)
      ET2(2)=ET2Z(2)

  11  ETTOT=ET2(1)+ET2(2)

      DO I=1,6
      RRD(I)=0.D0
      ENDDO

  96  IF(NTARG .EQ. NCENT) RETURN

      DO I=1,12
      LIST(I)=0
      ENDDO

C     CHECK FOR NUTATION CALL

      IF(NTARG.NE.14) GO TO 97
        IF(IPT(35).GT.0) THEN
          LIST(11)=2
          CALL STATE(ET2,LIST,PV,RRD)
          RETURN
        ELSE
          WRITE(6,297)
  297     FORMAT(' *****  NO NUTATIONS ON THE EPHEMERIS FILE  *****')
          STOP
        ENDIF

C     CHECK FOR LIBRATIONS

  97  IF(NTARG.NE.15) GO TO 98
        IF(LPT(2).GT.0) THEN
          LIST(12)=2
          CALL STATE(ET2,LIST,PV,RRD)
          DO I=1,6
          RRD(I)=PV(I,11)
          ENDDO
          RETURN
        ELSE
          WRITE(6,298)
  298     FORMAT(' *****  NO LIBRATIONS ON THE EPHEMERIS FILE  *****')
          STOP
        ENDIF

C       FORCE BARYCENTRIC OUTPUT BY 'STATE'

  98  BSAVE=BARY
      BARY=.TRUE.

C       SET UP PROPER ENTRIES IN 'LIST' ARRAY FOR STATE CALL

      DO I=1,2
      K=NTARG
      IF(I .EQ. 2) K=NCENT
      IF(K .LE. 10) LIST(K)=2
      IF(K .EQ. 10) LIST(3)=2
      IF(K .EQ. 3) LIST(10)=2
      IF(K .EQ. 13) LIST(3)=2
      ENDDO

C       MAKE CALL TO STATE

      CALL STATE(ET2,LIST,PV,RRD)

      IF(NTARG .EQ. 11 .OR. NCENT .EQ. 11) THEN
      DO I=1,6
      PV(I,11)=PVSUN(I)
      ENDDO
      ENDIF

      IF(NTARG .EQ. 12 .OR. NCENT .EQ. 12) THEN
      DO I=1,6
      PV(I,12)=0.D0
      ENDDO
      ENDIF

      IF(NTARG .EQ. 13 .OR. NCENT .EQ. 13) THEN
      DO I=1,6
      PV(I,13)=PV(I,3)
      ENDDO
      ENDIF

      IF(NTARG*NCENT .EQ. 30 .AND. NTARG+NCENT .EQ. 13) THEN
      DO I=1,6
      PV(I,3)=0.D0
      ENDDO
      GO TO 99
      ENDIF

      IF(LIST(3) .EQ. 2) THEN
      DO I=1,6
      PV(I,3)=PV(I,3)-PV(I,10)/(1.D0+EMRAT)
      ENDDO
      ENDIF

      IF(LIST(10) .EQ. 2) THEN
      DO I=1,6
      PV(I,10)=PV(I,3)+PV(I,10)
      ENDDO
      ENDIF

  99  DO I=1,6
      RRD(I)=PV(I,NTARG)-PV(I,NCENT)
      ENDDO

      BARY=BSAVE

      RETURN
      END


C++++++++++++++++++++++++++++++++
C
      SUBROUTINE STATE(ET2,LIST,PV,PNUT)
C
C++++++++++++++++++++++++++++++++
C
C THIS SUBROUTINE READS AND INTERPOLATES THE JPL PLANETARY EPHEMERIS FILE
C
C     CALLING SEQUENCE PARAMETERS:
C
C     INPUT:
C
C         ET2   DP 2-WORD JULIAN EPHEMERIS EPOCH AT WHICH INTERPOLATION
C               IS WANTED.  ANY COMBINATION OF ET2(1)+ET2(2) WHICH FALLS
C               WITHIN THE TIME SPAN ON THE FILE IS A PERMISSIBLE EPOCH.
C
C                A. FOR EASE IN PROGRAMMING, THE USER MAY PUT THE
C                   ENTIRE EPOCH IN ET2(1) AND SET ET2(2)=0.
C
C                B. FOR MAXIMUM INTERPOLATION ACCURACY, SET ET2(1) =
C                   THE MOST RECENT MIDNIGHT AT OR BEFORE INTERPOLATION
C                   EPOCH AND SET ET2(2) = FRACTIONAL PART OF A DAY
C                   ELAPSED BETWEEN ET2(1) AND EPOCH.
C
C                C. AS AN ALTERNATIVE, IT MAY PROVE CONVENIENT TO SET
C                   ET2(1) = SOME FIXED EPOCH, SUCH AS START OF INTEGRATION,
C                   AND ET2(2) = ELAPSED INTERVAL BETWEEN THEN AND EPOCH.
C
C        LIST   12-WORD INTEGER ARRAY SPECIFYING WHAT INTERPOLATION
C               IS WANTED FOR EACH OF THE BODIES ON THE FILE.
C
C                         LIST(I)=0, NO INTERPOLATION FOR BODY I
C                                =1, POSITION ONLY
C                                =2, POSITION AND VELOCITY
C
C               THE DESIGNATION OF THE ASTRONOMICAL BODIES BY I IS:
C
C                         I = 1: MERCURY
C                           = 2: VENUS
C                           = 3: EARTH-MOON BARYCENTER
C                           = 4: MARS
C                           = 5: JUPITER
C                           = 6: SATURN
C                           = 7: URANUS
C                           = 8: NEPTUNE
C                           = 9: PLUTO
C                           =10: GEOCENTRIC MOON
C                           =11: NUTATIONS IN LONGITUDE AND OBLIQUITY
C                           =12: LUNAR LIBRATIONS (IF ON FILE)
C
C
C     OUTPUT:
C
C          PV   DP 6 X 11 ARRAY THAT WILL CONTAIN REQUESTED INTERPOLATED
C               QUANTITIES.  THE BODY SPECIFIED BY LIST(I) WILL HAVE ITS
C               STATE IN THE ARRAY STARTING AT PV(1,I).  (ON ANY GIVEN
C               CALL, ONLY THOSE WORDS IN 'PV' WHICH ARE AFFECTED BY THE
C               FIRST 10 'LIST' ENTRIES (AND BY LIST(12) IF LIBRATIONS ARE
C               ON THE FILE) ARE SET.  THE REST OF THE 'PV' ARRAY
C               IS UNTOUCHED.)  THE ORDER OF COMPONENTS STARTING IN
C               PV(1,I) IS: X,Y,Z,DX,DY,DZ.
C
C               ALL OUTPUT VECTORS ARE REFERENCED TO THE EARTH MEAN
C               EQUATOR AND EQUINOX OF EPOCH. THE MOON STATE IS ALWAYS
C               GEOCENTRIC; THE OTHER NINE STATES ARE EITHER HELIOCENTRIC
C               OR SOLAR-SYSTEM BARYCENTRIC, DEPENDING ON THE SETTING OF
C               COMMON FLAGS (SEE BELOW).
C
C               LUNAR LIBRATIONS, IF ON FILE, ARE PUT INTO PV(K,11) IF
C               LIST(12) IS 1 OR 2.
C
C         NUT   DP 4-WORD ARRAY THAT WILL CONTAIN NUTATIONS AND RATES,
C               DEPENDING ON THE SETTING OF LIST(11).  THE ORDER OF
C               QUANTITIES IN NUT IS:
C
C                        D PSI  (NUTATION IN LONGITUDE)
C                        D EPSILON (NUTATION IN OBLIQUITY)
C                        D PSI DOT
C                        D EPSILON DOT
C
C           *   STATEMENT # FOR ERROR RETURN, IN CASE OF EPOCH OUT OF
C               RANGE OR I/O ERRORS.
C
C
C     COMMON AREA STCOMX:
C
C          KM   LOGICAL FLAG DEFINING PHYSICAL UNITS OF THE OUTPUT
C               STATES. KM = .TRUE., KM AND KM/SEC
C                          = .FALSE., AU AND AU/DAY
C               DEFAULT VALUE = .FALSE.  (KM DETERMINES TIME UNIT
C               FOR NUTATIONS AND LIBRATIONS.  ANGLE UNIT IS ALWAYS RADIANS.)
C
C        BARY   LOGICAL FLAG DEFINING OUTPUT CENTER.
C               ONLY THE 9 PLANETS ARE AFFECTED.
C                        BARY = .TRUE. =\ CENTER IS SOLAR-SYSTEM BARYCENTER
C                             = .FALSE. =\ CENTER IS SUN
C               DEFAULT VALUE = .FALSE.
C
C       PVSUN   DP 6-WORD ARRAY CONTAINING THE BARYCENTRIC POSITION AND
C               VELOCITY OF THE SUN.
C
C
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
C
      SAVE

      DIMENSION ET2(2),PV(6,12),PNUT(4),T(2),PJD(4),BUF(1500),
     . SS(3),CVAL(400),PVSUN(3,2)

      INTEGER LIST(12),IPT(3,13),LPT(3)

      LOGICAL FIRST
      DATA FIRST/.TRUE./

      CHARACTER*6 TTL(14,3),CNAM(400)
      CHARACTER*80 NAMFIL

      LOGICAL KM,BARY

      COMMON/EPHHDR/CVAL,SS,AU,EMRAT,NUMDE,NCON,IPT
      COMMON/CHRHDR/CNAM,TTL
      COMMON/STCOMX/KM,BARY,PVSUN

C
C       ENTRY POINT - 1ST TIME IN, GET POINTER DATA, ETC., FROM EPH FILE
C
      IF(FIRST) THEN
        FIRST=.FALSE.

C ************************************************************************
C ************************************************************************

C THE USER MUST SELECT ONE OF THE FOLLOWING BY DELETING THE 'C' IN COLUMN 1

C ************************************************************************

C        CALL FSIZER1(NRECL,KSIZE,NRFILE,NAMFIL)
C        CALL FSIZER2(NRECL,KSIZE,NRFILE,NAMFIL)
        CALL FSIZER3(NRECL,KSIZE,NRFILE,NAMFIL)

      IF(NRECL .EQ. 0) WRITE(*,*)'  ***** FSIZER IS NOT WORKING *****'

C ************************************************************************
C ************************************************************************

      IRECSZ=NRECL*KSIZE
      NCOEFFS=KSIZE/2

        OPEN(NRFILE,
     *       FILE=NAMFIL,
     *       ACCESS='DIRECT',
     *       FORM='UNFORMATTED',
     *       RECL=IRECSZ,
     *       STATUS='OLD')

      READ(NRFILE,REC=1)TTL,CNAM,SS,NCON,AU,EMRAT,
     . ((IPT(I,J),I=1,3),J=1,12),NUMDE,LPT

      READ(NRFILE,REC=2)CVAL

      DO I=1,3
      IPT(I,13)=LPT(I)
      ENDDO
      NRL=0

      ENDIF


C       ********** MAIN ENTRY POINT **********


      IF(ET2(1) .EQ. 0.D0) RETURN

      S=ET2(1)-.5D0
      CALL SPLIT(S,PJD(1))
      CALL SPLIT(ET2(2),PJD(3))
      PJD(1)=PJD(1)+PJD(3)+.5D0
      PJD(2)=PJD(2)+PJD(4)
      CALL SPLIT(PJD(2),PJD(3))
      PJD(1)=PJD(1)+PJD(3)

C       ERROR RETURN FOR EPOCH OUT OF RANGE

      IF(PJD(1)+PJD(4).LT.SS(1) .OR. PJD(1)+PJD(4).GT.SS(2)) GO TO 98

C       CALCULATE RECORD # AND RELATIVE TIME IN INTERVAL

      NR=IDINT((PJD(1)-SS(1))/SS(3))+3
      IF(PJD(1).EQ.SS(2)) NR=NR-1
      T(1)=((PJD(1)-(DBLE(NR-3)*SS(3)+SS(1)))+PJD(4))/SS(3)

C       READ CORRECT RECORD IF NOT IN CORE

      IF(NR.NE.NRL) THEN
        NRL=NR
        READ(NRFILE,REC=NR,ERR=99)(BUF(K),K=1,NCOEFFS)
      ENDIF

      IF(KM) THEN
      T(2)=SS(3)*86400.D0
      AUFAC=1.D0
      ELSE
      T(2)=SS(3)
      AUFAC=1.D0/AU
      ENDIF

C   INTERPOLATE SSBARY SUN

      CALL INTERP(BUF(IPT(1,11)),T,IPT(2,11),3,IPT(3,11),2,PVSUN)

      DO I=1,6
      PVSUN(I,1)=PVSUN(I,1)*AUFAC
      ENDDO

C   CHECK AND INTERPOLATE WHICHEVER BODIES ARE REQUESTED

      DO 4 I=1,10
      IF(LIST(I).EQ.0) GO TO 4

      CALL INTERP(BUF(IPT(1,I)),T,IPT(2,I),3,IPT(3,I),
     & LIST(I),PV(1,I))

      DO J=1,6
       IF(I.LE.9 .AND. .NOT.BARY) THEN
       PV(J,I)=PV(J,I)*AUFAC-PVSUN(J,1)
       ELSE
       PV(J,I)=PV(J,I)*AUFAC
       ENDIF
      ENDDO

   4  CONTINUE

C       DO NUTATIONS IF REQUESTED (AND IF ON FILE)

      IF(LIST(11).GT.0 .AND. IPT(2,12).GT.0)
     * CALL INTERP(BUF(IPT(1,12)),T,IPT(2,12),2,IPT(3,12),
     * LIST(11),PNUT)

C       GET LIBRATIONS IF REQUESTED (AND IF ON FILE)

      IF(LIST(12).GT.0 .AND. IPT(2,13).GT.0)
     * CALL INTERP(BUF(IPT(1,13)),T,IPT(2,13),3,IPT(3,13),
     * LIST(12),PV(1,11))

      RETURN

  98  WRITE(*,198)ET2(1)+ET2(2),SS(1),SS(2)
 198  format(' ***  Requested JED,',f12.2,
     * ' not within ephemeris limits,',2f12.2,'  ***')

      return

   99 WRITE(*,'(2I3,2F12.2,A80)')
     & ET2,NTARG,NCENT,'ERROR RETURN IN STATE'

      STOP

      END
C++++++++++++++++++++++++
C
      SUBROUTINE FSIZER3(NRECL,KSIZE,NRFILE,NAMFIL)
C
C++++++++++++++++++++++++
C
C  THE SUBROUTINE SETS THE VALUES OF  NRECL, KSIZE, NRFILE, AND NAMFIL.

      SAVE

      CHARACTER*80 NAMFIL

C  *****************************************************************
C  *****************************************************************
C
C  THE PARAMETERS NRECL, NRFILE, AND NAMFIL ARE TO BE SET BY THE USER

C  *****************************************************************

C  NRECL=1 IF "RECL" IN THE OPEN STATEMENT IS THE RECORD LENGTH IN S.P. WORDS
C  NRECL=4 IF "RECL" IN THE OPEN STATEMENT IS THE RECORD LENGTH IN BYTES

      NRECL=1

C  *****************************************************************

C  NRFILE IS THE INTERNAL UNIT NUMBER USED FOR THE EPHEMERIS FILE (DEFAULT: 12)

      NRFILE=12

C  *****************************************************************

C  NAMFIL IS THE EXTERNAL NAME OF THE BINARY EPHEMERIS FILE

      NAMFIL='JPLEPH'

C  *****************************************************************

C  KSIZE must be set by the user according to the ephemeris to be read

C  For  de200, set KSIZE to 1652
C  For  de403, set KSIZE to 2036
C  For  de404, set KSIZE to 1456

      KSIZE = 2036

C  *******************************************************************

      RETURN

      END

C+++++++++++++++++++++++++
C
      SUBROUTINE SPLIT(TT,FR)
C
C+++++++++++++++++++++++++
C
C     THIS SUBROUTINE BREAKS A D.P. NUMBER INTO A D.P. INTEGER
C     AND A D.P. FRACTIONAL PART.
C
C     CALLING SEQUENCE PARAMETERS:
C
C       TT = D.P. INPUT NUMBER
C
C       FR = D.P. 2-WORD OUTPUT ARRAY.
C            FR(1) CONTAINS INTEGER PART
C            FR(2) CONTAINS FRACTIONAL PART
C
C            FOR NEGATIVE INPUT NUMBERS, FR(1) CONTAINS THE NEXT
C            MORE NEGATIVE INTEGER; FR(2) CONTAINS A POSITIVE FRACTION.
C
C       CALLING SEQUENCE DECLARATIONS
C
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)

      DIMENSION FR(2)

C       MAIN ENTRY -- GET INTEGER AND FRACTIONAL PARTS

      FR(1)=DINT(TT)
      FR(2)=TT-FR(1)

      IF(TT.GE.0.D0 .OR. FR(2).EQ.0.D0) RETURN

C       MAKE ADJUSTMENTS FOR NEGATIVE INPUT NUMBER

      FR(1)=FR(1)-1.D0
      FR(2)=FR(2)+1.D0

      RETURN

      END
C+++++++++++++++++++++++++++++++++
C
      SUBROUTINE INTERP(BUF,T,NCF,NCM,NA,IFL,PV)
C
C+++++++++++++++++++++++++++++++++
C
C     THIS SUBROUTINE DIFFERENTIATES AND INTERPOLATES A
C     SET OF CHEBYSHEV COEFFICIENTS TO GIVE POSITION AND VELOCITY
C
C     CALLING SEQUENCE PARAMETERS:
C
C       INPUT:
C
C         BUF   1ST LOCATION OF ARRAY OF D.P. CHEBYSHEV COEFFICIENTS OF POSITION
C
C           T   T(1) IS DP FRACTIONAL TIME IN INTERVAL COVERED BY
C               COEFFICIENTS AT WHICH INTERPOLATION IS WANTED
C               (0 .LE. T(1) .LE. 1).  T(2) IS DP LENGTH OF WHOLE
C               INTERVAL IN INPUT TIME UNITS.
C
C         NCF   # OF COEFFICIENTS PER COMPONENT
C
C         NCM   # OF COMPONENTS PER SET OF COEFFICIENTS
C
C          NA   # OF SETS OF COEFFICIENTS IN FULL ARRAY
C               (I.E., # OF SUB-INTERVALS IN FULL INTERVAL)
C
C          IFL  INTEGER FLAG: =1 FOR POSITIONS ONLY
C                             =2 FOR POS AND VEL
C
C
C       OUTPUT:
C
C         PV   INTERPOLATED QUANTITIES REQUESTED.  DIMENSION
C               EXPECTED IS PV(NCM,IFL), DP.
C
C
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
C
      SAVE
C
      DOUBLE PRECISION BUF(NCF,NCM,*),T(2),PV(NCM,*),PC(18),VC(18)

C
      DATA NP/2/
      DATA NV/3/
      DATA TWOT/0.D0/
      DATA PC(1),PC(2)/1.D0,0.D0/
      DATA VC(2)/1.D0/
C
C       ENTRY POINT. GET CORRECT SUB-INTERVAL NUMBER FOR THIS SET
C       OF COEFFICIENTS AND THEN GET NORMALIZED CHEBYSHEV TIME
C       WITHIN THAT SUBINTERVAL.
C
      DNA=DBLE(NA)
      DT1=DINT(T(1))
      TEMP=DNA*T(1)
      L=IDINT(TEMP-DT1)+1

C         TC IS THE NORMALIZED CHEBYSHEV TIME (-1 .LE. TC .LE. 1)

      TC=2.D0*(DMOD(TEMP,1.D0)+DT1)-1.D0

C       CHECK TO SEE WHETHER CHEBYSHEV TIME HAS CHANGED,
C       AND COMPUTE NEW POLYNOMIAL VALUES IF IT HAS.
C       (THE ELEMENT PC(2) IS THE VALUE OF T1(TC) AND HENCE
C       CONTAINS THE VALUE OF TC ON THE PREVIOUS CALL.)

      IF(TC.NE.PC(2)) THEN
        NP=2
        NV=3
        PC(2)=TC
        TWOT=TC+TC
      ENDIF
C
C       BE SURE THAT AT LEAST 'NCF' POLYNOMIALS HAVE BEEN EVALUATED
C       AND ARE STORED IN THE ARRAY 'PC'.
C
      IF(NP.LT.NCF) THEN
        DO 1 I=NP+1,NCF
        PC(I)=TWOT*PC(I-1)-PC(I-2)
    1   CONTINUE
        NP=NCF
      ENDIF
C
C       INTERPOLATE TO GET POSITION FOR EACH COMPONENT
C
      DO 2 I=1,NCM
      PV(I,1)=0.D0
      DO 3 J=NCF,1,-1
      PV(I,1)=PV(I,1)+PC(J)*BUF(J,I,L)
    3 CONTINUE
    2 CONTINUE
      IF(IFL.LE.1) RETURN
C
C       IF VELOCITY INTERPOLATION IS WANTED, BE SURE ENOUGH
C       DERIVATIVE POLYNOMIALS HAVE BEEN GENERATED AND STORED.
C
      VFAC=(DNA+DNA)/T(2)
      VC(3)=TWOT+TWOT
      IF(NV.LT.NCF) THEN
        DO 4 I=NV+1,NCF
        VC(I)=TWOT*VC(I-1)+PC(I-1)+PC(I-1)-VC(I-2)
    4   CONTINUE
        NV=NCF
      ENDIF
C
C       INTERPOLATE TO GET VELOCITY FOR EACH COMPONENT
C
      DO 5 I=1,NCM
      PV(I,2)=0.D0
      DO 6 J=NCF,2,-1
      PV(I,2)=PV(I,2)+VC(J)*BUF(J,I,L)
    6 CONTINUE
      PV(I,2)=PV(I,2)*VFAC
    5 CONTINUE
C
      RETURN
C
      END

******************************************************************
*
      subroutine astromrates(yr,mon,day,rh,rm,rss,sign,dd,dm,ds,
     &                       aaa,bbb,lc)
*
******************************************************************

       real ggk,drad,pi
       real aaa,bbb,lcd,bcd,rate,rac,declc
       real ws,a,e,M,L,EA,x,y,rs,vs,lon,z,xequats
       real yequats,zequats,RAs,decls,ra1,dec1,ee,sbeta1
       real beta1,bcs,xx1,yy1,zz1,lc,lcs,lc2,dddd
       double precision day,rss,ds 
       integer yr,mon,rh,rm,dd,dm
       character sign

       ggk = 0.01720209895
       pi  = 3.14159265358979323846
       drad = pi/180.0D0

         dddd = 367*yr-(7*(yr+((mon+9)/12)))/4+(275*mon)/9+day-730530 

         rac = ((((rss/60)+rm)/60)+rh)*15.0D0

         if (sign .EQ. '+') then

           dd = dd

         else if (sign .EQ. '-') then

           dd = dd * (-1)

         else

           dd = dd

         end if
 
         if (dd .GE. 0.0D0 .AND. sign .EQ. '+') then

           declc = (((ds/60)+dm)/60)+dd

         else if (dd .EQ. 0 .AND. sign .EQ. '-') then

           declc = dd-(((ds/60)+dm)/60)

         else

           declc = dd-(((ds/60)+dm)/60)

         end if

* Getting the Sun's position

      ws = 282.9404 + 4.70935D-5 * dddd 
      ws = REV(ws)
      a = 1.000000D0
      e = 0.016709 - 1.151D-9 * dddd
      M = 356.0470 + 0.9856002585 * dddd
      M = REV(M)

* Getting obliquity of ecliptic

      oblecl = 23.4393 - 3.563D-7 * dddd

* Getting Sun's mean longitude

      L = ws + M
      L = REV(L)

* Getting eccentric anomaly

      EA = M+(180/pi)*e*sin(M*drad)*(1+e*cos(M*drad))

* Getting Sun's rectangular coordinates in plane of ecliptic

      x = cos(EA*drad) - e
      y = sin(EA*drad) * sqrt(1 - e*e)

* Get distance and true anomaly
 
      rs = sqrt(x*x + y*y)
      vs = atan2( y, x )
      vs = vs * (180.0D0/PI)

* Get longitude of sun

      lon = vs + ws
      lon = REV(lon)

* Compute Sun's ecliptic rectangular coordinates

      x = rs * cos(lon*drad)
      y = rs * sin(lon*drad)
      z = 0.0D0

      xequats = x
      yequats = y * cos(oblecl*drad) - z * sin(oblecl*drad)
      zequats = y * sin(oblecl*drad) + z * cos(oblecl*drad)

* Compute RA and DEC of Sun

      RAs = atan2(yequats,xequats)
      RAs = RAs * (180.0D0/PI)
      RAs = rev(RAs)
   
      decls = asin(zequats/rs)
      decls = decls * (180.0D0/PI)

* Compute Sun's ecliptic coords

      ra1 = ras * drad
      dec1 = decls * drad
      ee = oblecl * drad
      sbeta1 = cos(ee)*sin(dec1) - sin(ee)*cos(dec1)*sin(ra1)
      beta1 = Asin(sbeta1)
      bcs = beta1*180/PI
      xx1 = cos(dec1)*cos(ra1)
      yy1 = cos(ee)*cos(dec1)*sin(ra1) + sin(ee)*sin(dec1)
      zz1 = ATAN2(yy1,xx1)
      if (zz1 .lt. 0) then
         zz1= zz1+ 2*PI
      else
         zz1 = zz1
      endif
      lcs = zz1*(180/PI)
      lcs = rev(lcs)


* Compute Asteroid's ecliptic coords

      ra1 = rac * drad
      dec1 = declc * drad
      ee = oblecl * drad
      sbeta1 = cos(ee)*sin(dec1) - sin(ee)*cos(dec1)*sin(ra1) 
      beta1 = Asin(sbeta1)
      bc = beta1*180/PI
      xx1 = cos(dec1)*cos(ra1)
      yy1 = cos(ee)*cos(dec1)*sin(ra1) + sin(ee)*sin(dec1)
      zz1 = ATAN2(yy1,xx1)
      if (zz1 .lt. 0) then
         zz1= zz1+ 2*PI
      else
         zz1 = zz1
      endif
      lc = zz1*(180/PI)

      bbb = bc
      aaa = lcs - lc

      if (aaa .GT. 180.0D0) then
         aaa = (lcs - 360.0D0) - lc
      end if
  
      if (aaa .LT. -180.0D0) then
         aaa = (lcs + 360.0D0) - lc 
      end if

      end

**************************************************************
* FUNCTIONS *
**************************************************************

* Functions for various trig stuff

      FUNCTION SIND(X)
      PARAMETER(RADEG=57.2957795130823)
      SIND = SIN( X * (1.0/RADEG) )
      END

      FUNCTION COSD(X)
      PARAMETER(RADEG=57.2957795130823)
      COSD = COS( X * (1.0/RADEG) )
      END

      FUNCTION TAND(X)
      PARAMETER(RADEG=57.2957795130823)
      TAND = TAN( X * (1.0/RADEG) )
      END

      FUNCTION ATAND(X)
      PARAMETER(RADEG=57.2957795130823)
      ATAND = RADEG * ATAN(X)
      END

      FUNCTION ASIND(X)
      PARAMETER(RADEG=57.2957795130823)
      ASIND = RADEG * ASIN(X)
      END

      FUNCTION ACOSD(X)
      PARAMETER(RADEG=57.2957795130823)
      ACOSD = RADEG * ACOS(X)
      END

      FUNCTION ATAN2D(Y,X)
      PARAMETER(RADEG=57.2957795130823)
      ATAN2D = RADEG * ATAN2(Y,X)
      END

* Cubic root

      FUNCTION CBRT(X)
      IF (X.GE.0.0) THEN
        CBRT = X ** (1.0/3.0)
      ELSE
        CBRT = -((-X)**(1.0/3.0))
      ENDIF
      END

* Normalizing angles to the 0-360 range

      FUNCTION REV(X)
      REV = X - AINT(X/360.0)*360.0
      IF (REV.LT.0.0)  REV = REV + 360.0
      END

