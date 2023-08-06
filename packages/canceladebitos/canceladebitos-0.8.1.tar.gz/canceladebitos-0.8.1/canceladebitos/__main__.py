'''
    CLI para o script de cancelamento de débitos.
'''
import os

import fire
from .cancelador import Cancelador
#from .valida import main as Validador
from .valida import main_multprocess as Validador
from .__init__ import __version__
#nu_cpf = '41314514687'
#senha = 'Enzo3698'


def cli(cpf, senha, validador=False):
    os.system('cls')
    print(f'CANCELA DÉBITOS PARCELAMENTO v{__version__}')
    print(f'===================================\n')
    if validador:
        Validador(cpf, senha)
    else:
        Cancelador(cpf, senha)


def main():
    fire.Fire(cli)
