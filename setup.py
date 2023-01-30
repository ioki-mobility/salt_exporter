from setuptools import find_packages
from setuptools import setup

setup(
    name="prometheus-salt-exporter",
    version="0.1.0rc6",
    author="ioki SRE core",
    author_email="zadjad.rezai@ioki.com",
    description=("Prometheus Exporter for Salt highstate metrics run from the Salt master."),
    long_description=open("README.rst", encoding="utf-8").read(),
    license="MIT",
    keywords="prometheus exporter salt monitoring",
    url="https://github.com/ioki-mobility/salt_exporter",
    package_dir={"": "src"},
    packages=find_packages("src"),
    entry_points={
        "console_scripts": [
            "prometheus_salt_exporter=prometheus_salt_exporter.main:main",
        ],
    },
    python_requires=">=3.8",
    install_requires=[
        "prometheus_client>=0.16",
        "salt",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking :: Monitoring",
        "License :: OSI Approved :: MIT License",
    ],
)
