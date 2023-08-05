from setuptools import setup

setup(name='instagram-stalker',
      version='0.1.1',
      description="Observes given instagram account and notify when he makes his account public.",
      url='http://github.com/pkacprzak/instagram-stalker',
      author='Pawel Kacprzak',
      author_email='pawel.kacprzak.89@gmail.com',
      license='MIT',
      packages=['instagram_stalker'],
      install_requires=[
          'requests',
          'pync'
      ],
      zip_safe=False)
