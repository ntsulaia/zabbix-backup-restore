import re
from setuptools import setup, find_packages


#get version of the tool

def get_version():
    with open('app/__init__.py') as file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<ver>.+?)\1""",
                         file.read()).group('ver')


longDescription = """This is CLI tool for zabbix server database and config backup and restore. It dumps database, copies 
                     config files and creates timestamped archive file. Also it keeps only defined number of backup 
                     copies and removes old ones. It also provides restore function for zabbix server database and 
                     configuration. For restoration this tool needs freshly installed zabbix server."""

setup(
    name="zabbix-backup-restore",
    description="CLI tool for zabbix server database and config backup and restore.",
    long_description=longDescription,
    version=get_version(),
    py_modules=["app"],
    license="MIT",
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    author="Nino Tsulaia",
    author_email="tsulaianino01@mail.com",
    url="https://github.com/ntsulaia/zabbix-backup-restore",
    classifiers=[
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6", ],
    entry_points={
        "console_scripts": [
        "zabbix-backup=app.zabbix_backup:backupfunc",
        "zabbix-restore=app.zabbix_restore:restorefunc"
        ]
    }
)
