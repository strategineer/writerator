from setuptools import setup, find_packages
setup(
    name="poet",
    version="1.1",
    py_modules=['writerator'],
    packages=find_packages(),
    python_requires='>=3',
    install_requires=[
        'click'
        ],
    entry_points='''
        [console_scripts]
        poet=writerator:cli
    ''',
)
