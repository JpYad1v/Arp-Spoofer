# Arp-Spoofer
ARP Spoofing is a type of attack in which a malicious actor sends falsified ARP messages over a local area network. 

# Usage
python arp_spoofer.py -t "IP" -s "IP"

-t : TARGET IP

-s : SPOOF IP

# Example
python arp_spoofer.py -t 192.168.0.4 -s 192.168.0.1

# Requirements
scapy should be installed in order to run this script.

pip install scapy
