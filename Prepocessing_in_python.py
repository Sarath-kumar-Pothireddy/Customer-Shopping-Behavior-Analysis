#-- Customer shopping behaviour EDA analysis --# 

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel(r"C:\Users\LENOVO\OneDrive\Desktop\Own_project\data_set.xlsx") #it reads external files 

df.info

df.info()

df.describe() 
df.describe(include = 'all') #it uses describe about all columns (numerical & categorical) 


df.isnull().sum() #finding null values 

df['Review Rating'] = df.groupby('Category') ['Review Rating'].transform(lambda x: x.fillna(x.median())) #replace that null values into median value 

df.isnull().sum() #after replacing check null values

df.columns = df.columns.str.lower()  #it uses column name changes upper case into lower case 
df.columns = df.columns.str.replace(' ','_')  #it uses in column name inner spaces replaced into underscore '_'
df = df.rename(columns = {'purchase_amount_(usd)' : 'purchase_amount'}) #rename the column purchase_amount_(use) into purchase_amount

df.columns


# find skewness
df.age.skew()
df.purchase_amount.skew()
df.review_rating.skew()
df.previous_purchases.skew()

#Find outliers 
sns.boxplot(df.age)
sns.boxplot(df.purchase_amount)
sns.boxplot(df.review_rating)
sns.boxplot(df.previous_purchases)


#View how data is distribution 
sns.histplot(df['age'], kde = True)
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.title('Age distribution')
plt.show()

sns.histplot(df['purchase_amount'], kde = True)
plt.title('Purchase Amount')
plt.show()

sns.histplot(df['review_rating'], kde = True)
plt.title('Review Rating')
plt.show()

sns.histplot(df['previous_purchases'], kde = True)
plt.title('Previous Purchases')
plt.show()

#find duplicates Rows
duplicate = df.duplicated() 
duplicate
sum(duplicate)

#find column duplicates
duplicate_columns = df.columns[df.T.duplicated()]
duplicate_columns 

df[['discount_applied','promo_code_used']].head(10) #display the 10 rows of discount_applied & promocode_used

(df['discount_applied'] == df['promo_code_used']).all() #check the columns both same or notsame

df = df.drop('promo_code_used', axis = 1) #drop promo_code_used column 

df.columns


#create a new column age group
labels = ['Young Adult', 'Adult', 'Middle Aged', 'Senior']  #define labels
df['age_group'] = pd.qcut(df['age'], q = 4, labels = labels) #allot the lables according the data 

df[['age','age_group']].head(10) #check the data allouted or not 


#creating column purchase frequency days
frequency_mapping = {
    'Fortnightly'   : 14,
    'Weekly'        : 7,
    'Monthly'       : 30,
    'Quarterly'     : 90,
    'Bi-Weekly'     : 14,
    'Annually'      : 365, 
    'Every 3Months' : 90      }

df['purchase_frequency_days'] = df['frequency_of_purchases'].str.strip().str.title()
    
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)

df[['purchase_frequency_days','frequency_of_purchases']].head(10)




# import modules for connecting python to MySQl
from sqlalchemy import create_engine
from urllib.parse import quote

user =  'root'                       # give MySQL user name 
pw   =  quote('Sarath@1911')         # give pssword
db   =  'retail_customer_behavior'   # give data base name 

engine = create_engine(f"mysql+pymysql://{user}:{pw}@localhost/{db}")  #create the engine to connect the MySQL databse to SQLalchemy 

df.to_sql('data_set', con = engine, if_exists = 'replace', chunksize = 100, index = False) #push that data into MySQL 

sql = 'select * from data_set'

df = pd.read_sql_query(sql, con = engine)

print(df)

