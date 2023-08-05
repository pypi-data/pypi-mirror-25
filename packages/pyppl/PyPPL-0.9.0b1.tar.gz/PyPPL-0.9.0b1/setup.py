from setuptools import setup, find_packages
from pyppl import VERSION

setup (
	name             = 'PyPPL',
	version          = VERSION,
	description      = "A Python PiPeLine framework",
	url              = "https://github.com/pwwang/PyPPL",
	author           = "pwwang",
	author_email     = "pwwang@pwwang.com",
	license          = "Apache License Version 2.0",
	packages         = find_packages(),
	scripts          = ['bin/pyppl'],
	install_requires=[
		'python-box', 'six', 'filelock'
    ],
)
