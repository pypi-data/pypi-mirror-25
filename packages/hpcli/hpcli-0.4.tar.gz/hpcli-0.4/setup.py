from setuptools import setup
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('./requirements.txt', session='hack')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(name='hpcli',
      version='0.4',
      description='HighlyProbable SDK and CLI',
      url='https://github.com/Tranquant/highlyprobable-cli',
      author='Mehrdad Pazooki, David Briggs',
      author_email='info@tranquant.com',
      license='MIT',
      include_package_data=True,
      packages=['hpcli', 'hpcli.sdk', 'hpcli.hpclilib'],
      scripts=['hpcli/hpcli'],
      zip_safe=True,
      keywords='hpcli',
      install_requires=reqs
)
