from setuptools import find_packages
from setuptools import setup

# with open('requirements.txt') as f:
# content = f.readlines()
# requirements = [x.strip() for x in content if 'git+' not in x]
requirements = [
    'gcsfs==0.6.0',
    'pandas==0.24.2',
    'scikit-learn==0.23.2',
    'google-cloud-storage==1.26.0',
    'pygeohash',
    'category_encoders',
    'mlflow==1.8.0',
    'joblib==0.14.1',
    'numpy==1.18.4',
    'psutil==5.7.0',
    'pygeohash==1.2.0',
    'termcolor==1.1.0',
    'xgboost==1.1.1',
    'memoized-property==1.0.3',
    'scipy== 1.2.2',
    'category_encoders==2.2.2'
        ]

setup(name='TaxiFareModel',
      version="1.0",
      description="Project Description",
      packages=find_packages(),
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      install_requires=requirements
      )
# install_requires=requirements)
