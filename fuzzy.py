#import libraries
import os
import pandas as pd
import collections
import time
from fuzzywuzzy import fuzz

#set directory
os.chdir('C:\\Users\\YourFolder')

#created fictional dataset that resembles the original dataset 
d = {'Customer Name': ['ED SMITH','EDWARD SMITH','JOE DOE','PAT MUELLER','PATRICK MUELLER','LISA DANE', 
                       'ALEX SMITH', 'SMITH ALEX','DIANA HAYDEN','RUSS PARK','SARA JANE', 'AARON GOMSEY',
                       'ARON GOMSEY','KIM CHEN','SCOTT HARRIS','ELIZABETH HURN','LIZ HURN','ROBERT LIN',
                       'ANDY ROBERTSON','JORDAN HENDERSON'],
     'Customer Address': ['218-KENSINGTON-DETROIT-MI','218-KENSINGTON-DETROIT-MI','SUNPHARMA-NOVI-MI',
                          '7650-ASHWOODPARK-DALLAS-TX','7650-ASHWOODPARK-DALLAS-TX','2100-PEBBLEVALE-MIAMI-FL',
                          '16-MISSIONSTREET-SANFRANCISCO-CA','16-MISSIONSTREET-SANFRANCISCO-CA','FARM-WOOD-AZ',
                          'WEST-CAMBELL-LASVEGAS-NV','9-OAKS-APTS-BUFFALO-NY','11-DNAWAY-REDWOOD-CA',
                          '11-DNAWAY-REDWOOD-CA','8-ELMOND-BOLINGBROOK-IL','9024-SOUTHSTREET-MONSEY-NY',
                          '53-DOGWOOD-LIVINGSTON-NJ','53-DOGWOOD-LIVINGSTON-NJ','8505-CORONAAVE-BARBERTON-OH',
                          '11-PULASKIAVE-EASTSTROUD-PA','161-SUMMITDR-WAUSAU-WI'],
     'Customer ID': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]}

df = pd.DataFrame(data=d)
print(df.head())

#read nicknames csv file from below link
#"https://github.com/carltonnorthern/nickname-and-diminutive-names-lookup/blob/master/names.csv"
nick_df = pd.read_csv('Nicknames.csv', sep=',', header=0)
print(nick_df.head())

#update duplicate dictionary, keys are ID that is kept in final data
#vals are list of dups discarded as result of comparision with key
def update_dups(dupdict,keep,discard):
    if keep[2]!=discard[2] and discard[2] in dupdict:
        for id in dupdict[discard[2]]:
            dupdict[keep[2]].append(id)
        del dupdict[discard[2]]
    dupdict[keep[2]].append(discard[2])
    return dupdict


#define new function called dups that discards duplicates of higher ID number and creates a seperate dataframe 
#final resemble data without duplicates
#discarded consist duplicate records data
def dups(final, discard, people, key, dupdict):
    p1=people[0]
    if len(people)>1:
        iterpeople=people[1:]
        for p2 in iterpeople:
            if (p1[0] in inverse and p2[0] in inverse[p1[0]]) or (p2[0] in inverse and p1[0] in inverse[p2[0]]):
                if p1[2]<=p2[2]:
                    dupdict=update_dups(dupdict,p1,p2)
                    discard.append([p2[1],key,p2[2]])
                    people.remove(p2)
                else:
                    dupdict=update_dups(dupdict,p2,p1)
                    discard.append([p1[1],key,p1[2]])
                    return dups(final,discard,people[1:],key,dupdict)
        final.append([p1[1],key,p1[2]])
        if len(people)>1:
            return dups(final,discard,people[1:],key,dupdict)
        else:
            return final, discard, dupdict
    else:
        final.append([p1[1],key,p1[2]])
        return final, discard, dupdict
    

#updates duplicate dictionary, keys are ID that is kept in final data 
#vals are list of dups discarded as result of comparision with key
def update_fuzzy(dupdict,keep,discard):
    if keep[1]!=discard[1] and discard[1] in dupdict:
        for id in dupdict[discard[1]]:
            dupdict[keep[1]].append(id)
        del dupdict[discard[1]]
    dupdict[keep[1]].append(discard[1])
    return dupdict


#define new function called dups that discards duplicates of higher ID number and creates a seperate dataframe 
#final resemble data without duplicates
#discarded consist duplicate records data
def fuzzydups(final, discard, people, key, dupdict):
    p1=people[0]
    if len(people)>1:
        iterpeople=people[1:]
        for p2 in iterpeople:
            if fuzz.token_set_ratio(p1[0],p2[0]) > 80:
                if p1[1]<=p2[1]:
                    dupdict=update_fuzzy(dupdict,p1,p2)
                    discard.append([p2[0],key,p2[1]])
                    people.remove(p2)
                else:
                    dupdict=update_fuzzy(dupdict,p2,p1)
                    discard.append([p1[0],key,p1[1]])
                    return fuzzydups(final,discard,people[1:],key,dupdict)
        final.append([p1[0],key,p1[1]])
        if len(people)>1:
            return fuzzydups(final,discard,people[1:],key,dupdict)
        else:
            return final, discard, dupdict
    else:
        final.append([p1[0],key,p1[1]])
        return final, discard, dupdict


#create dict from nickname csv
start_time = time.time() 

d={}
for index, row in nick_df.iterrows():
    s=row[0].split(',')
    d[s[0]]=s[1:]
    
    
#invert dictionary so that nicknames are keys
inverse=dict()
for key in d:
    for val in d[key]:
        if val not in inverse:
            inverse[val]=[key]
        else:
            inverse[val].append(key)
            

#create dict from address to list of customers for nickname matching                    
testdict={}
for index,row in df.iterrows():
    if row[1] not in testdict:
        testdict[row[1]]=[[row[0].split(' ')[0].lower(),row[0],row[2]]]
    else:
        testdict[row[1]].append([row[0].split(' ')[0].lower(),row[0],row[2]])       

#run nickname matching
final=[]
discarded=[]
dupdict=collections.defaultdict(list)
for key,val in testdict.items():
    people=list(val)
    f,d,dupdict=dups([],[],people,key,dupdict)
    final+=f
    discarded+=d
newdf=pd.DataFrame(final, columns=['NAME', 'KEY', 'CUST_MSTR_ID'])
dropped=pd.DataFrame(discarded, columns=['NAME', 'KEY', 'CUST_MSTR_ID'])

print("My program took", time.time() - start_time, "to run") 

#create dict from filtered data for fuzzy matching
start_time = time.time() 

fuzzydict={}
for index,row in newdf.iterrows():
    if row[1] not in fuzzydict:
        fuzzydict[row[1]]=[[row[0],row[2]]]
    else:
        fuzzydict[row[1]].append([row[0],row[2]])
    
#run fuzzy matching
fuzzyfinal=[]
fuzzydiscard=[]
for key,val in fuzzydict.items():
    people=list(val)
    f,d,dupdict=fuzzydups([],[],people,key,dupdict)
    fuzzyfinal+=f
    fuzzydiscard+=d
fuzzydf=pd.DataFrame(fuzzyfinal, columns=['NAME', 'KEY', 'CUST_MSTR_ID'])
fuzzydropped=pd.DataFrame(fuzzydiscard, columns=['NAME', 'KEY', 'CUST_MSTR_ID'])

print("My program took", time.time() - start_time, "to run") 

#combine records dropped in nickname/fuzzy matching
alldropped=pd.concat([dropped,fuzzydropped], ignore_index=True)

#add column to final data with all duplicate IDs for row     
l=[]
for index, row in fuzzydf.iterrows():
    if row[2] in dupdict:
        l.append(dupdict[row[2]])
    else:
        l.append([])
fuzzydf['DUPLICATE_IDS']=pd.Series(l)


#save file with final data after fuzzy matching
writer = pd.ExcelWriter('fuzzy_final.xlsx', engine='xlsxwriter')
fuzzydf.to_excel(writer, index=False)
writer.save()

#save file with all dropped IDs
writer = pd.ExcelWriter('drop_final.xlsx', engine='xlsxwriter')
alldropped.to_excel(writer, index=False)
writer.save()