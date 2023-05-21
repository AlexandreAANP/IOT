#/bin
sudo apt install avahi-daemon
sudo systemctl restart avahi-daemon
sudo hostnamectl set-hostname $1
sudo systemctl restart avahi-daemon
