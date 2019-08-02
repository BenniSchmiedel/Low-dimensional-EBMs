def Tutorial_copy(*args,**kwargs):
    import shutil, sys, os
    path=kwargs.get('path',os.getcwd())

    possible_paths=[]
    for i in sys.path:
        possible_paths.append(i+'/lowEBMs/Tutorials')
    for trypath in possible_paths:
        exists = os.path.isdir(trypath)
        if exists:
            existsout= os.path.isdir(path)
            if existsout:
                print('Copy tutorial files to:'+path)
                shutil.copytree(trypath+'/Notebooks',path+'/Tutorials/Notebooks')
                shutil.copytree(trypath+'/Config',path+'/Tutorials/Config')
            else:
                print('Path could not be found, please insert a full path or relative paths')
            break

def update_plotstyle():
    import matplotlib
    matplotlib.rcParams['axes.titlesize']=24
    matplotlib.rcParams['axes.labelsize']=20
    matplotlib.rcParams['lines.linewidth']=3
    matplotlib.rcParams['lines.markersize']=10
    matplotlib.rcParams['xtick.labelsize']=16
    matplotlib.rcParams['ytick.labelsize']=16
    matplotlib.rcParams['ytick.labelsize']=16
    matplotlib.rcParams['ytick.minor.visible']=True
    matplotlib.rcParams['ytick.direction']='inout'
    matplotlib.rcParams['ytick.major.size']=10
    matplotlib.rcParams['ytick.minor.size']=5
    matplotlib.rcParams['xtick.minor.visible']=True
    matplotlib.rcParams['xtick.direction']='inout'
    matplotlib.rcParams['xtick.major.size']=10
    matplotlib.rcParams['xtick.minor.size']=5

def moving_average(signal, period):
    buffer = [np.nan] * period
    for i in range(period,len(signal)):
        buffer.append(signal[i-period:i].mean())
    return buffer

class constants:
    import numpy as np
    a = 6.373E6      # Radius of Earth (m)
    Lhvap = 2.5E6    # Latent heat of vaporization (J / kg)
    Lhsub = 2.834E6   # Latent heat of sublimation (J / kg)
    Lhfus = Lhsub - Lhvap  # Latent heat of fusion (J / kg)
    cp = 1004.     # specific heat at constant pressure for dry air (J / kg / K)
    Rd = 287.         # gas constant for dry air (J / kg / K)
    kappa = Rd / cp
    Rv = 461.5       # gas constant for water vapor (J / kg / K)
    cpv = 1875.   # specific heat at constant pressure for water vapor (J / kg / K)
    Omega = 2 * np.math.pi / 24. / 3600.  # Earth's rotation rate, (s**(-1))
    g = 9.8          # gravitational acceleration (m / s**2)
    kBoltzmann = 1.3806488E-23  # the Boltzmann constant (J / K)
    c_light = 2.99792458E8   # speed of light (m/s)
    hPlanck = 6.62606957E-34  # Planck's constant (J s)
    # sigma = 5.67E-8  # Stefan-Boltzmann constant (W / m**2 / K**4)
    #  sigma derived from fundamental constants
    sigma = (2*np.pi**5 * kBoltzmann**4) / (15 * c_light**2 * hPlanck**3)

    S0 = 1366.14      # solar constant (W / m**2)

    ps = 1000.       # approximate surface pressure (mb or hPa)

    rho_w = 1000.    # density of water (kg / m**3)
    cw = 4181.3      # specific heat of liquid water (J / kg / K)
    mb_to_Pa = 100.
    time_sec_year=60*60*24*365
    time_sec_day=60*60*24
