#rename_many.sh
# remember to chmod +x  rename_many.sh

# i want to print:
#Company, number of reports, passed/failed


#	cd Shareholder_decks; ls; cd .. # go print and come back

# number_of_companies = 
echo "number of companies:"
cd Shareholder_decks; ls | wc -w ; cd ..


# companies =
cd Shareholder_decks; ls | cat > companies 

# pwd: we are in the right place


NPZfiles=$(ls |  grep -e '.npz')


while IFS= read -r company; do
	bad=false
	if [[ $company == companies ]]
		then
			bad=True
	fi
	for n in NPZfiles; do
		if [[ $company == $n ]]
			then 
				bad=True
		fi



	if [[ $bad == false ]]
		
		then
			echo $company
			cd $company
			./../../../DBS_textual/rename_check.sh # change to execute when ready
			cd ..
			echo
	fi
done<companies


rm companies


