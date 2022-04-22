# Digital Business Strategy textual

The aim here is; extract text from shareholder decks, and look for occurance frequency of keywords associated with diffrent aspects of a business;
* Scope
* Scale
* Speed
* DBS
* Source


## How to use this repo
**Downloading**
1. Download shareholder decks into a folder for each company
**Renaming**
1. use rename_many.sh set to initialize rename_check.sh (line 27)
1. Fix original files names where it indicates an error
1. use rename_many.sh with rename_execute.sh (line 27)
**Keywords dict**
1. Run keyword.ipynb to obtain lemmanized and stemmed keywords
**Look up**
1. Run Shareholder_deck_keywords_newApproach to obtain occurance of keywords in the different shareholder decks.