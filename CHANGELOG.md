# Changelog

#### Keeping a Changelog
Refer to the SCM for formal processes and rules and use the following website for further guidance: https://keepachangelog.com/en/1.1.0/.
Contact Lianna if any clarification is needed :)

##### The names relative to the usernames on this file can be found on the README

### [0.3.3] - 12/03/2023: STIG Security Document and README Update
#### Added:
- Markdown file for justifications of our code against Category 1 on STIG [@DanielGuevara99]
- Tutorial videos in Google Drive Folder [@edgarzub, @liannae5]
- Installation and LNIDS setup instructions in README [@maholguin6]
#### Changed:
- Tech Stack to reflect all technologies used [@liannae5]
- Usage to reflect updated way of starting user interfaces [@liannae5]
### [0.3.4] - 12/03/2023: Alert Encryption
#### Added:
- Methods for encrypting and decrypting alerts using AES_128 [@edgarzub]
- Methods for framing in sending and receiving of alerts [@edgarzub, @maholguin6]
#### Changed:
- Existing framing code to be in Classes, making it easier to test [@maholguin6]

### [0.3.3] - 12/03/2023: Connected LIDS and LIDS-D GUI to backend processes
#### Added:
- copy of BACKEND files to LIDS and LIDS_D DJANGO folders [@@DanielGuevara99, @mjloya]
- subprocess/thread call to backend LIDS-D and LIDS services [@DanielGuevara99]
- html code to accept config file and pass value to backend [@DanielGuevara99]
- code to display remaining storage on LIDS-D GUI [@mundisp]
- code to automatically sort alerts by time on LIDS-D GUI [@mundisp]
#### Changed:
- pulling records from correct database table that backend processes are adding into [@liannae5]
- portScan severity_level to 3 to solve bug [@liannae5]
- fixed file path errors for PCAP storage and database connections [@liannae5]
- LIDS GUI to properly display user IP, fixed LIDS GUI formatting [@aldoSanchez2002]
#### Deleted:
- duplicate DB files [@mjloya]

### [0.3.2] - 12/02/2023: Finalization of Nodemap mapping to config file
#### Added:
-Python code to locate path of generated txt file from the config parser and store contents in array [@mundisp]
-AJAX request in Javascript code to construct nodes based on the information received [@mundisp]

### [0.3.1] - 12/01/2023: Bug fixing on backend code
#### Added:
- backend now creates proper pcap files[@ccruzduart]
- change threading to subprocessing for sync issues with pyshark[@ccruzduart]
- change file directories[@ccruzduart]
- updated methods to work with subprocessing[@ccruzduart]
- connected cli with backend[@ccruzduart]


### [0.3.0] - 11/30/2023: Installation files
#### Added:
- Bash script to install necessary software and python libraries [@maholguin6]
- Bash scripts to run LNIDS on start up [@maholguin6]
- Bash scripts for mounting/unmounting USB drive [@maholguin6]

### [0.2.4] - 11/27/2023: Cleanup of LIDS-D GUI
#### Changed
- LIDS-D Alerts Table to sort by time by default (including on refresh) [@mundisp]
- LIDS-D Nodemap to display nodes from nodemap.txt [@mundisp]

### [0.2.3] - 11/25/2023: Code Cleanup of Backend 
#### Added:
- Added error handling for ingesting the configuration file [@liannae5]
- Added error handling for ending client connection [@mjloya]
#### Changed:
- main.py to run without requiring connection to LIDS-D server [@aldosanchez]
- error handling for connecting to LIDS-D server [@aldosanchez]
#### Deleted:
- Unused code in clientMain[@mjloya]

### [0.2.2] - 11/23/2023: LIDS-D Refresh option for alerts table
#### Added:
- Refresh method that updates the table of alerts in LIDS-D GUI [@mundisp]

### [0.2.1] - 11/13/2023: LNIDS Presentaiton Iteration
#### Added:
- LNIDS main file to start LNIDS services [@liannae5]
- LIDS main file to start LIDS backend services (connection to LIDS-D, saving dummy data, calling detectAlerts) [@liannae5]
- detectedAlerts script to act as main call to all detection methods [@mjloya]
#### Changed:
- Port scan and failed login attempt methods to return src/dst ip, alert info instead of boolean to aid in alert generation [@liannae5]
- clientConnect script to send dummy alerts to LIDS-D and save it to LNIDS local database [@mjloya, @DanielGuevara99]

### [0.2.0] - 11/07/2023: Intial LNIDS Iteration
#### Added:
- LNIDS main file to start LNIDS services [@liannae5]
- LIDS main file to start LIDS backend services (connection to LIDS-D, saving dummy data, calling detectAlerts) [@liannae5]
- detectedAlerts script to act as main call to all detection methods [@mjloya]
#### Changed:
- Port scan and failed login attempt methods to return src/dst ip, alert info instead of boolean to aid in alert generation [@liannae5]
- clientConnect script to send dummy alerts to LIDS-D and save it to LNIDS local database [@mjloya, @DanielGuevara99]

### [0.1.6] - 11/06/2023: Added logic for remaining storage
#### Added:
- LIDS GUI method to get and display remaining device storage [@edgarzub]

### [0.1.5] - 11-06-2023: Alert table now color-coded by severity level
#### Added:
- Conditional statement to change color of alert based on severitylevel in LIDS and LIDS-D GUI [@mundisp]

#### Changed:
- Page title inside dashboard to restore filtering/sorting menu functionality [@mundisp]

### [0.1.4] - 10-30-2023: Addition of LoginAttempt and Portscan Functionality
#### Added:
- LIDS SSH Failed Login
- LIDS FTP Failed Login
- LIDS RTP Failed Login
- LIDS Port Scan [@aldosanchez2002, @liannae5, @maholguin6]

### [0.1.3] - 10-29-2023: Creation of Nodemap and modification of alerts table
#### Added:
- LIDS-D nodemap functionality [@mundisp]

#### Changed:
- LIDS-D/LIDS alerts table now displaying only relevant columns at startup [@mundisp]

### [0.1.2] - 10-26-2023: Cleaning up Nofication Box and Export on LIDS/LIDS-D GUI
#### Added:
- LIDS-D alert's page export functionalities [@DanielGuevara99]

#### Changed:
- LIDS-D GUI to include headers for conifguration, alerts, and network information page [@DanielGuevara99]

### [0.1.1] - 10-25-2023: LIDS CLI Accessing and displaying Alerts from Database
#### Added:
- Methods to access database [@ccruzduart]
- Pandas library to communicate with database and display alerts [@ccruzduart]
#### Changed:
- Updated the alerts display [@ccruzduart]
- Command to sort Alerts [@ccruzduart]

### [0.1.0] - 10-17-2023: LIDS-D GUI & client-server infrastructure
#### Added:
- Sqlite3 Databases to LIDS and LIDS-D for alerts storage [@liannae5, @edgarzub]
- LIDS-D GUI [@mundisp, @edgarzub]
- LIDS client and LIDS-D server infrastructure to send alerts to LIDS-D [@ccruzduart, @liannae5]

#### Changed:
- Sample config to match update from customer [@liannae5, @mjloya]
- LIDS GUI to include sorting and filtering in alerts display [@edgarzub]
- README to include LIDS-D usage [@liannae5]

#### Deleted:
- Extra unused folders [@liannae5]


### [0.0.1] - 09-17-2023: First Iteration of Detection System
#### Added:
- Packet Capture Code [@aldosanchez2002]
- Analyze packets for, failed ssh login attemps, port scan, malicious IP, packet length attack [@aldosanchez2002]
- Deleted unecessary files in php code from previously merged branch [@maholguin6]

### [0.0.0] - 09-17-2023: LIDS GUI and CLI Prototype
#### Added:
- Django local server to host LIDS GUI [@aldosanchez2002]
- LIDS GUI with Config, Alerts, and PCAP pages [@mjloya, @edgarzub, @DanielGuevara99, @aldosanchez2002]
- LIDS CLI with Config, Alerts, and PCAP displays [@liannae5]
- Alerts class [@maholguin6]
- Packet class [@maholguin6]
- README [@liannae5, @aldosanchez]
-
