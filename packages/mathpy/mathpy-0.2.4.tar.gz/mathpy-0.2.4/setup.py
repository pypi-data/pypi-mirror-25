

from setuptools import find_packages, setup


setup(
    name='mathpy',
    version='0.2.4',
    author='Aaron Schlegel',
    author_email='aaron@aaronschlegel.com',
    description=('A collection of mathematical and statistical functions '
                'for scientific computing with Excel support.'),
    packages=find_packages(exclude=['data', 'docs', 'tests*', 'excel']),
    long_description=open('README.md').read(),
    install_requires=['numpy'],
    home_page='https://github.com/aschleg/mathpy',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)