# SDN slices for Security Scenarios in ComNetsEmu
Created by Pawat Songkhopanit and Mariia Afonina, University of Trento
This is a part of the Networking course at the University of Trento

This project demonstrates how network slicing can be used within the ComNetsEmu environment to manage network resources dynamically through a Graphical User Interface (GUI). Leveraging Software-Defined Networking (SDN) principles allows network slices to be activated and deactivated based on specific security requirements.

Each network slice represents a logically isolated network segment tailored to particular applications, users, or services. This flexible approach makes it possible to simulate and test real-world security scenarios in which network policies must adapt to changing conditions, such as isolating compromised devices, prioritizing emergency traffic, or dynamically scaling resources for critical infrastructure.

By integrating with ComNetsEmu, this project provides an emulated platform to experiment with slice management, policy enforcement, and resource allocation in a safe and controlled environment—ideal for research, education, and prototyping secure network architectures.
## Getting Started
### Prerequisites

### Installation

## Running
1. Enable ryu controller to isolate the network topology into slices and creates the GUI:
```sh
$ ryu-manager ryu_slice.py --observe-links
```
3. Network creation in Mininet (in a new terminal):
```sh
$ sudo python3 topology.py
```
5. See real-time switches log file
```sh
$ sudo tail -f /var/log/openvswitch/ovs-vswitchd.log
```

Please execute the following command to clear everething before running new example:
```sh
$ sudo mn -c
```

## Usage
## Project layout
## About us
