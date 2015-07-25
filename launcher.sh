#!/bin/sh
# Make sure you can make virtual environments.
make_env(){
	req=$(find ~/ -iname require.txt)
	cd /envs
	virtualenv laundry
	source /envs/laundry/bin/activate
	pip install -r $req
}

vir_check=$(pip list | grep virtualenv)
if [[  $vir_check  ]]; then
	echo 'virtualenv has been installed!'
else
	echo "Need to install virtualenv"
	pip install virtualenv
	echo "Done"
fi
# Check if the environment root is in place, if not make it. 
if [[ -d /envs ]]; then
	echo "/envs already exists. "
	if [[ -d /envs/laundry/bin ]]; then
		echo "Virtual environment for laundry exists!"
	else
		echo "Virtual environment for laundry did not exist, let's make it."
		make_env
	fi
else
	cd /
	mkdir envs
	make_env
fi
