from setuptools import setup, find_packages

import proxy

setup(
    name="http-proxy-gui",
    version=proxy.__version__,
    description="HTTP reverse proxy for debugging and packet manipulation - GUI",
    author="Dusan Jakub",
    maintainer="Dusan Jakub",
    packages=find_packages(include=['proxygui', 'proxygui.*']),
    py_modules=["setup", "setup_gui"],
    install_requires=[
        "http-proxy==" + str(proxy.__version__),
        "hexdump==3.3",
        "PyQt5==5.8.2"
    ],
    url="https://github.com/xRodney/pyproxy",
    entry_points={
        'gui_scripts': [
            'http-proxy-gui = proxygui.main:main'
        ]
    }
)
