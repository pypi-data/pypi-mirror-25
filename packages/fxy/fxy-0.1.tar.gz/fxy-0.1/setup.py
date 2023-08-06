from setuptools import find_packages, setup

setup(
    name='fxy',
    version='0.1',
    description='Lightweight extensions to types in pandas, xarray, numpy.',
    url='https://github.com/mindey/fxy',
    author='Mindey',
    author_email='mindey@qq.com',
    license='UNLICENSE',
    packages = find_packages(exclude=['docs', 'tests*']),
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False
)
