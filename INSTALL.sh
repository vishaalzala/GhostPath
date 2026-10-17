#!/bin/bash
# Install script for ghostpath

	export BLUE='\033[1;94m'
	export GREEN='\033[1;92m'
	export RED='\033[1;91m'
	export RESETCOLOR='\033[1;00m'

	echo -e "This script will install ghostpath on your computer...\n"
	sleep 1
	cp -Rf opt/ghostpath /opt/ghostpath
	sleep 1
	cp -Rf ghostpath.desktop /usr/share/applications
	sleep 1
	cp -Rf etc/ghostpath.sh /etc/init.d/ghostpath.sh
	sleep 1
	cp -Rf usr/ghostpath /usr/bin/ghostpath
	sleep 1
	cp -Rf usr/ghostpath-on /usr/bin/ghostpath-on
	sleep 1
	cp -Rf usr/ghostpath-off /usr/bin/ghostpath-off
	sleep 1
	apt-get install tor macchanger resolvconf dnsmasq polipo privoxy tor-arm libnotify-bin curl bleachbit
	sleep 1
	cp -Rf polipo/config /etc/polipo/config
	sleep 1
	cp -Rf privoxy/config /etc/privoxy/config
	sleep 1
	cp -Rf tor/torrc /etc/tor/torrc
	sleep 1
	chmod +x /etc/init.d/ghostpath.sh /usr/bin/ghostpath /usr/bin/ghostpath-on /usr/bin/ghostpath-off /opt/ghostpath/ghostpath-gui
	sleep 1
	echo -e "\n	 ghostpath (v 1.0) Usage Ex:\n
	$RED ghostpath-on$BLUE  =>$GREEN automated protection [ON]
	$RED ghostpath-off$BLUE =>$GREEN automated protection$RED [OFF]\n
	$RED ADVANCED COMMANDS LIST:\n
	$RED┌──[$GREEN$USER$RED@$BLUE`hostname`$RED]─[$GREEN$PWD$RED]
	$RED└──╼ $GREEN"ghostpath" $RED{$GREEN"start"$RED|$GREEN"stop"$RED|$GREEN"change"$RED|$GREEN"status..."$RED}\n
	$BLUE----[ Tor Tunneling related features ]----
	$RED ghostpath start$BLUE            =>$GREEN Start Tor Tunneling	  
	$RED ghostpath stop$BLUE             =>$GREEN Stop Tor Tunneling
	$RED ghostpath change$BLUE           =>$GREEN Changes identity restarting TOR
	$RED ghostpath status$BLUE           =>$GREEN Tor Tunneling Status\n
	$BLUE----[ IP related features ]----
	$RED ghostpath status_ip$BLUE        =>$GREEN IP status\n
	$BLUE----[ I2P related features ]----
	$RED ghostpath start_i2p$BLUE        =>$GREEN Start i2p services
	$RED ghostpath stop_i2p$BLUE         =>$GREEN Stop i2p services
	$RED ghostpath status_i2p$BLUE       =>$GREEN i2p status\n
	$BLUE----[ privoxy related features ]----
	$RED ghostpath start_privoxy$BLUE    =>$GREEN Start privoxy services
	$RED ghostpath stop_privoxy$BLUE     =>$GREEN Stop privoxy services
	$RED ghostpath status_privoxy$BLUE   =>$GREEN privoxy status\n
	$BLUE----[ polipo related features ]----
	$RED ghostpath start_polipo$BLUE     =>$GREEN Start polipo services
	$RED ghostpath stop_polipo$BLUE      =>$GREEN Stop polipo services
	$RED ghostpath status_polipo$BLUE    =>$GREEN Polipo status\n
	$BLUE----[ macchanger related features ]----
	$RED ghostpath start_mac$BLUE        =>$GREEN Start macchanger services
	$RED ghostpath stop_mac$BLUE         =>$GREEN Stop macchanger services
	$RED ghostpath status_mac$BLUE       =>$GREEN macchanger status\n
	$BLUE----[ arm related features ]----
	$RED ghostpath start_arm$BLUE        =>$GREEN Start Monitoring Anonymizing Relay (arm)\n
	$BLUE----[ wipe related features ]----
	$RED ghostpath wipe$BLUE             =>$GREEN cache, RAM & swap-space cleaner\n
	$BLUE----[ hostname related features ]----
	$RED ghostpath change_hostname$BLUE  =>$GREEN Randomly Spoofing Hostname
	$RED ghostpath restore_hostname$BLUE =>$GREEN Restore Default Hostname
	$RED ghostpath status_hostname$BLUE  =>$GREEN Show Current Hostname\n

	$RESETCOLOR"
