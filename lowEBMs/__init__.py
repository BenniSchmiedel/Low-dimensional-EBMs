import shutil, sys, os

def Tutorial_copy(*args,**kwargs):
    
    path=kwargs.get('path',os.getcwd())

    possible_paths=[]
    for i in sys.path:
        possible_paths.append(i+'/lowEBMs/Tutorials')
    for trypath in possible_paths:
        exists = os.path.isdir(trypath)
        if exists:
            shutil.copytree(trypath+'/Notebooks',path+'/Tutorials/Notebooks')
            shutil.copytree(trypath+'/Config',path+'/Tutorials/Config')   
            break
