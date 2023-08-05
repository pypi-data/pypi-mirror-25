import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('quantumworldX/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(name='quantumworldX',
      version=version,
      description='Basic library for the QuantumWorld edX course',
      url='https://pythonhosted.org/quantumworldX/',
      author='Benjamin Sanchez Lengeling',
      author_email='beangoben@gmail.com',
      license='MIT',
      packages=['quantumworldX'],
      install_requires=['numpy>=1.11',
                        'matplotlib>=1.5',
                        'scipy>=0.12.0',
                        'cycler'],
      # download_url = 'https://github.com/peterldowns/mypackage/tarball/0.1',
      keywords=['Quantum Chemistry', 'edX',
                'Quantum Mechanics'],  # arbitrary keywords
      classifiers=[],
      )
