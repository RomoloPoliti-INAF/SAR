import rich_click as click
from MyCommonLib import debug_help_text,CONTEXT_SETTINGS, Vers, progEpilog,verbose_help_text
from SAR.config import conf
from planetary_coverage import ESA_MK,MetaKernel
from pathlib import Path

version=Vers((0,1,0,'d',1))

__version__ = version.full()

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.FOOTER_TEXT = progEpilog
click.rich_click.HEADER_TEXT = f"SOIM Authomatic Runner, version [blue]{
    __version__}[/blue]"
    
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-k','--kernel','kernel_folder',help="Kernels folder",metavar="FOLDER",default='kernels')
@click.option('-d','--debug', is_flag=True,help=debug_help_text, default=False)
@click.option('-v','--verbose', count=True,metavar="", help=verbose_help_text,default=0)
@click.version_option(__version__, '-V', '--version', prog_name='SOIM Authomatic Run')
def action(kernel_folder:Path,debug:bool, verbose:int):
    conf.debug=debug
    conf.verbose=verbose
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


if __name__=="__main__":
    action()