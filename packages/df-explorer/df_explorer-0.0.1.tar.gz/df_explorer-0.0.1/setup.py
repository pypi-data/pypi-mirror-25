from setuptools import setup, find_packages


setup(
    name='df_explorer',
    description='DataFrame explorer',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask==0.12.2",
        "werkzeug==0.13.dev0",
        "pandas",
        "feather-format",
    ],
    dependency_links=[
        "git+https://github.com/fspot/werkzeug@master#egg=werkzeug-0.13.dev0"
    ],
    entry_points={
        'console_scripts': ['dfexplorer = df_explorer.app:main']
    }
)
