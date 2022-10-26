#!/bin/bash

set -e

clear

BLACK='\e[30m'
RED='\e[31m'
GREEN='\e[92m'
YELLOW='\e[33m'
ORANGE='\e[93m'
BLUE='\e[34m'
PURPLE='\e[35m'
CYAN='\e[96m'
WHITE='\e[37m'
NC='\e[0m'
purpal='\033[35m'

clear

counter=0
(

while :
do
cat <<EOF
XXX
$counter
Loading DARKTOR INSTALLER ....( $counter%):
XXX
EOF

(( counter+=20 ))
[ $counter -eq 100 ] && break

sleep 1
done
) |
whiptail --title " DARKTOR " --gauge "Please wait" 7 70 0



clear

echo -e "${RED} "
echo ""
echo "        "
echo " ████████▄     ▄████████    ▄████████    ▄█   ▄█▄     ███      ▄██████▄     ▄████████  ";
echo " ███   ▀███   ███    ███   ███    ███   ███ ▄███▀ ▀█████████▄ ███    ███   ███    ███  ";
echo " ███    ███   ███    ███   ███    ███   ███▐██▀      ▀███▀▀██ ███    ███   ███    ███  ";
echo " ███    ███   ███    ███  ▄███▄▄▄▄██▀  ▄█████▀        ███   ▀ ███    ███  ▄███▄▄▄▄██▀  ";
echo " ███    ███ ▀███████████ ▀▀███▀▀▀▀▀   ▀▀█████▄        ███     ███    ███ ▀▀███▀▀▀▀▀    ";
echo " ███    ███   ███    ███ ▀███████████   ███▐██▄       ███     ███    ███ ▀███████████  ";
echo " ███   ▄███   ███    ███   ███    ███   ███ ▀███▄     ███     ███    ███   ███    ███  ";
echo " ████████▀    ███    █▀    ███    ███   ███   ▀█▀    ▄████▀    ▀██████▀    ███    ███  ";
echo "                           ███    ███   ▀                                  ███    ███ V1.2  ";
echo "                                                                                       ";
echo -e "${GREEN}                                        [!] Coded By 1ucif3r [!]${NC}"
echo -e "${BLUE}                                    https://github.com/D4RK-4RMY/darktor ${NC}"
echo -e "${RED}                                     [!] This Tool Must Run As ROOT [!]${NC}\n"
echo -e ${CYAN}                "Select Best Option : \n"
echo -e "${WHITE}              [1] Kali Linux (apt)"
echo -e "${WHITE}              [2] Arch Linux (pacman)" # added arch linux support because of feature request #231
echo -e "${WHITE}              [0] Exit "
echo -n -e "DarkTor >> "
read choice
INSTALL_DIR="/usr/share/doc/darktor"
BIN_DIR="/usr/bin/"
if [ $choice == 1 ] || [ $choice == 2 ]; then
	echo "[*] Checking Internet Connection .."
	wget -q --tries=10 --timeout=20 --spider https://google.com
	if [[ $? == 0 ]]; then
        echo -e ${BLUE}"[✔] Loading ... "
        if [ $choice == 1 ]; then
            sudo apt-get install tor python3-pip -y 
            sudo pip3 install -r requirements.txt
        elif [ $choice == 2 ]; then # added arch linux support because of feature request #231
            sudo pacman -Suy
            sudo pacman -S python-pip yay
        fi

	    echo "[✔] Checking directories..."
	    if [ -d "$INSTALL_DIR" ]; then
	        echo "[!] A Directory darktor Was Found.. Do You Want To Replace It ? [y/n]:" ;
	        read input
	        if [ "$input" = "y" ]; then
	            sudo rm -R "$INSTALL_DIR"
	        else
	            exit
	        fi
	    fi

        echo "[✔] Installing ...\n";
        sudo git clone https://github.com/D4RK-4RMY/DarkTor.git "$INSTALL_DIR";
        echo "#!/bin/bash
        python3 $INSTALL_DIR/darktor.py" '${1+"$@"}' > darktor;
        sudo chmod +x darktor;
        sudo cp darktor /usr/bin/ && rm darktor;

        echo "\n[✔] Trying to installing Requirements ..."
        if [ $choice == 1 ]; then
            sudo pip3 install lolcat boxes flask requests
            sudo apt-get install -y figlet
        elif [ $choice == 2 ]; then # added arch linux support because of feature request #231
            sudo pip3 install lolcat boxes flask requests
            yay -S boxes --noconfirm
            sudo pacman -S figlet
        fi

	else
		  echo -e $RED "Please Check Your Internet Connection ..!!"
	fi

    if [ -d "$INSTALL_DIR" ]; then
        echo "";
        echo "[✔] Successfuly Installed !!! \n\n";
        echo -e $ORANGE "       [+]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[+]"
        echo            "       [+]                                                             [+]"
        echo -e $ORANGE "       [+]     ✔✔✔ Now Just Type In Terminal (darktor) ✔✔✔         [+]"
        echo            "       [+]                                                             [+]"
        echo -e $ORANGE "       [+]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[+]"
    else
        echo "[✘] Installation Failed !!! [✘]";
        exit
    fi
elif [ $choice == 0 ] && [ $choice != 1 ] && [ $choice != 2 ]; then 
    echo -e $RED "[✘] THank Y0u !! [✘] "
    exit
else
    echo -e $RED "[!] Select Valid Option [!]"
fi