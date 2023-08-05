from setuptools import setup

setup(name='gae_django',
      version='0.4',
      description='helpers for Django project running on Google App Engine',
      keywords='django googleappengine gae',
      url='https://gitlab.com/taelimoh/gae-django',
      author='Tae-lim Oh',
      author_email='taelimoh@gmail.com',
      license='MIT',
      packages=['gae_django', 'gae_django/errors', 'gae_django/errors/templates', 'gae_django/storage', 'gae_django/storage/cloudstorage',],
      install_requires=[],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)