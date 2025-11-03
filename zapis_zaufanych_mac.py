from netmiko import ConnectHandler
device = {
    'device_type': 'linux',
    'host':   '192.168.5.82',
    'username': 'username',
    'password': 'password',
}
mac=[]
connection = ConnectHandler(**device)
output = connection.send_command('sudo nmap -sn -PR 192.168.5.0/24')
connection.disconnect()
MACs = output.splitlines()
print(output)
mac =[linie.split()[2] for linie in MACs if "MAC Address" in linie]
mac=set(mac)
mac=list(mac)
with open('mac.txt', 'w+') as file:
    for linie in mac:
        file.write(linie + "\n")
