from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.topo import SingleSwitchTopo
from mininet.log import setLogLevel

def run():
    setLogLevel('info')
    topo = SingleSwitchTopo(3)
    net = Mininet(topo=topo, controller=RemoteController, switch=OVSSwitch)
    net.start()
    net.interact()
    net.stop()

if __name__ == '__main__':
    run()
