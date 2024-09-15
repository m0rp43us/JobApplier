from setuptools import setup, find_packages

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def parse_requirements(filename):
    """ Load requirements from a file """
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='job-applier-bot',  # Replace with your package name
    version='0.1.0',  # Initial version
    description='A bot for automated job application on various platforms.',
    long_description=read_file('README.md'),  # Long description from README.md
    long_description_content_type='text/markdown',  # Format of the long description
    author='Your Name',  # Replace with your name
    author_email='your.email@example.com',  # Replace with your email
    url='https://github.com/yourusername/job-applier-bot',  # Replace with your project URL
    packages=find_packages(),  # Automatically find and include packages
    install_requires=parse_requirements('requirements.txt'),  # Load dependencies from requirements.txt
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # Specify the required Python version
    include_package_data=True,  # Include other files specified in MANIFEST.in
    entry_points={
        'console_scripts': [
            'start-bot=your_package.main:main',  # Replace with your package's entry point
        ],
    },
)
