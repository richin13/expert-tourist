from setuptools import setup

setup(
    name='expert_tourist',
    packages=['expert_tourist'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)

