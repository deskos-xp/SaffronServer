#! /usr/bin/bash

function main(){
	for i in `ls  shell/tests_*.sh -1` ; do
		echo $i 
		echo bash $i | bash 
		echo 
	done
}
main
