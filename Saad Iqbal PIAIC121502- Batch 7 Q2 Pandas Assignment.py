#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# # PART 1: US Census Data - 
# ## Make a scatterplot that shows average income in a state vs proportion of women in that state

# ### Task 1: 
# The first visualization your boss wants you to make is a scatterplot that shows average income in a state vs proportion of women in that state.
# 
# Open some of the census csv files in the navigator. How are they named? What kind of information do they hold? Will they help us make this graph?

# In[1066]:


df_states0 = pd.read_csv('Assignment/states0.csv')
df_states5 = pd.read_csv('Assignment/states5.csv')
df_states9 = pd.read_csv('Assignment/states9.csv')
display(df_states0, df_states5, df_states9)


# ### Task 2:
# It will be easier to inspect this data once we have it in a DataFrame. You can’t even call .head() on these csvs! How are you supposed to read them?
# 
# Using glob, loop through the census files available and load them into DataFrames. Then, concatenate all of those DataFrames together into one DataFrame, called something like us_census.

# In[2]:


import glob

# defining files path using glob
path = 'Assignment'
files = glob.glob(path + '/states*.csv') # to make sure any other irrelevant file such as inventory.csv is not uploaded

# looping through files to upload
statesList = []
for f in files:
    temp_df = pd.read_csv(f)
    statesList.append(temp_df)
    print(f'Successfully created dataframe for {f} with shape {temp_df.shape}')

# concatenating dataframes into one.
us_census = pd.concat(statesList, axis=0)
print(us_census.shape)

# Dropping the Unnamed Column, reindexing to count of elements and naming the index
us_census.drop(columns =['Unnamed: 0'], inplace = True)
us_census.index = range(len(us_census.index))
us_census.index.name='Index'
us_census.head(10)


# ### Task 3: 
# Look at the .columns and the .dtypes of the us_census DataFrame. Are those datatypes going to hinder you as you try to make histograms?

# In[3]:


print(us_census.dtypes)
print(us_census.columns) # check for Histogram


# ### Task 4: 
# Look at the .head() of the DataFrame so that you can understand why some of these dtypes are objects instead of integers or floats.

# In[4]:


us_census.head() # retrieving top 5 records 


# ### Task 5:
# Use regex to turn the Income column into a format that is ready for conversion into a numerical type.

# In[5]:


us_census['Income'] = us_census['Income'].replace('[\$,]', '', regex=True).astype(float)
print(us_census['Income'].iloc[0], us_census['Income'].dtypes)
us_census.head(1)


# ### Task 6:
# Look at the GenderPop column. We are going to want to separate this into two columns, the Men column, and the Women column.
# 
# Split the column into those two new columns using str.split and separating out those results.

# In[6]:


us_census[['GenderPop_M','GenderPop_F']] = us_census.GenderPop.str.split("_",expand=True) 

# Dropping old unified GenderPop column 
us_census.drop(columns =['GenderPop'], inplace = True) 
us_census.head()


# ### Task 7:
# Convert both of the columns into numerical datatypes.
# 
# There is still an M or an F character in each entry! We should remove those before we convert.

# In[7]:


us_census['GenderPop_M'] = us_census['GenderPop_M'].replace('M', '', regex=True)
us_census['GenderPop_F'] = us_census['GenderPop_F'].replace('F', '', regex=True)
us_census['GenderPop_M'] =pd.to_numeric(us_census['GenderPop_M'])
us_census['GenderPop_F'] =pd.to_numeric(us_census['GenderPop_F'])
print("Columns with Missing Values:")
print(us_census.isnull().sum(), us_census.dtypes)
us_census.head()


# ### Task 9:
# Did you get an error? These monstrous csv files probably have nan values in them! Print out your column with the number of women per state to see.
# 
# We can fill in those nans by using pandas’ .fillna() function.
# 
# You have the TotalPop per state, and you have the Men per state. As an estimate for the nan values in the Women column, you could use the TotalPop of that state minus the Men for that state.
# 
# Print out the Women column after filling the nan values to see if it worked!

# In[8]:


FPoP_Missing = us_census['GenderPop_F'].isnull()
print("Total Missing values in Women Population Column:",FPoP_Missing.sum())

select_index = np.array(np.where(FPoP_Missing==True)).tolist()
print("\n List of missing States:")
for i in select_index:
    x= us_census['State'].iloc[i] 
    print(x)
    
print(us_census[['State','GenderPop_F']]) # Women Population State wise

us_census['GenderPop_F'] = us_census['TotalPop'] - us_census['GenderPop_M'] # filling in the missing Women Population
print(us_census[['State','GenderPop_F']])


# ### Task 10:
# We forgot to check for duplicates! Use .duplicated() on your census DataFrame to see if we have duplicate rows in there.

# In[9]:


print(us_census['State'][us_census.duplicated()])


# ### Taske 11:
# Drop those duplicates using the .drop_duplicates() function.

# In[10]:


print("before removale of duplicates, DataFrame Shape:", us_census.shape)
us_census.drop_duplicates(keep='first',inplace=True,ignore_index=True) 
us_census.shape


# ### Task 12: Scatterplot 
# Make the scatterplot again. Now, it should be perfect! Your job is secure, for now.
# ### Task 8: Scatterplot 
# Now you should have the columns you need to make the graph and make sure your boss does not slam a ruler angrily on your desk because you’ve wasted your whole day cleaning your data with no results to show!
# 
# Use matplotlib to make a scatterplot!
# 
# plt.scatter(the_women_column, the_income_column) 
# Remember to call plt.show() to see the graph!

# In[11]:


import matplotlib as mpl
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
plt.title("Scatterplot \n Average income in a state\n vs \n Proportion of women in that state")
plt.xlabel("Propotion of Women")
plt.ylabel("Average Income")
plt.scatter(us_census['GenderPop_F'], us_census['Income']) 
plt.show()


# ### Task 13: Histograms of Races
# Now, your boss wants you to make a bunch of histograms out of the race data that you have. Look at the .columns again to see what the race categories are.

# In[777]:


us_census.columns[2:8]


# ### Task 14:
# Try to make a histogram for each one! i.e. each race
# 
# You will have to get the columns into numerical format, and those percentage signs will have to go.
# 
# Don’t forget to fill the nan values with something that makes sense! You probably dropped the duplicate rows when making your last graph, but it couldn’t hurt to check for duplicates again.
# 

# In[12]:


us_census['Hispanic'] = us_census['Hispanic'].replace('[\%]', '', regex=True)
us_census['Hispanic'] =pd.to_numeric(us_census['Hispanic'])
us_census['White'] = us_census['White'].replace('[\%]', '', regex=True)
us_census['White'] =pd.to_numeric(us_census['White'])
us_census['Black'] = us_census['Black'].replace('[\%]', '', regex=True)
us_census['Black'] =pd.to_numeric(us_census['Black'])
us_census['Native'] = us_census['Native'].replace('[\%]', '', regex=True)
us_census['Native'] =pd.to_numeric(us_census['Native'])
us_census['Asian'] = us_census['Asian'].replace('[\%]', '', regex=True)
us_census['Asian'] =pd.to_numeric(us_census['Asian'])
us_census['Pacific'] = us_census['Pacific'].replace('[\%]', '', regex=True)
us_census['Pacific'] =pd.to_numeric(us_census['Pacific'])
print("Missing values filled with NaN :")
display(us_census[["Hispanic","White","Black","Native","Asian","Pacific"]].isnull().sum())
display(us_census[["Hispanic","White","Black","Native","Asian","Pacific"]].dtypes)
print("Checking for duplicate values :")
print(us_census[us_census.duplicated()])


# In[13]:


slabs=[5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100] # self created bins
plt.title("Histogram/Population Spread of Race: Hispanic")
plt.hist(us_census['Hispanic'],slabs,
                    histtype='bar',
                    # rwidth=0.8,
                     label='Population Contribution')
plt.xlabel("% Population slabs")
plt.ylabel("Population Mode")
plt.legend()
plt.show()


# In[1080]:


slabs=[5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100] # self created bins
plt.title("Histogram/Population Spread of Race: White")
plt.hist(us_census['White'],slabs,
                    histtype='bar',
                    # rwidth=0.8,
                     label='Population Contribution')
plt.xlabel("% Population slabs")
plt.ylabel("Population Mode")
plt.legend()
plt.show()


# In[1081]:


slabs=[5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100] # self created bins
plt.title("Histogram/Population Spread of Race: Black")
plt.hist(us_census['Black'],slabs,
                    histtype='bar',
                    # rwidth=0.8,
                     label='Population Contribution')
plt.xlabel("% Population slabs")
plt.ylabel("Population Mode")
plt.legend()
plt.show()


# In[1082]:


slabs=[5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100] # self created bins
plt.title("Histogram/Population Spread of Race: Native")
plt.hist(us_census['Native'],slabs,
                    histtype='bar',
                    # rwidth=0.8,
                     label='Population Contribution')
plt.xlabel("% Population slabs")
plt.ylabel("Population Mode")
plt.legend()
plt.show()


# In[1083]:


slabs=[5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100] # self created bins
plt.title("Histogram/Population Spread of Race: Asian")
plt.hist(us_census['Asian'],slabs,
                    histtype='bar',
                    # rwidth=0.8,
                     label='Population Contribution')
plt.xlabel("% Population slabs")
plt.ylabel("Population Mode")
plt.legend()
plt.show()


# In[1084]:


us_census['Pacific'].fillna(us_census['Pacific'].mean())
slabs=[5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100] # self created bins
plt.title("Histogram/Population Spread of Race: Pacific")
plt.hist(us_census['Pacific'],slabs,
                    histtype='bar',
                    # rwidth=0.8,
                     label='Population Contribution')
plt.xlabel("% Population slabs")
plt.ylabel("Population Mode")
plt.legend()
plt.show()


# ### Task 15: Get Creative
# Phew. You’ve definitely impressed your boss on your first day of work.
# 
# But is there a way you really convey the power of pandas and Python over the drudgery of csv and Excel?
# 
# Try to make some more interesting graphs to show your boss, and the world! You may need to clean the data even more to do it, or the cleaning you have already done may give you the ease of manipulation you’ve been searching for.

# In[1091]:


plt.title("Women Population distribution wrt State")
plt.ylabel("Propotion of Women Population")
plt.boxplot(us_census['GenderPop_F'])
plt.show()


# In[1094]:


plt.title("Women Population distribution wrt State")
plt.ylabel("Propotion of Women Population")
plt.violinplot(us_census['GenderPop_F'])


# In[1095]:


plt.title("Men Population distribution wrt State")
plt.ylabel("Propotion of Men Population")
plt.violinplot(us_census['GenderPop_M'])


# In[1096]:


plt.title("Income distribution wrt State")
plt.ylabel("Propotion of Income")
plt.violinplot(us_census['Income'])


# In[ ]:





# In[34]:


print(us_census.columns)
Hispanic=((((us_census['Hispanic'])/100)*us_census['TotalPop']).sum()).astype(int)
White=((((us_census['White'])/100)*us_census['TotalPop']).sum()).astype(int)
Black=((((us_census['Black'])/100)*us_census['TotalPop']).sum()).astype(int)
Native=((((us_census['Native'])/100)*us_census['TotalPop']).sum()).astype(int)
Asian=((((us_census['Asian'])/100)*us_census['TotalPop']).sum()).astype(int)
Pacific=((((us_census['Pacific'])/100)*us_census['TotalPop']).sum()).astype(int)
print(Hispanic,White,Black,Native,Asian,Pacific)
Population_Race = [Hispanic, White, Black, Native, Asian, Pacific]
legend= ['Hispanic', 'White', 'Black', 'Native', 'Asian',
       'Pacific']
explode = (0, 0, 0, 2,0,2) 
plt.pie(Population_Race,radius=2, explode=explode, labels = legend,autopct='%1.2f%%',rotatelabels=True)
plt.legend(title = "Population Composition of USA wrt Race")
plt.show()


# # PART 1: Petal Power Inventory - 
# ## You’re the lead data analyst for a chain of gardening stores called Petal Power. Help them analyze their inventory!

# ### Task 1:
# Data for all of the locations of Petal Power is in the file inventory.csv. Load the data into a DataFrame called inventory.

# In[841]:


inventory = pd.read_csv('Assignment/inventory.csv')
print("DataFrame Shape: ",inventory.shape,'\n')
print("DataFrame Columns: ",inventory.columns,'\n')
print("DataFrame Columns DataTypes : \n",inventory.dtypes,'\n')
inventory['location']=inventory.location.astype("string")
inventory['product_type']=inventory['product_type'].astype("string")
inventory['product_description']=inventory['product_description'].astype("string")
print("DataFrame Columns DataTypes after conversion : \n",inventory.dtypes,'\n')
print("Checking for missing/null values :")
print(inventory.isnull().sum()) # checking for null values
print("Checking for duplicate records :")
print(inventory.duplicated().sum())


# ### Task 2:
# Inspect the first 10 rows of inventory.
# 

# In[810]:


inventory.head(10)


# ### Task 3:
# The first 10 rows represent data from your Staten Island location. Select these rows and save them to staten_island.

# In[813]:


staten_island = pd.DataFrame(inventory.loc[0:9])
staten_island


# ### Task 4:
# A customer just emailed you asking what products are sold at your Staten Island location. Select the column product_description from staten_island and save it to the variable product_request.

# In[844]:


product_request = staten_island['product_description']
product_request


# ### Task 5:
# Another customer emails to ask what types of seeds are sold at the Brooklyn location.
# 
# Select all rows where location is equal to Brooklyn and product_type is equal to seeds and save them to the variable seed_request

# In[849]:


seed_request = inventory[(inventory['location'] =='Brooklyn') & (inventory['product_type'] == 'seeds')]
seed_request


# ### Task 6:
# Add a column to inventory called in_stock which is True if quantity is greater than 0 and False if quantity equals 0.

# In[858]:


inventory['in_stock']=pd.Series(np.where(inventory['quantity'] > 0,True,False))
inventory


# ### Task 7:
# Petal Power wants to know how valuable their current inventory is.
# 
# Create a column called total_value that is equal to price multiplied by quantity.

# In[860]:


inventory['total_value'] = inventory.price * inventory.quantity
inventory.head()


# ### Task 8:
# The Marketing department wants a complete description of each product for their catalog.
# 
# The following lambda function combines product_type and product_description into a single string:
# 
# combine_lambda = lambda row: \
#     '{} - {}'.format(row.product_type,
#                      row.product_description)
# Paste this function into script.py.

# In[1012]:


get_ipython().run_line_magic('run', '"script.py"')


# ### Task 9:
# Using combine_lambda, create a new column in inventory called full_description that has the complete description of each product.

# In[1018]:


desc_list = []
for i in range(len(inventory.index)):
    desc_list.append(combine_lambda(inventory.iloc[i]))
inventory['full_description'] = pd.Series(desc_list)
inventory.tail()


# In[ ]:




