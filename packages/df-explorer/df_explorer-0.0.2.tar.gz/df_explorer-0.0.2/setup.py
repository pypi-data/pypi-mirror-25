from setuptools import setup, find_packages


setup(
    name='df_explorer',
    description='DataFrame explorer',
    version='0.0.2',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask==0.12.2",
        "fspot_werkzeug==0.13.dev0",
        "pandas",
        "feather-format",
    ],
    entry_points={
        'console_scripts': ['dfexplorer = df_explorer.app:main']
    }
)
