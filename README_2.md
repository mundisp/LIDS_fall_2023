# CS4311_LIDS_2AllSafe_Fall2023
### Description
The Lightweight Intrusion Detection System (LIDS) detects malicious traffic and generates and stores alerts to support DAC cyber analysts at DEVCOM’s Analysis Center during Cyber Vulnerability Assessments.

### Table of Contents

1. [Features](#features)
    - [LIDS](#lids)
    - [LNIDS](#lnids)
    - [LIDS-D](#lids-d)
2. [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
3. [Usage](#usage)
4. [Tech Stack](#tech-stack)
5. [Data Storage Architecture](#data-storage-architecture)
6. [Team Members](#team-members)
7. [License](#license)

## Features
The system is comprised of three sub systems: LIDS, LNIDS and LIDS-D. Each component's features are described below.

#### LIDS
- Detects malicious traffic and generate alerts when: a port scan is conducted, there are multiple failed login attempts, a source IP doesn't match whitelisted IPs, and network behavior matches threats categorized as high by the stig.
- Connects to LIDS-D server and sends encrypted alerts to LIDS-D and store them locally.
- Stores malicious packets on PCAPs that are saved locally.
- Displays list of alerts from current session, with the optional ability to sort by severity level, time, and source IP address.

#### LNIDS
- Detects malicious traffic and generate alerts when: a port scan is conducted, there are multiple failed login attempts, a source IP doesn't match whitelisted IPs, and network behavior matches threats categorized as high by the stig.
- Connects to LIDS-D server and sends encrypted alerts to LIDS-D.
- Stores all network traffic in PCAPs on an external drive.
- Operates without user input.

#### LIDS-D
- Receives and decrypts encrypted alerts sent by LIDS and LNIDS agents.
- Optionally exports current session's alert list as XML, CSV, or JSON.
- Displays alert list and node map when requested by the user.

## Getting Started
### Tutorials
Tutorials are available at the following link: https://drive.google.com/drive/u/1/folders/1E7ABM-2cNMTikwupQLq0SseVqylUUqWq
There are tutorials for the following:
- Installation
- LNIDS setup
- LIDS CLI
- LIDS GUI
- LIDS-D GUI

### Prequisites
1. A machine that has at least 8GB of disk space, 768M of RAM, 1 Ghz of CPU, and runs Linux.
2. Basic Experience with a command line.

### Installation
The installation file (install.sh) ensures the system has all the dependencies that our
system needs to run. Create necessary extensions that allow the use of external storage
devices. Creates paths to simplify the use of commands removing the need to navigate to the
different location to run the programs. Automate the startup prgram in the case of LNIDS
allowing the system to run without any user interaction. Collects the nessesay information
that the system needs to run. make nessesary file executable to permit the use commands more direct.
(in order for the install.sh script tu run properly make sure you are using bash shell.)
1. Download the CS4311_LIDS_2AllSafe_Fall2023 repository.
2. cd to  CS4311_LIDS_2AllSafe_Fall2023 file and cd into CS4311_LIDS_2AllSafe_Fall2023 (unzip if needed ).
3. Run bash installation.sh (root privileges needed, password is required).

    - Use the command 'chmod +x installation.sh' to give executable privileges to the file
    - You may need to input your password as some point in the installation process, as some installation commands require 'sudo'.
    - List of Dependencies:
        - python3
        - python3-pip
        - tshark
        - python3-django
        - pyshark
        - djangorestframework
        - pandas
        - dpkt
        - requests
        - psutil

4. Copy necessary files to mount and unmount the usb drvie.

    - list of files:
        - usb-mount.sh
        - usb-mount.service
5. Install.sh is run by systemd to start stop the usb-mount service
6. Instlal.sh add 2 rules to the /etc/udev/rules.d/99-com.rules file to automate the mount unmount

7. Collects system inforamtion to be used by the different systems.
    - Information collected:
        - host ip
        - host name
        - usb device name

8. Extends executable provileges to LIDS,LIDS-D,LNIDS.
    - List of files:
        - main.py (for LIDS).
        - clientMain.py ( for LIDS)
        - serverMain.py ( for LIDS-D)
        - main.py ( for LIDS_CLI)
9. Make shortcut commands (aliases) to eliminate navigating trough folders to run commands.
    - Aliases:
    - lidsd_gui ( runs the GUI in terminal)
    - lids_gui ( runs the GUI in client)
    - lnids (runs LNIDS)
    - lids_t (run LIDS in terminal)
    - lids_c (runs LIDS client in terminal)
    - lids_s ( runs LIDS-D in terminal)
    - lids_cli (runs LIDS terminal )

#### LNIDS Installation (see LNIDS Tutorial video for help)
1. edit the cron_jobs.sh with the full file path to where you stored this project
2. edit the lnids_starter.sh with the full file path to where you stored this project, and the path to the config file
3. run cron_jobs.sh
4. Optionally run usb-mount.sh to allow use of USB port

LNIDS should now run on start-up

## Usage
It is reccommended that users watch the tutorial videos to learn more about how to use each User Interface. 
The following are steps to start up each interface.
### LIDS GUI
1. If the project is installed in the path shown of the alias in .bashrc, then you can run the command 'lids_gui' from any directory in your terminal
2. Otherwise navigate to 'CS4311_LIDS_2AllSafe_Fall2023/DJANGO/LIDS' and run 'python3 manage.py runserver'
3. ctrl+click or copy the link: 'http://127.0.0.1:8000/' that is given to open the GUI in your browser

### LIDS CLI 
1. Navigate to the main directory file: CS4311_LIDS_2ALLSAFE_FALL2023
2. Run command main.py
3. When prompted for the config  file path, enter the full path to the configuration file
4. Type 'help' to get the full list of commands and usage. Here are common commands
   - showalerts: displays the current alerts in the database
   - sort: display alert by a given column. User will be prompted to enter sort value
   - filter: display alerts by given filter value. User will be prompted to enter filter value
   - showpcap: displays generated pcap files
   - openpcap: will open the most resent pcap on wireshark
   - openpcap <fileName>: opens the file in wireshark

### LIDS-D GUI
1. If the project is installed in the path shown of the alias in .bashrc, then you can run the command 'lidsd_gui' from any directory in your terminal
2. Otherwise navigate to 'CS4311_LIDS_2AllSafe_Fall2023/DJANGO/LIDS_D' and run 'python3 manage.py runserver'
3. ctrl+click or copy the link: 'http://127.0.0.1:8000/' that is given to open the GUI in your browser

## Tech Stack
#### Backend (Python)
- Web Framework: Django. A Python web framework, with lots of documentation for handling backend logic and serving APIs.
- Packet Capture and Analysis: pyshark. A Python library that acts as a wrapper for tshark and is used for packet capture and analysis, additionally integrates with Wireshark.
- Alert Generation: Custom code within Django storage needs.
- Rest API Framework: Djangorestframework. An application follows the MVC (Model-View-Controller) architectural pattern where models define the data structure, views handle the user interface and user input, and controllers (views in Django) manage the interaction between models and views.
- Database data structure framework: Panda.  Used to export serialized data into different file formats, such as JSON, CSV,and XML. We use it to format  the data,  pull records from from the database and manipulate them in the GUI and CLI. It helps to create the alerts' table and sort them.
#### Frontend (HTML/CSS/JS/JINJA)
- Bootstrap: A front-end styling framework for building user interfaces,with multiple libraries de css that allows to utilize multiple object from html with properties fo css that have been already defined.
- Javascript: Used for handling minor computations or methods that need to be run for frontend services.
#### Validation and Verification (Python)
- Testing: Pytest. A Python testing framework for unit and integration testing.
- Integration Testing: Much of our testing was done manually as a simple approach to ensuring backend and frontend processes were connection with each other during development

## Data Storage Architecture
- This is how the system reduces memory usage and instead uses device storage. This allows the system to be lightweight
![Data Architecture](https://github.com/aldosanchez2002/CS4311_LIDS_2AllSafe_Fall2023/assets/52171931/2285abfc-371d-47b4-8447-8eb34a49080d)

## Team Members
#### Lead Analyst
- Aldo Sanchez [@aldosanchez]
#### Lead Designers
- Lianna Estrada [@liannae5]
- Maria Jose Loya [@mjloya]
#### Lead Programmers
- Cristian Cruz Duarte [@ccruzduart]
- Edmundo Pariente [@mundisp]
#### Lead V&V
- Edgar Garnica [@edgarzub]
- Daniel Guevara [@DanielGuevara99]
- Martin Holguin [@maholguin6]

