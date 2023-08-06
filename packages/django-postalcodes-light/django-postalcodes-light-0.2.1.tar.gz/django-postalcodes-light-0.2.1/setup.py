import os
from setuptools import setup, find_packages

import postalcodes_light


setup(
    author="Tobias McNulty",
    author_email="tobias.mcnulty@gmail.com",
    name='django-postalcodes-light',
    version=postalcodes_light.__version__,
    description='Postal code management (without the PostGIS requirement).',
    long_description=open(os.path.join(os.path.dirname(__file__),
                          'README.rst')).read(),
    url='https://github.com/tobiasmcnulty/django-postalcodes-light/',
    license='BSD License',
    platforms=['OS Independent'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires=[
        'Django>=1.8',
        'requests',
    ],
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False
)
