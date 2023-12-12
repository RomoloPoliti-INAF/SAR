from MyCommonLib import Configure
from pathlib import Path


class Conf(Configure):
    _logger:str="SAR"
    check_file:Path=Path('check.yml')

conf=Conf()