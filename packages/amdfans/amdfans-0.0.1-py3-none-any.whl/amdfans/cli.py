from .config import Config
from .controller import Controller
from .logger import Logger
import builtins
import click

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-v', '--verbose', default=False, is_flag=True, help='Enable verbose logging.')
@click.option('-q', '--quiet', default=False, is_flag=True, help='Disable stdout logging.')
@click.argument('percentage', type=int)
def cli(**kwargs):
  if Config.validate():
    builtins.ui = {k: v for k, v in kwargs.items() if v}
    builtins.logger = Logger(ui)
    
    if Controller.main():
      status = 0
    else:
      status = 1

    logger.info('')
    logger.info("Exiting.")
    return status

def main():
  cli(obj={})

if __name__ == '__main__':
  main()