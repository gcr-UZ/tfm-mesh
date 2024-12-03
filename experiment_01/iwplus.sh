#!/bin/bash
#sudo iw dev wlp1s0 scan | egrep "^BSS|freq|signal|SSID:[[:space:]]GTE_MESH"> output.txt
#sudo iw dev wlp0s20f3 scan | egrep "^BSS|freq|signal|SSID:[[:space:]]GTE_MESH"> output.txt
sudo iw dev wlp0s20f3 scan | egrep "^BSS|freq|signal|SSID:[[:space:]]sagemcom8938-5G"> output.txt
linea=$(cat output.txt | grep -n SSID | cut -d ':' -f 1)

while read l 
do
	cat output.txt | head -n$l | tail -n4
done <<< $linea



#sudo iw dev wlp0s20f3 scan | egrep "^BSS|freq|signal|SSID:[[:space:]]sagemcom8938-5G"> output.txt