from setuptools import setup

setup(name='django_error_assist',
      version='0.1.4',
      description='Allows user to search the django errors on google/stackoverflow with a link.',
      url='http://github.com/im-shyam/django_error_assist',
      author='Shyam Satyaprasad',
      author_email='shyam.ns114@gmail.com',
      license='MIT',
      packages=['django_error_assist'],
      install_requires=[
          'django',
      ],
      zip_safe=False)
