#! /usr/bin/env python3

import os
import sys
import signal
from time import sleep
from pathlib import Path
import database_functions
import subprocess

cwd = os.getcwd()
print(cwd)
database = database_functions.establishConnection(cwd+'/BACKEND/LIDS_client/alerts.sqlite3')
commands = {'help':"View a list of commands",
            'showpcap': 'will show generated pcap files',
            'openpcap': ['will open pcap in wireshark',
                         {"-no argument": "it will open the most resent pcap file",
                          "-pcap_name": "will open the selected pcap"
                         }
                         ],
            'showalerts':["Show the real-time list of alerts generated during the session",
                          "Sort alert list using the following flag list (time is the default): ",
                          { "-time": "Sort alerts from oldest to newest",
                            "-severity_level": "Sort alerts from highest to lowest severitye",
                            "-ip_src": "Sort alerts by source IP address",
                            "-ip_dst" : "Sort alerts by destination IP address",
                            "-protocol" : "Sort by protocol",
                            "-reason" : "sort alerts by type",
                            "-filename" : "sort alerts by their PCAP file name"
                          },
                          "Filter alert list using the following flag list: ",
                          {"-time": "show only alerts at filtered time",
                           "-severity_level": "show only filtered severity_level",
                            "-ip_src": "show only filtered IP source",
                            "-ip_dst" : "show only filtered destination IP address",
                            "-protocol" : "how only protocol seleced",
                            "-reason" : "show alerts with reason selected",
                            "-filename" : "show only alerts filtered by their PCAP file name"}
                        ],
            'exit': "Ends the session.\n"
            }

# Handles input commands
def commandsHandler(args):
    if args[0] == 'help':
        displayHelp()
    elif args[0] == 'showpcap':
        displayPCAPFile()
    elif args[0] == 'openpcap':
        if len(args) > 1:
            displayPCAPSelected(args[1])
        else:
            displayPCAP()
    elif args[0] == 'showalerts':
        if len(args) > 1:
            if args[1] == 'sort':
                displaySortedAlerts()
            elif args[1] == 'filter':
                displayFilteredAlerts()
            else:
                print("\ninvalid option for showalerts")
        else:    
            displayAlerts()
    elif args[0] == 'start':
        configFilePath = input("Enter file path for config file here: ")
        displayStart(configFilePath)
    elif args[0] == 'sort':
        displaySortedAlerts()
    elif args[0] == 'filter':
        displayFilteredAlerts()
    elif args[0] == 'getConfig':
        getConfig()
    else:
        print("invalid command. Enter 'help' to see a list of commands")

def displaySortedAlerts():
    os.system('cls' if os.name == 'nt' else 'clear')
    sort = input('\nPlease enter the column to sort from:\nalert_id, severity_level, ip_src, ip_dst, descripton, filename\n>> ')
    os.system('cls' if os.name == 'nt' else 'clear')
    database_functions.getRecordsSorted(database,sort)

def displayFilteredAlerts():
    os.system('cls' if os.name == 'nt' else 'clear')
    filtered = input('\nPlease enter the column to contain the value to be filter\nalert_id, severity_level, ip_src, ip_dst, descripton, filename\n>> ')
    value = input('\nPlease enter the value to be filter\n>> ')
    os.system('cls' if os.name == 'nt' else 'clear')
    database_functions.getRecordsFiltered(database,filtered,value)

# Show available commands
def displayHelp():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Here are a list of commands available for LIDS:\n')
    for command, details in commands.items():
        if isinstance(details, str):
            print(f"{command}: {details}")
        elif isinstance(details, list):
            print(f"{command}: {details[0]}")
            for item in details[1:]:
                if isinstance(item, str):
                    print(f"\t{item}")
                elif isinstance(item, dict):
                    for flag, description in item.items():
                        print(f"\t\t{flag}: {description}")

def displayAlerts(flag='-t'):
    os.system('cls' if os.name == 'nt' else 'clear')
    database_functions.getRecords(database)

def displayPCAPFile():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Displaying PCAP files: \n")
    directory = cwd+'/BACKEND/trafficCaptures'
    if os.path.exists(directory):
        files = os.listdir(directory)
        for file in files:
            print(file)
    else:
        print(f"The directory {directory} does not exist.")
    print("")

def displayPCAP():
    directory = cwd+'/BACKEND/trafficCaptures'
    wireSharkPath = '/usr/bin/wireshark' # Find a way to access wireshark on any device w/ any path
    if os.path.exists(directory):
        # List all pcap files in the directory
        pcap_files = [file for file in os.listdir(directory) if file.endswith('.pcap')]
        # Sort the pcap files based on their modification time
        pcap_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
        # Check if there are any pcap files
        if pcap_files:
            # Get the most recent pcap file
            most_recent_pcap = pcap_files[0]
            # Construct the full path to the most recent pcap file
            most_recent_pcap_path = os.path.join(directory, most_recent_pcap)
            subprocess.Popen([wireSharkPath, most_recent_pcap_path])
        else:
            print("No pcap files found in the directory.")
    else:
        print(f"The directory {directory} does not exist.")

def displayPCAPSelected(filename):
    directory = cwd+'/BACKEND/trafficCaptures/'+filename
    wireSharkPath = '/usr/bin/wireshark' 
    subprocess.Popen([wireSharkPath, directory])

# Welcome message and config file read
def displayStart():
    os.system('cls' if os.name == 'nt' else 'clear')
    stars = '*' * 16
    print('\n'+stars)
    print("WELCOME TO LIDS!")
    print(stars+'\n')

def getConfig():
    while True:
        config_name = input("Please enter the config file name\n>>")
        target_dir = Path.cwd() / config_name
        if not target_dir.exists():
            print("The target config file doesn't exist. Try again.")
        else:
            print(f"Config file path that was entered: {config_name}\n")
            return str(target_dir)

if __name__ == "__main__":
    displayStart()
    config_path = getConfig()
    lids_path = cwd + '/BACKEND/main.py'
    command = ['python3',lids_path,'LIDS',config_path]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        args = input("LIDS> ")
        args = args.split()
        if len(args) == 0:
            pass
        elif args[0] == "exit":
            print("Ending session. Goodbye!")
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            sys.exit()
        else:
            commandsHandler(args)
