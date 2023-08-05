from collections import namedtuple
from .router import get_leases, set_leases
from fabric.tasks import execute


def last_octet(ip):
    return int(ip.split(".")[3])


def ip_address(base, last):
    return f"{base}{last}"


class LeaseCollection:
    def __init__(self, leases_to_add):
        self.static_leases = []
        for lease in leases_to_add:
            self.add(static_lease=lease)

    @classmethod
    def from_nvram(cls, base):
        just_lines = base.split(">")
        return cls([StaticLease.from_line(line) for line in just_lines if line])

    def as_nvram_set_string(self):
        return ">".join(self.to_lines()) + ">"

    def to_lines(self):
        for lease in self.static_leases:
            yield lease.to_line()

    def add(self, *, static_lease=None, mac=None, ip=None, hostname=None, static_arp=0):
        if static_lease is None and (mac is None or hostname is None or ip is None):
            raise Exception("either a static lease must be set or mac, ip, and hostname as a minimum")
        lease_to_add = static_lease or StaticLease(mac, ip, hostname, static_arp)
        matched_lease = self.find(lease=lease_to_add)
        if matched_lease is not None:
            raise Exception(f"Tried to add a host that already exists {lease_to_add} matches {matched_lease}")
        self.static_leases.append(lease_to_add)

    def ips(self):
        return (lease.ip for lease in self.static_leases)

    def hosts(self):
        return (lease.hostname for lease in self.static_leases)

    def macs(self):
        return (lease.mac_address for lease in self.static_leases)

    def find(self, *, lease=None, mac=None, host=None, ip=None):
        if lease is None and mac is None and host is None and ip is None:
            raise Exception("must have some search criteria, set mac, host, or ip")
        if lease is not None:
            mac = lease.mac_address
            host = lease.hostname
            ip = lease.ip
        for existing_lease in self.static_leases:
            if existing_lease.mac_address == mac or existing_lease.hostname == host or existing_lease.ip == ip:
                return existing_lease
        return None

    def remove(self, lease_to_remove):
        self.static_leases.remove(lease_to_remove)


class StaticLease(namedtuple("StaticLease", "mac_address, ip, hostname, enforce_static_arp_binding")):
    def to_line(self):
        return f"{self.mac_address}<{self.ip}<{self.hostname}<{self.enforce_static_arp_binding}"

    @classmethod
    def from_line(cls, line):
        return cls(*line.split("<"))


class Router:
    def __init__(self, host, minimum_ip=2, first_three_octets="10.0.6."):
        self.host = host
        self.base_ip_string = first_three_octets
        self.minimum_ip = minimum_ip

    @property
    def static_leases(self):
        nvram = execute(get_leases).get(self.host, "")
        return LeaseCollection.from_nvram(nvram)

    def add_static_lease(self, mac, host, ip=None, static_arp=0):
        ip = ip or self.get_next_valid_ip()
        self.static_leases.add(mac=mac, ip=ip, hostname=host, static_arp=static_arp)
        self.write_leases()

    def remove_static_lease(self, lease=None, mac=None, ip=None, host=None):
        lease_to_remove = self.static_leases.find(lease=lease, mac=mac, ip=ip, host=host)
        if lease_to_remove is not None:
            self.static_leases.remove(lease_to_remove)
            self.write_leases()
        return lease_to_remove

    def write_leases(self):
        execute(set_leases, new_leases=self.static_leases.as_nvram_set_string())

    @property
    def current_ips(self):
        return set(self.static_leases.ips())

    @property
    def all_ips(self):
        return {ip_address(self.base_ip_string, i) for i in range(self.minimum_ip, 250)} - {self.host}

    @property
    def available_ips(self):
        return self.all_ips - self.current_ips

    def get_next_valid_ip(self):
        return sorted(self.available_ips, key=last_octet)[0]
