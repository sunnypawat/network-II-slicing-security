
<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<p align="center">
  <a href="https://github.com/sunnypawat/network-II-slicing-security/">
    <img src="images/logos_and_icons/icon.png" alt="Logo" width="250" height="250">
  </a>
</p>

<h1 align="center" style="color:#E34C26">SDN Slices for Security Scenarios in ComNetsEmu</h1>

<p align="center">
  <em>Dynamic and secure network slicing made simple</em>
    <br />
  <a href="https://docs.google.com/presentation/d/1a5Nu0xaqI02GTYYub3PESSVfszO_r_Mgpqkt9nufSZo/edit?slide=id.g304dfe70e09_0_40#slide=id.g304dfe70e09_0_40"><strong>Explore the Presentation »</strong></a>
  <br />
  <br />
  <a href="https://youtu.be/uhIPjDqtWho">View Video Demo</a>
  ·
  <a href="https://github.com/sunnypawat/network-II-slicing-security/">Project GitHub</a>
</p>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#how-to-run">How to Run</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#project-layout">Project Layout</a></li>
    <li><a href="#about-us">About Us</a></li>
    <li><a href="#contacts">Contacts</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

SDN Slices for Security Scenarios in ComNetsEmu demonstrates how network slicing can be leveraged in ComNetsEmu to dynamically manage network resources and enforce security policies using SDN principles.

Each network slice represents a logically isolated segment that can be activated or deactivated depending on security requirements.

Example scenarios include:
- Isolating compromised devices
- Prioritizing emergency traffic
- Scaling resources dynamically for critical infrastructure

This project provides a flexible environment for research, education, and prototyping secure network architectures.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Welcome to our repository! To get started and have a working local copy of "SDN Slices for Security Scenarios" follow these steps.

### Prerequisites

Our software is developed with [ComNetsEmu](https://www.granelli-lab.org/researches/relevant-projects/comnetsemu-labs).

```bash
$ cd ~
$ git clone https://git.comnets.net/public-repo/comnetsemu.git
$ cd ./comnetsemu
$ vagrant up comnetsemu
$ vagrant ssh comnetsemu
```

You will also need an X server like [VcXsrv](https://sourceforge.net/projects/vcxsrv/) to export the GUI.

### Installation

```bash
git clone https://github.com/sunnypawat/network-II-slicing-security/
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- HOW TO RUN -->
## How to Run

First go to the project directory:

```bash
cd ./networking_security_slicing/
```

1. Enable Ryu controller:

```bash
$ ryu-manager ryu_slice.py --observe-links
```

Alternative (with configuration file):

```bash
$ ryu-manager ryu_slice.py --config-file slice.conf
```

2. Start Mininet topology:

```bash
$ sudo python3 topology.py
```

3. View Open vSwitch logs:

```bash
$ sudo tail -f /var/log/openvswitch/ovs-vswitchd.log
```

4. Cleanup:

```bash
$ sudo mn -c
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

The project implements on-demand network slicing for security scenarios.

- Activate/deactivate slices as needed.
- Isolate network segments.
- Enforce adaptive security policies.

_For more details, refer to the [Video Demo](https://youtu.be/uhIPjDqtWho)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- PROJECT LAYOUT -->
## Project Layout

```
└── [networking_security_slicing]
     ├── [Images]
     ├── ryu_slice.py
     ├── topology.py
     ├── slice.conf
     └── README.md
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ABOUT US -->
## About Us

We are students at the University of Trento interested in network security and software-defined networking. This project was developed as part of the Networking course.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contacts

- Pawat Songkhopanit — pawat.songkhopanit@studenti.unitn.it
- Mariia Afonina — mariia.afonina@studenti.unitn.it

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [ComNetsEmu](https://git.comnets.net/public-repo/comnetsemu)
* [Mininet](http://mininet.org/)
* [Python](https://www.python.org/)
* [University of Trento](https://www.unitn.it/en)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<p align="center"><b>Thank you for visiting our page!</b></p>

<!-- LINKS -->
[Python-logo]: https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat
[Python-url]: https://www.python.org/
[VSC-logo]: https://img.shields.io/badge/-Visual%20Studio%20Code-007ACC.svg?logo=visual-studio-code&style=flat
[VSC-url]: https://code.visualstudio.com/
[Mininet-logo]: images/logos_and_icons/mininet.png
[Mininet-url]: http://mininet.org/
[Comnetsemu-logo]: images/logos_and_icons/comnetsemu.png
[Comnetsemu-url]: https://www.granelli-lab.org/researches/relevant-projects/comnetsemu-labs
[GUI]: images/GUI.png
