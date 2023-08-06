'''
    CLI para o script de cancelamento de débitos.
'''
import os

import fire

from .cancelador import Cancelador
from .config import config_siapa
#from .valida import main as Validador
from .valida import main_multprocess as Validador
from .__init__ import __version__


def cli(validador=False):
    os.system('cls')
    print(f'CANCELA DÉBITOS PARCELAMENTO v{__version__}')
    print(f'===================================\n')
    if validador:
        Validador(config_siapa['cpf'], config_siapa['senha'])
    else:
        Cancelador(config_siapa['cpf'], config_siapa['senha'])


def main():
    fire.Fire(cli)
