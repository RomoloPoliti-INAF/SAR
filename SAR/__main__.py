from pathlib import Path
from sys import exit

import rich_click as click
from MyCommonLib import (CONTEXT_SETTINGS, FMODE, Vers, debug_help_text,
                         progEpilog, read_yaml, verbose_help_text)
from planetary_coverage import ESA_MK, MetaKernel
from rich import inspect

from SAR.config import conf

version=Vers((0,1,0,'d',2))

__version__ = version.full()

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.FOOTER_TEXT = progEpilog
click.rich_click.HEADER_TEXT = f"SOIM Authomatic Runner, version [blue]{
    __version__}[/blue]"

class KernelType:
    def __init__(self,name,item) -> None:
        self.name=name
        self.list=[item]
    def __repr__(self) -> str:
        return f"[{' , '.join(x for x in self.list)}]"


class KernelsTypes:
    def type_list(self)->list:
        ls=[]
        for item in self.__dict__:
            if not item.startswith('_'):
                ls.append(item)
        return ls
    
    def add(self,ker):
        parts=ker.split('/')
        if parts[1] not in self.type_list():
            setattr(self,parts[1],KernelType(parts[1],parts[2]))
        else:
            item=getattr(self,parts[1])
            item.list.append(parts[2])
def compare_kernels(ls1:list,ls2:list)->tuple[list,list]:
    a= set(ls1).intersection(ls2)
    b=set(ls1) - set(ls2)
    return list(a), list(b)
    
def check_updated(kernels:KernelsTypes)->bool:
    if conf.check_file.exists():
        data=read_yaml(conf.check_file)
    else:
        data={'kernels':[]}
        import yaml
        with open(conf.check_file,FMODE.WRITE) as fl:
            yaml.dump(data,fl)
        
    
    if len(data['kernels']) == 0:
        conf.log.info('No kernels to check', verbosity=1)
        return False
    else:
        present, missing=compare_kernels(data['kernels'].keys(),kernels.type_list())
        if len (missing) !=0:
            conf.log.critical(f"Some selected kernels types are missing in the MetaKernel ({','.join(missing)})")
            exit(1)
        elif len(present)==0:
            conf.log.critical("None of the selected kernel types are in the MetaKernel")
            exit(1)
        else:
            pass
        # if data['kernels'].keys() == kernels.type_list():



@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-k','--kernel','kernel_folder',help="Kernels folder",metavar="FOLDER",default='kernels', show_default=True)
@click.option('-d','--debug', is_flag=True,help=debug_help_text, default=False)
@click.option('-v','--verbose', count=True,metavar="", help=verbose_help_text,default=0)
@click.version_option(__version__, '-V', '--version', prog_name='SOIM Authomatic Run')
def action(kernel_folder:Path,debug:bool, verbose:int):
    conf.debug=debug
    conf.verbose=verbose
    # conf.logFile=Path('mylog.log')
    info = ESA_MK['MPO']
    conf.console.print(info['latest'])
    kernel_folder=Path(kernel_folder)
    if not kernel_folder.exists():
        kernel_folder.mkdir(parents=True)
    a= MetaKernel(
        info['latest'],
        kernels=kernel_folder,
        download=True,
    )
    conf.console.print(a)
    kernels=KernelsTypes()
    for item in a.kernels:
        kernels.add(item)
        
    # Quale kernel deve essere controllato?
    if check_updated(kernels):
        pass


if __name__=="__main__":
    action()