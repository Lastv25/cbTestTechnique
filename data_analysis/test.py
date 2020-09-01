# Library imports
import pandas as pd
import re
import sys
##################################################################################################################

def main(argv):
    
    try:
        nbr_to_show = int(argv)
    except:
        print('The input parameter needs to be an integer')
        return 1
    
    ##################################################################################################################
    # Data files imported as pandas Dataframes
    with open('references initialized in shop.csv') as csv_file_not_cleaned:
        csv_text = csv_file_not_cleaned.read()

    list_refs = []
    for i in [x.split(',""') for x in csv_text.split('\n')]:
        if len(i) == 5:
            list_refs.append(i)

    ref_in_shop = pd.DataFrame(list_refs[1:], columns=list_refs[0])
    reteailer_extract = pd.read_excel('retailer extract vLB.xls')
    reteailer_extract['EAN'] = reteailer_extract['EAN'].astype(str)
    #####################################################################################################################

    # Removing the "" from the data so as to compare it with the EAN in the other dataframe
    ref_in_shop['reference_id""'] = ref_in_shop['reference_id""'].apply(lambda x: re.sub('""', '', x))
    ref_in_shop['aisle""'] = ref_in_shop['aisle""'].apply(lambda x: re.sub('""', '', x))

    ####################################################################################################################
    # Getting two dataframes: one where the products initialized are stored and the other the remaining products

    ref_not = reteailer_extract.loc[~reteailer_extract['EAN'].isin(ref_in_shop['reference_id""'].tolist())]
    ref_in = reteailer_extract.loc[reteailer_extract['EAN'].isin(ref_in_shop['reference_id""'].tolist())]

    ####################################################################################################################
    # Filtering the products by category present in the initialized file
    ref_in_filtered_by_famille = ref_not.loc[ref_not['Libellé  Sous-Famille '].isin(ref_in['Libellé  Sous-Famille '].tolist())]

    #####################################################################################################################

    # Filtering the products to consider by stock quantity

    ref_in_filtered_by_stock = ref_in_filtered_by_famille.loc[ref_in_filtered_by_famille['Stock en quantité'] != 0]

    #####################################################################################################################

    # Filtering the products by their state of sorting in the aisle
    ref_in_filtered_by_etat = ref_in_filtered_by_stock[~ref_in_filtered_by_stock['Etat Assortiment'].str.contains("Hors")]
    
    #####################################################################################################################
    
    # Final DataFrame
    results = ref_in_filtered_by_etat.reset_index()
    
    ####################################################################################################################
    
    # Creating a dictionary associating category and aisle name
    dict_aisles = {}
    for i in ref_in_shop.index:
        t = ref_in.loc[ref_in['EAN'] == ref_in_shop['reference_id""'].iloc[i]]
        if not t.empty:
            dict_aisles[t.iloc[0]['Libellé  Sous-Famille ']] = ref_in_shop.iloc[i]['aisle""']

    #####################################################################################################################
    # Code to get the ordered list of libellé Famille from the one with the most products to the one with the least
    tf = ref_in[['Libellé  Famille ', 'Article Libellé Long']].groupby(['Libellé  Famille ']).count()
    tf = tf.reset_index()
    tf = tf.sort_values(by=['Article Libellé Long'], ascending=False)
    list_ordered_familles = tf['Libellé  Famille '].tolist()
    
    #####################################################################################################################
    # Code to get the most pertinent products shown
    counter = 0
    i = 0
    fam = list_ordered_familles[0]
    while counter < nbr_to_show:  # While the number of products shown is inferior to the number defined by the user
        sub_dataframe = ref_in_filtered_by_etat.loc[ref_in_filtered_by_etat['Libellé  Famille '] == fam]
        
        # Code to get the ordered list of libellé Sous-Famille from the one with the most products to the one with the least
        tf2 = sub_dataframe[['Libellé  Sous-Famille ', 'Article Libellé Long']].groupby(['Libellé  Sous-Famille ']).count()
        tf2 = tf2.reset_index()
        tf2 = tf2.sort_values(by=['Article Libellé Long'], ascending=False)
        list_ordered_sous_familles = tf2['Libellé  Sous-Famille '].tolist()
        
        for sfam in list_ordered_sous_familles:  # for each sous-famille 
            sub_dataframe2 = sub_dataframe.loc[sub_dataframe['Libellé  Sous-Famille '] == sfam]
            sub_dataframe2 = sub_dataframe2.reset_index()
            for i in sub_dataframe2.index:  # printing each product
                print('le produit {} dans le rayon {} peut etre initialisé'.format(sub_dataframe2['Article Libellé Long'].iloc[i], dict_aisles[sub_dataframe2.iloc[i]['Libellé  Sous-Famille ']]))
                counter += 1
                if counter >= nbr_to_show:
                    break
            if counter >= nbr_to_show:
                break
        i += 1
        fam = list_ordered_familles[i]
        if i == len(list_ordered_familles):
            break

    return 0


if __name__ == "__main__":
   main(sys.argv[1])
