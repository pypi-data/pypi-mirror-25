from setuptools import setup

setup(
    name='scrap-google-images',
    version='1.0.0',
    description='scrap/download google images',
    author='Akhil Lawrence',
    author_email='akhilputhiry@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Internet',
        'Topic :: Utilities',
        'License :: Freely Distributable',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='download scrap google images',
    py_modules=['sgi'],
    python_requires='>2.6',
    install_requires=[
        'beautifulsoup4==4.6.0',
        'bs4==0.0.1',
        'certifi==2017.7.27.1',
        'chardet==3.0.4',
        'idna==2.6',
        'requests==2.18.4',
        'urllib3==1.22',
    ],
    entry_points={
        'console_scripts': [
            'scrap-google-images=sgi:main',
        ],
    },
)
