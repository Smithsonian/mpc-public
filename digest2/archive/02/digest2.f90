!
! Digest2
!
! Copyright (c) 2005 Kyle Smalley, Carl Hergenrother, Robert McNaught,
! David Asher
!
! Permission is hereby granted, free of charge, to any person obtaining
! a copy of this software and associated documentation files (the
! "Software"), to deal in the Software without restriction, including
! without limitation the rights to use, copy, modify, merge, publish,
! distribute, sublicense, and/or sell copies of the Software, and to
! permit persons to whom the Software is furnished to do so, subject
! to the following conditions:
!
! The above copyright notice and this permission notice shall be
! included in all copies or substantial portions of the Software.
!
! THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
! EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
! MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
! IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
! CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
! TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
! SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

!=============================================================
! Note:  The term 'NEO' used within this program really means any object
! that the MPC would term 'unusual.' Currently that is not just q < 1.3
! (NEOs) but also objects with e > .5 or i > 40.  Code dependent on this
! definition is marked with the special comment word NEODEFSENSITIVE.

!=============================================================
! Module Hierarchy:
!    main program
!    mobject
!    mdistance
!    mangle
!    bins
!    morbit
!    mconfig,mconstants,mbxaei,msve
!
! modules are in reverse order so that the source will compile
! in a single pass

!====================================================================
module mconstants
   !pi constants
   real(8),parameter :: pi    = 3.14159265358979323846d0
   real(8),parameter :: pi2   = pi*2d0
   real(8),parameter :: drad  = pi/180d0
   real(8),parameter :: radd  = 180d0/pi

   !gravitational constants
   real(8),parameter :: k     = .01720209895d0
   real(8),parameter :: invk  = 1d0/k
   real(8),parameter :: u     = k*k

   !handy
   real(8),parameter :: inv60 = 1d0/60d0
end module

!=============================================================

module mconfig
   type tconfig
      logical binmulti
      logical headings
      logical messages
      logical neoflag
      real(8) flagscore
      logical utest
      real(8) dstep
      real(8) astep
   end type
   type(tconfig) config

contains
   subroutine helpconfig
      implicit none
      integer start,len

      ! config help text is right here with the code so that the two can
      ! be kept in sync more easily.  text defined with & for line breaks
      ! to keep it readable and not waste too much data or code space.

      character(len=*),parameter :: helptext = "&
&&&
&Configuration file name:  .digest2&&
&&&
&Options:&&
&&&
&   algorithm 02/01&&
&   headings on/off&&
&   messages on/off&&
&   neoflag on/off&&
&   flagscore <integer, 1 or 2 digits>&&
&   dstep <decimal number>&&
&   astep <decimal number>&&
&   utest off/on&&
&&&
&If an option is not present, it defaults to the first value listed&&
&above.  Default flagscore is 50 for algorithm=02 and 25 for&&
&algorithm=01.  Default dstep is .025 (unit is AU), default astep is 2&&
&(unit is degrees.)  Options and values must be lower case, must be&&
&flush left, and only a single space or = sign can be between the option&&
&and the value.  Anything invalid is ignored.  If configuration file is&&
&not present, default values are used for all options.&&
&&&
&See README for complete documentation.&"

      start = 1
      do
         len = index(helptext(start:),'&')
         if (len .eq. 0) then
            write (*,'(a)') helptext(start:)
            exit
         endif
         write (*,'(a)') helptext(start:start+len-2)
         start = start+len
      enddo
   end subroutine

   subroutine readconfig
      use mconstants
      implicit none
      integer iostatf,iostat32
      character*40 configline

      config%binmulti = .false.
      config%headings = .true.
      config%messages = .true.
      config%neoflag = .true.
      config%utest = .false.
      config%dstep = .025d0
      config%astep = 2d0
      config%flagscore = -1d0
      open(32,file='.digest2',status='old',iostat=iostat32)
      if (iostat32 .eq. 0) then
         do
            read(32,'(a)',iostat=iostat32) configline
            if (iostat32 .ne. 0) exit
            if (configline(1:9) .eq. 'algorithm' .and. &
                configline(11:12) .eq. '01') then
               config%binmulti = .true.
            endif
            if (configline(1:8) .eq. 'headings' .and. &
                configline(10:12) .eq. 'off') then
               config%headings = .false.
            endif
            if (configline(1:8) .eq. 'messages' .and. &
                configline(10:12) .eq. 'off') then
               config%messages = .false.
            endif
            if (configline(1:7) .eq. 'neoflag' .and. &
                configline(9:11) .eq. 'off') then
               config%neoflag = .false.
            endif
            if (configline(1:5) .eq. 'utest' .and. &
                configline(7:8) .eq. 'on') then
               config%utest = .true.
            endif
            if (configline(1:5) .eq. 'dstep') then
               read (configline(7:14),'(f8.0)',iostat=iostatf) config%dstep
               if (iostatf .ne. 0) config%dstep = .025d0
            endif
            if (configline(1:5) .eq. 'astep') then
               read (configline(7:14),'(f8.0)',iostat=iostatf) config%astep
               if (iostatf .ne. 0) config%astep = 2d0
            endif
            if (configline(1:9) .eq. 'flagscore') then
               read (configline(11:12),'(f2.0)',iostat=iostatf) config%flagscore
               if (iostatf .ne. 0) config%flagscore = -1
            endif
         end do
         close(32)
      endif
      if (config%flagscore .lt. 0d0) then
         if (config%binmulti) then
            config%flagscore = 25d0
         else
            config%flagscore = 50d0
         endif
      endif
      config%astep = config%astep*drad
   end subroutine
end module

!====================================================================
! bin index
!
! 4 dimensions, h and hc must be set together,
! h is used as a bin index,
! hc is h shifted to work as a string index where character strings
! are used to represent flags, hc=h-5
!
! a: 0..23
! e: 0..4
! i: 0..17
! h: 6..30
! hc: 1..25

module mbx
   type tbx
      integer a,e,i,h,hc
   end type
end module

!====================================================================
! state vector
!
! o is position
! v is velocity

module msv
   type tsv
      real(8) o(3)
      real(8) v(3)
      real(8) hmag 
   end type
end module

!=============================================================
! module represents a single orbit

module morbit
   use msv
   use mbx
   private

   !initializers
   public orbitreset
   public seto
   public setv

   !calculators
   public solveaei
   public solvehmag
   public orbitneo

   !accessors
   public orbitr
   public orbitbx

   public writeEls

   type(tsv)    sv      ! state vector.  independent.
   real(8)      rsq,ro  ! |sve%o| computed when sv%o is set
   real(8)      a,e,i   ! elements derived from sv by solveaei
   real(8)      d1      ! observer-object distance, stored by solvehmag
   type(tbx)    x       ! bin index values.  set by solveaei and solvehmag
   logical      ovalid,vvalid,aeivalid,hmagvalid

   ! work variables used by solveaei
   logical izero
   real(8) hv(3),hsq,hm,vsq,inva,ci,irad

contains
   subroutine writeEls()
      write (37,'(f0.3,",",f0.3,",",f0.2,",",f0.2)') a,e,i,sv%hmag
   end subroutine

   subroutine orbitreset()
      implicit none
      ovalid = .false.
      vvalid = .false.
      aeivalid = .false.
      hmagvalid = .false.
   end subroutine

   subroutine seto(po)
      implicit none
      real(8),intent(in) :: po(3)
      call orbitreset
      sv%o = po
      rsq=dot_product(po,po)
      ro=dsqrt(rsq)
      ovalid = .true.
   end subroutine

   subroutine setv(pv)
      use mconstants
      implicit none
      real(8),intent(in) :: pv(3)
      ! scale by gravitational constant
      sv%v = pv*invk
      vvalid = .true.
      aeivalid = .false.
   end subroutine

   subroutine solvehmag(dd1,d,vmag)
      implicit none
      real(8),intent(in) :: dd1(3),d,vmag
      real(8) rdelta,cospsi,tanhalf,phi1,phi2

      d1 = d

      rdelta = ro*d1
      cospsi = dot_product(sv%o,dd1)/rdelta
      if (cospsi .gt. -.9999d0) then
         tanhalf = dsqrt(1d0-cospsi*cospsi)/(1d0+cospsi)
         PHI1=dexp(-3.33d0*tanhalf**0.63d0)
         PHI2=dexp(-1.87d0*tanhalf**1.22d0)
         sv%hmag=vmag-5d0*dlog10(rdelta)+2.5d0*dlog10(.85d0*PHI1+.15d0*PHI2)
      else
         ! object is straight into the sun.  doesn't seem too likely,
         ! but anyway, this gives it a valid value.
         sv%hmag = 30d0 
      endif

      call solvehx
   end subroutine

   subroutine solvehx
      implicit none

      x%h = nint(sv%hmag)
      if (x%h .lt. 6) then
         x%h = 6
      elseif (x%h .gt. 30) then
         x%h = 30
      endif
      x%hc = x%h - 5

      hmagvalid = .true.
   end subroutine

   logical function solveaei()
      use mconstants
      implicit none
      real(8) temp

      if (.not. (ovalid .and. vvalid)) call oex('aei')

      ! momentum vector
      hv(1) = sv%o(2)*sv%v(3)-sv%o(3)*sv%v(2)
      hv(2) = sv%o(3)*sv%v(1)-sv%o(1)*sv%v(3)
      hv(3) = sv%o(1)*sv%v(2)-sv%o(2)*sv%v(1)
      hsq = dot_product(hv,hv)
      hm = dsqrt(hsq)

      ! solve for semi-major axis
      ! (and the inverse--it comes in handy)
      vsq = dot_product(sv%v,sv%v)
      temp = 2d0-ro*vsq
      ! stability test:  require a < 100
      if (ro .gt. temp*100d0) goto 99
      a = ro/temp
      inva = temp/ro

      ! solve for eccentricity
      ! (stability test on a (above) should keep result real)
      e = dsqrt(1d0-hsq*inva)
      ! stability test:  require e < .99
      if (e .gt. .99d0) goto 99

      ! solve for inclination.

      ! reliable check for i=0.  handles
      ! loss of precision in h computation.
      izero = hv(3) .ge. hm

      ! combination of stability tests on a and e (above) should
      ! ensure that h is well above zero.
      if (izero) then
         i = 0d0
      else
         ci = hv(3)/hm
         irad = dacos(ci)
         i = irad*radd
      endif

      x%a = int(4d0*a)
      if (x%a.gt.23) x%a=23
      x%e = int(e*5d0)
      x%i = int(i*.2d0)
      if (x%i.gt.17) x%i=17

      aeivalid = .true.
      solveaei = .true.
      return

99    aeivalid = .false.
      solveaei = .false.
   end function

   real(8) function orbitr()
      implicit none
      if (.not. ovalid) call oex('r')
      orbitr = ro
   end function

   type(tbx) function orbitbx()
      implicit none
      if (.not. (aeivalid .and. hmagvalid)) call oex('bx')
      orbitbx = x
   end function

   logical function orbitneo()
      implicit none
      if (.not. aeivalid) call oex('neo')
      !NEODEFSENSITIVE
      orbitneo = x%i .ge. 8 .or. e .ge. .5d0 .or. a*(1d0-e) .lt. 1.3d0
   end function

   subroutine oex(amsg)
      implicit none
      character(len=*) amsg
      call msg('orbit exception: '//amsg)
      stop
   end subroutine
end module

!=============================================================
module bins
   use msv
   private
   public readbins,settagsingle,clearalltags,cleardtags,initbintype
   public mergetags,neoscore,ctags,btags,ctagsnz,btagsnz,orbits
   public countmulti

   ! key for tags:
   !   ' ' = no orbit found for bin
   !   '+' = orbit found
   type tags
      character(25) tag(0:17,0:4,0:23)
   end type

   type(tags) alltags
   type(tags) dtags
   character bintype(0:17,0:4,0:23)

   real(8) pop(6:30,0:17,0:4,0:23)
   real(8) mb_count,neo_count
   integer orbits,ctags,btags,ctagsnz,btagsnz
   logical allneo

contains
   subroutine countmulti
      use mbx
      use morbit
      use mconfig
      implicit none
      type(tbx) x
      real(8) binpop

      x = orbitbx()
      binpop = pop(x%h,x%i,x%e,x%a)

      if (binpop .gt. 0d0) then
         if (orbitneo()) then
            neo_count = neo_count + binpop
         else
            mb_count = mb_count + binpop
         endif
      endif

      if (config%utest) then
         orbits = orbits + 1
         if (dtags%tag(x%i,x%e,x%a)(x%hc:x%hc) .eq. ' ') then
            dtags%tag(x%i,x%e,x%a)(x%hc:x%hc) = '+'
            if (alltags%tag(x%i,x%e,x%a)(x%hc:x%hc) .eq. ' ') then
               call writeEls
            endif
            ctags = ctags + 1
            if (binpop .gt. 0d0) ctagsnz = ctagsnz + 1
         endif
      endif
   end subroutine

   subroutine readbins
      implicit none
      integer a,e,i,h
      logical unkn
      inquire(file='AST.UNKN.POP',exist=unkn)

      if (unkn) then
         open(32,file='AST.UNKN.POP',status='old')
         call msg('Unknown population.')
      else
         open(32,file='AST.BIAS.POP',status='old')
         call msg('Complete population.')
      endif

      do a = 0,23
         do e = 0,4
            do i = 0,17
               read(32,'(15X,25(1X,F13.2))') (pop(h,i,e,a),h=6,30)
            enddo
         enddo
      enddo

      close (32)
   end subroutine

   logical function settagsingle()
      use mbx
      use morbit
      implicit none
      type(tbx) x

      orbits = orbits + 1
      x = orbitbx()

      settagsingle = dtags%tag(x%i,x%e,x%a)(x%hc:x%hc) .eq. ' '
      if (settagsingle) dtags%tag(x%i,x%e,x%a)(x%hc:x%hc) = '+'

      if (allneo) then
         if (.not. orbitneo()) allneo = .false.
      endif
   end function

   subroutine clearalltags
      implicit none
      alltags%tag = ' '
      neo_count = 0d0
      mb_count = 0d0
      orbits = 0
      ctags = 0
      btags = 0
      ctagsnz = 0
      btagsnz = 0
      allneo = .true.
   end subroutine

   subroutine cleardtags
      implicit none
      dtags%tag = ' '
   end subroutine

   ! NEODEFSENSITIVE (see note at top of file)
   subroutine initbintype
      implicit none
      integer a,e,i

      do a = 0,23
         do e = 0,4
            do i = 0,17
               if (e.gt.2 .or. i.gt.7 .or. (1+a)*(5-e).le.26) then
                  bintype(i,e,a) = 'n' !neo bin
               elseif (e.lt.2 .and. i.le.7 .and. a*(4-e).gt.26) then
                  bintype(i,e,a) = 'm' !main belt
               else
                  !both--bin contains both neo and main belt orbits
                  bintype(i,e,a) = 'b'
               endif
            enddo
         enddo
      enddo
   end subroutine

   integer function mergetags()
      use mconfig
      implicit none
      integer a,e,i,hc
      real(8) binpop

      mergetags = 0

      do a = 0,23
         do e = 0,4
            do i = 0,17
               if (dtags%tag(i,e,a) .ne. ' ' .and. &
                     dtags%tag(i,e,a) .ne. alltags%tag(i,e,a)) then
                  do hc = 1,25
                     if (dtags%tag(i,e,a)(hc:hc) .ne. ' ' .and. &
                           alltags%tag(i,e,a)(hc:hc) .eq. ' ') then

                        alltags%tag(i,e,a)(hc:hc) = '+'
                        mergetags = mergetags + 1
                        binpop = pop(hc+5,i,e,a)

                        if (binpop .gt. 0d0) then
                           if (bintype(i,e,a) .eq. 'n') then
                              neo_count = neo_count + binpop
                           elseif (bintype(i,e,a) .eq. 'm') then
                              mb_count = mb_count + binpop
                           endif
                        endif

                        if (config%utest) then
                           if (bintype(i,e,a) .eq. 'b') then
                              btags = btags + 1
                              if (binpop .gt. 0) btagsnz = btagsnz + 1
                           else
                              ctags = ctags + 1
                              if (binpop .gt. 0) ctagsnz = ctagsnz + 1
                           endif
                        endif
                     endif
                  enddo
               endif
            enddo
         enddo
      enddo
   end function

   real(8) function neoscore()
      use mconfig
      implicit none
      real(8) n
      n = max(1d0,neo_count)
      if (config%binmulti .or. allneo .or. mb_count .gt. 0d0) then
         neoscore = 100d0*n/(n+mb_count)
      else
         neoscore = 99.9d0
      endif
   end function

end module

!====================================================================
! (The following is all easily visualised by drawing a rough sketch)
! If i=1,2 is the obsn & j=1,2,3 the coord (ref frame ecliptic J2000)
! then T(i) is JDE
! EE(i,j) is vector Sun -> observer
! DD(i,j) is unit vector observer -> object (apparent; will subtract
!  light travel time from perihelion passage time)
! O(j) is Sun -> object at T(1)
! DD0(j) is observer at T(2) -> object at T(1)
! TZ is angle between object at T1 & T2 as viewed by observer at T2
! TH is cos(TZ), calculated using scalar product
! D2 is object-observer dist at T2, calculated using sine rule
! V(j) is velocity, assuming obsns are close enough in time that the
!  object's motion can be approximated as uniform
! Now use solveaei to calculate orbital elements from position & velocity
!====================================================================

module mangle
   private
   public solveangle

contains
   logical function solveangle(an,dp,tz,dd0,dd,invdt)
      use mconstants
      use morbit
      implicit none
      real(8),intent(in) :: an,dp,tz,dd0(3),dd(2,3),invdt
      real(8) d2

      D2=DP*dsin(AN)/dsin(pi-AN-TZ)
      call setv((d2*dd(2,:)-dd0)*invdt)
      solveangle = solveaei()
   end function
end module

!====================================================================
module mdistance
   private
   public gothedistance

   real(8) tz
   real(8) dd0(3),dd(2,3),invdt
   real(8) dp
   real(8) o(3)

contains
   ! return value = -1 means all solutions hyperbolic at this distance.
   ! otherwise, return value >= 0 indicates the number of new bins tagged
   integer function gothedistance(d1,ee,pdd,pdt,vmag)
      use bins
      use mconfig
      use morbit
      use mangle
      use mconstants
      implicit none
      real(8),intent(in) :: d1,ee(2,3),pdd(2,3),pdt,vmag

      real(8) ang(2),alower,aupper,an
      real(8) dd1(3)
      real(8) th
      real(8) aa,bb,cc
      real(8) d2,ca,sa
      real(8) nn,nns
      real(8) dps,dsc,sd,inv2aa,d2s

      gothedistance = -1

      dd = pdd
      invdt = 1d0/pdt
      dd1 = d1*dd(1,:)
      o = ee(1,:)+dd1
      call seto(o)
      dd0 = o-ee(2,:)
      dps = dot_product(dd0,dd0)
      dp = dsqrt(dps)

      call solvehmag(dd1,d1,vmag)

      th=dot_product(dd0,dd(2,:))/dp
      tz=dacos(th)

      AA=invdt*invdt
      BB=(-2d0*DP*TH)*aa
      CC=dps*aa-2d0*U/orbitr()
      dsc = BB*BB-4d0*AA*CC

      if (dsc .le. 0d0) then
         return
      endif

      ! more common subexpressions
      sd = dsqrt(dsc)
      inv2aa = .5d0/aa

      ! For 1st parabloic solution

      D2=(-BB-sd)*inv2aa
      d2s = d2*d2
      nns = d2s+dps-2d0*D2*DP*th
      NN=dsqrt(nns)
      CA=(nns+dps-d2s)/(2d0*NN*DP)
      SA=D2*dsin(TZ)/NN
      ANG(1)=2d0*datan2(SA,1d0+CA)

      ! For 2nd parabloic solution

      D2=(-BB+sd)*inv2aa
      d2s = d2*d2
      nns = d2s+dps-2d0*D2*DP*th
      NN=dsqrt(nns)
      CA=(nns+dps-d2s)/(2d0*NN*DP)
      SA=D2*dsin(TZ)/NN
      ANG(2)=2d0*datan2(SA,1d0+CA)

      if (ang(1) .lt. ang(2)) then
         alower = ang(1)
         aupper = ang(2)
      else
         alower = ang(2)
         aupper = ang(1)
      endif

      if (config%binmulti) then
         an = alower + config%astep * .5d0
         do
            if (an .ge. aupper) exit
            if (solveangle(an,dp,tz,dd0,dd,invdt)) then
               call countmulti
            endif
            an = an + config%astep
         enddo
      else
         call cleardtags
         call sweepvv(alower,aupper)
         gothedistance = mergetags()
      endif
   end function

   recursive subroutine sweepvv(ang1,ang2)
      use bins
      use mangle
      implicit none
      real(8),intent(in) :: ang1,ang2
      real(8) mid

      mid = (ang2+ang1)*.5d0
      if (solveangle(mid,dp,tz,dd0,dd,invdt)) then
         if (settagsingle()) then
            call sweepvv(ang1,mid)
            call sweepvv(mid,ang2)
            return
        endif
      endif
      ! (else)
      call sweepvi(ang1,mid)
      call sweepiv(mid,ang2)
   end subroutine

   recursive subroutine sweepvi(ang1,ang2)
      use bins
      use mangle
      use mconfig
      implicit none
      real(8),intent(in) :: ang1,ang2
      real(8) mid

      if (ang2-ang1 .lt. 1d-2) return
      mid = (ang2+ang1)*.5d0
      if (solveangle(mid,dp,tz,dd0,dd,invdt)) then
         if (settagsingle()) then
            call sweepvv(ang1,mid)
            call sweepvi(mid,ang2)
            return
         endif
      endif
      ! (else)
      call sweepvi(ang1,mid)
   end subroutine

   recursive subroutine sweepiv(ang1,ang2)
      use bins
      use mangle
      use mconfig
      implicit none
      real(8),intent(in) :: ang1,ang2
      real(8) mid

      if (ang2-ang1 .lt. 1d-2) return
      mid = (ang2+ang1)*.5d0
      if (solveangle(mid,dp,tz,dd0,dd,invdt)) then
         if (settagsingle()) then
            call sweepiv(ang1,mid)
            call sweepvv(mid,ang2)
            return
         endif
      endif
      ! (else)
      call sweepiv(mid,ang2)
   end subroutine
end module

!====================================================================
module mobject
   private
   public digestobject

   real(8) dt
   REAL(8) dd(2,3)
   REAL(8) ee(2,3)
   real(8) vmag
   real(8) soe,coe
   integer linenumber

contains
   subroutine digestobject(i5,hold,obs,aaa1,bbb1,bbb2,dddd1,dddd2,lc1,lc2)
      use mconfig
      use mconstants
      use msv
      use morbit
      use bins
      implicit none

      integer,intent(in)      :: i5
      character*80,intent(in) :: hold(2)
      REAL(8),intent(in)      :: OBS(0:1999,3)
      real(8),intent(in)      :: aaa1,bbb1,bbb2,dddd1,dddd2,lc1,lc2

      CHARACTER     DESIG*7,neoflag*3
      character*1   MAGTYPE(2)
      character*80  msgbuf

      integer ii
      INTEGER YEAR,MONTH
      character*3 OBSCODE

      REAL(8) DAY
      real(8) ra,de
      REAL(8) MAGOBS(2)
      REAL(8) T(2)
      REAL(8) TH
      REAL(8) LONG,DXY,DZ
      real(8) et
      real(8) score
      real(8) rate,bcd,lcd
      real(8) ec(3)
      integer obsx,ocindex

      linenumber = i5

      DO II=1,2
         CALL READOBS2000(hold(ii),DESIG,YEAR,MONTH,DAY,&
            RA,DE,MAGOBS(II),MAGTYPE(II),OBSCODE)

         CALL JDATE(YEAR,MONTH,DAY,T(II))
         ! sloppy
         ET = 7.5d-4
         T(II)=T(II)+ET

         obsx = ocindex(obscode)
         LONG=OBS(obsx,1)
         DXY =OBS(obsx,2)
         DZ  =OBS(obsx,3)

         CALL se2000 (T(II),ec)
         CALL LST(T(II)-ET,LONG,TH)

         ! store sun-observer vector in ecliptic coordinates
         ee(ii,:)=rotate((/dxy*dcos(th),dxy*dsin(th),dz/)-ec)

         ! store observer-object unit vectors in ecliptic coordinates
         dd(ii,:)=rotate((/dcos(ra)*dcos(de),dsin(ra)*dcos(de),dsin(de)/))
      enddo

      DT=T(2)-T(1)
      vmag = magobs(2)
      call clearalltags

      if (config%binmulti) then
         call digestmulti
      else
         call digestsingle
      endif

      score = neoscore()

      if (config%neoflag .and. score .GE. config%flagscore) then
         neoflag = 'NEO'
      else
         neoflag = '   '
      end if

      lcd = (lc2 - lc1)/(dddd2 - dddd1)

      if (lcd .GE. 180d0) then
         lcd = lcd - 360D0
      else if (lcd .LE. -180d0) then
         lcd = lcd + 360D0
      else
         lcd = lcd
      end if

      bcd = (bbb2 - bbb1)/(dddd2 - dddd1)
      lcd = lcd * dcos(bbb1*drad)
      rate = dsqrt(bcd*bcd + lcd*lcd)

      write (msgbuf,'(i6,1x,a12,3x,F5.1,3x,a3,3x,&
         &F6.1,1X,F5.1,1X,F7.3,1X,F7.3,1X,F7.3,2X,F4.1)')&
         i5,desig,score,neoflag, aaa1,bbb1,lcd,bcd,rate,vmag

      if (index(msgbuf,'*') .eq. 0) then
         write(*,'(a)') msgbuf
      else
         call msg(msgbuf)
      endif

      if (config%utest) then
         if (config%binmulti) then
            write (36,'(i6,1x,a12,1x,i8,1x,i7,f9.1,a,i8,5x,f7.2,a)')&
               i5,desig,orbits,ctags,100d0*ctags/max(orbits,1),'% ',&
               ctagsnz,100d0*ctagsnz/max(ctags,1),'%'
         else
            write (36,'(i6,1x,a12,i9,i8,i8,i7,i11)')&
               i5,desig,orbits,ctags+btags,ctags+btags-ctagsnz-btagsnz,&
               btagsnz,ctagsnz
         endif
      endif
   end subroutine

   subroutine digestmulti
      use bins
      use mconfig
      use mdistance
      implicit none
      integer z !dummy
      real(8) d1
      call cleardtags
      d1 = .05d0
      do
         z = gothedistance(d1,ee,dd,dt,vmag)
         if (d1 .ge. 7d0) exit
         d1 = d1 + config%dstep
      end do
   end subroutine

   subroutine digestsingle
      use mconstants
      use bins
      use mdistance
      implicit none

      if (gothedistance(7d0,ee,dd,dt,vmag) .gt. 0) then
         call rangeiv(.05d0,7d0)
      else
         call rangeii(.05d0,7d0)
      endif
   end subroutine

!=============================================================
!+
!  J2000 solar ephemeris
!  ---------------------
!
!  Given:
!     JDE
!
!  Returned:
!     Geocentric Sun-Earth vector (equatorial J2000) in AU
!
!  Approximate solar coordinates, per USNO, see
!  http://aa.usno.navy.mil/faq/docs/SunApprox.html.
!  Angles on that page converted to radains here
!  so that all math could be done in radians.
!-
   subroutine se2000(jd,ec)
      implicit none
      real*8,intent(in)  :: jd
      real*8,intent(out) :: ec(3)
      real*8 d,g,q,g2,l,r,e

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
      soe = dsin(e)
      coe = dcos(e)

! equatorial coordinates
      ec(1) = r * dcos(l)
      ec(2) = r * dsin(l)
      ec(3) = ec(2) * soe
      ec(2) = ec(2) * coe
   end subroutine

   ! a little fast and loose--soe and coe are set in se2000
   pure function rotate(c)
      implicit none
      real(8),intent(in) :: c(3)
      real(8) rotate(3)
      rotate=(/c(1),c(3)*soe+c(2)*coe,c(3)*coe-c(2)*soe/)
   end function

   ! ii stands for invalid-invalid, meaning don't look for solutions
   ! at either the inner or outer distance.  just try to find somthing
   ! inbetween.
   !
   ! "invalid" can mean no solutions were possible (ie, all were hyperbolic)
   ! or it can mean that no new bins were discovered (ie, searches at similar
   ! distances have already mined out all the bins.)  either way, it means
   ! don't search any further in this direction.
   recursive subroutine rangeii(inner, outer)
      use bins
      use mdistance
      implicit none
      real(8),intent(in) :: inner,outer
      real(8) middle

      middle = inner + (outer-inner)*.7D0
      if (gothedistance(middle,ee,dd,dt,vmag) .ge. 0) then
         call rangeiv(inner,middle)
         call rangevi(middle,outer)
      else if ((middle-inner)*30d0 .gt. middle) then
         call rangeii(inner,middle)
      end if
   end subroutine

   ! iv stands for invalid-valid, meaning look for solutions near
   ! the outer distance.
   recursive subroutine rangeiv(inner, outer)
      use bins
      use mdistance
      implicit none
      real(8),intent(in) :: inner,outer
      real(8) middle
      integer newtags

      middle = (inner+outer)*.5D0
      newtags = gothedistance(middle,ee,dd,dt,vmag)
      if (newtags .gt. 0) then
         call rangeiv(inner,middle)
         call rangevv(middle,outer)
      endif
   end subroutine

   ! vi stands for valid-invalid, meaning look for solutions near
   ! the inner distance
   recursive subroutine rangevi(inner, outer)
      use bins
      use mdistance
      implicit none
      real(8),intent(in) :: inner,outer
      real(8) middle
      integer newtags

      middle = (inner+outer)*.5D0
      newtags = gothedistance(middle,ee,dd,dt,vmag)
      if (newtags .gt. 0) then
         call rangevv(inner,middle)
         call rangevi(middle,outer)
      else if (newtags .lt. 0 .and. (middle-inner)*30d0 .gt. middle) then
         call rangevi(inner,middle)
      endif
   end subroutine

   recursive subroutine rangevv(inner, outer)
      use bins
      use mdistance
      implicit none
      real(8),intent(in) :: inner,outer
      real(8) middle
      integer newtags

      middle = (inner+outer)*.5D0
      newtags = gothedistance(middle,ee,dd,dt,vmag)
      if (newtags .gt. 0) then
         call rangevv(inner,middle)
         call rangevv(middle,outer)
      else if (newtags .lt. 0) then
         call rangevi(inner,middle)
         call rangeiv(middle,outer)
      endif
   end subroutine
end module

!=============================================================
program digest2
   use mconstants
   use mconfig
   use morbit
   use bins
   use mobject
   implicit none

   CHARACTER*99 INPUTFILE
   character*13 desig8,desig9
   character    sign8,sign9,magtype8,magtype9
   character*80 hold(2)
   character*80 msgbuf

   integer iargc
   integer iostat34
   integer i5
   integer year8,year9,month8,month9,rahr8,rahr9,ramin8,ramin9
   integer deg8,deg9,decmin8,decmin9
   character*3 obscode8,obscode9
!  integer ieeer, ieee_handler, fph  ! Variables used for debugging
   integer magcount
   integer obscount

   real(8) magn8,magn9
   real(8) dddd1,dddd2,aaa1,aaa2,bbb1,bbb2
   real(8) lc1,lc2
   real(8) rasec8,rasec9,decsec8,decsec9,day8,day9
   REAL(8) OBS(0:1999,3)
   real(8) magsum

!----------------------------------------------------

! Format statements for reading and writing MPC format astrometry

 120  FORMAT (A12,3X,I4,1X,I2,1X,F8.5,1X,I2,1X,I2,1X,F5.2,1X,&
     &        A1,I2,1X,I2,1X,F4.1,10X,F4.1,1X,A1,6X,a3)

 121  FORMAT (A12,3X,I4,1X,I2,1X,F8.0,1X,I2,1X,I2,1X,F5.0,1X,&
     &        A1,I2,1X,I2,1X,F4.0,10X,F4.0,1X,A1,6X,a3)

!----------------------------------------------------

!  ieeer = ieee_handler('set', 'common', fph)

!----------------------------------------------------

   call readconfig

!----------------------------------------------------
   if (config%utest) then
      open(36,file='utest.out',status='replace')
      if (config%binmulti) then
         write (36,*) 'dstep = ',config%dstep
         write (36,*) 'astep = ',config%astep*radd
         write (36,'(a)') '                     Orbits     Unique &
     & % of       Non-empty  % of'
         write (36,'(a)') '     #      Desig.   generated  bins   &
     & generated  bins       unique'
      else
         write (36,'(a)') '                                       &
     &        Non-empty  Non-empty'
         write (36,'(a)') '                     Orbits     Unique &
     & Empty  border     counted'
         write (36,'(a)') '     #      Desig.   generated  bins   &
     & bins   bins       bins'
      endif
      open(37,file='utest.els',status='replace')
      write(37,*) 'a,e,i,H'
   endif

! Look for obs file on command line

   if (iargc() .gt. 0) then
      call getarg(1, inputfile)
   elseif (config%messages) then

! Ask user for file containing asteroid photometry

      PRINT *, 'INPUTFILE (J2000 OBSERVATIONS)'
      READ '(A)', INPUTFILE
   else

! Let's leave this as a print rather than a msg().  If the user has
! the config option set to no messages but he's really clueless, then
! he'd get no output and wouldn't know why.

      print *,'No data file specified.'
      stop
   endif

   if (inputfile .eq. '-helpconfig') then
      call helpconfig
      stop
   endif

!----------------------------------------------------

   call orbitreset
   call readbins

!----------------------------------------------------
! Calls Observatory subroutine which extracts observatory topocentric params

   CALL OBSERVATORY(OBS)

   open(34,file=inputfile,status='old')

! Write column header to output

   if (config%headings) write(*,'(a)') &
      '     #      Desig.    Score   NEO?   Elong  Elat  ElongR&
      &   ElatR  TotalR  VMag'

! Start loop to read in astrometry, produce orbital solutions,
! determine probabilities and write the output to the terminal

   i5 = 0
   call initbintype

   read(34,121,end=799) desig9,&
      year9,month9,day9,rahr9,ramin9,rasec9,&
      sign9,deg9,decmin9,decsec9,magn9,&
      magtype9,obscode9

   do
      write(hold(1),120) desig9,&
         year9,month9,day9,rahr9,ramin9,rasec9,&
         sign9,deg9,decmin9,decsec9,magn9,&
         magtype9,obscode9

      i5 = i5 + 1
      dddd1 = day9
      obscount = 1

      call astromrates(year9,month9,day9,rahr9,ramin9,rasec9,&
         sign9,deg9,decmin9,decsec9,aaa1,bbb1,lc1)

      if (magn9 .gt. 1d0) then
         if (magtype9 .eq. 'R') then
            magn9 = magn9 + 0.4d0
         else if (magtype9 .eq. 'B' .or. magtype9 .eq. ' ') then
            magn9 = magn9 - 0.8d0
         end if
         magsum = magn9
         magcount = 1
      else
         magsum = 0
         magcount = 0
      endif

      read(34,121,end=799) desig8,&
         year8,month8,day8,rahr8,ramin8,rasec8,&
         sign8,deg8,decmin8,decsec8,magn8,&
         magtype8,obscode8

      if (desig8 .ne. desig9) then
         write (msgbuf,'(i4,3x,a12,a)') i5,desig9,&
            '   Single position.  Skipped.'
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

         cycle
      endif

      do
         obscount = obscount + 1

         if (magn8 .gt. 1d0) then
            if (magtype8 .eq. 'R') then
               magn8 = magn8 + 0.4d0
            else if (magtype8 .eq. 'B' .or. magtype8 .eq. ' ') then
               magn8 = magn8 - 0.8d0
            end if
            magsum = magsum + magn8
            magcount = magcount + 1
         endif

         read(34,121,iostat=iostat34) desig9,&
            year9,month9,day9,rahr9,ramin9,rasec9,&
            sign9,deg9,decmin9,decsec9,magn9,&
            magtype9,obscode9

         if (iostat34 .lt. 0 .or. desig9 .ne. desig8) exit

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
      enddo

      if (magcount .gt. 0) then
         magn8 = magsum/magcount
      else
         magn8 = 19d0
      endif
      magtype8 = 'V'

      write(hold(2),120) desig8,&
         year8,month8,day8,rahr8,ramin8,rasec8,&
         sign8,deg8,decmin8,decsec8,magn8,&
         magtype8,obscode8

      dddd2 = day8

      call astromrates(year8,month8,day8,rahr8,ramin8,rasec8,&
            sign8,deg8,decmin8,decsec8,aaa2,bbb2,lc2)

      call digestobject(i5,hold,obs,aaa1,bbb1,bbb2,dddd1,dddd2,lc1,lc2)

      if (iostat34 .lt. 0) exit
   enddo

 799 close(34)
   if (config%utest) then
      close(36)
      close(37)
   endif
end

!=============================================================
subroutine msg(text)
   use mconfig
   implicit none
   character*(*) text

   if (config%messages) write(*,'(a)') text
end

!=============================================================
   subroutine astromrates(yr,mon,day,rh,rm,rss,sign,dd,dm,ds,aaa,bbb,lc)
   use mconstants
   implicit none
       real(8) aaa,bbb
       real(8) rac,declc
       real(8) ws,e,M,L,EA,x,y,rs,vs,lon,z,xequats
       real(8) yequats,zequats,RAs,decls,ra1,dec1,ee,sbeta1
       real(8) beta1,xx1,yy1,zz1,lc,lcs
       real(8) dddd
       real(8) day,rss,ds
       integer yr,mon,rh,rm,dd,dm
       character sign
       real(8) oblecl
       real(8) bc

         dddd = 367*yr-(7*(yr+((mon+9)/12)))/4+(275*mon)/9+day-730530d0

         rac = ((((rss*inv60)+rm)*inv60)+rh)*15D0

         if (sign .EQ. '+') then

           dd = dd

         else if (sign .EQ. '-') then

           dd = dd * (-1)

         else

           dd = dd

         end if

         if (dd .GE. 0D0 .AND. sign .EQ. '+') then

           declc = (((ds*inv60)+dm)*inv60)+dd

         else if (dd .EQ. 0 .AND. sign .EQ. '-') then

           declc = dd-(((ds*inv60)+dm)*inv60)

         else

           declc = dd-(((ds*inv60)+dm)*inv60)

         end if

! Getting the Sun's position

      ws = 282.9404d0 + 4.70935D-5 * dddd
      ws = modulo(ws,360d0)
      e = 0.016709d0 - 1.151D-9 * dddd
      M = 356.0470d0 + 0.9856002585d0 * dddd
      M = modulo(M,360d0)

! Getting obliquity of ecliptic

      oblecl = 23.4393d0 - 3.563D-7 * dddd

! Getting Sun's mean longitude

      L = ws + M
      L = modulo(L,360d0)

! Getting eccentric anomaly

      EA = M+radd*e*dsin(M*drad)*(1+e*dcos(M*drad))

! Getting Sun's rectangular coordinates in plane of ecliptic

      x = dcos(EA*drad) - e
      y = dsin(EA*drad) * dsqrt(1d0 - e*e)

! Get distance and true anomaly

      rs = dsqrt(x*x + y*y)
      vs = datan2( y, x )
      vs = vs * radd

! Get longitude of sun

      lon = vs + ws
      lon = modulo(lon,360d0)

! Compute Sun's ecliptic rectangular coordinates

      x = rs * dcos(lon*drad)
      y = rs * dsin(lon*drad)
      z = 0D0

      xequats = x
      yequats = y * dcos(oblecl*drad) - z * dsin(oblecl*drad)
      zequats = y * dsin(oblecl*drad) + z * dcos(oblecl*drad)

! Compute RA and DEC of Sun

      RAs = datan2(yequats,xequats)
      RAs = RAs * radd
      RAs = modulo(RAs,360d0)

      decls = dasin(zequats/rs)
      decls = decls * radd

! Compute Sun's ecliptic coords

      ra1 = ras * drad
      dec1 = decls * drad
      ee = oblecl * drad
      sbeta1 = dcos(ee)*dsin(dec1) - dsin(ee)*dcos(dec1)*dsin(ra1)
      beta1 = dasin(sbeta1)
      xx1 = dcos(dec1)*dcos(ra1)
      yy1 = dcos(ee)*dcos(dec1)*dsin(ra1) + dsin(ee)*dsin(dec1)
      zz1 = datan2(yy1,xx1)
      if (zz1 .lt. 0d0) then
         zz1= zz1+pi2 
      else
         zz1 = zz1
      endif
      lcs = zz1*radd
      lcs = modulo(lcs,360d0)


! Compute Asteroid's ecliptic coords

      ra1 = rac * drad
      dec1 = declc * drad
      ee = oblecl * drad
      sbeta1 = dcos(ee)*dsin(dec1) - dsin(ee)*dcos(dec1)*dsin(ra1)
      beta1 = dasin(sbeta1)
      bc = beta1*radd
      xx1 = dcos(dec1)*dcos(ra1)
      yy1 = dcos(ee)*dcos(dec1)*dsin(ra1) + dsin(ee)*dsin(dec1)
      zz1 = datan2(yy1,xx1)
      if (zz1 .lt. 0d0) then
         zz1= zz1+pi2
      else
         zz1 = zz1
      endif
      lc = zz1*radd

      bbb = bc
      aaa = lcs - lc

      if (aaa .GT. 180D0) then
         aaa = (lcs - 360D0) - lc
      end if

      if (aaa .LT. -180D0) then
         aaa = (lcs + 360D0) - lc
      end if

      end

!=============================================================
!nteger function fph(sig, code, context)
!  implicit none
!  integer sig, code, context(5)
!  call abort()
!  fph = 0
!nd

!=============================================================
      SUBROUTINE JDATE(Y,M,DAY,JDAY)
   implicit none
      REAL(8) JDAY,DAY
      INTEGER Y,M,JD
      JD=367*Y-7*(Y+(M+9)/12)/4-3*((Y+(M-9)/7)/100+1)/4+275*M/9+1721029
      JDAY=JD+DAY-0.5
      END

!=============================================================
      SUBROUTINE LST(J,LONG,TH)
   IMPLICIT NONE
      real(8) J,J1,T,TH,UT,LONG

      T=(J-2415020d0)/36525d0

      TH=(6.6460656d0+2400.051262d0*T+0.00002581d0*T*T)/24d0

      J1=J-.5d0
      UT=(J1-INT(J1))

      TH=TH+UT+LONG
      TH=(TH-INT(TH))*6.28318530d0

      END

!=============================================================
      integer function ocindex(oc3)
         character,intent(in) :: oc3*3
         if (llt(oc3,'A')) then
            read (oc3, '(i3)', iostat=iostatf) ocindex
         else
            read (oc3(2:3), '(i2)', iostat=iostatf) ocindex
            ocindex = (iachar(oc3(1:1))-55) * 100 + ocindex
         endif

         if (ocindex .gt. 1999 .or. ocindex .lt. 0 .or. iostatf .ne. 0) then
            ocindex = 500
         endif
      end function

      subroutine observatory(obs)
         real(8),intent(out) :: obs(0:1999,3)

         ! units of rho sin/cos phi in obscode.dat are equatorial radii
         ! of the Earth.  convert to AU here for easier use later.
         ! also units of longitude are degrees.
         ! convert here to circles for easier use later.

         ! scale factor = earth radius in m / 1 AU in m
         real(8),parameter :: sf = 6.37814d6/149.59787d9

         character oc3*3
         real(8) pc(3)
         integer iunit,ios,ocx,ocindex

         call opflrd('obscode.dat', iunit)
         do
            read (iunit,'(a3,x,f9.5,f8.6,f9.5)',iostat=ios) oc3,pc
            if (ios .ne. 0) exit
            ocx = ocindex(oc3)
            if (ocx .ne. 500) then
               obs(ocx,1) = pc(1)/360d0
               obs(ocx,2) = pc(2)*sf
               obs(ocx,3) = pc(3)*sf
            endif
         end do
         close(iunit)
      end subroutine

!=============================================================
      SUBROUTINE OPFLRD (FLNM, IUNIT)
!+
!  FLNM should be the name of an existing file; then OPFLRD looks for
!  the 1st unopened unit numbered in the range 50-99, connects FLNM to
!  that unit for reading & returns the unit number.
!  Stops program execution if no unopened unit can be found.
!
!  960323:  Removed READONLY from OPEN statement (only needed on Vax)
!-
   implicit none
      CHARACTER FLNM*(*)
      integer iunit
      integer minu,maxu
      LOGICAL L
      PARAMETER (MINU=50,MAXU=99)
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

!=============================================================
      SUBROUTINE READOBS2000 (OBS,DESIG,&
                              YEAR,MONTH,DAY,RA,DEC,MAG,MAGTYPE,OBSCODE)
!+
!  Given:
!    OBS      [CHARACTER*80, an observation in MPC J2000 format]
!
!  Returned:
!    NUMBER   [INTEGER]
!    DESIG    [CHARACTER*7]
!    DISC     [CHARACTER*1]
!    COMMENT1 [CHARACTER*1]
!    COMMENT2 [CHARACTER*1]
!    YEAR     [INTEGER]
!    MONTH    [INTEGER]
!    DAY      [real(8)]
!    RA       [real(8), in radians]
!    DEC      [real(8), in radians]
!    MAG      [real(8)]
!    MAGTYPE  [CHARACTER*1]
!    OBSCODE  [INTEGER]
!
!  Last update 971222 (changed format X to 1X as some compilers require)
!-
      use mconstants
      implicit none
      CHARACTER OBS*80,DESIG*7,SIGN,MAGTYPE
      INTEGER YEAR,MONTH,RAHR,RAMIN,DEG,DECMIN
      character*3 OBSCODE
      integer im1,im2,im3
      real(8) RA,DEC,DAY,RASEC,DECSEC,MAG

920   FORMAT (5x,a7,3x,I4,I3,F10.0,I2,I3,F6.0,1X,A,I2,I3,F5.0,&
         10X,I2,1X,2I1,A,6X,a3)

      READ (OBS,920) DESIG,&
       YEAR,MONTH,DAY, RAHR,RAMIN,RASEC, SIGN,DEG,DECMIN,DECSEC,&
       IM1,IM2,IM3,MAGTYPE, OBSCODE

!   Possible problems (depending on compiler) with trailing blanks:
      MAG=IM1+IM2/10D0+IM3/100D0

      RA=(RAHR+RAMIN/60.0D0+RASEC/3600)*15*drad
      DEC=(DEG+DECMIN/60.0D0+DECSEC/3600)*drad
      IF (SIGN.EQ.'-') DEC=-DEC

!   Default is that mag is a B mag
      IF (MAGTYPE.EQ.' ') MAGTYPE='B'

      END
