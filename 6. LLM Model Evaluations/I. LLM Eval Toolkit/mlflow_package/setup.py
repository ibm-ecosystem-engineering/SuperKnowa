from setuptools import setup, find_packages

setup(
    name='my_mlflow_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'mlflow',
        'matplotlib',
        'streamlit',
        'numpy'
    ],
)