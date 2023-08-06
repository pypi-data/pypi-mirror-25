import glob
import os
import warnings

from setuptools import setup, find_packages

MPINT_DIR = os.path.dirname(os.path.abspath(__file__))

setup(
    name="MPInterfaces_Latest_Test",
    version="1.0.2",
    install_requires=["pymatgen>=4.7.0", "FireWorks>=1.4.0",
                      "custodian>=1.0.1", "pymatgen-db>=0.5.1",
                      "ase>=3.11.0", "six", "pyyaml", "pyhull>=1.5.3"],
    extras_require={"babel": ["openbabel", "pybel"],
                    "remote": ["fabric"],
                    "doc": ["sphinx>=1.3.1", "sphinx-rtd-theme>=0.1.8"]
                    },
    author="Kiran Mathew, Joshua J. Gabriel, Michael Ashton, "
           "Arunima K. Singh, Joshua T. Paul, Seve G. Monahan, "
           "Richard G. Hennig",
    author_email="joshgabriel92@gmail.com, kmathew@lbl.gov, ashtonmv@gmail.com",
    maintainer="Joshua J. Gabriel, Michael Ashton",
    maintainer_email="joshgabriel92@ufl.edu, ashtonmv@gmail.com",
    description=(
        "High throughput analysis of interfaces using VASP and Materials Project tools"),
    license="MIT",
    url="https://github.com/henniggroup/MPInterfaces",
    packages=find_packages(),
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",        
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    scripts=glob.glob(os.path.join(MPINT_DIR, "mpinterfaces", "scripts", "*"))
)

# create the config file in the users home directory
import yaml
user_configs = {key:None for key in ['username','normal_binary','twod_binary',\
               'vdw_kernel','potentials','MAPI_KEY', 'queue_system', 'queue_template']}

with open(os.path.join(os.path.expanduser('~'),'.mpint_config.yaml'),'w') as config_file:
    yaml.dump(user_configs, config_file, default_flow_style=False)

warnings.warn('User must configure the .mpint_config.yaml created in your home directory.\
               You can do this using mpinterfaces.utils.load_config_vars for ipython passing \
               by passing the dict at least containing:\
               {"MAPI_KEY": MaterialsProject API key\
                "potentials": /path/to/your/potentials} ')
#from mpinterfaces import SETTINGS
