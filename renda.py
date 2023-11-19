import pandas as pd
import numpy as np

renda = pd.read_csv('gdp.csv', decimal='.')

#limpando os dados e transformando os dados 
renda['Year'].apply(lambda x: int(x.split('/')[-1])) #limpado a coluna ANO

renda['Year'] = renda['Year'].apply(lambda x: int(x.split('/')[-1]))

float(renda[' GDP_pp '].iloc[0].split()[0]) #transformando os a coluna em float

renda[' GDP_pp '].apply(lambda x: float(x.split()[0].replace(',', ''))) #trnasformando todos os dados em float

renda['GDP_pp'] = renda[' GDP_pp '].apply(lambda x: float(x.split()[0].replace(',', '')))

del renda[' GDP_pp '] #deletando a ultima coluna


renda.groupby('Country')['Year'].min()

renda.groupby('Country')['Year'].min().value_counts() #descobrindo a quantidade de paises por ano

renda.groupby('Country')['Year'].min() [renda.groupby('Country')['Year'].min() == 1991] #descobrindo qual país tinha o ano 1991

renda[renda['Year'] < 2000].max()

renda_start = renda[renda['Year']==1901]
renda_end = renda[renda['Year']==1996]

((renda_end.groupby('Region')['GDP_pp'].mean() / renda_start.groupby('Region')['GDP_pp'].mean() -1) *100).sort_values()


arr_year = np.arange(renda['Year'].min(), renda['Year'].max()) 

arr_all_year = pd.DataFrame(arr_year, columns=['Year'])
arr_all_year.index = arr_all_year['Year'] #colocando a coluna ano como index


arr_off_year = ~ arr_all_year['Year'].isin(renda['Year']) #pegando os anos que nao estao na base de dados original

arr_off_year = arr_all_year.loc[arr_off_year].index
arr_off_year

renda = renda.sort_values(['Country', 'Year'])

renda['delta_gdp'] = renda['GDP_pp'] - renda['GDP_pp'].shift(1)
renda['delta_year'] = renda['Year'] - renda['Year'].shift(1)
renda['dpg_year'] = (renda['delta_gdp'] / renda['delta_year']).shift(-1)


renda['next_year'] = renda['Year'].shift(-1)
del renda['delta_gdp'], renda['delta_year']

renda_new = pd.DataFrame()

for idx, row in renda.iterrows():
    if row['Year'] == 2011:
        continue
    years_add = arr_off_year[(arr_off_year < row['next_year']) & (arr_off_year > row['Year'])]
                            
    for new_year in years_add:
        add_row = row.copy()
        add_row['GDP_pp'] = (new_year - add_row['Year']) * add_row['GDP_pp'] + add_row['GDP_pp']
        add_row['Year'] = new_year
        add_row['kind'] = 'estimated'
        renda_new = pd.concat([renda_new, add_row.to_frame().transpose()])



renda = pd.concat([renda, renda_new])

renda.sort_values(['Country', 'Year'], inplace= True)

renda.index = renda['Year']

renda['kind'].fillna('real', inplace=True)
renda

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(20,5))
country = 'Brazil'
renda[(renda['kind'] == 'real') & (renda['Country'] == country)].plot(kind='scatter',y='GDP_pp', x='Year', ax=ax)
renda[(renda['kind'] == 'estimated') & (renda['Country'] == country)].plot(kind='scatter',y='GDP_pp', x='Year', ax=ax, color='orange')


#DESAFIO
renda['Year'] = renda['Year'].astype(int)
renda['GDP_pp'] = renda['GDP_pp'].astype(float)
import plotly.express as px
df = px.data.gapminder()

dict_iso_alpha = df.set_index('country').to_dict()['iso_alpha']# transformando uma coluna de uma dataframe em um dicionario
dict_num = {j: i for i, j in enumerate(renda['Country'].unique())} #enumerando cada pais 

renda['iso_alpha'] = renda['Country'].map(dict_iso_alpha)
renda['iso_num'] = renda['Country'].map(dict_num)

fig = px.choropleth(renda[renda['kind'] == "real"].reset_index(drop=True), locations='iso_alpha', color='GDP_pp', hover_name='Country', animation_frame='Year')
fig.update_layout(height=600)
fig.show()

