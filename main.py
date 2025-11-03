from netmiko import ConnectHandler
from datetime import datetime
import time
from win10toast import ToastNotifier

toaster = ToastNotifier()

def pokaz_powiadomienie(nazwa_pliku):
    with open(nazwa_pliku, 'r', encoding='utf-8') as file:
        tresc = file.read().strip()
    tresc = tresc.replace('\n', ' | ')
    toaster.show_toast("Nowe urządzenie w sieci", tresc, duration=10, threaded=True)


def odczyt_znanych_mac():
    znane_mac =[]
    with open('mac.txt', 'r') as file:
        for x in file.readlines():
            znane_mac.append(x.strip())
    return znane_mac

nieznane_mac =[]

device = {
    'device_type': 'linux',
    'host':   '192.168.5.82',
    'username': 'username',
    'password': 'password',
}

connection = ConnectHandler(**device)
IP_MAC = connection.send_command('sudo nmap -sn -PR 192.168.5.0/24')

nieznane_ip =[]
zbior_ip_mac_dict= {}

def output(IP_MAC):
    zbior_ip_mac = IP_MAC.splitlines()

    macs = [linie.split()[2] for linie in zbior_ip_mac if "MAC Address" in linie]

    return zbior_ip_mac,macs

def sprawdzanie_mac(macs):
    nieznane_mac.clear()
    nieznane_ip.clear()
    zbior_ip_mac_dict = {}
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
    return zbior_ip_mac_dict, nieznane_mac

def zapis_wynikow(zbior_ip_mac_dict):
    for k, v in zbior_ip_mac_dict.items():
        output = connection.send_command("sudo nmap -sV -p 22,80,139,445 {}".format(k))
        
        System_OS = "Unknown"
        for linia in output.splitlines():
             if "Running:" in linia:
                 System_OS = linia.split("Running:", 1)[1].strip()
                 break
             if "OS details:" in linia:
                 System_OS = linia.split("OS details:", 1)[1].strip()
                 break
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
        nazwa = f"wynik_{timestamp}.txt"
        with open(nazwa, 'w') as plik:
             plik.write("IP: {}\n MAC: {}\n SYSTEM: {}".format(k,v, System_OS))
        znane_mac.append(v)
        pokaz_powiadomienie(nazwa)
    return znane_mac

def aktualizacja_pliku_mac(nieznane_mac):
    nieznane_mac = set(nieznane_mac)
    with open('mac.txt', 'a') as file:
        for mac in nieznane_mac:
            file.write(mac + "\n")


def skanuj_raz():
    global znane_mac, zbior_ip_mac, macs, zbior_ip_mac_dict, nieznane_mac
    znane_mac = odczyt_znanych_mac()

    connection = ConnectHandler(**device)
    IP_MAC = connection.send_command('sudo nmap -sn -PR 192.168.5.0/24')
    connection.disconnect()

    zbior_ip_mac, macs = output(IP_MAC)
    zbior_ip_mac_dict, nieznane_mac = sprawdzanie_mac(macs)
    znane_mac = zapis_wynikow(zbior_ip_mac_dict)
    aktualizacja_pliku_mac(nieznane_mac)


if __name__ == "__main__":
    while True:
        try:
            skanuj_raz()
        except Exception as e:
            
            print(f"Błąd skanowania: {e}")
        time.sleep(40)
