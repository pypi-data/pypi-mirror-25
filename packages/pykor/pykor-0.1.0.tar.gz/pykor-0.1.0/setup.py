import os
import sys

from setuptools import find_packages, setup
from setuptools.command import install, develop


# cx_Freeze: we added a undocumented option to enable building frozen versions
# of our packages. This should be refactored for a more safe approach in the
# future.
setup_kwargs = {}
if '--cx-freeze' in sys.argv:
    from cx_Freeze import setup, Executable

    build_options = {
        'include_files': [],
        'packages': ['os', 'pykor', 'pygments', 'transpyler'],
        'excludes': [
            'tkinter', 'redis', 'lxml',
            'qturtle.qsci.widgets',
            'nltk', 'textblob',
            'matplotlib', 'scipy', 'numpy', 'sklearn',
            'notebook',
            'java',
            'sphinx', 'PIL', 'PyQt4'
        ],
        'optimize': 1,
    }
    base = 'Win32GUI' if sys.platform == 'win32' else None

    setup_kwargs['executables'] = [
        Executable(
            'src/pykor/__main__.py',
            base=base,
            targetName='pykor.exe' if sys.platform == 'win32' else 'pykor',
            shortcutName='pykor',
            shortcutDir='DesktopFolder',
        )
    ]
    setup_kwargs['options'] = {'build_exe': build_options}
    sys.argv.remove('--cx-freeze')


# Save version and author to __meta__.py
version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'src', 'pykor', '__meta__.py')
meta = '''# Automatically created. Please do not edit.
__version__ = '%s'
__author__ = 'F\\xe1bio Mac\\xeado Mendes'
''' % version
with open(path, 'w') as F:
    F.write(meta)


# Run setup() function
setup(
    name='pykor',
    version=version,
    description='한국의 파이썬 인터프리터.',
    author='Jiyoung Hwang',
    author_email='jy.hwng@gmail.com',
    url='https://github.com/transpyler/pykor',
    long_description=('''
    포르투갈어로 명령을 받아들이도록 Python 구문을 수정하는 프로그래밍 언어입니다. 이 언어는
    포르투갈어로 명령을 받아들이는 Python의 확장으로 개발되었습니다.

    PyKor의 유일한 목표는 프로그래밍 학습을 촉진하는 것입니다. 일단 기초가 잡히면 (Python의
    경우) 실제 언어로의 전환이 점진적이고 자연스러워집니다.
    '''),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],

    # Packages and dependencies
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'transpyler>=0.4.1',
        'qturtle>=0.4.0',
    ],
    extra_requires={
        'gui': [],
    },

    # Scripts
    entry_points={
        'console_scripts': [
            'pykor = pykor.__main__:main',
        ],
    },

    # Data files
    package_data={
        'pykor': [
            'assets/*.*',
            'doc/html/*.*',
            'doc/html/_modules/*.*',
            'doc/html/_modules/tugalib/*.*',
            'doc/html/_sources/*.*',
            'doc/html/_static/*.*',
            'examples/*.pytg'
        ],
        'pykor': [
            'ipykor/assets/*.*',
        ],
    },
    # data_files=DATA_FILES,
    zip_safe=False,
    **setup_kwargs
)
