import os 
import pandas as pd
import numpy as np
import string
from random import randint

class Telemetry_Pattern_Analyzer(object):
    def __init__(self, df_uniqcode,separator=','):
        ''' Constructor for this class. '''
        self.df_uncode_value = df_uniqcode
        self.separator=separator
        
        
 
    def makeDna(self,markers):
        count=0
        aa=markers.split('|')
        ss=len(aa)
        dna=str()
        df_lookup=self.df_uncode_value
        df_add_plus = pd.DataFrame(columns=['key','value'])

        for i in list(reversed(range(ss))):
            row_item=df_lookup.loc[df_lookup['value'] == aa[i]]
            if row_item.shape[0] > 0:
                dna+=str(row_item.iloc[0][0])
            else: #case it is not found
                row_item=df_add_plus.loc[df_add_plus['value'] == aa[i]]
                if row_item.shape[0] > 0:
                    dna+=str(row_item.iloc[0][0])
                else:
                    #generate a new code and add to the df_uncode_value
                    ucode = str(randint(0, 9))+aa[i][0:2]+str(randint(0, 9))
                    #print ('new ucode',ucode,aa[i] )
                    df_add=pd.DataFrame([[ucode,aa[i]]],columns=['key','value'])
                    df_add_plus=df_add_plus.append(df_add,ignore_index=True)
                    df_add_plus.reset_index()
                    #print df_uncode_value.shape
                    #now add the newly generated code to the string
                    dna+=str(ucode)
                    #row_item=df_uncode_value.loc[df_uncode_value['value'] == aa[i-1]]
                    count +=1
                #print count
        return dna,df_add_plus


    #convert every marker into a unique keyword
    def MakeUniqueMarkerList(errorMarkers):
        errorMarkers_unique=[]
        errorMarkers_all=[]
        for i in errorMarkers:
            j=i.split(',')
            errorMarkers_all.extend(j)

        for i in errorMarkers_all:
            if i not in errorMarkers_unique:
                errorMarkers_unique.append(i)
        return errorMarkers_unique
    
    def GenerateMarkerUniqueCode(self,errorMarkers_unique):
        uncode_value=[]
        index=0
        for i in errorMarkers_unique:
            ucode = str(index%10)+i[0:2]+str(len(i)%10)
            index +=1
            uncode_value.append([ucode,i])
            #uncode_value['code']=ucode
            #uncode_value['marker']=i

        df_uncode_value =pd.DataFrame(uncode_value)
        df_uncode_value.columns=['key','value']
        return df_uncode_value 

    def GetMarkerDescription(self,code):
        code_string = code
        code_string_tuple_len = len(code_string)
        marker=str()
        for i in range(0,code_string_tuple_len,4):
            code_string_tuple=code_string[i:i+4]
            marker += self.df_uncode_value[self.df_uncode_value['key']==code_string_tuple].iloc[0][1]+'|'

        return marker
    
    def GetMarkerCode(self,marker):
        if sum(self.df_uncode_value['value']==marker) == 0:
            return ''
        else:
            return self.df_uncode_value[df_uncode_value['value']==marker].reset_index().key[0]  

        
    def GetDNA_Set(dna_strain):
        nibbles=[]
        for i in range(0,len(dna_strain),4):
            start=i
            end=i+4
            nibbles.append(dna_strain[start:end])
        return set(nibbles)
    
    def find_str(s, char):
        index = 0

        if char in s:
            c = char[0]
            for ch in s:
                if ch == c:
                    if s[index:index+len(char)] == char:
                        return index

                index += 1

        return -1 
    
    def SearchPattern(self,df_target_pattern,df_filter):
        MACS = []
        match_marker=[]
        
        df_test_dna_code_all = df_target_pattern
        df_final_custom_filter_dna=df_filter
        for index,i in df_test_dna_code_all.iterrows():
            for j in df_final_custom_filter_dna['dna']:
                template=GetDNA_Set(j)
                target=GetDNA_Set(i['dna'])
                len_template=len(template)
                len_target=len(target)
                len_intersect=len(template&target)
                max_len=max(len_template,len_target)
                if len_intersect > 0:
                    MACS.append(i['MAC'])
                    match_marker.append(next(iter(target&template)))
                    break
        return MACS,match_marker
