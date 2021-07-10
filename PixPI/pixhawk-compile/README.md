## pixhawk compile part - ( Test Successed )

sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install git
sudo apt-get install git
sudo apt-get install gitk git-gui

git submodule update --init --recursive

Tools/environment_install/install-prereqs-ubuntu.sh -y

. ~/.profile

./waf distclean 

./waf list_boards

./waf configure --board MatekF405-Wing

./waf copter
