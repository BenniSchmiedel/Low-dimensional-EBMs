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
