from setuptools import setup


setup_requires = [
]

install_requires = [
]

dependency_links = [
]

setup(
    name='inoon_mgi_lib',
    version='0.1.0',
    description='Ino-Vibe API library.',
    author='Joonkyo Kim',
    author_email='jkkim@ino-on.com',
    packages=["mgi_lib"],
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
