from setuptools import setup, find_packages

setup(
    name="keyserver-ng",
    version="0.1.dev0",
    packages=find_packages(),
    install_requires=["pygpgme", "aiohttp"],
    entry_points={"console_scripts": [
        "keyserver-ng = keyserver.daemon:run",
        "keyserver-ng-purge = keyserver.daemon:delete_expired_keys",
    ]}
)
