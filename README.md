# Fuzzy and Nickname Matching

## Challenge
* Redundancy in database due to same customer records with different variation of names.(for example: Alexander and Alex. Both are same people with similar household address but recorded as different users in database) 
* 3 million records and difficult to manually check and edit in database. Duplicated records took extra storage in database that resulted in slower speeds for querying.

## Dataset

* Two different dataset. One through dedicated database that consisted customer name, customer address and customer ID
* The another dataset for nickname matching obtained from https://github.com/carltonnorthern/nickname-and-diminutive-names-lookup/blob/master/names.csv (credits to carltonnorthern)

## Objective

* Create a Python script that first matches nicknames with customer name from data and deletes rows with 2 or more same customers.(delete record with higher customer ID so that database has one record of the first time customer information was entered)
* For some instances, nickname matching wont solve the problem, for example customer name entered Alex Smith and Smith Alex. To fix this, fuzzy matching can be used(score can be set based on threshold for false positive)

## Outcome

* The script eliminated more than 500,000 duplicate rows from dataset. I added a new column with deleted ID's of respective customers so that it can be cross verified if deleted records are indeed duplicate.
