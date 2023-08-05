from setuptools import setup

setup(name='gae_django',
      version='0.1',
      description='helpers for Django project running on Google App Engine',
      keywords='django googleappengine gae',
      url='https://gitlab.com/taelimoh/gae-django',
      author='Tae-lim Oh',
      author_email='taelimoh@gmail.com',
      license='MIT',
      packages=['gae_django'],
      install_requires=[],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)