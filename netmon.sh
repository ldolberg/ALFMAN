#!/bin/bash
while true; do
echo $(date +"%T") $(ps aux| grep iperf | wc -l) $(cat /sys/class/net/eth0/statistics/rx_bytes) $(cat /sys/class/net/eth0/statistics/rx_packets) $(cat /sys/class/net/eth0/statistics/tx_bytes) $(cat /sys/class/net/eth0/statistics/tx_packets)>> netmon.log
sleep 0.1
done

