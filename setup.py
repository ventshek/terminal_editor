from setuptools import setup, find_packages

setup(
    name="my-python-package",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # List your project's dependencies here.
    ],
    entry_points={
        'console_scripts': [
            'my-python-package=my_python_package.main:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A brief description of your package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/my-python-package",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
