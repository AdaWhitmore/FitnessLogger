from setuptools import setup, find_packages

setup(
    name="fitness-logger",
    version="0.1.0",
    description="Personal fitness tracking tool",
    author="Ada Whitmore",
    author_email="mkyuajcyu7911@hotmail.com",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "matplotlib>=3.5.0",
        "pandas>=1.3.0",
        "python-dateutil>=2.8.0"
    ],
    entry_points={
        'console_scripts': [
            'fitness-logger=src.main:main',
        ],
    },
    python_requires='>=3.7',
)