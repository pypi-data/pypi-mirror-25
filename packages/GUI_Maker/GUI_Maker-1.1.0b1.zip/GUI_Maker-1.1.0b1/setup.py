from distutils.core import setup
setup(
	name = 'GUI_Maker',
	packages = ['GUI_Maker'], # this must be the same as the name above
	version = '1.1.0b1', #https://www.python.org/dev/peps/pep-0440/
	description = 'Streamlines wxPython to simplify your code and make it easier to create a GUI.',
	author = 'Joshua Mayberry',
	author_email = 'dragonkade333@gmail.com',

	url = 'https://github.com/JoshMayberry/GUI_Maker', # use the URL to the github repo
	download_url = 'https://github.com/JoshMayberry/GUI_Maker/archive/v0.1-beta.1.tar.gz', # I'll explain this in a second
	keywords = ['GUI', 'wxPython', 'Interface'], # arbitrary keywords
	license='MIT',
	python_requires='>=3',
	classifiers=[
		#https://pypi.python.org/pypi?%3Aaction=list_classifiers
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: User Interfaces',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Natural Language :: English',
		'Programming Language :: Python :: 3.4',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: Microsoft :: Windows :: Windows 10',
		'Operating System :: Microsoft :: Windows :: Windows 7',
		'Operating System :: Microsoft :: Windows :: Windows XP'
	],
	install_requires=[
			'wxPython_Phoenix',
			'openpyxl',
			'numpy',
			'matplotlib',
			'py2exe',
			'pillow',
			'pycryptodomex',
			'atexit',
			'netaddr',
			'elaphe',
			'sqlite3',
			'python3-ghostscript',
	],
)

#Upload project
# import subprocess
# subprocess.Popen(['py', '-m', 'twine', 'upload', 'dist/*']