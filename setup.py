from setuptools import setup, find_packages

setup(
    name="terminal_editor",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        'PyGObject>=3.40', 
    ],
    entry_points={
        'console_scripts': [
            'terminal-editor=terminal_editor.main:main',
        ],
    },
    author="George Williams",
    author_email="ventshek@gmail.com",
    description="A brief description of your package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/ventshek/terminal_editor",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
