import setuptools

version = '0.4.2'

setuptools.setup(
        name='ctec_consumer',
        version=version,
        packages=setuptools.find_packages(),
        author='ZhangZhaoyuan',
        author_email='zhangzhy@chinatelecom.cn',
        url='http://www.189.cn',
        description='189 rabbitMQ consumer',
        install_requires=['gevent==1.2.2', 'pika==0.11.0']
)
