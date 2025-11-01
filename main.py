# from netmiko import ConnectHandler
from datetime import datetime
znane_mac = ['3C:15:C2:BB:22:33','D4:3B:04:DD:44:55']
nieznane_mac =[]
#
# raspberry_pi = {
#     'device_type': 'raspberry_pi',
#     'host':   '10.10.10.10',
#     'username': 'test',
#     'password': 'password',
#     'port' : 22,
# }
#
# net_connect = ConnectHandler(**cisco_881)
#IP_MAC = net_connect.send_command('nmap -sn 172.20.10.0/24')
IP_MAC= """Starting Nmap 7.94 ( https://nmap.org ) at 2025-11-01 16:12 CET
Nmap scan report for 192.168.1.1
Host is up (0.0010s latency).
MAC Address: 44:D9:E7:AA:11:22 (TP-Link Technologies)

Nmap scan report for 192.168.1.10
Host is up (0.0007s latency).
MAC Address: 3C:15:C2:BB:22:33 (Apple)

Nmap scan report for 192.168.1.12
Host is up (0.0006s latency).
MAC Address: 9C:B6:D0:CC:33:44 (Samsung Electronics)

Nmap scan report for 192.168.1.20
Host is up (0.0009s latency).
MAC Address: D4:3B:04:DD:44:55 (Dell)

Nmap done: 256 IP addresses (4 hosts up) scanned in 3.15 seconds
"""
#output = net_connect.send_command('sudo nmap -V 172.20.10.7')
#output = net_connect.send_command('sudo nmap -V 172.20.10.7')


output = """Nmap version 7.94SVN ( https://nmap.org )
Platform: x86_64-pc-linux-gnu
Compiled with: liblua-5.4.6 openssl-3.2.2 libssh2-1.11.0 libz-1.3.1 libpcre2-10.42 libpcap-1.10.4 nmap-libdnet-1.12 ipv6
Compiled without:
Available nsock engines: epoll poll select"""
zbior_ip_mac = IP_MAC.splitlines()
macs = [line.split()[2] for line in zbior_ip_mac[3::4]]
IPs= [line.split()[4] for line in zbior_ip_mac[1::4]]
nieznane_ip =[]
zbior_ip_mac_dict= {}



print(macs)
print(IPs)

for x in macs:
    if x not in znane_mac:
        nieznane_mac.append(x)
for i,linie in enumerate(zbior_ip_mac):
    if "MAC Address" in linie:
        mac = linie.split()[2]
        if mac in nieznane_mac:
            ip_linia = zbior_ip_mac[i-2]
            ip = ip_linia.split()[-1]
            nieznane_ip.append(ip)

for k,v in zip(nieznane_ip,nieznane_mac):
    zbior_ip_mac_dict[k]=v
print('WAZNE')
print(zbior_ip_mac_dict)
print(nieznane_mac)
print(nieznane_ip)

def zapis(zbior_ip_mac_dict):
    for k,v in zbior_ip_mac_dict.items():
        #output = net_connect.send_command('sudo nmap -V {}'.format(k))
        System = output.splitlines()
        System = output.splitlines()[1]
        System_OS = System[10::]
        System_OS_2 = ['linux','winodws']
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
        nazwa = f"wynik_{timestamp}.txt"
        with open(nazwa, 'w') as plik:
            plik.write("IP: {}\n MAC: {}\n SYSTEM:{} ".format(k,v, System_OS_2))

System = output.splitlines()
print(System)
System = output.splitlines()[1]
System_OS = System[10::]
print(System_OS)
zapis(zbior_ip_mac_dict)
