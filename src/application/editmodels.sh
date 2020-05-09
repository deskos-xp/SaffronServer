#! /usr/bin/bash
for i in `ls models -1` ; do
	echo "$i"
	if test "$i" != "__init__.py" ; then
		if test ! -d "$i" ; then
			vim models/$i models/schema_$i
			read -rp "quit" q 
			if test "$q" == 'y' ; then
				break
			fi
		fi
	fi
done
