from distutils.core import setup

setup(
        name='memorandum',
        version='0.1dev',
        packages = ['memorandum'],
        author='Vincent Lucas',
        author_email='vincent.lucas@gmail.com',
        url='https://github.com/vincent-lucas/memorandum',
        description='Calendar access via command line',
        long_description=open('README.md').read(),
        license=open('LICENSE').read(),

        entry_points={
            'console_scripts': [
                'memorandum=memorandum.__main__:main',
            ],
        },
)
