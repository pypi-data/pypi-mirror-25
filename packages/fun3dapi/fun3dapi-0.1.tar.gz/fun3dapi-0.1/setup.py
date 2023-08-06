from setuptools import setup
version = 0.1
setup(
    name='fun3dapi',
    version=version,
    description='A Python API for high-throughput FUN3D',
    author='FlexCompute, Inc.',
    author_email='john@simulation.cloud',
    packages=['fun3dapi'],
    install_requires=['requests']
)
