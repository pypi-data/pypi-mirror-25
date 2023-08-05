from setuptools import setup

setup(
    name='quickstep',
    description='Quickstep GRPC API',
    author='Robert Claus',
    author_email='robertclaus@gmail.com',
    version='0.0.7',
    py_modules=['quickstep','proto.NetworkCli_pb2','proto.NetworkCli_pb2_grpc'],
    license='Apache'
)
