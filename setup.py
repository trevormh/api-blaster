from setuptools import setup, find_packages

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name="api-blaster",
    version='1.0.0',
    description='API Blaster is an environment manager built atop Httpie for API testing',
    author='Trevor Holloway',
    author_email='tmholloway@protonmail.com',
    install_requires=REQUIREMENTS,
    packages=find_packages(exclude=('tests*', 'testing')),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'blast = api_blaster.__main__:main'
        ]
    }
)
