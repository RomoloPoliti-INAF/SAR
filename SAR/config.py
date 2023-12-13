from MyCommonLib import Configure
from pathlib import Path


class Conf(Configure):
    _logger:str="SAR"
    check_file:Path=Path('check.yml')
    distribution:list=[
        'Romolo Politi romolo.politi@inaf.it',
        'Emanuele Simioni emanuele.simioni@inaf.it'
        ]

conf=Conf()