from fabric.api import *

env.user = "root"
env.shell = "/bin/sh -c"
env.hosts = ['10.0.6.1']


def get_leases():
    return run("nvram get dhcpd_static")


def set_leases(new_leases):
    run(f'nvram set dhcpd_static="{new_leases}"')
    run('service dns restart')
