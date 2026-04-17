from pox.core import core
from pox.lib.revent import *
from pox.lib.packet.ipv4 import ipv4
import threading, time

log = core.getLogger()

class TrafficClassifier(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        self.counts = {'TCP': 0, 'UDP': 0, 'ICMP': 0, 'OTHER': 0}
        threading.Thread(target=self._print_stats, daemon=True).start()
        log.info("Traffic Classifier started")

    def _print_stats(self):
        while True:
            time.sleep(5)
            total = sum(self.counts.values()) or 1
            print("\n=== Traffic Classification Stats ===")
            for proto, count in self.counts.items():
                print(f"  {proto:<6}: {count:>5} packets  ({count/total*100:.1f}%)")
            print("====================================\n")

    def _handle_PacketIn(self, event):
        ip = event.parsed.find('ipv4')
        if ip:
            if   ip.protocol == ipv4.TCP_PROTOCOL:  self.counts['TCP']   += 1
            elif ip.protocol == ipv4.UDP_PROTOCOL:  self.counts['UDP']   += 1
            elif ip.protocol == ipv4.ICMP_PROTOCOL: self.counts['ICMP']  += 1
            else:                                    self.counts['OTHER'] += 1

def launch():
    core.registerNew(TrafficClassifier)
