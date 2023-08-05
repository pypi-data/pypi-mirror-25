from setuptools import setup

setup(name='my_funniest',
      version='0.1',
      description='The funniest joke in the world',
      url='http://github.com/storborg/funniest',
      author='Bram Vernaas',
      author_email='amavermaas@gmail.com',
      username='bvermaas',
      license='MIT',
      packages=['my_funniest'],
      install_requires=[
          'markdown',
      ],
      zip_safe=False)