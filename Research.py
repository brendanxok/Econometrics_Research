import pandas as pd

# Reading all the files
gnidata = pd.read_csv('GNI.csv', encoding='latin-1')
prisondata = pd.read_csv('prison_population.csv', encoding='latin-1')
educationdata=pd.read_csv('mean_years_of_schooling.csv', encoding='latin-1')
lifedata=pd.read_csv('life_expectancy_index.csv', encoding='latin-1')

#cleaning up the data
cleangni = gnidata[['Country', '2015']].copy()
cleangni.columns=['Country','GNI Per Capita']
cleanprison = prisondata[['Country','2004-2015']].copy()
cleanprison.columns=['Country','Prison Population']
cleaneducation = educationdata[['Country','2015']].copy()
cleaneducation.columns=['Country','Mean Years of Schooling']
cleanlife = lifedata[['Country',"2015"]].copy()
cleanlife.columns=['Country','Life Expectancy']

#merge the dataframes then fix the index
mergeddf = pd.merge(cleangni,cleaneducation, how="left")
sndmerge = pd.merge(mergeddf,cleanlife,how='left')
totaldata = pd.merge(sndmerge,cleanprison,how='left')
totaldata = totaldata.dropna(how='any')
totaldata.reset_index(drop=True, inplace=True)

#convert to dummy variables for Life Expectancy and Prison Population
row = 0
next = 0
for x in totaldata.loc[:,'Life Expectancy']:
    if x < 0.79:
        totaldata.loc[row,'Life Expectancy'] = 0
        row+=1
    else:
        totaldata.loc[row,'Life Expectancy'] = 1
        row+=1

for x in totaldata.loc[:,'Prison Population']:
    if x < 166:
        totaldata.loc[next,'Prison Population'] = 0
        next+=1
    else:
        totaldata.loc[next,'Prison Population'] = 1
        next+=1

#save 
totaldata.to_csv('country_data.csv')
