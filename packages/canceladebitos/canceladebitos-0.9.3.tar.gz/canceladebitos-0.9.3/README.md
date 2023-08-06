# Parcelamento - Cancelamento de Débitos #

Busca no banco de dados do SPUNET os débitos renegociados em operações de parcelamento e efetua o cancelamento no SIAPA.

### Instalação ###

git clone https://rafael_ribeiro_dev@bitbucket.org/derep/cancela-debitos.git
python setup.py install


### Instalação ###

O script é executado através do prompt de comando:

* Cancelamento dos débitos parcelados
  canceladebitos [CPF] [SENHA]

* Validação do cancelamento
  canceladebitos [CPF] [SENHA] --validador
