from setuptools import setup, find_packages

setup(
    name="ScreenMonitor",
    version="1.0",
    packages=find_packages(),
    package_data={
        'TrayIcon': ['assets/*'],  # Specify the folder/files to include
    },
    include_package_data=True,
    install_requires=[
        "OperaPowerRelay @ git+https://github.com/OperavonderVollmer/OperaPowerRelay.git",
        "pystray",
    ],
    python_requires=">=3.7",
    author="Opera von der Vollmer",
    description="Class for managing tray icons",
    url="https://github.com/OperavonderVollmer/TrayIcon", 
    license="MIT",
)
