#!/bin/sh
if [[ -d /Users/AsianCheddar ]]; then
	echo 'this is a mac'
	cd ~/raspy
	scp run_acceptor.py laundry_main.py pi@raspy.local:~/laundry_prog
fi
if [[ -d /home/pi ]]; then
	cd ~/laundry_prog
	python run_acceptor.py start
	python laundry_main.py 
fi

