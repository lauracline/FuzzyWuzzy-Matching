# Fuzzy and Nickname Matching

## Challenge
* Multiple same customer records in database with different variation of names(for example: Alexander and Alex. Both are same people with similar household address but recorded as different users in database.) 
* 2.5 million records and thus difficult to manually perform this operation. Also due to duplication of records, extra storage was being taken in database that resulted in slower speeds for querying.

## Dataset

* Two different dataset. One through dedicated database that consisted Customer Name, Customer Address and Customer ID
* The another dataset for nickname matching obtained from https://github.com/carltonnorthern/nickname-and-diminutive-names-lookup/blob/master/names.csv (credits to carltonnorthern)

## Objective

* Write a script in Python that first matches nicknames with Customer Name from data and deletes rows with 2 or more same customers.(delete record with higher Customer ID so that database has one record of the first time customer information was entered.)
* For some instances, nickname matching wont solve the problem.(for example customer name entered Alex Smith and Smith Alex). To fix this, fuzzy matching can be used(score can be set based on threshold for false positive)

## Script

* Initially I hard-coded the script(underestimating the size of data). The result was that it took more than 18 hours to run the script. Not feasible solution!
* Even though the script was working correctly, I had to come up with solution that makes the computation faster.
* Creating dictionary, functions and changing logic helped as it reduced the computational time from 18 hours to 30 minutes. 

## Conclusion

* The script eliminated more than 500,000 duplicate rows from dataset. I added a new column with deleted ID's of respective Customers so that it can be cross verified if deleted records are indeed duplicate.
