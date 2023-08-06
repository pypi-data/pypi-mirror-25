from setuptools import setup

setup(name='ttnmqtt',
      version='0.7.1',
      description='small package to make mqtt connection to ttn',
      author='Emmanuelle Lejeail',
      author_email='manu.lejeail@gmail.com',
      license='MIT',
      packages=['ttnmqtt'],
      install_requires=[
          'paho-mqtt',
          'pydispatch',
      ],
      zip_safe=False)
