C
C Digest2
C
C Copyright (c) 2005 Kyle Smalley, Carl Hergenrother, Robert McNaught,
C David Asher
C
C Permission is hereby granted, free of charge, to any person obtaining
C a copy of this software and associated documentation files (the
C "Software"), to deal in the Software without restriction, including
C without limitation the rights to use, copy, modify, merge, publish,
C distribute, sublicense, and/or sell copies of the Software, and to
C permit persons to whom the Software is furnished to do so, subject
C to the following conditions:
C
C The above copyright notice and this permission notice shall be
C included in all copies or substantial portions of the Software.
C
C THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
C EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
C MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
C IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
C CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
C TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
C SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
*       lines are Hergenrother/Smalley.
******************************************************************

      IMPLICIT NONE

      common /cmsg/ lmessages
      logical lmessages

      REAL*8 DAY,E,A
      real*8 DT,R
      REAL*8 RA,N,I,XS,YS,ZS,ELONG,PSI,K
      REAL*8 M1,TH
      real*8 mb_count,neo_count
      real*8 score
      REAL*8 LONG,DXY,DZ
      REAL*8 RD,RSUN
      REAL*8 EE(2,3),DD(0:2,3),DE,T(2)
      REAL*8 O(3),V(3),D1,D2,TZ,DP,AA,BB,CC,U,SA,CA,ANG(2),AN
      REAL*8 MAGOBS(2),HMAG,G
      REAL*8 OBS(0:1999,3),ET
      INTEGER YEAR,MONTH,NUMBER
      integer obsx,ocindex
      character*3 OBSCODE
      INTEGER II
      real h(6:30,0:17,0:4,0:23)
      integer az,ez,nz
      integer I5
      integer year8,year9,month8,month9,rahr8,rahr9,ramin8,ramin9
      integer deg8,deg9,decmin8,decmin9
      character*3 obscode8,obscode9
      double precision rasec8,rasec9,decsec8,decsec9,day8,day9
      real magn8,magn9
      real dddd1,dddd2,aaa1,aaa2,bbb1,bbb2,rate,bcd,lcd
      real pi,drad,lc1,lc2,magobs2

      character*13 desig8,desig9
      character    sign8,sign9,magtype8,magtype9
      CHARACTER    DESIG*7,OBSN*80,neoflag*3
      character*1  MAGTYPE(2),CDUM1(3)
      CHARACTER*99 INPUTFILE
      character*80 hold(2)
      character*40 configline
      character*80 msgbuf

      integer iargc
      integer hz
      integer iostat32
      integer iostat34
      logical unkn
      logical lheadings
      logical lneoflag

c Variables used for debugging
c     integer ieeer, ieee_handler, fph

c------------------------------------------------

* Format statement for debug output

*59   FORMAT(1X,F5.3,1X,F5.1,1X,F4.0,1X,F6.3,1X,F6.3,1X,
*    /       F7.3,1X,F7.3,1X,F7.3,1X,F6.3)

* Format statement for reading in asteroid population

 102  format(15X,25(1X,F13.2))

* Format statement for reading and writing MPC format astrometry

 120  FORMAT (A12,3X,I4,1X,I2,1X,F8.5,1X,I2,1X,I2,1X,F5.2,1X,
     &        A1,I2,1X,I2,1X,F4.1,10X,F4.1,1X,A1,6X,A3)

* Format statement for writing output

 122  format(i6,1x,a12,3x,F5.1,3x,a3,3x,F6.1,1X,F5.1,1X,F7.3,1X,F7.3,
     &       1X,F7.3,2X,F4.1)

* Format statement for writing column header for output

 123  format('     #      Design    Score   NEO?   Elong  Elat  ElongR
     & ElatR  TotalR  VMag')

* Skipped single positions

 124  format(i6,1x,a12,'   Single position.  Skipped.')

c------------------------------------------------

      i5 = 0
      G=0.15
      K=0.01720209895
      RD=57.2957795131
      pi  = 3.14159265358979323846
      drad = pi/180.0D0

c     ieeer = ieee_handler('set', 'common', fph)

      lheadings = .true.
      lmessages = .true.
      lneoflag = .true.
      open(32,file='.digest2',status='old',iostat=iostat32)
      if (iostat32 .eq. 0) then
 100        read(32,'(a)',end=101) configline
            if (configline(1:8) .eq. 'headings' .and.
     &          configline(10:11) .ne. 'on') then
               lheadings = .false.
            endif
            if (configline(1:8) .eq. 'messages' .and.
     &          configline(10:11) .ne. 'on') then
               lmessages = .false.
            endif
            if (configline(1:7) .eq. 'neoflag' .and.
     &          configline(9:10) .ne. 'on') then
               lneoflag = .false.
            endif
            goto 100
 101     close(32)
      endif

      inquire(file='AST.UNKN.POP',exist=unkn)
      if (unkn) then
         open(32,file='AST.UNKN.POP',status='old')
         call msg('Unknown population.')
      else
         open(32,file='AST.BIAS.POP',status='old')
         call msg('Complete population.')
      endif

* Look for obs file on command line

      if (iargc() .gt. 0) then
         call getarg(1, inputfile)
      elseif (lmessages) then

* Ask user for file containing asteroid photometry

         PRINT *, 'INPUTFILE (J2000 OBSERVATIONS)'
         READ '(A)', INPUTFILE
      else
         print *,'No data file specified.'
         stop
      endif

      open(34,file=inputfile,status='old')

* Read asteroid population into array

      do az = 0,23
         do ez = 0,4
            do nz = 0,17
               read(32,102) (h(hz,nz,ez,az),hz=6,30)
            enddo
         enddo
      enddo

* Calls Observatory subroutine which extracts observatory topocentric params

      CALL OBSERVATORY(OBS)

* Write column header to output

      if (lheadings) write(*,123) 

* Start loop to read in astrometry, produce orbital solutions,
* determine probabilities and write the output to the terminal

* Major loops go three levels deep.  701 iterates over objects in input
* file, 801 varies distance, 901 varies angle.

 701  read(34,120,end=799) desig9,
     &   year9,month9,day9,rahr9,ramin9,rasec9,
     &   sign9,deg9,decmin9,decsec9,magn9,
     &   magtype9,obscode9

 702     write(hold(1),120) desig9,
     &      year9,month9,day9,rahr9,ramin9,rasec9,
     &      sign9,deg9,decmin9,decsec9,magn9,
     &      magtype9,obscode9   

         i5 = i5 + 1

         dddd1 = day9

         call astromrates(year9,month9,day9,rahr9,ramin9,rasec9,
     &      sign9,deg9,decmin9,decsec9,aaa1,bbb1,lc1)

 703     read(34,120,end=799) desig8,
     &      year8,month8,day8,rahr8,ramin8,rasec8,
     &      sign8,deg8,decmin8,decsec8,magn8,
     &      magtype8,obscode8

         if (desig8 .ne. desig9) then
            write (msgbuf,124) i5,desig9
            call msg(msgbuf)

            desig9 = desig8
            year9 = year8
            month9 = month8
            day9 = day8
            rahr9 = rahr8
            ramin9 = ramin8
            rasec9 = rasec8
            sign9 = sign8
            deg9 = deg8
            decmin9 = decmin8
            decsec9 = decsec8
            magn9 = magn8
            magtype9 = magtype8
            obscode9 = obscode8

            goto 702
         endif

 704  read(34,120,end=710,iostat=iostat34) desig9,
     &   year9,month9,day9,rahr9,ramin9,rasec9,
     &   sign9,deg9,decmin9,decsec9,magn9,
     &   magtype9,obscode9

         if (desig9 .ne. desig8) goto 710

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

         goto 704

 710  write(hold(2),120) desig8,
     &   year8,month8,day8,rahr8,ramin8,rasec8,
     &   sign8,deg8,decmin8,decsec8,magn8,
     &   magtype8,obscode8

      dddd2 = day8

      call astromrates(year8,month8,day8,rahr8,ramin8,rasec8,
     &      sign8,deg8,decmin8,decsec8,aaa2,bbb2,lc2)

      DO II=1,2

         READ (hold(II), '(A)') OBSN
         CALL READOBS2000(OBSN,NUMBER,DESIG,
     $      CDUM1(1),CDUM1(2),CDUM1(3),YEAR,MONTH,DAY,
     $      RA,DE,MAGOBS(II),MAGTYPE(II),OBSCODE)

         if (ii .eq. 2) then
            if (magobs(1) .ge. 1 .and. magobs(2) .ge. 1) then
               magobs2 = (magobs(1) + magobs(2)) * 0.5
            else if (magobs(1) .le. 1) then
               magobs2 = magobs(2)
            else if (magobs(2) .le. 1) then
               magobs2 = magobs(1)
            else if (magobs(1) .le. 1 .and.  magobs(2) .le. 1) then
               magobs2 = 19.0 
            end if
         end if

         if (magtype(2) .eq. 'B' .or. magtype(2) .eq. ' ') then
            magobs2 = magobs2 - 0.8
         else if (magtype(2) .eq. 'R') then
            magobs2 = magobs2 + 0.4
         else
            magobs2 = magobs2
         end if

         CALL JDATE(YEAR,MONTH,DAY,T(II))
         ! sloppy
         ET = 7.5d-4
         T(II)=T(II)+ET

         obsx = ocindex(obscode)
         LONG=OBS(obsx,1)/360
         DXY =OBS(obsx,2)
         DZ  =OBS(obsx,3)

         CALL SE2000 (T(II),XS,YS,ZS)
         CALL LST(T(II)-ET,LONG,TH)
         EE(II,1)=-(XS+DXY*COS(TH)*1E-7)
         EE(II,2)=-(YS+DXY*SIN(TH)*1E-7)
         EE(II,3)=-(ZS+DZ*1E-7)

         DD(II,1)=COS(RA)*COS(DE)
         DD(II,2)=SIN(RA)*COS(DE)
         DD(II,3)=SIN(DE)

      enddo

C CALCULATE POSITION AND VELOCITY VECTOR OF OBJECT

      DT=T(2)-T(1)

      mb_count = 0.0D0
      neo_count = 0.0D0

      D1=0.0
 801  D1=D1+.025
      if (d1 .gt. 7.0) goto 899

      O(1)=EE(1,1)+D1*DD(1,1)
      DD(0,1)=O(1)-EE(2,1)
      O(2)=EE(1,2)+D1*DD(1,2)
      DD(0,2)=O(2)-EE(2,2)
      O(3)=EE(1,3)+D1*DD(1,3)
      DD(0,3)=O(3)-EE(2,3)

      DP=SQRT(DD(0,1)**2+DD(0,2)**2+DD(0,3)**2)
      R=SQRT(O(1)**2+O(2)**2+O(3)**2)
      rsun=sqrt(ee(1,1)**2+ee(1,2)**2+ee(1,3)**2)

      CALL MAG(rsun,R,D1,0D0,G,ELONG,PSI,M1)
      HMAG=MAGOBS(1)-M1
      IF (MAGTYPE(1) .EQ. 'B') HMAG=HMAG-0.8
      if (magtype(1) .eq. 'R') hmag=hmag+0.4

      TH=(DD(0,1)*DD(2,1)+DD(0,2)*DD(2,2)+DD(0,3)*DD(2,3))/DP
      tz = acos(th)

      U=2.95912208E-4
      AA=1/(DT**2)
      BB=(-2*DP*TH)/(DT**2)
      CC=DP**2/DT**2-2*U/R

      if (BB*BB-4*AA*CC .le. 0) goto 801

C For 1st parabloic solution

      D2=(-BB-SQRT(BB*BB-4*AA*CC))/(2*AA)
      N=SQRT(D2*D2+DP*DP-2*D2*DP*COS(TZ))
      CA=(N*N+DP*DP-D2*D2)/(2*N*DP)
      SA=D2*SIN(TZ)/N
      ang(1)=atan2(sa,ca)*rd

C For 2nd parabloic solution

      D2=(-BB+SQRT(BB*BB-4*AA*CC))/(2*AA)
      N=SQRT(D2*D2+DP*DP-2*D2*DP*COS(TZ))
      CA=(N*N+DP*DP-D2*D2)/(2*N*DP)
      SA=D2*SIN(TZ)/N
      ang(2)=atan2(sa,ca)*rd

      if (ang(1) .lt. ang(2)) then
         an = ang(1)
      else
         an = ang(2)
         ang(2) = ang(1)
      endif

 901  D2=SIN((180-AN)/RD-TZ)
      if (d2 .eq. 0d0) goto 998
      D2=DP*SIN(AN/RD)/D2

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

      CALL METEORORBIT(T(1),O,V,A,E,I)

      IF (A.EQ.0d0) GOTO 998

      I=I*RD

********************************************************************
* Getting bias numbers from asteroid pops
********************************************************************

      if (e .lt. 1) then
         az = aint(4*a)
         if (az .gt. 23) az = 23

         ez = aint(e*5)
      else
         az = 23

         ez = 4
      endif

      nz = aint(i*.2)
      if (nz .gt. 17) nz = 17

      hz = nint(hmag)
      if (hz .lt. 6) then
         hz = 6
      elseif (hz .gt. 30) then
         hz = 30
      endif

      if (a*(1d0-e) .GE. 1.3D0 .AND. I .LE. 40D0 .AND. E .LT. .5D0) then
             mb_count = mb_count + h(hz,nz,ez,az)
      else
             neo_count = neo_count + h(hz,nz,ez,az)
      end if

 998  if (an .lt. ang(2)) then
         an = an + 2.0
         if (an .gt. ang(2)) an = ang(2)
         goto 901
      endif
 
 999  goto 801

 899  if (neo_count .LE. 0.95D0) then
         neo_count = 1.0D0
      end if

      score = (neo_count / (neo_count + mb_count))*100.0D0
      if (lneoflag .and. score .GE. 25) then
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
     &   -0.01D0 .AND. lcd .GE. -0.08D0) .AND. (bcd .LE. 0.02D0
     &   .AND. bcd .GE. -0.02D0)) then
         neoflag = 'OSS'
      end if

c     if (score .GE. 00.0D0) then
         write(msgbuf,122) i5,desig8,score,neoflag,aaa1,bbb1,
     &                lcd,bcd,rate,magobs2
         if (index(msgbuf,'*') .eq. 0) then
            write(*,'(a)') msgbuf
         else
            call msg(msgbuf)
         endif
c     end if

      if (iostat34 .ge. 0) goto 702

799   CLOSE(UNIT=9)

      END

********************************************************************
********************************************************************

c---------------------------

      integer function fph(sig, code, context)
      integer sig, code, context(5)
      call abort()
      fph = 0
      end

c---------------------------
      subroutine msg(text)
      implicit none
      common /cmsg/ lmessages
      logical lmessages

      character*(*) text

      if (lmessages) write(*,'(a)') text
      end

c---------------------------

      SUBROUTINE METEORORBIT(T1,O,VD,A,E,I)

C     T1=TIME AT POSITION O=(X,Y,Z) WITH VELOCITY VD=(XD,YD,ZD)
C        WITH (1950) EQUATORIAL COORDINATES
C     'A' IS IN AU
C     I IN RADIANS, EQUINOX 1950

*  Changed the value of EPS in the hope that this makes it work in J2000
*  instead of B1950   - DJA, 950320

      IMPLICIT NONE
      REAL*8 T1,X,Y,Z,XD,YD,ZD,A,E,I,H,HH,HX,HY,HZ,R
      REAL*8 U,P,C,V,CI,PI,PI2
      REAL*8 O(3),VD(3),EPS,RR,TH,VEL,RD

      A=0
      E=0
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
      th=atan2(z,y)
      Y=COS(TH-EPS)*RR
      Z=SIN(TH-EPS)*RR

      XD=VD(1)
      YD=VD(2)
      ZD=VD(3)

      VEL=SQRT(XD*XD+YD*YD+ZD*ZD)
      RR=SQRT(YD*YD+ZD*ZD)
      th=atan2(zd,yd)
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

58    CI=HZ/H
      i=acos(ci)
      IF (I.LT.0.0) I=PI+I

60    END

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

      integer function ocindex(oc3)
         character,intent(in) :: oc3*3
         if (llt(oc3,'A')) then
            read (oc3, '(i3)', iostat=iostatf) ocindex
         else
            read (oc3(2:3), '(i2)', iostat=iostatf) ocindex
            ocindex = (iachar(oc3(1:1))-55) * 100 + ocindex
         endif

         if (ocindex .gt. 1999 .or. ocindex .lt. 0 .or.
     &         iostatf .ne. 0) ocindex = 500
      end function

      subroutine observatory(obs)
         real(8),intent(out) :: obs(0:1999,3)

         ! crazy conversion factor for existing code =
         !    -1e7 scale factor * earth radius in m / 1 AU in m
         real(8),parameter :: c = -1e7*6378140.0/149597870000.0

         character oc3*3
         real(8) pc(3)
         integer iunit,ios,ocx,ocindex

         call opflrd('obscode.dat', iunit)
         do
            read (iunit,'(a3,x,f9.5,f8.6,f9.5)',iostat=ios) oc3,pc
            if (ios .ne. 0) exit
            ocx = ocindex(oc3)
            if (ocx .ne. 500) then
               obs(ocx,1) = pc(1)
               obs(ocx,2) = pc(2)*c
               obs(ocx,3) = pc(3)*c
            endif
         end do
         close(iunit)
      end subroutine

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
*    OBSCODE  [character*3]
*
*  Last update 971222 (changed format X to 1X as some compilers require)
*-
      CHARACTER OBS*80,DESIG*7,DISC,COMMENT1,COMMENT2,SIGN,MAGTYPE,C5*5
      INTEGER YEAR,MONTH,RAHR,RAMIN,DEG,DECMIN
      character*3 OBSCODE
      DOUBLE PRECISION RA,DEC,DAY,RASEC,DECSEC,MAG,RD
      PARAMETER (RD=57.295779513082321D0)

      READ (OBS,920) C5,DESIG,DISC,COMMENT1,COMMENT2,
     / YEAR,MONTH,DAY, RAHR,RAMIN,RASEC, SIGN,DEG,DECMIN,DECSEC,
     / IM1,IM2,IM3,MAGTYPE, OBSCODE
*   Possible problems (depending on compiler) with trailing blanks:
      MAG=IM1+IM2/10D0+IM3/100D0

920   FORMAT (5A,
     / I4,I3,F10.7, I2,I3,F6.3, 1X,A,I2,I3,F5.2, 10X,I2,1X,2I1,A, 6X,A3)

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
      REAL*8 JDAY,DAY
      INTEGER Y,M,JD,YD,MD,C,D
      JD=367*Y-7*(Y+(M+9)/12)/4-3*((Y+(M-9)/7)/100+1)/4+275*M/9
     1+1721029
      JDAY=JD+DAY-0.5
      END
*+
*  J2000 solar ephemeris
*  ---------------------
*
*  Given:
*     JDE
*
*  Returned:
*     Geocentric x, y, z coords (equatorial J2000) of Sun in AU
*
*  SLALIB code and JPL code replaced with this simple
*  approximation, 19 Aug 2005, KES.
*
*  Approximate solar coordinates, per USNO, see
*  http://aa.usno.navy.mil/faq/docs/SunApprox.html.
*  Angles on that page converted to radains here
*  so that all math could be done in radians.
*-
      subroutine se2000(jd,x,y,z)
         implicit none
         real*8 jd,d,g,q,g2,l,r,e,x,y,z

         d = jd - 2451545d0
         g = 6.240058d0 + 1.720197d-2 * d
         q = 4.894933d0 + 1.720279d-2 * d
         g2 = g + g

! ecliptic longitude
         l = q + 3.342306d-2 * dsin(g) + 3.490659d-4 * dsin(g2)

! distance in AU
         r = 1.00014d0 - 1.671d-2 * dcos(g) - 1.4d-4 * dcos(g2)

! obliquity of ecliptic
         e = .409088d0 - 6.283d-9 * d

! equatorial coordinates
         x = r * dcos(l)
         y = r * dsin(l)
         z = y * dsin(e)
         y = y * dcos(e)
      end subroutine

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

******************************************************************
*
      subroutine astromrates(yr,mon,day,rh,rm,rss,sign,dd,dm,ds,
     &                       aaa,bbb,lc)
*
******************************************************************

       real ggk,drad,pi
       real aaa,bbb
c      real lcd,bcd,rate
       real rac,declc
       real ws,a,e,M,L,EA,x,y,rs,vs,lon,z,xequats
       real yequats,zequats,RAs,decls,ra1,dec1,ee,sbeta1
       real beta1,bcs,xx1,yy1,zz1,lc,lcs
c      real lc2
       real dddd
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


* Normalizing angles to the 0-360 range

      FUNCTION REV(X)
      REV = X - AINT(X/360.0)*360.0
      IF (REV.LT.0.0)  REV = REV + 360.0
      END

