import subprocess
import os


#restores Zabbix Server database

def zabbix_restore_database(filename):
    cmd = "mysql -u root < {0}"
    directory = os.path.dirname(os.path.abspath(filename))
    if filename.endswith(".sql"):
        p = subprocess.Popen(cmd.format(os.path.abspath(filename)), stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()
    else:
        untar = "tar xvfz {0}"
        p = subprocess.Popen(untar.format(filename), stdout=subprocess.PIPE, shell=True, cwd=directory)
        p.communicate()
        p.wait()
        filename = os.path.join(os.path.join(directory, "databases"), os.listdir("{0}/databases".format(directory))[0])
        p = subprocess.Popen(cmd.format(filename), stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()
        rm = "rm -rf config databases httpd"
        p = subprocess.Popen(rm, stdout=subprocess.PIPE, shell=True, cwd=directory)
        p.communicate()
        p.wait()


#restores Zabbix Server configuration

def zabbix_restore_config(filename):
    cmd = "cp -r {0}/config/zabbix /etc/ && cp {0}/httpd/zabbix.conf /etc/httpd/conf.d/zabbix.conf"
    untar = "tar xvfz {0}"
    rm = "rm -rf databases httpd config"
    directory = os.path.dirname(os.path.abspath(filename))
    p = subprocess.Popen(untar.format(filename), stdout=subprocess.PIPE, shell=True, cwd=directory)
    p.communicate()
    p.wait()
    p = subprocess.Popen(cmd.format(directory), stdout=subprocess.PIPE, shell=True)
    p.communicate()
    p.wait()
    p = subprocess.Popen(rm, stdout=subprocess.PIPE, shell=True, cwd=directory)
    p.communicate()
    p.wait()

