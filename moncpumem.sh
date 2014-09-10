#!/bin/bash
while true; do
echo $(date +"%T") $(ps aux| grep iperf | wc -l) $(ps aux|grep $1|grep root| cut -d' ' -f 9,11) >> cpu_mem_$1.log
sleep 0.1
done

