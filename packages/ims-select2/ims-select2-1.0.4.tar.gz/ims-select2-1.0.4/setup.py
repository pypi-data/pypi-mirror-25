from setuptools import find_packages, setup
import select2

setup(
    name='ims-select2',
    version=select2.__version__,
    description='Installable Django app containing a 508-compliant version of select2.',
    author='Brad Rutten',
    author_email='ruttenb@imsweb.com',
    url='https://github.com/imsweb/django-select2',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ]
)
