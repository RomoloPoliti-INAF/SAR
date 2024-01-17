from pathlib import Path

from MyCommonLib import Configure,read_yaml
# from importlib.resources import files
from SAR.check import chk


class Conf(Configure):
    _logger:str="SAR"
    curr_kernel: Path = Path('current_kernel.json')
    check_update:dict = chk #read_yaml(files("SAR").joinpath('check.yml'))
    distribution:list=["emanuele.simioni@inaf.it",
                       "romolo.politi@inaf.it"]
    message:str=""
    # [
    #     'Romolo Politi romolo.politi@inaf.it',
    #     'Emanuele Simioni emanuele.simioni@inaf.it'
    #     ]

conf=Conf()