from setuptools import setup, find_packages
with open('requirements.txt') as f:
    data = f.read()
reqs = data.split()

setup(
    name='powerpbackend-client',
    version='0.1.3',
    packages=find_packages(),
    url='https://gitlab.com/gisce/backend-client',
    license='MIT',
    author='GISCE-TI, S.L.',
    author_email='devel@gisce.net',
    description='Client of PowERP Backend',
    entry_points='''
    ''',
    install_requires=reqs
)
