# Libraries imports
import pandas as pd
import re
######################################################################################################################

# Datasets imports as pandas DataFrames
with open('references initialized in shop.csv') as csv_file_not_cleaned:
    csv_text = csv_file_not_cleaned.read()
    
list_refs = []
for i in [x.split(',""') for x in csv_text.split('\n')]:
    if len(i) == 5:
        list_refs.append(i)

ref_in_shop = pd.DataFrame(list_refs[1:], columns=list_refs[0])

reteailer_extract = pd.read_excel('retailer extract vLB.xls')
reteailer_extract['EAN'] = reteailer_extract['EAN'].astype(str)
######################################################################################################################

# Removing the "" from the data of studied columns
ref_in_shop['reference_id""'] = ref_in_shop['reference_id""'].apply(lambda x: re.sub('""', '', x))
ref_in_shop['aisle""'] = ref_in_shop['aisle""'].apply(lambda x: re.sub('""', '', x))
ref_in_shop['last_control"""'] = ref_in_shop['last_control"""'].apply(lambda x: re.sub('"""', '', x)).apply(pd.to_datetime)

######################################################################################################################

# Selecting in the retailer extract the products that are found in the references initialized in shop file
ref_in = reteailer_extract.loc[reteailer_extract['EAN'].isin(ref_in_shop['reference_id""'].tolist())]

######################################################################################################################

# For each Label, the number of Unique values is given
print('Number of Unique values for each Libellé')
print('Libellé                          In Retailer              In reference')
for i in reteailer_extract.columns:
    if 'Libellé' in i:
        print('{}   {}             {}'.format(i, reteailer_extract[i].describe(include = ['O'])['unique'], ref_in[i].describe(include = ['O'])['unique']))
print('-'*100)

######################################################################################################################

# For each label, showing the statistical analysis of the spread of products for each category
print('Analysis of the number of products by the label Famille')
tf = ref_in[['Libellé  Famille ', 'Article Libellé Long']].groupby(['Libellé  Famille ']).count()
print(tf.describe())
print('-'*100)

print('Analysis of the number of products by the label Sous-Famille')
tsf = ref_in[['Libellé  Sous-Famille ', 'Article Libellé Long']].groupby(['Libellé  Sous-Famille ']).count()
print(tsf.describe())
print('-'*100)

print('Analysis of the number of products by the label Unité de Besoin')
tub = ref_in[['Libellé Unité de Besoin ', 'Article Libellé Long']].groupby(['Libellé Unité de Besoin ']).count()
print(tub.describe())
print('-'*100)

print('Analysis of the number of products by the label code interne Enseigne')
tie = ref_in[['Libellé code interne Enseigne', 'Article Libellé Long']].groupby(['Libellé code interne Enseigne']).count()
print(tie.describe())
print('-'*100)
######################################################################################################################

print('Analysis of the quantity in stock values')
print(reteailer_extract['Stock en quantité'].describe())
print('-'*100)

######################################################################################################################

print('Odest date and Newest date')
print('For the initialized references: ', ref_in_shop['last_control"""'].min(),'   ', ref_in_shop['last_control"""'].max())
print('For the retailer extract: ', reteailer_extract['Date dernière réception'].min(), '   ',reteailer_extract['Date dernière réception'].max())
