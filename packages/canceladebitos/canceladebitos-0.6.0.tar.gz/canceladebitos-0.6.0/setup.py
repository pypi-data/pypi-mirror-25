from setuptools import setup


setup(
    name="canceladebitos",
    packages=["canceladebitos"],
    entry_points={
        "console_scripts": ['canceladebitos = canceladebitos.__main__:main']
        },
    version='0.6.0',
    description="Cancelamentos dos débitos renegociados em operações de parcelamento.",
    author="Rafael Alves Ribeiro",
    author_email="rafael.alves.ribeiro@gmail.com",
    url="http://www.bitbucket.com",
    )
