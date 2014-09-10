#!/bin/bash
COUNTER=1
while [ $COUNTER -lt 30 ] ; do
	echo "Starting iteration" $COUNTER
	for i in `seq 1 $COUNTER`; do
		iperf -c 192.168.2.2 -t $(echo 15+$COUNTER | bc )  > /dev/null  &
		PID=$! 
		#python Linux\ Service/src/awareness_deamon/login.py $PID &
		sleep 1
	done
	#echo $(date +"%T") $COUNTER $(cat $COUNTER.psaux.log|grep '[i]perf'| cut -d' ' -f 5| paste -s -d + -) $(cat $COUNTER.psaux.log|grep '[i]perf'| cut -d' ' -f 7| paste -s -d + -)  $(cat $COUNTER.psaux.log|grep '[s]ervice_deamon'| cut -d' ' -f 9| paste -s -d + -) $(cat $COUNTER.psaux.log|grep '[s]ervice_deamon'| cut -d' ' -f 11| paste -s -d + -) 
	ps aux > $COUNTER.psaux.log
	#echo $(date +"%T") $COUNTER $(cat /sys/class/net/eth0/statistics/rx_bytes) $(cat /sys/class/net/eth0/statistics/rx_packets) $(cat /sys/class/net/eth0/statistics/tx_bytes) $(cat /sys/class/net/eth0/statistics/tx_packets)>> netmon.log
	let COUNTER=$COUNTER+1
	sleep 10
done
