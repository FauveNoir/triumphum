from setuptools import setup, find_packages
from triumphum.__init__ import *

# Lis les dépendances depuis requirements.txt
with open('requirements.txt') as f:
	required_packages = f.readlines()

setup(
	name=APP_FANCY_NAME,
	author=APP_AUTHOR,
	author_email=APP_AUTHOR_MAIL,
	version=APP_VERSION,
	packages=find_packages(),
	install_requires=[
		# liste de tes dépendances, si tu en as
		install_requires=[pkg.strip() for pkg in required_packages],  # Prends les paquets de requirements.txt
	],
	entry_points={
		'console_scripts': [
			'triumphum = main:main',  # définir le point d'entrée pour ton script
		],
	},
	classifiers=[
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Operating System :: POSIX :: Linux",
	], #other informations for the package
)

