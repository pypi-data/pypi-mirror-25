from setuptools import setup


setup(
    name="canceladebitos",
    packages=["canceladebitos"],
    entry_points={
        "console_scripts": ['canceladebitos = canceladebitos.__main__:main']
        },
    version='0.7.0',
    description="Cancelamentos dos débitos renegociados em operações de parcelamento.",
    author="Rafael Alves Ribeiro",
    author_email="rafael.alves.ribeiro@gmail.com",
    install_requires=[
        "codecov",
        "fire",
        "numpy",
        "pandas",
        "psycopg2",
        "pytest",
        "selenium",
        "siapatools",
        "siapa_robo",
        "tqdm",
    ],
    )
