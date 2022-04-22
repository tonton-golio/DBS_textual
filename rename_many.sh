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

while IFS= read -r company; do
	if [[ $company == companies ]]
		then
			blank=2 # pass
		else
			echo $company
			cd $company
			./../../../DBS_textual/rename_check.sh # change to execute when ready
			cd ..
			echo
	fi
done<companies