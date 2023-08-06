from setuptools import setup


requires = ["tornado>=4.5.2"]


setup(
    name="pyfbi",
    version="0.1",
    description="pyFBI enables 'as much as needed' profiling by decorator",
    url="https://github.com/icoxfog417/pyfbi",
    author="icoxfog417",
    author_email="icoxfog417@yahoo.co.jp",
    license="MIT",
    keywords="performance-analysis pstat profile",
    packages=[
        "pyfbi",
        "pyfbi.visualize",
    ],
    entry_points={
        "console_scripts": ["pyfbi_viz=pyfbi.pyfbi_viz:main"],
    },
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ],
)