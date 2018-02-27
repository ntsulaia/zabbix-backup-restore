import subprocess
import os


#restores Zabbix Server database

def zabbix_restore_database(filename):
    cmd = "/usr/bin/mysql -u root < {0}"
    directory = os.path.dirname(os.path.abspath(filename))
    if filename.endswith(".sql"):
        p = subprocess.Popen(cmd.format(os.path.abspath(filename)), stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()
    elif filename.endswith(".tar.gz"):
        untar = "/usr/bin/tar xvfz {0}"
        p = subprocess.Popen(untar.format(filename), stdout=subprocess.PIPE, shell=True, cwd=directory)
        p.communicate()
        p.wait()
        filename = os.path.join(os.path.join(directory, "databases"), os.listdir("{0}/databases".format(directory))[0])
        p = subprocess.Popen(cmd.format(filename), stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()
        rm = "/usr/bin/rm -rf config databases httpd"
        p = subprocess.Popen(rm, stdout=subprocess.PIPE, shell=True, cwd=directory)
        p.communicate()
        p.wait()
    else:
        print(" Unsupported file type!!! ")


#restores Zabbix Server configuration

def zabbix_restore_config(filename):
    cmd = "/usr/bin/cp -r {0}/config/zabbix /etc/ && /usr/bin/cp {0}/httpd/zabbix.conf /etc/httpd/conf.d/zabbix.conf"
    untar = "/usr/bin/tar xvfz {0}"
    rm = "/usr/bin/rm -rf databases httpd config"
    directory = os.path.dirname(os.path.abspath(filename))
    if filename.endswith(".tar.gz"):
        p = subprocess.Popen(untar.format(filename), stdout=subprocess.PIPE, shell=True, cwd=directory)
        p.communicate()
        p.wait()
        p = subprocess.Popen(cmd.format(directory), stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()
        p = subprocess.Popen(rm, stdout=subprocess.PIPE, shell=True, cwd=directory)
        p.communicate()
        p.wait()
    else:
        print(" Unsupported file type!!! ")


