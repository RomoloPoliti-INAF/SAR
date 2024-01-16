from pathlib import Path
from sys import exit

import rich_click as click
from MyCommonLib import (CONTEXT_SETTINGS, FMODE, Vers, debug_help_text,
                         progEpilog, read_yaml, verbose_help_text)
from planetary_coverage import ESA_MK, MetaKernel
from rich import inspect

from SAR.config import conf
from SAR.sendmail import mail, page
from SOIM.core import core_soim



version = Vers((1, 0, 1, 'd', 1))

__version__ = version.full()

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.FOOTER_TEXT = progEpilog
click.rich_click.HEADER_TEXT = f"SOIM Authomatic Runner, version [blue]{__version__}[/blue]"


class KernelType:
    def __init__(self, name, item) -> None:
        self.name = name
        if isinstance(item,str):
            self.list = [item]
        else:
            self.list=[*item]

    # def __repr__(self) -> str:
    #     return f"[{' , '.join(x for x in self.list)}]"

    def __eq__(self, other):
        if isinstance(other, KernelType):
            return self.name == other.name and self.list == other.list
        return False
    
    def __sub__(self, other):
        return list(set(self.list)-set(other.list))


class KernelsTypes:
    def type_list(self) -> list:
        ls = []
        for item in self.__dict__:
            if not item.startswith('_'):
                ls.append(item)
        return ls

    def add(self, ker):
        parts = ker.split('/')
        if parts[1] not in self.type_list():
            setattr(self, parts[1], KernelType(parts[1], parts[2]))
        else:
            item = getattr(self, parts[1])
            item.list.append(parts[2])

    def __eq__(self, other) -> bool:
        # Check if the type lists are the same
        for x in self.type_list():
            diff=getattr(self,x)-getattr(other,x)
            if len(diff)== 0:
                return True
            else:
                if x in conf.check_update.keys():
                    if with_substring(x.list,conf.check_update[x]):
                        return False
                    else:
                        return True
                else:
                    return False

        return all(getattr(self, x) == getattr(other, x)
                   for x in self.type_list())


def with_substring(list_string, list_substring):
    # Itera attraverso ogni stringa nella lista delle substringhe
    for substring in list_substring:
        # Verifica se la substringa è presente in almeno una delle stringhe nella lista
        if any(substring in elem for elem in list_string):
            return True
    # Se nessuna corrispondenza è stata trovata, restituisci False
    return False


def find_element_with_substring(lst, substring):
    # Use a list comprehension to find elements containing the substring
    result = [element for element in lst if substring in element]

    # Return the first match (or None if not found)
    return result[0] if result else None


def serialize_kernels_types(kernels_types):
    import json
    return json.dumps(kernels_types, default=lambda obj: obj.__dict__, indent=4)


def deserialize_kernels_types(json_data):
    import json
    data = json.loads(json_data)
    kernels_types = KernelsTypes()

    for key, value in data.items():
        setattr(kernels_types, key, KernelType(value['name'], value['list']))

    return kernels_types


def compare_kernels(ls1: list, ls2: list):
    a = set(ls1).intersection(ls2)
    b = set(ls1) - set(ls2)
    return list(a), list(b)


def item_version(item: str) -> str:
    return f"{item.split('_')[-1].split('.')[0]}."


def check_updated(kernels: KernelsTypes) -> bool:
    with open(conf.curr_kernel, FMODE.READ) as inp:
        old_kernels: KernelsTypes = deserialize_kernels_types(inp.read())
    if old_kernels == kernels:
        return False
    else:
        return True

def save_kernel(kernels:KernelsTypes)->None:
    with open(conf.curr_kernel, FMODE.WRITE) as outp:
        outp.write(serialize_kernels_types(kernels))

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-k', '--kernel', 'kernel_folder', help="Kernels folder", metavar="FOLDER", default='kernels', show_default=True)
@click.option('-d', '--debug', is_flag=True, help=debug_help_text, default=False)
@click.option('-v', '--verbose', count=True, metavar="", help=verbose_help_text, default=0)
@click.option('--save-current', is_flag=True, hidden=True, default=False)
@click.version_option(__version__, '-V', '--version', prog_name='SOIM Authomatic Run')
def action(kernel_folder: Path, debug: bool, verbose: int, save_current: bool):
    conf.debug = debug
    conf.verbose = verbose
    # conf.logFile=Path('mylog.log')
    info = ESA_MK['MPO']
    conf.console.print(info['latest'])
    kernel_folder = Path(kernel_folder)
    if not kernel_folder.exists():
        kernel_folder.mkdir(parents=True)
    a = MetaKernel(
        info['latest'],
        kernels=kernel_folder,
        download=True,
    )
    conf.console.print(a)
    kernels = KernelsTypes()
    for item in a.kernels:
        kernels.add(item)
    if save_current:
        save_kernel(kernels)
        exit(0)
    if check_updated(kernels):
        conf.console.print("run Update")
        conf.log.info("Saving the current Kernel", verbosity=1)
        save_kernel(kernels)
        txt=f"The SOIM Output was updatet due a Metakernel changes ({Path(info['latest']).name})"
        project_list_file = Path('project_list.yml')
        core_soim(read_yaml(project_list_file),info['latest'],kernel_folder)
        try:
            mail('SOIM Output Updated', text=txt, html=page(
                f"<strong>{txt}</strong><br/>"))
        except Exception as e:
            conf.log.error(f"Impossible send the email. ({e.args[1]})")


if __name__ == "__main__":
    action()
