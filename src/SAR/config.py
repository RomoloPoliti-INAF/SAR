from pathlib import Path

from MyCommonLib import Configure,read_yaml


class Conf(Configure):
    _logger:str="SAR"
    curr_kernel: Path = Path('current_kernel.json')
    check_update:Path = read_yaml(Path('check.yml'))
    distribution:list=[
        'Romolo Politi romolo.politi@inaf.it',
        'Emanuele Simioni emanuele.simioni@inaf.it'
        ]

conf=Conf()