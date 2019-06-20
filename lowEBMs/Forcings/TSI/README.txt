This directory contains solar forcing functions for use in the
PMIP3/CMIP5 simulations of the last millennium. 

For each reconstruction, we provide an estimate of the Total Solar
Irradiance (TSI) as a function of year back to 850 CE, along with a
high-spectral resolution estimate of the variations at individual
wavelengths.

There are multiple source datasets for these forcings, see
descriptions below. Note that the extension of the quasi-11yr cycle
and spectral characterstics of the reconstructions prior to 1610 (for
the Delaygue/Bard (DB) and Muscheler et al (MEA) reconstructions) and
for the spectral variations prior to 1850 for the Vieira, Krivova et
al (VK) and Steinhilber et al (SBF) reconstrucitons are synthetic and
added in for consistency of the forcing fields through time. Note that
the DB and MEA extensions are scaled directly to the Wang et al (WLS)
reconstructions back to 1610. The VK and SBF reconstructions are
joined in 1849 since their Maunder Minimum values differ significantly
from WLS. Note that the cosmogenic nuclide based reconstructions do
not perfectly match the observed TSI changes from 1976 onwards and so,
WLS are preferred for the post 1850 period.

The synthetic 11 yr cycle is based on the average shape of solar
cycles over the 20th Century in TSI from WLS, and the spectral
characteristics are derived from a regression with TSI over the period
1610-2000 in the WLS spectral data.

All reconstructions (except MEA) are calibrated to the WLS modern
values (1976-2006) 1366.14 W/m2. Note that this is slightly higher
than the PMOD composite of TSI over the same period which is 1365.96
W/m2 (a difference of 0.18 W/m2). The MEA record is more difficult to
scale sensibly (though an inverse regression is used below). If a
different calibration is required, we suggest a simple multiplicative
scaling.


Files:

1) Wang et al (1610-2000)

tsi_WLS.txt  (2 records)

The Wang et al TSI reconstruction to 1610, with and without background
changes.

spectra_WLS_1610_2000_rescaled.txt

From the original file spectra_1610_2000a_21Jan09.txt, with rescaled
spectral values (so that the integral of the components equals the annual
TSI). Slightly modified format (see notes below).

spectra_WLS_1610_2000_rescaled_nobackground.txt

An estimate of the spectral changes for the WLS no-background change
case. This was calculated by scaling the 11yr smooth for each
component so that the Maunder Minimum value was the same as the value
in modern minima. This is provisional and may be superseded. Note that
because this is estimated based on the w/background case, the TSI
values are not exactly identical to the TSI nobackground case in the
first file.


2) Delaygue+Bard extension (850-1609):

spectra_DB_850-1609_background.txt
spectra_DB_850-1609_nobackground.txt
tsi_DB_lin_40_11yr.txt (2 records)

extensions of the WLS solar reconstrucitons based on an Antarctic
stack of 10Be records, scaled to the Maunder Minimum to modern changes
in TSI seen in WLS and calibrated to the modern WLS value. The TSI
values were derived by linear interpolation, a 40 yr smoothing and the
addition of a synthetic 11 yr cycle.

3) Muscheler extension (850-1609):

tsi_MEA_11yr.txt (two records)
spectra_MEA_850-1609_background.txt
spectra_MEA_850-1609_nobackground.txt

14C-based reconstruction, 40 yr smoothing, inverse regression to WLS
over period 1630-1930, synthetic 11 yr cycle. 

4) Steinhilber extension (850-1849):

tsi_SBF_11yr.txt
spectra_SBF_850-1849.txt  

TSI from 850 to 1849, scaled to modern WLS values. Synthetic 11yr
cycle starting from the solar minimum in 1844. Join to WLS
with/background data in 1850 for extension to the present day. 

5) Vieira, Krivova extension (850-1849):

tsi_VK.txt
spectra_VK_850-1849.txt

TSI from 850 to 1849 calibrated to modern WLS. 11 yr cycle already
imposed. Join to WLS with/background in 1850 for extension to present
day. 

6) Figures:

tsi.pdf 

TSI reconstructions from 850 CE to 2000 CE.

Notes:

- The average, normalised 11 yr cycle used had yearly components: 
  (-0.786483,-0.299496,0.317166,0.636872,1.0,0.701905,0.342438,
  -0.0689046,-0.36599,-0.676228,-0.934423)
  (the TSI anomaly for any one year is the magnitude of the solar
  cycle, multiplied these coefficents added to the 40 year smoothed
  value). Note that the synthetic cycle is exactly 11 years. 

- the format of the spectra files is slightly different to the
  original file provided by Judith Lean. There is an extra line of
  text to prevent inadvertent confusion, but the main difference is
  that the spectral components are scaled so that the integral of the
  spectra is exactly equal to the TSI for that year. They can be read
  using the following fortran:

      integer, parameter :: nlean=3780,nyr=2000	    
      character*80 title(7)
      real*8 wslean(nlean),fslean(nlean),spectra(nlean,nyr),tsi(nyr)
      real*8 year(nyr)
      integer :: yr1=1610, yr2=2000   ! change depending on file

      do i=1,4
        read(1,'(A80)') title(i)
      end do
      read(1,'(5F14.2)') fslean
      read(1,'(A80)') title(5)
      do i=1,nlean/5
        read(1,*) (wslean((i-1)*5+j),j=1,5)
      end do
      read(1,'(A80)') title(6)
      read(1,'(A80)') title(7)

      do n=yr1,yr2
        read(1,*) year(n-yr1+1),tsi(n-yr1+1)
        do i=1,nlean/5
          read(1,*) (data((i-1)*5+j,n-yr1+1), j=1,5)
        end do
      end do

- Source data for the spectra and Wang and Lean TSI:
http://www.geo.fu-berlin.de/en/met/ag/strat/forschung/SOLARIS/Input_data/CMIP5_solar_irradiance.html

References:

Lean J, "Calculations of Solar Irradiance" http://www.geo.fu-berlin.de/en/met/ag/strat/forschung/SOLARIS/Input_data/Calculations_of_Solar_Irradiance.pdf

Delaygue, G and E. Bard. Solar forcing based on Be-10 in Antarctica
ice over the past millennium and beyond', EGU 2009 General Assembly, #
EGU2009-6943, http://meetingorganizer.copernicus.org/EGU2009/EGU2009-6943.pdf

Muscheler, R., F. Joos, J. Beer, S.A. Müller, M. Vonmoos, and
I. Snowball.  2007. Solar activity during the last 1000 yr inferred
from radionuclide records Quaternary Science Reviews, Vol. 26, pp. 82-97.
doi:10.1016/j.quascirev.2006.07.012			

Steinhilber, F., J. Beer, and C. Frohlich, Total solar irradiance
during the Holocene, GRL, 2009

Vieira et al, 

Wang, Y.-M., J. L. Lean, and N. R. Sheeley, Jr. (2005), Modeling the
Sun’s Magnetic Field and Irradiance since 1713, ApJ, 625, 522–538,
doi:10.1086/429689.



