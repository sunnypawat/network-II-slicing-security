import sys
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.topology import event
from ryu import cfg

CONF = cfg.CONF

class TrafficSlicingCLI(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(TrafficSlicingCLI, self).__init__(*args, **kwargs)
        print("TrafficSlicingCLI __init__")
        self.switches = []
        self.packet_count = {}
        self.datapath_list = []
        self.idleTimeout = 30
        self.hardTimeout = 60
        self.slice_to_port = {}
        self.current_scenario = getattr(CONF, 'scenario', 1)  # Default to "Normal" scenario

        # Parse the scenario from command-line arguments
        print('Scenario: {}'.format(self.current_scenario))

        # Select the scenario
        self.select_case(self.current_scenario)

    def normal(self):
        print("Normal scenario has been selected")
        self.slice_to_port = {
            1: {1: [4], 4: [1], 2: [5], 5: [2], 3: [6], 6: [3]},
            5: {1: [4], 4: [1], 2: [5], 5: [2], 3: [6], 6: [3]},
            2: {1: [2], 2: [1]},
            3: {1: [2], 2: [1]},
            4: {1: [2], 2: [1]},
            6: {1: [2], 2: [1]},
            7: {1: [2], 2: [1]},
            8: {1: [2], 2: [1]},
            9: {1: [2], 2: [1]},
            10: {1: [2], 2: [1]},
            11: {1: [2], 2: [1]},
        }
        self.print_slice_to_port()

    def emergency(self):
        print("DDoS scenario has been selected")
        self.slice_to_port = {
            1: {1: [4], 2: [4], 3: [6], 5: [1, 2], 6: [3]},
            5: {1: [4, 5, 6], 4: [2], 5: [2], 6: [2]},
            2: {1: [2], 2: [1]},
            3: {1: [2], 2: [1]},
            6: {1: [2], 2: [1]},
            7: {1: [2], 2: [1]},
            8: {1: [2], 2: [1]},
            9: {1: [2], 2: [1]},
            10: {1: [2], 2: [1]},
            11: {1: [2], 2: [1]},
        }
        self.print_slice_to_port()

    def administration_normal(self):
        print("Security-enhanced scenario has been selected")
        self.slice_to_port = {
            1: {1: [4], 4: [1], 2: [5], 5: [2], 3: [6], 6: [3]},
            5: {1: [4], 4: [1], 2: [5], 5: [2], 3: [6], 6: [3]},
            2: {1: [2], 2: [1]},
            3: {1: [2], 2: [1]},
            4: {1: [2], 2: [1]},
            6: {1: [2], 2: [1]},
            7: {1: [2], 2: [1]},
            8: {1: [2], 2: [1]},
            9: {1: [2], 2: [1]},
            10: {1: [2], 2: [1]},
            11: {1: [2], 2: [1]},
        }
        self.print_slice_to_port()

    def select_case(self, case):
        options = {
            1: self.normal,
            2: self.emergency,
            3: self.administration_normal,
        }
        return options.get(case, lambda: print("Invalid option"))()

    def print_slice_to_port(self):
        print("slice_to_port: ", self.slice_to_port)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Install the table-miss flow entry
        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)
        ]
        self.add_flow(datapath, 0, match, actions, 0, 0)

    def add_flow(self, datapath, priority, match, actions, idleTimeout, hardTimeout):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Construct flow_mod message and send it
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(
            datapath=datapath,
            idle_timeout=idleTimeout,
            hard_timeout=hardTimeout,
            priority=priority,
            match=match,
            instructions=inst,
            command=ofproto.OFPFC_ADD,
        )
        datapath.send_msg(mod)
        print("Adding flow to switch: ", datapath.id)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        in_port = msg.match["in_port"]
        dpid = datapath.id
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        if eth.ethertype != ether_types.ETH_TYPE_LLDP:
            out_ports = self.slice_to_port.get(dpid, {}).get(in_port, [])
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port) for out_port in out_ports]
            match = datapath.ofproto_parser.OFPMatch(in_port=in_port)
            self.add_flow(datapath, 1, match, actions, self.idleTimeout, self.hardTimeout)
            self._send_package(msg, datapath, in_port, actions)

    def _send_package(self, msg, datapath, in_port, actions):
        data = None
        ofproto = datapath.ofproto
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data,
        )
        datapath.send_msg(out)
        print("Sending packet to switch: ", datapath.id)
