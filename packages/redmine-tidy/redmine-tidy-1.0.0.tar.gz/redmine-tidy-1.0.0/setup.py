from setuptools import setup

major_version = 1
minor_version = 0
build_version = 0

version = str(major_version) + '.' + str(minor_version) + '.' + str(build_version)

setup(
    name='redmine-tidy',
    version=version,
    description='Redmine Tidy: Close tickets with no recent updates',
    author='Quentin Stafford-Fraser',
    url='https://github.com/telemarq/redmine_tidy',
    license='GNU GPL 2',
    packages=(),
    scripts = ['redmine-tidy.py'],
    install_requires=('python-redmine','docopt'),
)
