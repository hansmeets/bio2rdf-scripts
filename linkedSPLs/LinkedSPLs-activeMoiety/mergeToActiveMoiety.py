'''
Created 08/15/2014

@authors: Yifan Ning

@summary: merge preferred term, UNII, NUI, preferredNameAndRole, Drug bank URI, ChEBI URI, rxnorm URI, OMOP id, DrOn id for active moiety together.

'''

import os, sys
import pandas as pd
from StringIO import StringIO
import numpy as np
#from numpy import nan

## Define data inputs

#UNIIS = "../linkedSPLs-update/data/UMLS/UNIIs-from-UMLS.txt"
#PT_UNII = "mappings/FDAPreferredTermToUNII.tsv"
#PT_RXCUI = "mappings/fda-active-moiety-string-name-rxnorm-mapping.csv"

UNII_PT_RXCUI = "mappings/PreferredTerm-UNII-Rxcui-mapping.txt"
DRON_CHEBI_RXCUI = "mappings/cleaned_dron-to-chebi-and-rxnorm-11192014.txt"
OMOP_RXCUI = "mappings/mappings-backup-0723/omopid_rxcui.csv"
PT_CHEBI = "mappings/UNIIToChEBI-11162014.txt"
PT_DRUGBANK = "mappings/fda-substance-preferred-name-to-drugbank-11162014.txt"
UNII_NUI_PREFERRED_NAME_ROLE = "mappings/EPC_extraction_most_recent_11162014.txt"

CHEBI_BASE_URI = "http://purl.obolibrary.org/obo/"



## read mappings of pt, unii and rxcui

unii_pt_rxcui_cols = ['unii','pt','rxcui']
unii_pt_rxcui_DF = pd.read_csv(UNII_PT_RXCUI, sep='\t', names=unii_pt_rxcui_cols, skiprows=[0])


## read mappings of pt and drugbank uri

pt_drugbank_cols = ['pt','db_uri1','db_uri2']
pt_drugbank_DF = pd.read_csv(PT_DRUGBANK, sep='\t', names=pt_drugbank_cols)


## read mappings of omop id and rxcui
omop_rxcui_cols = ['omopid','rxcui']
omop_rxcui_DF = pd.read_csv(OMOP_RXCUI, sep='|', names=omop_rxcui_cols)
#print omop_rxcui_DF.info()


## read mappings of pt and chebi

pt_chebi_cols = ['pt','chebi']
pt_chebi_DF = pd.read_csv(PT_CHEBI, sep='\t', names=pt_chebi_cols)
#print pt_chebi_DF.info()


## read mappings of dron and rxcui

dron_chebi_rxcui_cols = ['dron','chebi','rxcui']
dron_chebi_rxcui_DF = pd.read_csv(DRON_CHEBI_RXCUI, sep='|', names=dron_chebi_rxcui_cols)[['dron','rxcui']]
dron_chebi_rxcui_DF = dron_chebi_rxcui_DF[dron_chebi_rxcui_DF.dron.notnull()]

print dron_chebi_rxcui_DF


## read mappings of unii, nui and preferredNameAndRole
unii_nui_namerole_cols = ['setid', 'unii','nui','nameAndRole']
unii_nui_namerole_DF = pd.read_csv(UNII_NUI_PREFERRED_NAME_ROLE, sep='\t', names=unii_nui_namerole_cols)[['unii','nui','nameAndRole']]
#print unii_nui_namerole_DF.info()



## merge pt, unii, rxcui and drugbank uri

unii_pt_rxcui_db_DF = unii_pt_rxcui_DF.merge(pt_drugbank_DF, on=['pt'], how='left')
print unii_pt_rxcui_db_DF.info()


# ## merge omop to pt_unii_db_rxcui_DF

merged_omop_DF = unii_pt_rxcui_db_DF.merge(omop_rxcui_DF, on=['rxcui'], how='left')
print merged_omop_DF.info()


# ## merge chebi to merged_omop_DF

merged_chebi_DF = merged_omop_DF.merge(pt_chebi_DF, on=['pt'], how='left')
print merged_chebi_DF.info()


# ## merge dronid to merged_chebi_DF
merged_dron_DF = merged_chebi_DF.merge(dron_chebi_rxcui_DF, on=['rxcui'], how='left')
print merged_dron_DF.info()


# ## merge <nui> and <preferred name and role> to merged_dron_DF

merged_epc_DF = merged_dron_DF.merge(unii_nui_namerole_DF, on=['unii'], how='left')

#merged_epc_DF[['rxcui']] = merged_epc_DF[['rxcui']].astype(str)
#merged_epc_DF[['omopid']] = merged_epc_DF[['omopid']].astype(str)

merged_epc_DF.to_csv('mergedActiveMoiety.csv', sep='\t', index=False)

