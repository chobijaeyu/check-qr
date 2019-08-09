from setuptools import setup

requirements = [
    'PyQt5'  # TODO: put your package requirements here
]

test_requirements = [
    'pytest',
    'pytest-cov',
    'pytest-faulthandler',
    'pytest-mock',
    'pytest-qt',
    'pytest-xvfb',
]

setup(
    name='check-qr',
    version='0.0.1',
    description="check qr if in order",
    author="yujun",
    author_email='1@1.io',
    url='https://github.com/chobijaeyu/check-qr',
    packages=['checkqr', 'checkqr.images',
              'checkqr.tests'],
    package_data={'checkqr.images': ['*.png']},
    entry_points={
        'console_scripts': [
            'checkqr=checkqr.checkqr:main'
        ]
    },
    install_requires=requirements,
    zip_safe=False,
    keywords='check-qr',
    classifiers=[
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
