import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    readme = f.read()

with open(os.path.join(here, 'VERSION')) as f:
    version = f.read().strip()

setup(name='casepropods.family_connect_subscription',
      version=version,
      description=('FamilyConnect subscriptions data pod for casepro. Returns '
                   ' case specific information about stage based messaging '
                   'subscriptions.'),
      long_description=readme,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Django",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Praekelt Foundation',
      author_email='dev@praekelt.com',
      url='http://github.com/praekelt/casepropods.family_connect_subscription',
      license='BSD',
      keywords='',
      packages=['casepropods.family_connect_subscription'],
      include_package_data=True,
      zip_safe=False,
      namespace_packages=['casepropods'],
      entry_points={},
      install_requires=['seed-services-client>=0.31.0', 'pretty-cron==1.0.2'],
      )
