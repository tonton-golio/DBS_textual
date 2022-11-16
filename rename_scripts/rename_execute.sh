#!/bin/bash

# ./../../../DBS_textual/rename_check.sh | grep -e Q0

# 
# 
# 


loc=$(pwd | cut -d / -f 9) # get current location

ls | cat>files # make ned file called files with the list of filenames


while IFS= read -r file; do  #

file_original=$file
if [[ $file == files ]]
then
	blank=2 # pass
else

	#echo $file

	year=$(echo $file | grep --only --extended-regexp '20[0-2][0-9]')

	if [[ $year -gt 0 ]]
	then
	  year=$year
	else
	  year=$(echo $file | grep --only --extended-regexp '[0-2][0-9]')
	  
	  MYVAR=$file
	  #echo MYVAR $MYVAR
	  #echo year $year

	  NAME_head=${MYVAR%$year*}  # retain the part before the colon
	  NAME_tail=${MYVAR##*$year}  # retain the part after the last slash
	  
	  #echo NAME_head $NAME_head
	  #echo NAME_tail $NAME_tail


	  file_original=$file
	  file=$NAME_head$NAME_tail
	  #echo $file

	  year='20'$year
	fi





	quarter=$(echo $file | grep --ignore-case --only --extended-regexp 'q[1-4]')

	Q_num=$(echo $quarter | grep --only --extended-regexp -o -e '[0-9]')

	if [[ $Q_num -gt 0 ]]
	then
	  quarter=$quarter
	else
	  quarter=$(echo $file | grep --ignore-case --only --extended-regexp '[1-4]q|q[1-4]')
	fi
	Q_num=$(echo $quarter | grep --only --extended-regexp -o -e '[0-9]')
	#echo $Q_num
	if [[ $Q_num -gt 0 ]]
	then
	  quarter=$quarter
	else
		quarter=$(echo $file | grep --ignore-case --only --extended-regexp 'first')
		if [[ $quarter == 'first'  ||  $quarter == 'First' ||  $quarter == 'FIRST' ]]
		then
			quarter=1

		else
			quarter=$(echo $file | grep --ignore-case --only --extended-regexp 'second')
			if [[ $quarter == 'second'  ||  $quarter == 'Second' ||  $quarter == 'SECOND' ]]
			then
				quarter=2
			else
				quarter=$(echo $file | grep --ignore-case --only --extended-regexp 'third')
				if [[ $quarter == 'third'  ||  $quarter == 'Third' ||  $quarter == 'THIRD' ]]
				then
					quarter=3
				else
					quarter=$(echo $file | grep --ignore-case --only --extended-regexp 'fourth')
					if [[ $quarter == 'fourth'  ||  $quarter == 'Fourth' ||  $quarter == 'FOURTH' ]]
					then
						quarter=4
					else
						quarter=0
					fi
				fi
			fi
		fi
	fi
	Q_num=$(echo $quarter | grep --only --extended-regexp -o -e '[0-9]')


	Q=_Q
	Q_Qnum="$Q$Q_num"
	combined=$loc'_'$year$Q_Qnum'.pdf'
	
	#echo $Q_num

	# just print errors
	if [[ $Q_num -gt 0 ]]
	then
		mv -v "$file_original"  "$combined"
	else
		echo
		echo $file_original'    '$combined
		#echo; echo; echo
	fi
	
fi
done < files

rm files
