# An-Interactive-Dashboard_Energy-Market-Analysis

An interactive dashboard is created using the hourly dataset of European Power Plants, Generators, and Technologies like Solar, Wind Offshore/Onshore, Hydrogen, etc. It has a couple of tabs and subtabs; by clicking on them, different type of graphs and an explanation of them is displayed.

#!/usr/bin/env python
# coding: utf-8

# In[48]:


import pandas as pd
import os
import zipfile
import tempfile


# In[5]:


zip_file_path = r'S:\TEAM\Energy System Planning\@all locations\02_GE\Mitarbeiter\Mina\BZR\results.zip'


# In[3]:


zip_file_path = r'S


# # Reading Big Data

# In[ ]:


with tempfile.TemporaryDirectory() as temp_dir:
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        print(f"Extracted files to temporary directory: {temp_dir}")
    except Exception as e:
        print(f"Error in extracting the ZIP file: {e}")

    dataframes = []

    for root, dirs, files in os.walk(temp_dir):
        for filename in files:
            if filename.startswith("RAO_Results_t") and filename.endswith(".csv"):
                print(f"Reading file {filename}")
                filepath = os.path.join(root, filename)
                
                try:
                    df = pd.read_csv(filepath, encoding='ISO-8859-1')
                    dataframes.append(df[['Gebotzone Anf.', 'Gebotzone End.', 'EPL Ausfall nach Opt.']])
                    
                except Exception as e:
                    print(f"Error reading file {filename}: {e}")
                
    


# In[ ]:


# combined_df = pd.concat(dataframes, ignore_index=True)
# # combined_df.iloc[2000:2004, :]

# grouped_df['Gebotzone']= combined_df.apply(lambda x: '-'.join(sorted([x['Gebotzone Anf.'], x['Gebotzone End.']])),axis=1)
                   
# grouped_df.drop(['Gebotzone Anf.','Gebotzone End.'], axis=1, inplace=True)


# In[ ]:


combined_df = pd.concat(dataframes, ignore_index=True)
# combined_df.iloc[2000:2004, :]
grouped_df = combined_df.groupby(['Gebotzone Anf.', 'Gebotzone End.'])[['EPL Ausfall nach Opt.']].sum().reset_index()
grouped_df['Gebotzone']= grouped_df.apply(lambda x: '-'.join(sorted([x['Gebotzone Anf.'], x['Gebotzone End.']])),axis=1)                 
grouped_df

output_file_path = 'results_final.xlsx'
grouped_df.to_excel(output_file_path, index=False)
print(f"Final results saved to {output_file_path}")


# # Generation Per Change

# In[6]:


with zipfile.ZipFile(zip_file_path) as myzip:
    with myzip.open('generation_per_plant_change.csv') as myZipCsv:
        df = pd.read_csv(myZipCsv)


# In[7]:


df=df.iloc[2:,:]
df.iloc[865:,:]


# In[8]:


rao_planzs=pd.read_csv("rao_plants.csv", sep=";", decimal=",")


# In[9]:


market_areas=pd.read_csv("market_areas.csv", sep=";", decimal=",")
# market_areas.columns[0]= market_area_ID
# market_areas=market_areas.rename(columns={'ID':'market_area_ID'})
market_areas


# In[10]:


df_c=pd.merge(df, market_areas[['ID', 'name']], left_on='market_area_ID', right_on='ID',  how='left')
df_cp=pd.merge(df_c, rao_planzs[['ID', 'name']], left_on='plant_ID', right_on='ID',  how='left')

df_cp.drop(['market_area_ID', 'plant_ID', 'ID_x', 'ID_y'], axis=1, inplace=True)

df_c


# In[11]:


df_cp_pos=df_cp.copy()
mask=df_cp_pos.iloc[:,1:-2] < 0
df_cp_pos.iloc[:,1:-2]=df_cp_pos.iloc[:,1:-2].mask(df_cp_pos.iloc[:,1:-2]<0,0)
df_cp_pos


# In[ ]:


output_file_path_neg_type = 'df_cp_pos.csv'
df_cp_pos.to_csv(output_file_path_neg_type, index=False)
print(f"Final results saved to {output_file_path_neg_type}")


# In[12]:


df_cp_neg=df_cp.copy()
mask=df_cp_neg.iloc[:,1:-2] > 0
df_cp_neg.iloc[:,1:-2]=df_cp_neg.iloc[:,1:-2].mask(df_cp_neg.iloc[:,1:-2]>0,0)
df_cp_neg


# In[ ]:


output_file_path_neg_type = 'df_cp_neg.csv'
df_cp_neg.to_csv(output_file_path_neg_type, index=False)
print(f"Final results saved to {output_file_path_neg_type}")


# In[ ]:


df_cp_pos.iloc[861:,:]


# In[ ]:


df_cp_neg.iloc[861:,:]


# In[ ]:


df_cp


# In[13]:


mapping_dict = dict(zip(rao_planzs['type_ID'], rao_planzs['mover']))

df_cp_pos['pemmdb_type_ID'] = df_cp_pos['pemmdb_type_ID'].map(mapping_dict).fillna(df_cp_pos['pemmdb_type_ID'])

df_cp_pos


# In[14]:


mapping_dict = dict(zip(rao_planzs['type_ID'], rao_planzs['mover']))

df_cp_neg['pemmdb_type_ID'] = df_cp_neg['pemmdb_type_ID'].map(mapping_dict).fillna(df_cp_neg['pemmdb_type_ID'])

df_cp_neg


# In[15]:



rao_planzs_new_name=rao_planzs[['type_ID', 'mover']]
rao_planzs_new_named=rao_planzs_new_name.rename(columns={'type_ID': 'pemmdb_type_ID'})
rao_planzs_new_named


# In[ ]:





# # Market Area - Positive

# In[16]:


value_columns=df_cp_pos.columns[1:-2]
market_group_pos=df_cp_pos.groupby(['name_x'])[value_columns].sum().reset_index()
abbv=market_group_pos['name_x'].tolist()
market_group_pos


# In[17]:


######################## Transformation of the Name of Countries ###########################################
Countries=['Austria', 'Belgium', 'Switzerland', 'Czechia', 'Deutschland','Denmark', 'France', 'Croatia', 'Hungary','Italy', 'Netherland', 'Poland', 'Romania', 'Slovenia', 'Slovakia']
market_group_pos1_count=market_group_pos.copy()
for idx, i in enumerate(Countries):
    market_group_pos1_count['name_x'][idx]=i
market_group_pos1_count


# In[ ]:


output_file_path_neg_type = 'market_group_pos1_count.csv'
market_group_pos1_count.to_csv(output_file_path_neg_type, index=False)
print(f"Final results saved to {output_file_path_neg_type}")


# In[18]:


# market_group_pos[0:2]
# market_group_pos['name_x'].max(axis=0)
# max(market_group_pos.iloc[0:1,:].values)

market_group_pos['Max']=market_group_pos.max(axis=1)
numeric_columns=market_group_pos.columns[1:-2]
market_group_pos['Hour'] = market_group_pos[numeric_columns].idxmax(axis=1)
market_group_pos


# In[ ]:





# In[19]:


market_group_pos1=market_group_pos[['name_x','Max','Hour']].sort_values(by='Max', ascending=False)
market_group_pos1


# In[20]:


output_file_path_neg_type = 'market_group_pos1.csv'
market_group_pos1.to_csv(output_file_path_neg_type, index=False)
print(f"Final results saved to {output_file_path_neg_type}")


# In[21]:


from matplotlib import pyplot as plt

fig, ax = plt.subplots(figsize=(18, 10))
bars = ax.bar(market_group_pos1['name_x'], market_group_pos1['Max'], color='skyblue')

for bar, max_val, max_time_val in zip(bars, market_group_pos1['Max'], market_group_pos1['Hour']):
    height = bar.get_height()
    max_val_str = f'{max_val:.2f}'
    
    bbox_props = dict(boxstyle="round,pad=0.3", edgecolor="blue", facecolor="white")
    ax.text(bar.get_x() + bar.get_width() / 2, height, max_val_str, ha='center', va='bottom', fontsize=10, bbox=bbox_props)

    ax.text(bar.get_x() + bar.get_width() / 2, height -100, f'{max_time_val}', ha='center', va='top', fontsize=10)

ax.set_title('Average Generation Change for Different Market Area (Positive)',fontsize=20)
ax.set_xlabel('Market Area',fontsize=15)
ax.set_ylabel('Hours',fontsize=15)

plt.savefig('Generation_Change_Market_Area_Positive.png')
plt.show()


# In[22]:


import plotly.express as px
fig = px.scatter_geo(market_group_pos1, locations="name_x",
                     size="Max", # size of markers, "pop" is one of the columns of gapminder
                     )
fig.show()


# # Market Area - Negative

# In[23]:


value_columns=df_cp_neg.columns[1:-2]
market_group_neg=df_cp_neg.groupby([ 'name_x'])[value_columns].sum().reset_index()
market_group_neg


# In[24]:


market_group_neg['Max']=market_group_neg.min(axis=1)
numeric_columns=market_group_neg.columns[1:-2]
market_group_neg['Hour'] = market_group_neg[numeric_columns].idxmax(axis=1)
market_group_neg


# In[ ]:





# In[ ]:





# In[25]:


market_group_neg1=market_group_neg[['name_x','Max','Hour']].sort_values(by='Max', ascending=True)
market_group_neg1


# In[37]:


market_group_neg1['Max']=market_group_neg1['Max'].abs()
fig = px.pie(market_group_neg1, values='Max', names='name_x', title='Population of European continent')
fig.show()


# In[ ]:





# In[ ]:


output_file_path_neg_type = 'market_group_neg1.csv'
market_group_neg1.to_csv(output_file_path_neg_type, index=False)
print(f"Final results saved to {output_file_path_neg_type}")


# In[26]:




fig, ax = plt.subplots(figsize=(18, 10))
bars = ax.bar(market_group_neg1['name_x'], market_group_neg1['Max'], color='red')

for bar, max_val, max_time_val in zip(bars, market_group_neg1['Max'], market_group_neg1['Hour']):
    height = bar.get_height()
    max_val_str = f'{max_val:.2f}'
    
    bbox_props = dict(boxstyle="round,pad=0.3", edgecolor="red", facecolor="white")
    ax.text(bar.get_x() + bar.get_width() / 2, height, max_val_str, ha='center', va='bottom', fontsize=10, bbox=bbox_props)

    ax.text(bar.get_x() + bar.get_width() / 2, height -100, f'{max_time_val}', ha='center', va='top', fontsize=10)

ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top')

ax.tick_params(axis='x', pad=15)

# plt.xticks(rotation=45) 
ax.set_title('Average Generation Change for Different Market Area (Negative)', pad=8, fontsize=20)
ax.set_xlabel('Market Area' , labelpad=8, fontsize=15)
ax.set_ylabel('Hours', fontsize=15)

plt.savefig('Generation_Change_Market_Area_Negative.png')
plt.show()


# In[ ]:


######################## Transformation of the Name of Countries ###########################################
Countries1=['Austria', 'Belgium', 'Switzerland', 'Czechia', 'Deutschland', 'Denmark', 'France', 'Croatia', 'Hungary',  'Italy', 'Netherland', 'Poland', 'Romania', 'Slovenia', 'Slovakia']

# market_group_neg1_count=market_group_neg1
for idx, i in enumerate(Countries1):
    market_group_neg['name_x'][idx]=i
market_group_neg

##########################################################


# In[ ]:


market_group_final=pd.merge(market_group_pos1, market_group_neg1, left_on='name_x', right_on='name_x', how='left')
market_group_final


# In[ ]:


market_path='Market_Area_Max_Hour.xlsx'
market_group_final.to_excel(market_path, index=False)


# # Power Plants - Positive

# In[27]:


group_plants_pos=df_cp_pos.groupby([ 'name_y'])[value_columns].sum().reset_index()
group_plants_pos


# In[28]:


group_plants_pos['name_y']=group_plants_pos['name_y'].str[:-8]
group_plants_pos=group_plants_pos.groupby('name_y').sum().reset_index()
# group_plants_pos['name_y']
group_plants_pos2=group_plants_pos.transpose().reset_index()
group_plants_pos2 = group_plants_pos2.rename(columns=group_plants_pos2.iloc[0]).loc[1:]
group_plants_pos2


# In[ ]:


output_file_path_neg_type = 'group_plants_pos2.csv'
group_plants_pos2.to_csv(output_file_path_neg_type, index=False)
print(f"Final results saved to {output_file_path_neg_type}")


# In[29]:


group_plants_pos['Max']=group_plants_pos.iloc[:,1:].max(axis=1)
group_plants_columns=group_plants_pos.columns[1:-3]
group_plants_pos['Hour']=group_plants_pos[group_plants_columns].idxmax(axis=1)
group_plants_pos1=group_plants_pos[['name_y','Max','Hour']]
# group_plants_neg=group_plants_neg.sort_values(by='Max')[0:10]
group_plants_pos1


# In[ ]:


output_file_path_neg_type = 'group_plants_pos1.csv'
group_plants_pos1.to_csv(output_file_path_neg_type, index=False)
print(f"Final results saved to {output_file_path_neg_type}")


# In[30]:


# from matplotlib import pyplot as plt

fig, ax = plt.subplots(figsize=(18, 10))
bars = ax.bar(group_plants_pos['name_y'], group_plants_pos['Max'], color='skyblue')

for bar, max_val, max_time_val in zip(bars, group_plants_pos['Max'], group_plants_pos['Hour']):
    height = bar.get_height()
    max_val_str = f'{max_val:.2f}'
    
    bbox_props = dict(boxstyle="round,pad=0.3", edgecolor="blue", facecolor="white")
    ax.text(bar.get_x() + bar.get_width() / 2, height, max_val_str, ha='center', va='bottom', fontsize=10, bbox=bbox_props)

    ax.text(bar.get_x() + bar.get_width() / 2, height -100, f'{max_time_val}', ha='center', va='top', fontsize=10)

plt.xticks(rotation=45) 
ax.set_title('Average Generation Change for Different Power Plants (Positive)' , fontsize=20)
ax.set_xlabel('Power Plants',  labelpad=8, fontsize=15)
ax.set_ylabel('Hours' , fontsize=15)
plt.show()


# # Power Plants - Negative

# In[31]:


group_plants_neg=df_cp_neg.groupby([ 'name_y'])[value_columns].sum().reset_index()
group_plants_neg


# In[32]:


group_plants_neg['name_y']=group_plants_neg['name_y'].str[:-8]
group_plants_neg=group_plants_neg.groupby('name_y').sum().reset_index()

group_plants_neg2=group_plants_neg.transpose().reset_index()
group_plants_neg2 = group_plants_neg2.rename(columns=group_plants_neg2.iloc[0]).loc[1:]
group_plants_neg2

group_plants_neg


# In[ ]:


output_file_path_neg_type = 'group_plants_neg2.csv'
group_plants_neg2.to_csv(output_file_path_neg_type, index=False)
print(f"Final results saved to {output_file_path_neg_type}")


# In[ ]:


group_plants_neg['Max']=group_plants_neg.iloc[:,1:].min(axis=1)
group_plants_columns=group_plants_pos.columns[1:-3]
group_plants_neg['Hour']=group_plants_neg[group_plants_columns].idxmax(axis=1)
group_plants_neg1=group_plants_neg[['name_y','Max','Hour']]
# group_plants_neg=group_plants_neg.sort_values(by='Max')[0:10]
group_plants_neg1


# In[ ]:


output_file_path_neg_type = 'group_plants_neg1.csv'
group_plants_neg1.to_csv(output_file_path_neg_type, index=False)
print(f"Final results saved to {output_file_path_neg_type}")


# In[ ]:


# from matplotlib import pyplot as plt

fig, ax = plt.subplots(figsize=(18, 10))
bars = ax.bar(group_plants_neg1['name_y'], group_plants_neg1['Max'], color='red')

for bar, max_val, max_time_val in zip(bars, group_plants_neg1['Max'], group_plants_neg1['Hour']):
    height = bar.get_height()
    max_val_str = f'{max_val:.2f}'
    
    bbox_props = dict(boxstyle="round,pad=0.3", edgecolor="red", facecolor="white")
    ax.text(bar.get_x() + bar.get_width() / 2, height, max_val_str, ha='center', va='bottom', fontsize=10, bbox=bbox_props)

    ax.text(bar.get_x() + bar.get_width() / 2, height -70, f'{max_time_val}', ha='center', va='top', fontsize=10)

# plt.xticks(rotation=45) 
ax.set_title('Generation Change for Different Power Plants (Negative)')
ax.set_xlabel('Power Plants')
ax.set_ylabel('Hours')
plt.show()


# # Types - Positive

# In[38]:


group_types_pos=df_cp_pos.groupby([ 'pemmdb_type_ID'])[value_columns].sum().reset_index()

group_types_pos['Max']=group_types_pos.max(axis=1)
group_types_pos_columns=group_types_pos.columns[1:-1]
group_types_pos['Hour']=group_types_pos[group_types_pos_columns].idxmax(axis=1)

group_types_pos=group_types_pos.sort_values(by='Max', ascending=False)
group_types_pos1=group_types_pos[['pemmdb_type_ID','Max','Hour']]
group_types_pos1


# In[41]:


fig2 = px.pie(group_types_pos1, values='Max', names='pemmdb_type_ID', title='Population of European continent')
fig2.show()


# In[39]:


output_file_path_neg_type = 'group_types_pos1.csv'
group_types_pos1.to_csv(output_file_path_neg_type, index=False)
print(f"Final results saved to {output_file_path_neg_type}")


# In[40]:


fig, ax = plt.subplots(figsize=(18, 10))
bars = ax.bar(group_types_pos['pemmdb_type_ID'], group_types_pos['Max'], color='skyblue')

for bar, max_val, max_time_val in zip(bars, group_types_pos['Max'], group_types_pos['Hour']):
    height = bar.get_height()
    max_val_str = f'{max_val:.2f}'
    
    bbox_props = dict(boxstyle="round,pad=0.3", edgecolor="blue", facecolor="white")
    ax.text(bar.get_x() + bar.get_width() / 2, height, max_val_str, ha='center', va='bottom', fontsize=10, bbox=bbox_props)

    ax.text(bar.get_x() + bar.get_width() / 2, height -100, f'{max_time_val}', ha='center', va='top', fontsize=10)

plt.xticks(rotation=45) 
ax.set_title('Average Generation Change for Different Type of Power Plants (Positive)' , fontsize=20)
ax.set_xlabel('Types' , labelpad=8, fontsize=15)
ax.set_ylabel('Hours' , fontsize=15)

plt.savefig('Generation_Change_Types_Positive.png')
plt.show()


# # Types - Negative

# In[42]:


group_types_neg=df_cp_neg.groupby([ 'pemmdb_type_ID'])[value_columns].sum().reset_index()
group_types_neg['Max']=group_types_neg.min(axis=1)
group_types_pos_columns=group_types_neg.columns[1:-1]
group_types_neg['Hour']=group_types_neg[group_types_pos_columns].idxmax(axis=1)
group_types_neg


# In[45]:


group_types_neg=group_types_neg[['pemmdb_type_ID','Max','Hour']]
group_types_neg=group_types_neg.sort_values(by='Max')
group_types_neg


# In[47]:


group_types_neg['Max']=group_types_neg['Max'].abs()
fig2 = px.pie(group_types_neg, values='Max', names='pemmdb_type_ID', title='Population of European continent')
fig2.show()


# In[ ]:


output_file_path_neg_type = 'group_types_neg.csv'
group_types_neg.to_csv(output_file_path_neg_type, index=False)
print(f"Final results saved to {output_file_path_neg_type}")


# In[ ]:


from matplotlib import pyplot as plt

fig, ax = plt.subplots(figsize=(18, 10))
bars = ax.bar(group_types_neg['pemmdb_type_ID'], group_types_neg['Max'], color='red')

for bar, max_val, max_time_val in zip(bars, group_types_neg['Max'], group_types_neg['Hour']):
    height = bar.get_height()
    max_val_str = f'{max_val:.2f}'
    
    bbox_props = dict(boxstyle="round,pad=0.3", edgecolor="red", facecolor="white")
    ax.text(bar.get_x() + bar.get_width() / 2, height, max_val_str, ha='center', va='bottom', fontsize=10, bbox=bbox_props)

    ax.text(bar.get_x() + bar.get_width() / 2, height -100, f'{max_time_val}', ha='center', va='top', fontsize=10)

plt.xticks(rotation=45) 
ax.set_title('Average Generation Change for Different Type of Power Plants (Negative)' , fontsize=20)
ax.set_xlabel('Types' , labelpad=8, fontsize=15)
ax.set_ylabel('Hours' , fontsize=15)

plt.savefig('Generation_Change_Types_Negative.png')
plt.show()


# In[ ]:




