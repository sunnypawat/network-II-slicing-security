# SDN slices for Security Scenarios in ComNetsEmu
This is a part of the Networking course at the University of Trento

This project demonstrates how network slicing can be used within the ComNetsEmu environment to manage network resources dynamically through a Graphical User Interface (GUI). Leveraging Software-Defined Networking (SDN) principles allows network slices to be activated and deactivated based on specific security requirements.

Each network slice represents a logically isolated network segment tailored to particular applications, users, or services. This flexible approach makes it possible to simulate and test real-world security scenarios in which network policies must adapt to changing conditions, such as isolating compromised devices, prioritizing emergency traffic, or dynamically scaling resources for critical infrastructure.

By integrating with ComNetsEmu, this project provides an emulated platform to experiment with slice management, policy enforcement, and resource allocation in a safe and controlled environment—ideal for research, education, and prototyping secure network architectures.
## Getting Started
To get started, follow these steps!
### Prerequisites
Our software is developed with ComNetsEmu.
For more detailed information about ComNetsEmu, please visit here.
```sh
$ cd ~
$ git clone https://git.comnets.net/public-repo/comnetsemu.git
$ cd ./comnetsemu
$ vagrant up comnetsemu
# Take a coffee and wait about 15 minutes

# SSH into the VM when it's up and ready (The ComNetsEmu banner is printed on the screen)
$ vagrant ssh comnetsemu
```

### Installation

## Running
1. Option 1: Enable ryu controller to isolate the network topology into slices and create the GUI: 
```sh
$ ryu-manager ryu_slice.py --observe-links
```
Option 2: Enable ryu controller to isolate the network topology into slices with .conf file:
```sh
$ ryu-manager ryu_slice.py --config-file slice.conf
```
You must configure the scenario in the slice.conf file
2. Network creation in Mininet (in a new terminal):
```sh
$ sudo python3 topology.py
```
3. See real-time switches log file
```sh
$ sudo tail -f /var/log/openvswitch/ovs-vswitchd.log
```

Please execute the following command to clear everything before running a new example:
```sh
$ sudo mn -c
```

## Testing
To test that everything is working properly, execute the following commands:
1. Ping to check connectivity (in Mininet)
```sh
mininet>pingall
```
3. Bandwidth Check (in Mininet)
```sh
mininet>iperf h1 h4
```

## Project layout
## About Us and Contact
- Pawat Songkhopanit
- Mariia Afonina

