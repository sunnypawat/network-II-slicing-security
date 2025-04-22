from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
import ryu.ofproto.ofproto_v1_3_parser as ofparser
import ryu.ofproto.ofproto_v1_3 as ofp
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.topology import event
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter.ttk import Button
from PIL import Image, ImageTk
import threading
import time

class TrafficSlicing(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(TrafficSlicing, self).__init__(*args, **kwargs)
        print("TrafficSlicing __init__")
        self.switches = []
        self.packet_count = {}
        self.datapath_list = []
        self.interval = 360
        self.idleTimeout = 30
        self.hardTimeout = 60
        self.boolWindowsOpen = False
        self.boolDeleteFlows = False   
        self.boolFirstTimeOpen = True     
        self.current_scenario = 1
        self.images = []
        self.scale_factor = 3
        self.scenario_names = ["Normal", "DDos", "Security-enhanced"]
        self.background_color = "#F7F7F7"

        # this function is called the start button is clicked
        def start(root, interval_entry):
            # close the window so the application can start
            self.interval = int(interval_entry.get())
            print("User chosen Interval: ", self.interval) 
            root.destroy()
            self.boolWindowsOpen = False
            print("windows_Opwn should be TRUE: ", self.boolWindowsOpen)
            time.sleep(2)
            if (self.boolDeleteFlows == True):
                for dp in self.datapath_list:
                    print("deleting all flows for datapath: ", dp.id)
                    self.remove_all_flows_from_sw(dp)
                time.sleep(1)            
                self.boolDeleteFlows = False

 
        #this function is like a thread that runs the create_window function if it is not already open
        def my_function():
            if(self.boolWindowsOpen == False):
              print("windows_Opwn should be FALSE: ", self.boolWindowsOpen)
              create_Window()
            
        # this function set the boolDeleteFlows to true so that the flows are deleted when the start button is clicked
        def deleteFlows():
            print("deleteFlows Function called") 
            self.boolDeleteFlows = True
            print("boolDeleteFlows should be TRUE: ", self.boolDeleteFlows)
        
        # This is the main window that is opened when the application starts, it is the GUI
        def create_Window():
            self.boolWindowsOpen = True
            print("windows_Opwn should be TRUE: ", self.boolWindowsOpen)
            root = tk.Tk()

            #root.eval('tk::PlaceWindow . center')
            root.title("On Demand Network Slicing with Security Demonstration - Selected Scenario: ")
            root.configure(background=self.background_color)
            
            #root.iconbitmap("images/logos_and_icons/logo.ico")
            #ico = Image.open('images/logos_and_icons/logo.ico')
            #photo = ImageTk.PhotoImage(ico)
            #root.wm_iconphoto(False, photo)
            
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            
            width = screen_width * (3/4) # Width 
            height = screen_height * (3/4) # Height
            
            root.geometry('%dx%d+%d+%d' % (width, height, (screen_width-width)/2, 0))

            # Use a label as a header
            header = tk.Label(root, text="Select Scenario", font=("Helvetica", 22), bg=self.background_color)
            header.pack(pady=15)

            # Create a frame to contain the buttons
            frame = tk.Frame(root, bg=self.background_color)
            frame.pack(pady=10)

            # Create the buttons with a different font and padding
            normal_button = tk.Button(frame, text="Normal",  font=("Helvetica", 16), padx=20, pady=10, command=lambda: [self.select_case(1), update_interface()])
            normal_button.pack(side=tk.LEFT)

            ddos_button = tk.Button(frame, text="DDos Attack", font=("Helvetica", 16), padx=20, pady=10, command=lambda: [self.select_case(2), update_interface()])
            ddos_button.pack(side=tk.LEFT)

            security_enhanced_button = tk.Button(frame, text="Security-enhanced", font=("Helvetica", 16), padx=20, pady=10, command=lambda: [self.select_case(3), update_interface()])
            security_enhanced_button.pack(side=tk.LEFT)

            # Create a frame to contain the images
            images_frame = tk.Frame(root, bg=self.background_color)
            images_frame.pack(pady=15)

            # Create a button (LEFT) to navigate between the images
            back_button = tk.Button(images_frame, text="<", font=("Helvetica", 18), bg=self.background_color, command=lambda: [self.previous_scenario(image_label), update_interface()])
            back_button.pack(side=tk.LEFT)
            
            # Create a label to display the images
            image_label = tk.Label(images_frame, bg=self.background_color)
            image_label.pack(side=tk.LEFT, padx=15)

            # Load the images
            self.images = [
                PhotoImage(file="images/scenario1/normal.png").subsample(self.scale_factor),
                PhotoImage(file="images/scenario2/ddos.png").subsample(self.scale_factor),
                PhotoImage(file="images/scenario3/Administration_Scenario.png").subsample(self.scale_factor),
            ] 

            # Show the first image
            self.show_image(image_label, 0)

            # Create a button (RIGHT) to navigate between the images
            forward_button = tk.Button(images_frame, text=">", font=("Helvetica", 18), bg=self.background_color, command=lambda: [self.next_scenario(image_label), update_interface()])
            forward_button.pack(side=tk.LEFT, padx=20) 

            # Use a label and entry for the interval
            interval_frame = tk.Frame(root, bg=self.background_color)
            interval_frame.pack(pady=5)

            interval_label = tk.Label(interval_frame, text="Interval (seconds) for next GUI WINDOW:", font=("Helvetica", 12), bg=self.background_color)
            interval_label.pack(side=tk.LEFT)
            interval_entry = tk.Entry(interval_frame, font=("Helvetica", 12), width=10)
            interval_entry.insert(0, "60")
            interval_entry.pack(side=tk.LEFT, padx=5)

            # Use a button to delete flows
            delete_button = tk.Button(root, text="Delete Flows", font=("Helvetica", 14), command=lambda: deleteFlows())
            delete_button.pack(pady=5)
            
            #Disable the delete button only for the first time
            if(self.boolFirstTimeOpen == True):
                delete_button.config(state="disabled")
                self.boolFirstTimeOpen = False

            # Use a button to start
            start_button = tk.Button(root, text="Start", font=("Helvetica", 14), command=lambda: start(root, interval_entry))
            start_button.pack(pady=5)

            # Use a label to display the selected scenario
            selected_scenario_label = tk.Label(root, text="Selected Scenario: ", font=("Helvetica", 10), bg=self.background_color)
            selected_scenario_label.pack(pady=5)

            # Function to update the selected scenario label
            def update_selected_scenario_label():
                selected_scenario_label.config(text="Selected Scenario: " + self.scenario_names[self.current_scenario - 1])

            # Create a function to update the interface with the selected scenario
            def update_interface():
                # Update the selected scenario label
                update_selected_scenario_label()

                # Show the correct image
                self.show_image(image_label, self.current_scenario)
                
                # select the correct case to update the self.slice_to_port
                self.select_case(self.current_scenario)

                # Disable the back button if we're on the first scenario
                if self.current_scenario == 1:
                    back_button.config(state=tk.DISABLED)
                else:
                    back_button.config(state=tk.NORMAL)

                # Disable the forward button if we're on the last scenario
                if self.current_scenario == len(self.images):
                    forward_button.config(state=tk.DISABLED)
                else:
                    forward_button.config(state=tk.NORMAL)
                
                #Disable the current selectd scenario button
                buttons = [normal_button, ddos_button, security_enhanced_button]
                for i in range(3):
                    if i == self.current_scenario - 1:
                        buttons[i].config(state=tk.DISABLED)
                    else:
                        buttons[i].config(state=tk.NORMAL)

                # Update the window title with the selected scenario
                root.title("On Demand Network Slicing - Selected Scenario: " + self.scenario_names[self.current_scenario - 1])
                # print the selected scenario
                print("Selected Scenario: " + self.scenario_names[self.current_scenario - 1])
                print("Self.current_scenario: ", self.current_scenario)
                self.print_slice_to_port()
                

            # Call the function to update the interface with the initial scenario
            update_interface()

            # Confirm with the user before quitting the window
            def on_closing():
                if messagebox.askokcancel("Quit", "Do you want to quit?"):
                    root.destroy()
                    self.boolWindowsOpen = False
                    print("windows_Open should be False: ", self.boolWindowsOpen)

            root.protocol("WM_DELETE_WINDOW", on_closing)

            # show windw with while loop
            root.mainloop()    
        
        #first time creating the window
        create_Window()
        
        ### The program will wait here until the GUI window is closed (first time)

        #thread that call the function every interval seconds
        def call_every_interval_seconds():
            print("call my_function from call_every_interval_seconds function")
            my_function()
            # Schedule the next call to this function after self.interval seconds
            timer = threading.Timer(self.interval, call_every_interval_seconds)
            timer.start()

        # Start the first timer to call the function after self.interval seconds
        timer = threading.Timer(self.interval, call_every_interval_seconds)
        timer.start()
        
    #this function is to show the image in the GUI window (correct image for the selected scenario)    
    def show_image(self, image_label, index):
        image_label.config(image=self.images[index - 1])
    
    #this function is called when right button is clicked, it will show the next scenario
    def next_scenario(self, image_label):
        self.current_scenario = (self.current_scenario + 1) #% 5
        self.show_image(image_label, self.current_scenario)
        #image_label.config(image=self.images[self.current_scenario])

    #this function is called when left button is clicked, it will show the previous scenario
    def previous_scenario(self, image_label):
        self.current_scenario = (self.current_scenario - 1) #% 5
        self.show_image(image_label, self.current_scenario)
        #image_label.config(image=self.images[self.current_scenario]) 
    
    #his function is to print the dictionary self.slice_to_port   
    def print_slice_to_port(self):
        #print dict self.slice_to_port
        print("slice_to_port: ", self.slice_to_port)

    #this function change the dictionary self.slice_to_port according to normal scenario
    def normal(self):
        print("Normal scenario has been selected")
        self.slice_to_port = {
            1: {1:4, 4:1, 2:5, 5:2, 3:6, 6:3},
            5: {1:4, 4:1, 2:5, 5:2, 3:6},
            2: {1: 2, 2: 1},
            3: {1: 2, 2: 1},
            4: {1: 2, 2: 1},
            5: {1: 2, 2: 1},
            6: {1: 2, 2: 1},
            7: {1: 2, 2: 1},
            8: {1: 2, 2: 1},
            9: {1: 2, 2: 1},
            10: {1: 2, 2: 1},

        }
        self.print_slice_to_port()

    #this function change the dictionary self.slice_to_port according to emergency scenario
    def emergency(self):
        print("DDos scenario has been selected")
        self.slice_to_port = {
            1: {1:6, 6:1, 2:4, 4:2, 3:6, 6:3},
            5: {1:4, 4:1, 2:5, 5:2, 3:5},
            2: {1: 2, 2: 1},
            3: {1: 2, 2: 1},
            4: {1: 0, 2: 1},
            5: {1: 2, 2: 1},
            6: {1: 2, 2: 1},
            7: {1: 2, 2: 1},
            8: {1: 2, 2: 1},
            9: {1: 2, 2: 1},
            10: {1: 2, 2: 1},

        }
        self.print_slice_to_port()

    #this function change the dictionary self.slice_to_port according to administration_normal scenario
    def administration_normal(self):
        print("Security-enhanced scenario has been selected")
        self.slice_to_port = {
            1: {1:5, 5:1, 2:6, 6:2, 3:4, 4:3},
            4: {2:4, 4:2, 3:5, 5:3, 1:6, 6:1},
            2: {1: 2, 2: 1},
            3: {1: 2, 2: 1},            
            5: {1: 2, 2: 1},
            6: {1: 2, 2: 1},
            7: {1: 2, 2: 1},
            8: {1: 2, 2: 1},
            9: {1: 2, 2: 1},
            10: {1: 2, 2: 1},
            
        }
        self.print_slice_to_port()
    
    #this function is to select the scenario according to the selected option        
    def select_case(self, case):
        options = {
            1: self.normal,
            2: self.emergency,
            3: self.administration_normal
        }
        self.current_scenario = case
        return options.get(case, lambda: print("Invalid option"))()
    

    # this the switch features handler
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)
        ]
        self.add_flow(datapath, 0, match, actions, 0, 0)

    # this function is to add flow to the switch
    def add_flow(self, datapath, priority, match, actions, idleTimeout, hardTimeout):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

         # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(
            datapath=datapath, idle_timeout=idleTimeout, hard_timeout=hardTimeout, priority=priority, match=match, instructions=inst
        )
        datapath.send_msg(mod)
        print("Adding flow to switch: ", datapath.id)
        #print("MOD", mod)

    #this function is to send packet to the switch
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
        #print("message type: ", msg.msg_type)
        #print("OUT", out)

   #this function is to remove all flows from the switch with the priority 1   
    def remove_all_flows_from_sw(self, datapath):
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser
        
        # Create a match object with no match fields
        match = ofp_parser.OFPMatch()
        
        # Create a flow mod message with command DELETE and match object
        mod = ofp_parser.OFPFlowMod(
            datapath=datapath, command=ofp.OFPFC_DELETE_STRICT,
            out_port=ofp.OFPP_ANY, out_group=ofp.OFPG_ANY,
            priority=1, match=match
        )
        
        # Send the flow mod message to the switch
        datapath.send_msg(mod)
        print("Removing all flows from switch: ", datapath.id)
        print("MOD", mod)
    
    #this is the packet in handler, main function of the controller           
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        in_port = msg.match["in_port"]
        dpid = datapath.id
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        if(self.boolDeleteFlows == False and eth.ethertype != ether_types.ETH_TYPE_LLDP):
            
            out_port = self.slice_to_port[dpid][in_port]
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
            match = datapath.ofproto_parser.OFPMatch(in_port=in_port)            

            self.add_flow(datapath, 1, match, actions, self.idleTimeout, self.hardTimeout)
            self._send_package(msg, datapath, in_port, actions)
        
        
    #this handler is for the switch enter event   
    @set_ev_cls(event.EventSwitchEnter)
    def switch_enter_handler(self, ev):
        switch_dp = ev.switch.dp
        switch_dpid = switch_dp.id
        ofp_parser = switch_dp.ofproto_parser

        self.logger.info(f"Switch has been plugged in PID: {switch_dpid}")

        if switch_dpid not in self.switches:
            self.switches.append(switch_dpid)               
            self.datapath_list.append(switch_dp)