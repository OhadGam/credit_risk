# -*- coding: utf-8 -*-
"""Credit_Risk_EDA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TUrIisX9CEAdnoVvk3vKuYf0JFoQTNl-

# Data and Libraries
"""

#import libararies
import numpy as np 
import pandas as pd 
from datetime import datetime

# mount drive
from google.colab import drive
drive.mount('/content/drive')

import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.preprocessing import MaxAbsScaler, MinMaxScaler, StandardScaler

pd.set_option("max_columns",0)

df = pd.read_csv('/content/drive/MyDrive/Naya - Keren Ohad Rotem/CSV//df_total.csv')
df.drop(['Unnamed: 0', 'ID'], axis=1, inplace=True)

df,head()

df.info()

"""# EDA

## Outliers

We tested outliers on all the features in the dataframe.
An example of the test procedure for a specific column - DAYS_EMPLYED is shown below:
"""

sns.boxplot(df['DAYS_EMPLOYED'])

"""<font color='blue'>The column shows the total days in the last workplace in relation to the date of the current loan application.There can be no values higher than 0"""

df['AGE']=-(df['DAYS_BIRTH']/365).astype('int')

mask_days_emp=df[df['DAYS_EMPLOYED'] <= 0]
sns.boxplot(mask_days_emp['DAYS_EMPLOYED'])

"""<font color='blue'>Minimum values are obtained in a column of about 17,000 days - about 50 years. We will check in comparison with the age column that the figure is indeed possible:"""

plt.scatter(data=mask_days_emp, x='DAYS_EMPLOYED' ,y='AGE')
plt.xlabel('DAYS_EMPLOYED')
plt.ylabel('AGE')
plt.title('DAYS_EMPLOYED VS AGE')

"""<font color='blue'>High number of working days - about 50 years, obtained ages 60-70 years.
it makes sense that those costuners started working at the age of 20.
"""

#fuction for dropping outliers from all columns

def outliers_drop(df):

    df_eda1=pd.DataFrame(df)
    outliers_index = df.loc[(df['AMT_INCOME'] > 2000000) | (df['AMT_APP'] > 2800000) |\
                        (df['AMT_ANNUITY'] >185000) | (df['BU_SUM_LOAN']> 200000000) |\
                        (df['BU_SUM_OPEN_DEBT']> 20000000) | (df['HC_NUM_APP']> 15) |\
                        (df['BU_NUM_LOAN']> 80) | (df['HC_MEAN_AMT_APP'] > 2500000) |\
                        (df['HC_MEAN_PER_AMT_APPROVAL'] > 1.6) | (df['HC_PER_DEBT'] > 0) |\
                        (df['HC_MEAN_ANNUITY'] > 200000) | (df['HC_MEAN_NUM_INST'] > 80) |\
                        (df['HC_MEAN_AMT_INST'] > 1000000) | (df['HC_MEAN_PER_DOWN'] > 0.90) |\
                        (df['HC_MEAN_DELAY_INST'] > 300)].index

    df_eda1= df_eda1.drop(outliers_index , axis=0)
    df_eda1= df_eda1.drop('AGE' , axis=1)
    df_eda1['DAYS_EMPLOYED'].replace(365243, 0, inplace=True)
    return df_eda1

df_eda1=outliers_drop(df)

df_eda1.shape

"""<font color='blue'>finally- after outliers EDA we droped 333 index.

## Dummies EDA

<font color='blue'>Dummis was made for the categorial features. let's have a look on their behavior:
"""

#TYPE EDUCATION features
col_type_education = ['TYPE_EDUCATIOM:Higher', 'TYPE_EDUCATIOM:Incomplete', 'TYPE_EDUCATIOM:Secondary']

#TYPE HOUSE features
col_type_house = ['TYPE_HOUSE:House', 'TYPE_HOUSE:Municipal', 'TYPE_HOUSE:Rented', 'TYPE_HOUSE:Parents']

#FAMILY STATUS features
col_type_family = ['FAMILY_STATUS:Married', 'FAMILY_STATUS:Widow', 'FAMILY_STATUS:Single']

#TYPE INCOME features
col_type_income = ['TYPE_INCOME:Associate', 'TYPE_INCOME:Pensioner', 'TYPE_INCOME:Unemployed','TYPE_INCOME:Working']

#TYPE previous loans status features
col_prev_loan_status = ['BU_PER_ACCTIVE','BU_PER_CLOSED','HC_PER_ACCTIVE','HC_PER_CLOSED']

df_edu = df_eda1.filter(col_type_education, axis=1)
df_house = df_eda1.filter(col_type_house, axis=1)
df_family = df_eda1.filter(col_type_family, axis=1)
df_income = df_eda1.filter(col_type_income, axis=1)
df_prev_status = df_eda1.filter(col_prev_loan_status, axis=1)

"""### Education Type Features"""

df_edu.sum(axis=0)/df_edu.shape[0]

# plotting correlation heatmap
fig=plt.figure(figsize=(4,4))
dataplot = sns.heatmap(df_edu.corr(), cmap="YlGnBu", annot=True)

# displaying heatmap
plt.show()

"""<font color='blue'> * Secondary status is 72% of the data, and with corr of 0.92 to higher status. By that, we have chosen to represent the 3 statuses in one column TYPE_EDUCATIN:Higher

<font color='blue'> - 0 values represented the status incomplete + secondary.

<font color='blue'> - 1 values represented higher education.

<font color='blue'> * The unification of the groups is due to the fact that the incomplete status constitutes only 3% of the group of secondary education status.
<font color='blue'>

### House Type Features
"""

df_house.sum(axis=0)/df_house.shape[0]

# plotting correlation heatmap
fig=plt.figure(figsize=(4,4))
dataplot = sns.heatmap(df_house.corr(), cmap="YlGnBu", annot=True)

# displaying heatmap
plt.show()

"""<font color='blue'> TYPE_HOUSE:House column is about 90% of the data.
<font color='blue'>  * we have chosen to represent the 4 statuses in one column TYPE_HOUSE:House. 

<font color='blue'> - 1 values represented TYPE_HOUSE:House .

<font color='blue'> - 0 values represented the others status all together.

<font color='blue'> * The unification of the groups is due to the fact that the Parents, Rented and Municipal status constitutes only 10% of the data and their status refers to less economical stable status.
</font>

### Family Status Features
"""

df_family.sum(axis=0)/df_family.shape[0]

# plotting correlation heatmap
fig=plt.figure(figsize=(4,4))
dataplot = sns.heatmap(df_family.corr(), cmap="YlGnBu", annot=True)

# displaying heatmap
plt.show()

"""<font color='blue'> FAMILY STATUS:Married column is about 74% of the data.
<font color='blue'> * we have chosen to represent the 3 statuses in one column TYPE_HOUSE:House. 

<font color='blue'>- 1 values represented FAMILY STATUS:Married .

<font color='blue'>- 0 values represented the others status. 

<font color='blue'>* The unification of the statuses is due to the fact that widow is only 5% of the data and is close to the group of single by that both groups coul'd be with less economic stability.

### Income Type Features
"""

df_income.sum(axis=0)/df_income.shape[0]

# plotting correlation heatmap
fig=plt.figure(figsize=(4,4))
dataplot = sns.heatmap(df_income.corr(), cmap="YlGnBu", annot=True)

# displaying heatmap
plt.show()

"""<font color='blue'> TYPE_INCOME column: there are 4 dummis in the dataframe.Unemployed column with less then 1% of the data, this column

Previous loans status
"""

# plotting correlation heatmap
fig=plt.figure(figsize=(4,4))
dataplot = sns.heatmap(df_prev_status.corr(), cmap="YlGnBu", annot=True)

# displaying heatmap
plt.show()

"""<font color='blue'> active and closed previous loans status are complement (corr=1) each other and their by we will drop 'closed' status column for HC and BU data.

<font color='blue'> -1 values represant active loan status.

<font color='blue'> -0 values represent close loan atatus.
"""

#dropping columns as decided in this section (Dummies EDA)
df_eda2=df_eda1.drop(['TYPE_HOUSE:Municipal', 'TYPE_HOUSE:Rented',
                          'TYPE_HOUSE:Parents','TYPE_INCOME:Unemployed',
                          'TYPE_EDUCATIOM:Incomplete','TYPE_EDUCATIOM:Secondary',
                          'FAMILY_STATUS:Widow', 'FAMILY_STATUS:Single',
                          'BU_PER_CLOSED','HC_PER_CLOSED'], axis=1)

"""## Correlation Between Features"""

col_corr= ['AMT_ANNUITY','AMT_APP','HC_MEAN_AMT_APP','HC_MEAN_ANNUITY','HC_MEAN_PER_DOWN','HC_MEAN_PER_AMT_APPROVAL']
df_corr=df_eda2.filter(col_corr,axis=1)

# plotting correlation heatmap
fig=plt.figure(figsize=(5,5))
dataplot = sns.heatmap(df_corr.corr(), cmap="YlGnBu", annot=True)

# displaying heatmap
plt.show()

"""<font color='blue'>**Let's explore the columns with correlation**:"""

sns.regplot(data = df_eda2,
            x='HC_MEAN_PER_DOWN',
            y='HC_MEAN_PER_AMT_APPROVAL',
            line_kws={'color': 'red'},
            scatter_kws = {'alpha' : 0.2})

"""<font color='blue'>Loan approval ratio is higher while debt reduction is lower, whic also consistant with the logic. Since there is a correlation between these two columns, we will drop one of them : HC_MEAN_PER_DOWN.
 
"""

sns.regplot(data = df_eda2,
            x='AMT_ANNUITY',
            y='AMT_APP',
            line_kws={'color': 'red'},
            scatter_kws = {'alpha' : 0.2})

sns.regplot(data = df_eda2,
            x='HC_MEAN_AMT_APP',
            y='HC_MEAN_ANNUITY',
            line_kws={'color': 'red'},
            scatter_kws = {'alpha' : 0.2})

"""<font color='blue'> Loan application amountis higher while Annuity amount is higher. Since there is a correlation between these two columns, we will drop one of them : AMT_ANNUITY
 
"""

df_eda3=df_eda2.drop(['HC_MEAN_PER_DOWN','HC_MEAN_ANNUITY','AMT_ANNUITY'],axis=1)

"""##Imbalanced Data"""

#The part that constitutes whether he received a loan (0) or if he was rejected (1) from in TARGET column
df['TARGET'].value_counts()/df.shape[0]

"""<font color='blue'>rejected loans are 7.8% from the data. We'll address this at the model part.

## Features (int type) VS TARGET
"""

col_amt = [ 'DAYS_BIRTH',  'HC_NUM_APP', 'BU_NUM_LOAN','HC_NUM_APP','HC_MEAN_NUM_INST', 
           'HC_MEAN_AMT_DIFF_INST', 'DAYS_EMPLOYED','CNT_CHILDREN' ]

df_amt=df_eda2.filter(col_amt,axis=1)

scaler = StandardScaler()

df_amt[col_amt] = scaler.fit_transform(df_amt[col_amt])

df_amt['TARGET']=df_eda2['TARGET']

color_main = 'gold'
my_colors = [color_main, 'salmon', 'wheat', 'red']

# Dist plot of all numberical features
fig, ax = plt.subplots(ncols=2, nrows=4, figsize=(15,15))
index, ax = 0, ax.flatten()
title = "numerical features distribution"
sample = df_eda3.reset_index()
sns.set(font_scale=0.9)

for col in col_amt:
    sns.kdeplot(data=df_eda3, x=col,common_norm=False,hue='TARGET',
                    palette=my_colors[:2],shade=True, edgecolor="black",
                   ax=ax[index]).set_title(f"{col} distribution", weight="bold")
    index += 1
plt.tight_layout(pad=0.5, w_pad=0.7, h_pad=3.0)

"""<font color='blue'>**It is almost impossible to distinguish between the features associated with target 0 and those associated with target 1.**"""

mask_0= df_eda3[df_eda3['TARGET']==0]
mask_1=df_eda3[df_eda3['TARGET']==1]

plt.figure()
plt.plot(mask_0.HC_MEAN_AMT_DIFF_INST, mask_0.DAYS_EMPLOYED, '.b')
plt.plot(mask_1.HC_MEAN_AMT_DIFF_INST, mask_1.DAYS_EMPLOYED, 
         linewidth=3, color='g', ls='', marker='.')

plt.xlabel('HC_MEAN_AMT_DIFF_INST')
plt.ylabel('DAYS_EMPLOYED')
plt.title('days employed vs. installments payment difference')
plt.legend(['0', '1'], loc='best')

"""<font color='blue'>An example of the behavior of two features with a distinction between the target. It can be seen that the target group 1 is contained in the target group 0. This behavior is very similar to all the features, which will make it very difficult for the models for prediction."""

df_eda3.to_csv('/content/drive/MyDrive/Naya - Keren Ohad Rotem/Keren_SelfWork/CSV/df_final_eda.csv')

df_eda3.info()