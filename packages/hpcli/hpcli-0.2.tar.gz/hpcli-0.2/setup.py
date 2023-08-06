from setuptools import setup

setup(name='hpcli',
      version='0.2',
      description='HighlyProbable SDK and CLI',
      url='https://github.com/Tranquant/highlyprobable-cli',
      author='Mehrdad Pazooki, David Briggs',
      author_email='info@tranquant.com',
      license='MIT',
      packages=['hpcli', 'hpcli.sdk', 'hpcli.hpclilib'],
      scripts=['hpcli/hpcli'],
      zip_safe=True,
      keywords='hpcli',
      install_requires=[
          "certifi",
          "chardet",
          "docopt",
          "idna",
          "requests",
          "urllib3"
      ]
)
