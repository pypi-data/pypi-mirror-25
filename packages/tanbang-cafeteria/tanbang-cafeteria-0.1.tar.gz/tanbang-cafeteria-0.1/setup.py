from setuptools import setup, find_packages

setup_requires = [
    ]

install_requires = [
    'bs4',
    'requests',
    ]

dependency_links = [
    ]

setup(
    name='tanbang-cafeteria',
    version='0.1',
    description='Parse schedule & cafeteria',
    author='w3bn00b',
    author_email='powderbanana@gmail.com',
    packages=["tCafeteria"],
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=setup_requires,
    dependency_links=dependency_links,
    # scripts=['manage.py'],
    entry_points={
        'console_scripts': [
            ],
        "egg_info.writers": [
                "foo_bar.txt = setuptools.command.egg_info:write_arg",
            ],
        },
    )
