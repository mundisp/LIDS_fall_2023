#!/usr/bin/env bash

#########################################################################################################################
########################################### install dependencies ########################################################



#check if python is installed
echo "checking for installed dependencies...."

if ! [ -x "$(command -v python3)" ]; then
  echo 'Error: python3 is not installed.' >&2
  #nstall python3
  sudo apt-get install python3 -y
  #exit 1
fi

#check if pip is installed
if ! [ -x "$(command -v pip)" ]; then
  echo 'Error: pip is not installed.' >&2
  #install pip
  sudo apt-get install python3-pip
  #exit 1
fi

#check if tshark is installed
if ! [ -x "$(command -v tshark)" ]; then
  echo 'Error: tshark is not installed.' >&2
  #install tshark
  sudo apt-get install tshark -y
  #exit 1
fi


#check if DJANGO is installed
if ! [ -x "$(command -v django-admin)" ]; then
  echo 'Error: DJANGO is not installed.' >&2
  #install DJANGO
  sudo apt-get install python3-django -y
  #exit 1
fi



#check if pyshark is installed
if ! [ -x "$(command -v pyshark)" ]; then
  echo 'Error: pyshark is not installed.' >&2
  #install pyshark
  python3 -m pip install pyshark
  #exit 1
fi


#check if djangorestframework is installed
if ! [ -x "$(command -v djangorestframework)" ]; then
  echo 'Error: djangorestframework is not installed.' >&2
  #install djangorestframework
  python3 -m pip install djangorestframework
  #exit 1
fi

#check if pandas is installed
if ! [ -x "$(command -v pandas)" ]; then
  echo 'Error: pandas is not installed.' >&2
  #install pandas
  python3 -m pip install pandas
  #exit 1
fi

#check if dktp is installed
if ! [ -x "$(command -v dktp)" ]; then
  echo 'Error: dktp is not installed.' >&2
  #install dktp
  python3 -m pip install dpkt
  #exit 1
fi

#check if requests is installed
if ! [ -x "$(command -v requests)" ]; then
  echo 'Error: requests is not installed.' >&2
  #install requests
  python3 -m pip install requests
  #exit 1
fi

#check if psutil is installed
if ! [ -x "$(command -v psutil)" ]; then
  echo 'Error: psutil is not installed.' >&2
  #install psutil
  python3 -m pip install psutil
  #exit 1
fi
echo "done checking for installed dependencies"

#########################################################################################################################
########################################### mount usb storage device ####################################################

#copy usb-mount to /usr/local/bin/
echo "copying usb-mount.sh to /usr/local/bin/"
sudo cp usb-mount.sh /usr/local/bin/

#copy usb-mount.service to /etc/systemd/system
sudo cp usb-mount.service /etc/systemd/system/

#copy usb-mount.sh to /usr/local/bin/
sudo cp usb-mount.sh /usr/local/bin/

#append the usb-mount to the /etc/udev/rules.d/99-com.rules file
echo 'KERNEL=="sd[a-z][0-9]", SUBSYSTEMS=="usb", ACTION=="add", RUN+="/bin/systemctl start usb-mount@%k.service"' | sudo tee --append /etc/udev/rules.d/99-com.rules

echo 'KERNEL=="sd[a-z][0-9]", SUBSYSTEMS=="usb", ACTION=="remove", RUN+="/bin/systemctl stop usb-mount@%k.service"' | sudo tee --append /etc/udev/rules.d/99-com.rules

#load the udev rules
sudo udevadm control --reload-rules

#start the usb-mount service
sudo systemctl start usb-mount@sd*

echo "done copying usb-mount.sh to /usr/local/bin/"

#########################################################################################################################
########################################### unzip main folder ########## ################################################


#unzip the file
#unzip $MAIN_DIR.zip

#tar.gz the file directory
#tar -czvf $USB_STORAGE_DEVICE_NAME.tar.gz $PYTHON_DIR

#decompress the tar.gz file
#tar -xvzf $USB_STORAGE_DEVICE_NAME.tar.gz

#############################################################################################################################
########################################### collect computer information ####################################################

# define the directory where the python files are located
MAIN_DIR="~/CS4311_LIDS_2AllSafe_Fall2023"

#change to the python directory
# cd $MAIN_DIR

#capture kali linux username
KALI_USERNAME=$(whoami)

#capture kali linux ip address and use awk to get the first ip address
KALI_IP=$(hostname -I | awk '{print $1}')

# capture the usb storage device name
USB_STORAGE_DEVICE_NAME=$(lsblk | grep sda | awk '{print $7}')


#########################################################################################################################
########################################### make python files executeble ################################################

#make files executable
#overkill as the aliases will run with python3 command
echo "making python files executable...."
sudo chmod +x BACKEND/main.py
sudo chmod +x BACKEND/LIDS_client/clientMain.py
sudo chmod +x BACKEND/LIDSD_server/serverMain.py
sudo chmod +x LIDS_CLI/main.py
sudo chmod +x LNIDS/main.py
sudo chmod +x DJANGO/LIDS/main.py
sudo chmod +x DJANGO/LIDS/manage.py
sudo chmod +x DJANGO/LIDS_D/manage.py
echo "done making python files executable"
#########################################################################################################################
########################################### create aliases to run the different apps ####################################

#make alias for main.py in LIDS
echo "making aliases...."
sudo echo "alias lids_gui='$MAIN_DIR/DJANGO/LIDS/manage.py runserver'" >> ~/.bashrc

#make alias for main.py in LIDS-D
sudo echo "alias lidsd_gui='$MAIN_DIR/DJANGO/LIDS_D/manage.py runserver'" >> ~/.bashrc

#make alias for main.py in LNIDS
sudo echo "alias lnids='$MAIN_DIR/LNIDS/main.py'" >> ~/.bashrc

#make alias for main.py in BACKEND
sudo echo "alias lids_t='$MAIN_DIR/BACKEND/main.py'" >> ~/.bashrc

#make alias for clientMain.py
sudo echo "alias lids_c='$MAIN_DIR/BACKEND/LIDS_client/clientMain.py'" >> ~/.bashrc

#make alias for serverMain.py
sudo echo "alias lids_s='$MAIN_DIR/BACKEND/LIDSD_server/serverMain.py'" >> ~/.bashrc

#make alias for main.py in LIDS_CLI
sudo echo "alias lids_cli='$MAIN_DIR/LIDS_CLI/main.py'" >> ~/.bashrc

#source ~/.bashrc
source ~/.bashrc
echo "Done making aliases!"
echo "Please run the following command: "
echo ". ~/.bashrc"
exit 1
