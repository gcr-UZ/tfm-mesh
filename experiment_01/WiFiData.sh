#!/bin/bash
ESSID=$(iwconfig wlp0s20f3 | head -n 1 | cut -d ':' -f 2)
Frequency=$(iwconfig wlp0s20f3 | grep Frequency | cut -d ':' -f 3 | cut -d ' ' -f 1)
Frequency_unit=$(iwconfig wlp0s20f3 | grep Frequency | cut -d ':' -f 3 | cut -d ' ' -f 2)

MAC_AP=$(iwconfig wlp0s20f3 | grep Access | cut -d ':' -f 4-9)
MAC_ID=$(echo $MAC_AP | cut -d ':' -f 6)

case $MAC_ID in
	7A | 7B )
		node=Node_1;;
	46 | 47 )
		node=Node_2;;
	*)
		node=Node_3;;
esac
 
bps=$(iwconfig wlp0s20f3 | grep Bit | cut -d '=' -f 2| cut -d ' ' -f 1)
bps_unit=$(iwconfig wlp0s20f3 | grep Bit | cut -d '=' -f 2| cut -d ' ' -f 2)
Ptx=$(iwconfig wlp0s20f3 | grep Bit | cut -d '=' -f 3| cut -d ' ' -f 1)
Ptx_unit=$(iwconfig wlp0s20f3 | grep Bit | cut -d '=' -f 3| cut -d ' ' -f 2)
LQ=$(iwconfig wlp0s20f3 | grep Link | cut -d '=' -f 2 | cut -d ' ' -f 1)
RSSI=$(iwconfig wlp0s20f3 | grep Signal | cut -d '=' -f 3 | cut -d ' ' -f 1)
RSSI_unit=$(iwconfig wlp0s20f3 | grep Signal | cut -d '=' -f 3 | cut -d ' ' -f 2)

echo "ESSID=$ESSID MAC_AP=$MAC_AP node=$node"
echo "Frequency=$Frequency $Frequency_unit  Vt=$bps $bps_unit"
echo "Ptx=$Ptx $Ptx_unit"
echo "Link Quality=$LQ RSSI=$RSSI $RSSI_unit"
