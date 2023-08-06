from distutils.core import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='test_module123123281933',
    packages=['test_module'],
    version='1.1',  # Ideally should be same as your GitHub release tag varsion
    description='description',
    long_description=readme(),
    author='m3fh4q',
    author_email='m3fh4q@yandex.com',
    url='https://github.com/m3fh4q/test_module',
    download_url='https://github.com/m3fh4q/test_module/archive/master.zip',
    keywords=['tag1', 'tag2'],
    include_package_data=True
)
