from setuptools import setup, find_packages

with open('README') as f:
    readme = f.read()

setup(
    name='jojo',
    version='0.0.8',
    description="jojo's programming adventure in python",
    url='http://github.com/xieyuheng/jojo-on-python',

    author='xieyuheng',
    author_email='xyheme@gmail.com',

    py_modules=['jojo'],
    scripts=['jojo'],
    packages=find_packages(exclude=('tests', 'docs')),

    long_description=readme,
    license="I dedicate all my works here to all human beings.",
)
