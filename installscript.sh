#!/usr/bin/env bash

# Update system
sudo pacman -Syyu

# Install yay
sudo pacman -S git
cd /opt
sudo git clone https://aur.archlinux.org/yay-git.git
sudo chown -R hp:hp ./yay-git
cd yay-git
sudo makepkg -si

# Copy pacman config
cd ~/awesomebackup
# copy dotfiles
mkdir $HOME/.config
cd ~/awesomebackup/
# cp -r .fonts ~/
sudo cp -r ./etc/ /
sudo cp pfetch /usr/local/bin/
rsync -av --progress ./.config/ $HOME/.config --exclude .git

# Install essential packages
yay -S emacs zsh intel-media-driver intel-gpu-tools va-utils thunar sshfs picom dmenu xorg-xinput brightnessctl alsa-utils seahorse polkit-gnome gnome-keyring libgnome-keyring bluez bluez-tools bluez-utils speedtest-cli lxappearance-gtk3 material-black-colors-theme dunst perl playerctl pnmixer xautolock cmake fzf feh cmus gnome-disk-utility python-pip python iw net-tools htop mpv tk ctags nodejs npm xclip xsel yarn firewalld picom pacman-contrib neovim gvfs gvfs-mtp adobe-source-code-pro-fonts tlp tlp-rdw cargo

# tlp setup
sudo systemctl enable tlp
sudo systemctl mask systemd-rfkill.service systemd-rfkill.socket
sudo tlp start
tlp-rdw

# caffeinate
cargo install --git https://github.com/rschmukler/caffeinate
sudo cp ~/.cargo/bin/caffeinate /usr/local/bin/

# Install pulseaudio or pipewire. My gpd pocket 2 somehow randomly only works with either one on different distros.
# pipewire
# yay -S pipewire pipewire-pulse pipewire-alsa lib32-pipewire
# systemctl --user --daemon-reload
# systemctl --user enable pipewire pipewire.socket

# pulseaudio
yay -S pulseaudio-bluetooth pulseaudio pulseaudio-alsa pulseaudio-ctl lib32-libpulse pulseaudio-qt
systemctl --user --daemon-reload
systemctl --user enable pulseaudio pulseaudio.socket

# Install personal packages
yay -S interception-tools nextcloud-client ranger flameshot ncdu steam ardour fortune-mod aircrack-ng bully reaaver tmux libreoffice-fresh metasploit cowpatty wireshark termshark macchanger pixiewps john android-sdk-platform-tools nerd-fonts-jetbrains-mono krita xorg-fonts gucharmap qbittorrent rustscan cpupower-gui wine-staging bottom vlc tldr lutris fcitx5 fcitx5-gtk fcitx5-qt fcitx5-unikey kcm-fcitx5 btop clipmenu gparted pass pass-otp sxiv scrcpy qutebrowser trash-cli kdeconnect zathura zathura-pdf-mupdf easytag gnome-power-manager

# Install AUR packages
yay -S caffeine-ng cava cmus-notify google-chrome material-black-colors-theme ncmatrix nerd-fonts-ubuntu-mono pyrit python-pulsectl ticker timeshift-bin noto-fonts-emoji-apple mangohud-git ttf-unifont ttf-font-awesome otf-font-awesome protonvpn goverlay ttf-ubuntu-font-family ttf-ms-fonts nuclear-player-bin routersploit-git update-grub

# Post installation
# refresh font cache
fc-cache -fv

# install and move to zsh
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
sudo chsh -s /usr/bin/zsh

# pip packages
sudo pip install python-nmap
pip install wheel pyxdg iwlib

# enable bluetooth and other systemd services
sudo modprobe btusb
sudo systemctl enable bluetooth cronie firewalld
sudo systemctl start bluetooth cronie firewalld

# Additional packages

# dmenu fork
cd ~
# git clone https://github.com/sbstnc/dmenu-ee
git clone https://gitlab.com/dwt1/dmenu-distrotube.git
cd dmenu-distrotube.git
sudo make clean install
cd ~

# wifite fork
cd ~
git clone https://github.com/kimocoder/wifite2
cd wifite2
pip install -r requirements.txt
sudo pip install python-nmap
sudo python setup.py install
make help
cd ~

# neovim plug
sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
# Run :PlugInstall

git clone --depth 1 https://gitlab.com/VandalByte/darkmatter-grub-theme.git && cd darkmatter-grub-theme
sudo python3 darkmatter-theme.py --install
