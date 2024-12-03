- NORMALIZAR PORCENTAJES

set_network 0 bgscan "simple:30:-120:86400"

alfa1
10 -> 1Mbps
11 -> 1Mbps
12 -> 1Mbps
13 -> 5Mbps
14 -> 5Mbps
15 -> 11Mbps
16 -> 11Mbps

alfa2
01 -> 1Mbps
02 -> 1Mbps
03 -> 5Mbps
04 -> 5Mbps
05 -> 11Mbps
06 -> 11Mbps

intel
01 -> 1Mbps
02 -> 1Mbps
03 -> 5Mbps
04 -> 11Mbps
05 -> 11Mbps CON bgscan ACTIVADO

hacer resta ultima graf (la de Nº paquetes)



((!(icmp.type == 3) && ip.dst == 192.168.68.101) && !(ntp) && udp) && !(dns)

((((((!(icmp.type == 3)) && !(ntp) && udp) && !(dns)) && !(ssdp)) && !(dhcpv6)) && !(mdns)) && !(quic)