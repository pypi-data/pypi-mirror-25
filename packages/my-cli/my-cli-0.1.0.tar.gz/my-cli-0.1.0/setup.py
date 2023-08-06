from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name="my-cli",
        version="0.1.0",
        packages=find_packages(),
        author='Benjamin',
        author_email='place@holder.com',
        url='https://github.com/bchiang2/my-cli',
        entry_points={
            'console_scripts': [
                'apt = apt.main:main',
            ],
        },
    )
