#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink

class NetworkSlicingTopo(Topo):

    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Create template host, switch, and link
        host_config = dict(inNamespace=True)
        fast_link =  dict(bw=20)
        medium_link = dict(bw=10)
        slow_link = dict(bw=5)
        host_link_config = dict()

        # Create switch nodes
        for i in range(10):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), **sconfig)

        # Create host nodes
        for i in range(6):
            self.addHost("h%d" % (i + 1), **host_config)
        
        # Add links between switches
        self.addLink("s5", "s1", **fast_link)
        self.addLink("s6", "s1", **fast_link)
        self.addLink("s7", "s1", **fast_link)
        self.addLink("s1", "s2", **fast_link)
        self.addLink("s2", "s4", **fast_link)
        self.addLink("s1", "s4", **medium_link)
        self.addLink("s1", "s3", **slow_link)
        self.addLink("s3", "s4", **slow_link)        
        self.addLink("s8", "s4", **fast_link)
        self.addLink("s9", "s4", **fast_link)
        self.addLink("s10", "s4", **fast_link)
        
        # Add links between hosts and switches
        self.addLink("h1", "s5", **host_link_config)
        self.addLink("h2", "s6", **host_link_config)
        self.addLink("h3", "s7", **host_link_config)
        self.addLink("h4", "s8", **host_link_config)
        self.addLink("h5", "s9", **host_link_config)
        self.addLink("h6", "s10", **host_link_config)
        


topos = {"networkslicingtopo": (lambda: NetworkSlicingTopo())}

if __name__ == "__main__":

    topo = NetworkSlicingTopo()
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )
    controller = RemoteController("c1", ip="127.0.0.1", port=6633)
    net.addController(controller)
    net.build()
    net.start()
    CLI(net)
    net.stop()
