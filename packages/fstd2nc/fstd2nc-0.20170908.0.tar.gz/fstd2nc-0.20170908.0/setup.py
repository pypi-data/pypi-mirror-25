from setuptools import setup, find_packages
from fstd2nc import __version__

setup (
  name="fstd2nc",
  version=__version__,
  description = 'Converts RPN standard files (from Environment Canada) to netCDF files.',
  url = 'https://github.com/neishm/fstd2nc',
  author="Mike Neish",
  license = 'LGPL-3',
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    'Programming Language :: Python :: 2.7',
    'Topic :: Scientific/Engineering :: Atmospheric Science',
  ],
  packages = find_packages(),
  py_modules = ['fstd2nc','fstd2dap','fstd2nc_extra'],
  install_requires = ['numpy >= 1.13.0','netcdf4','fstd2nc-deps'],
  extras_require = {
    'dap': ['Pydap','Pydap[server]'],
  },
  package_data = {
    'fstd2nc_locale': ['*/LC_MESSAGES/fstd2nc.mo'],
  },
  entry_points={
    'console_scripts': [
      'fstd2nc = fstd2nc:_fstd2nc_cmdline_trapped',
    ],
    'pydap.handler': [
      'fstd = fstd2dap:FST_Handler',
    ],
  },

)

