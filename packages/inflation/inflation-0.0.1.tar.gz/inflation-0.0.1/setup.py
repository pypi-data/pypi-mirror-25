from setuptools import setup

setup(
    name='inflation',
    version='0.0.1',
    description='inflation app',
    url='https://github.com/terminal-labs/sample-project',
    author='Michael Verhulst',
    author_email='michael@terminallabs.com',
    packages=['app'],
    zip_safe=False,
    install_requires=['click'],
    entry_points={
          'console_scripts': [
              "inflation=app.__main__:main"
          ]
      },
    )
