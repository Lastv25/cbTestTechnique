# Library imports
import pandas as pd
import re
import tqdm
import matplotlib.pyplot as plt

# Data files imported as pandas Dataframes
with open('/home/hgmnjx/Desktop/references initialized in shop.csv') as csv_file_not_cleaned:
    csv_text = csv_file_not_cleaned.read()

lengths = []
list_refs = []
for i in [x.split(',""') for x in csv_text.split('\n')]:
    lengths.append(len(i))
    if len(i) == 5:
        list_refs.append(i)

ref_in_shop = pd.DataFrame(list_refs[1:], columns=list_refs[0])
reteailer_extract = pd.read_excel('/home/hgmnjx/Desktop/retailer extract vLB.xls')
reteailer_extract['EAN'] = reteailer_extract['EAN'].astype(str)
#print(reteailer_extract['EAN'].describe())
#####################################################################################################################

# Removing the "" from the data so as to compare it with the EAN in the other dataframe
ref_in_shop['reference_id""'] = ref_in_shop['reference_id""'].apply(lambda x: re.sub('""', '', x))
ref_in_shop['aisle""'] = ref_in_shop['aisle""'].apply(lambda x: re.sub('""', '', x))


####################################################################################################################
# Getting two dataframes: one where the products initialized are stored and the other the remaining products

ref_not = reteailer_extract.loc[~reteailer_extract['EAN'].isin(ref_in_shop['reference_id""'].tolist())]
ref_in = reteailer_extract.loc[reteailer_extract['EAN'].isin(ref_in_shop['reference_id""'].tolist())]

print(len(reteailer_extract['Libellé  Sous-Famille '].unique()), len(ref_not['Libellé  Sous-Famille '].unique()), len(ref_not.index))

#####################################################################################################################

# Filtering the products to consider by stock quantity

ref_in_filtered_by_stock = ref_not.loc[ref_not['Stock en quantité'] != 0]
print(len(reteailer_extract['Libellé  Sous-Famille '].unique()), len(ref_in_filtered_by_stock['Libellé  Sous-Famille '].unique()), len(ref_in_filtered_by_stock.index))
#print(ref_in['Stock en quantité'].unique())

#####################################################################################################################

# Filtering the products by category present in the initialized file

ref_in_filtered_by_famille = ref_in_filtered_by_stock.loc[ref_in_filtered_by_stock['Libellé  Sous-Famille '].isin(ref_in['Libellé  Sous-Famille '].tolist())]
print(len(reteailer_extract['Libellé  Sous-Famille '].unique()), len(ref_in_filtered_by_famille['Libellé  Sous-Famille '].unique()), len(ref_in_filtered_by_famille.index))


#####################################################################################################################

# Filtering the products by their state of sorting in the aisle
ref_in_filtered_by_etat = ref_in_filtered_by_famille[~ref_in_filtered_by_famille['Etat Assortiment'].str.contains("Hors")]
print(len(reteailer_extract['Libellé  Sous-Famille '].unique()), len(ref_in_filtered_by_etat['Libellé  Sous-Famille '].unique()), len(ref_in_filtered_by_etat.index))

#####################################################################################################################

# Creating a dictionary associating category and aisle name
dict_aisles = {}
for i in ref_in_shop.index:
    t = ref_in.loc[ref_in['EAN'] == ref_in_shop['reference_id""'].iloc[i]]
    if not t.empty:
        dict_aisles[t.iloc[0]['Libellé  Sous-Famille ']] = ref_in_shop.iloc[i]['aisle""']

#print(dict_aisles)

#####################################################################################################################

# Printing every product to initialize and the aisle it should be found in 
results = ref_in_filtered_by_etat.reset_index()

for i in results.index:
    print('le produit {} dans le rayon {} peut etre initialisé'.format(results['Article Libellé Long'].iloc[i], dict_aisles[results.iloc[i]['Libellé  Sous-Famille ']]))



####################################################################################################################
# Viz

# results = []
# for n in tqdm.tqdm(range(len(ref_in_filtered_by_etat['Libellé  Famille '].unique().tolist()))):
#     i = ref_in_filtered_by_etat['Libellé  Famille '].unique().tolist()[n]
#     df_1 = ref_in_filtered_by_etat.loc[ref_in_filtered_by_etat['Libellé  Famille '] == i]
#     nbr_of_sf = len( df_1['Libellé  Sous-Famille '].unique().tolist())
#
#     for j in df_1['Libellé  Sous-Famille '].unique().tolist():
#         df_2 = df_1.loc[df_1['Libellé  Sous-Famille '] == j]
#         nbr_of_ub = len(df_1['Libellé Unité de Besoin '].unique().tolist())
#
#         for k in df_2['Libellé Unité de Besoin '].unique().tolist():
#             df_3 = df_2.loc[df_2['Libellé Unité de Besoin '] == k]
#             nbr_of_cE = len(df_2['Libellé code interne Enseigne'].unique().tolist())
#
#             for m in df_3['Libellé code interne Enseigne'].unique().tolist():
#                 df_4 = df_3.loc[df_3['Libellé code interne Enseigne'] == m]
#                 nbr_of_p = len(df_3['Article Libellé Long'].unique().tolist())
#
#                 results.append((i, nbr_of_sf, nbr_of_ub, nbr_of_cE, nbr_of_p))
#
# t = pd.DataFrame(results,columns=['Famille', 'Sous-Famille', 'UBesoin', 'IEnseigne', 'NbrProd'])
# t = t.groupby(['Famille']).mean()
#
# print(t)
# plt.figure()
# t.plot(kind='bar')
# plt.show()