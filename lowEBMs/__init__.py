def Tutorial_copy(*args,**kwargs):
    import shutil, sys, os
    path=kwargs.get('path',os.getcwd())
    possible_paths=[]
    if path!=os.getcwd():
        subdir=['..','../..','../../..','../../../..','../../../../..']
        for i in subdir:
            possible_paths.append(i+path)
            
    data_paths=[]
    for i in sys.path:
        data_paths.append(i+'/lowEBMs/Tutorials')
    for data in data_paths:
        exists = os.path.isdir(data)
        if exists:
            location=data
            break
    exit=False
    for trypath in possible_paths:
        exists= os.path.isdir(trypath)
        if exists:
            
            if os.path.exists(trypath+'/Tutorials/Notebooks') and os.path.exists(trypath+'/Tutorials/Config'):
                shutil.rmtree(trypath+'/Tutorials/Notebooks')
                shutil.rmtree(trypath+'/Tutorials/Config')
            shutil.copytree(data+'/Notebooks',trypath+'/Tutorials/Notebooks')
            shutil.copytree(data+'/Config',trypath+'/Tutorials/Config')
            exit=True
            break
    if exit:
        print('Copy tutorial files to:'+trypath)
    else:
        print('Path could not be found, please insert a valid path')
        

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
    import numpy as np
    buffer = [np.nan] * period
    for i in range(period,len(signal)):
        buffer.append(signal[i-period:i].mean())
    return buffer

