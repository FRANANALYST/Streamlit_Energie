import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import geopandas as gpd
import matplotlib.colors as mcolors
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stat
from scipy.stats import pearsonr
from sklearn.metrics  import  r2_score
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pickle



df = pd.read_csv('eco2mix-regional-cons-def-bis.csv', sep = ';')
df_ml=pd.read_csv('df_ml.csv', sep=',')
df_ml['date_heure_simplifiée'] = pd.to_datetime(df_ml['date_heure_simplifiée'])



template=pd.read_csv('Template.csv', sep=',')

st.title("Production et Consommation d'Électricité en France")
st.sidebar.title("Sommaire")
pages=["Présentation","Exploration", "DataVizualization", "Modélisation","Perspective"]
page=st.sidebar.radio("Aller vers", pages)





st.sidebar.markdown (':people_holding_hands:***:blue[Auteurs]***')
st.sidebar.write('*Legardinier François*')
st.sidebar.write('*Gendronneau Thomas*')


if page== pages[0] :
  st.write ("### Présentation")
  st.image("energie.jpg",caption="energie")
  st.write ("""Depuis fin 2022, le gouvernement français alerte sur la possibilité de coupures d'électricité durant l'hiver. Ces interruptions, bien que limitées à des zones géographiques restreintes et n'excédant pas deux heures, soulèvent des questions importantes sur la résilience de notre réseau électrique. Ces coupures localisées, dues principalement à des pics de consommation, montrent que la France dispose encore de marges de manoeuvre, offrant un aperçu rassurant de notre capacité à gérer la demande en électricité. Cependant, cette situation nous pousse également à réfléchir sur notre aptitude à affronter des crises électriques futures potentiellement plus graves, exacerbées par nos habitudes de consommation et nos besoins croissants.

   Face à la variabilité de la demande et à l'intermittence des sources renouvelables, la France se trouve à un carrefour. Le pays s'appuie fortement sur l'énergie nucléaire pour son approvisionnement stable en électricité, tout en intégrant progressivement des énergies renouvelables pour diversifier son mix énergétique et réduire son empreinte carbone. Cette transition est essentielle non seulement pour répondre aux objectifs environnementaux mais aussi pour assurer une sécurité énergétique durable.

   Nous traversons actuellement une crise électrique attribuable à trois facteurs principaux :
   1. Augmentation du prix du gaz.
   2. Le changement climatique (notamment la sécheresse).
   3. Retard dans l'entretien des réacteurs nucléaires.
    
   Ces éléments ont catalysé une réflexion urgente sur la nécessité de réduire la dépendance aux énergies fossiles et de diminuer la dépendance énergétique vis-à-vis de la Russie. Le Sénat traite actuellement ce sujet au travers d'une commission d'enquête sur l'électricité, en réponse aux engagements de décarbonation pris lors de la COP22, visant une réduction de 35% des émissions de gaz à effet de serre d'ici 2030. La solution envisagée repose largement sur l'augmentation de l'électrification, bien que l'électricité ne soit pas stockable sur de longues périodes (stockage journalier possible).

   A travers ce projet nous allons essayer de prédire la consommation électrique future.
    """)
  





if page == pages[1] : 
  st.write("### Exploration")
 
  st.write("Note jeux de Donnée principale est : Données éCO2mix régionales consolidées et définitives (janvier 2013 à janvier 2023:")
  st.write ("""Le jeu de données Eco2Mix contient des informations complètes et détaillées sur la consommation électrique et la production pour différentes filières, incluant le nucléaire, l'éolien, le solaire et le thermique.Les données sont mises à jour toutes les demi-heures, offrant ainsi une granularité fine qui permet d'analyser les variations de consommation et de production en temps quasi-réel. Les données sont regroupées au niveau régional, ce qui permet une analyse précise des variations géographiques de la consommation et de la production électrique.""")

  st.write("**Affichage des 5 premières lignes :**")  

  st.dataframe(df.head())

  st.write ("Le nombre de ligne du jeu de donnée est :", df.shape[0])
  st.write ("Le nombre de colonne du jeu de donnée est :", df.shape[1])

  colonne= template['Nom de la colonne'].unique()

  st.write ("**Dictionnaire de donnée :**")
  selection_colonne=st.selectbox("Choissisez une colonne:", colonne)

  filtre_template=template[template ['Nom de la colonne']== selection_colonne]

  st.dataframe(filtre_template['Description'])

  st.write ('**Quelques statistiques**')
  
  st.dataframe(df['consommation'].describe())

  
  st.write ('**NA**')
  if st.checkbox("Afficher les NA") :
   st.dataframe(df.isna().sum())
  
  st.write ("""Le jeu de données Eco2Mix est d'excellente qualité, sans doublons et avec très peu de données manquantes ce qui nous permet d'avoir une bonne qualité dans nos analyses.Une compréhension approfondie du domaine a permis de repérer et de corriger des anomalies telles que les fausses NaN dans la production nucléaire, qui correspondaient en réalité à des régions dépourvues de centrales nucléaires. Ces NaN ont été remplacés par des valeurs nulles pour maintenir l'intégrité des données.""")
  
  st.write ("**Autres sources de données**")
  st.write ("""Nous avons récupéré d'autres jeux de données :
      ● Température (source : Température quotidienne régionale (depuis janvier 2016) - data.gouv.fr) : Il s'agit des températures moyennes, minimum et maximum par région et par jours.
     ● Secteurs d'activités : Consommation et thermosensibilité électriques annuelles à la maille région (source : https://data.enedis.fr/explore/dataset/consommation-electrique-par-secteur-dactivite-region/table/?sort=annee) : Il s'agit des consommations annuelles par secteur d'activité par région avec un détail sur le résidentiel (Années des logements, part thermosensibilité…).
     ● Hydraulique
     ● Gdf : Géographie des régions avec leurs coordonnées ainsi que leur superficie""" )

  st.write("""Les données étant très propre, nous n'avons pas eu besoin de nettoyer les données. Le jeu de données température fonctionne aussi de façon journalière tandis que les données sur le secteur d'activité sont des données annualisées.""")



if page == pages[2] : 
  st.write("### DataVizualization")
  
  

  production_columns = ['thermique', 'nucleaire', 'eolien', 'solaire', 'hydraulique', 'bioenergies']
  for energy in production_columns:
      df[energy] = pd.to_numeric(df[energy], errors='coerce')


  df['date'] = pd.to_datetime(df['date'], errors='coerce')


  years = [2018, 2019, 2020, 2021, 2022]
  selected_year = st.selectbox("Sélectionnez l'année pour la répartition de la production d'énergie :", years)


  df_selected_year = df[df['date'].dt.year == selected_year]


  production_totale_par_type = df_selected_year[production_columns].sum()


  production_totale_par_type = production_totale_par_type.dropna().sort_values(ascending=False)


  colors = ['green', 'orange', 'lightgreen', 'red', 'skyblue', 'blue']


  st.write(f"### Répartition de la Production d'Énergie française par Source en {selected_year}")
  plt.figure(figsize=(8, 6))
  production_totale_par_type.plot(kind='pie', colors=colors, autopct='%1.1f%%', startangle=140)
  plt.ylabel('')
  plt.title(f"Répartition de la Production d'Énergie française par Source en {selected_year}")
  st.pyplot(plt)
  
  
  

  df['date'] = pd.to_datetime(df['date'], errors='coerce')


  production_columns = ['thermique', 'nucleaire', 'eolien', 'solaire', 'hydraulique', 'bioenergies']
  for energy in production_columns:
      df[energy] = pd.to_numeric(df[energy], errors='coerce')


  df['year'] = df['date'].dt.year


  years = [2018, 2019, 2020, 2021, 2022]
  selected_years = st.multiselect("Sélectionnez les années pour afficher l'évolution de la production d'énergie :", years, default=years)


  df_selected_years = df[df['year'].isin(selected_years)]


  yearly_production = df_selected_years.groupby('year')[production_columns].sum().reset_index()


  colors = {
    'eolien': 'red',
    'solaire': 'skyblue',
    'hydraulique': 'orange',
    'thermique': 'Lightgreen',
    'bioenergies': 'blue',
    'nucleaire': 'green'
}


  fig_renewable = go.Figure()
  for energy in ['eolien', 'solaire', 'hydraulique']:
      fig_renewable.add_trace(go.Scatter(x=yearly_production['year'], y=yearly_production[energy],
                                         mode='lines+markers', name=energy.capitalize(), line=dict(color=colors[energy])))

  fig_renewable.update_layout(
      title="Évolution de la Production d'Énergie Renouvelable en France",
      xaxis_title='Année',
      yaxis_title='Production (en MWh)',
      xaxis=dict(dtick=1, tickfont=dict(color='black')),
      yaxis=dict(tickfont=dict(color='black')),
      title_font=dict(color='black'),
      plot_bgcolor='white',
      paper_bgcolor='white',
      legend=dict(
          title=dict(text="Type d'Énergie", font=dict(color="black")),
          font=dict(color="black"),
          bgcolor="white",
          bordercolor="black",
          borderwidth=1
    )
)


  fig_fossil = go.Figure()
  for energy in ['thermique', 'bioenergies', 'nucleaire']:
      fig_fossil.add_trace(go.Scatter(x=yearly_production['year'], y=yearly_production[energy],
                                      mode='lines+markers', name=energy.capitalize(), line=dict(color=colors[energy])))

  fig_fossil.update_layout(
      title="Évolution de la Production d'Énergie Fossile et Nucléaire en France",
      xaxis_title='Année',
      yaxis_title='Production (en MWh)',
      xaxis=dict(dtick=1, tickfont=dict(color='black')),
      yaxis=dict(tickfont=dict(color='black')),
      title_font=dict(color='black'),
      plot_bgcolor='white',
      paper_bgcolor='white',
      legend=dict(
          title=dict(text="Type d'Énergie", font=dict(color="black")),
          font=dict(color="black"),
          bgcolor="white",
          bordercolor="black",
          borderwidth=1
    )
)


  st.write("### Évolution de la Production d'Énergie Renouvelable en France (2018-2022)")
  st.plotly_chart(fig_renewable)

  st.write("### Évolution de la Production d'Énergie Fossile et Nucléaire en France (2018-2022)")
  st.plotly_chart(fig_fossil)
  
  
  



  energy_types = ['eolien', 'solaire', 'nucleaire', 'thermique', 'hydraulique']


  for energy in energy_types:
      df[energy] = pd.to_numeric(df[energy], errors='coerce')


  selected_energy = st.selectbox("Sélectionnez le type d'énergie pour la corrélation avec la consommation :", energy_types)


  filtered_df = df[['consommation', selected_energy]].dropna()


  st.write(f"### Corrélation entre la consommation et la production électrique française de {selected_energy.capitalize()}")

  plt.figure(figsize=(10, 6))
  sns.scatterplot(x='consommation', y=selected_energy, data=filtered_df)
  plt.title(f"Corrélation Consommation vs {selected_energy.capitalize()}")
  plt.xlabel("Consommation (MWh)")
  plt.ylabel(f"{selected_energy.capitalize()} (MWh)")
  st.pyplot(plt)
  
  
  
  

  df['date'] = pd.to_datetime(df['date'], errors='coerce')
  df.set_index('date', inplace=True)


  df['consommation'] = pd.to_numeric(df['consommation'], errors='coerce')


  periode = st.selectbox("Sélectionnez la période pour la consommation moyenne mensuelle :", ["2012-2017", "2018-2022"])


  if periode == "2012-2017":
     df_filtered = df[(df.index.year >= 2013) & (df.index.year <= 2017)]
  else:
      df_filtered = df[(df.index.year >= 2018) & (df.index.year <= 2022)]


  consommation_mensuelle = df_filtered['consommation'].resample('M').mean()


  st.write(f"### Consommation Moyenne d'Énergie par Mois ({periode})")
  plt.figure(figsize=(12, 6))
  plt.plot(consommation_mensuelle.index, consommation_mensuelle, marker='o', linestyle='-', color='blue')
  plt.title(f"Consommation Moyenne d'Énergie par Mois ({periode})")
  plt.xlabel('Mois')
  plt.ylabel('Consommation Moyenne (MWh)')
  plt.grid(True)
  plt.xticks(rotation=45)
  st.pyplot(plt)







  df['date_heure'] = pd.to_datetime(df['date_heure'], errors='coerce')


  df['consommation'] = pd.to_numeric(df['consommation'], errors='coerce')


  df['year'] = df['date_heure'].dt.year
  df['month'] = df['date_heure'].dt.month


  years = list(range(2013, 2023))
  selected_years = st.multiselect("Sélectionnez les années pour afficher la consommation moyenne par mois :", years, default=[2022])


  df_filtered = df[df['year'].isin(selected_years)]


  pivot_df = df_filtered.pivot_table(values='consommation', index='month', columns='year', aggfunc='mean')


  st.write("### Consommation Moyenne d'Énergie par Mois pour Chaque Année Sélectionnée")
  plt.figure(figsize=(14, 7))
  for year in pivot_df.columns:
      plt.plot(pivot_df.index, pivot_df[year], marker='', label=year)


  plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
  plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))

  plt.title('Consommation Moyenne d\'Énergie par Mois pour Chaque Année')
  plt.xlabel('Mois')
  plt.ylabel('Consommation Moyenne (MWh)')
  plt.legend(title='Année')
  plt.grid(True)
  st.pyplot(plt)
  
  
  
  
  
  
  


  production_columns = ['thermique', 'nucleaire', 'eolien', 'solaire', 'hydraulique', 'bioenergies']
  for energy in production_columns:
      df[energy] = pd.to_numeric(df[energy], errors='coerce')


  df['consommation'] = pd.to_numeric(df['consommation'], errors='coerce')


  years = [2018, 2019, 2020, 2021, 2022]
  selected_year = st.selectbox("Sélectionnez l'année pour le phasage entre la consommation et la production :", years)


  df_year = df[df['date_heure'].dt.year == selected_year].copy()


  consommation_par_mois = df_year.groupby(df_year['date_heure'].dt.to_period('M'))['consommation'].sum().reset_index()
  consommation_par_mois.columns = ['mois', 'consommation_totale']


  df_year['production_totale'] = df_year[production_columns].sum(axis=1)
  production_par_mois = df_year.groupby(df_year['date_heure'].dt.to_period('M'))['production_totale'].sum().reset_index()
  production_par_mois.columns = ['mois', 'production_totale']


  phasage = pd.merge(consommation_par_mois, production_par_mois, on='mois')


  st.write(f"### Phasage entre la consommation et la production par mois en {selected_year}")
  plt.figure(figsize=(14, 8))
  plt.plot(phasage['mois'].astype(str), phasage['consommation_totale'], label='Consommation', color='blue', linestyle='-', marker='o')
  plt.plot(phasage['mois'].astype(str), phasage['production_totale'], label='Production Totale', color='green', linestyle='-', marker='o')
  plt.fill_between(phasage['mois'].astype(str), phasage['consommation_totale'], phasage['production_totale'],
                   where=(phasage['production_totale'] >= phasage['consommation_totale']), facecolor='green', alpha=0.3, label='Surproduction')
  plt.fill_between(phasage['mois'].astype(str), phasage['consommation_totale'], phasage['production_totale'],
                   where=(phasage['production_totale'] < phasage['consommation_totale']), facecolor='red', alpha=0.3, label='Sous-production')

  plt.title(f"Phasage entre la consommation et la production par mois en {selected_year}")
  plt.xlabel("Mois")
  plt.ylabel("Énergie (MWh)")
  plt.legend()
  plt.grid(True)
  plt.xticks(rotation=45)
  st.pyplot(plt)
  
  
  
  
  
  
  
  st.write ("### Carte de la Consommation ou de la Production Électrique par Région en France en 2022")
  
  gdf = gpd.read_file('regions-20180101-shp/regions-20180101.shp') 


  gdf = gdf.rename(columns={'nom': 'libelle_region'})
  gdf = gdf[['libelle_region', 'geometry']] 


  df['date_heure'] = pd.to_datetime(df['date_heure'], errors='coerce')


  df_2022 = df[df['date_heure'].dt.year == 2022]


  consommation_par_region = df_2022.groupby('libelle_region')['consommation'].sum().reset_index()
  production_renouvelable_par_region = df_2022.groupby('libelle_region')[['eolien', 'solaire', 'hydraulique']].sum().sum(axis=1).reset_index()
  production_non_renouvelable_par_region = df_2022.groupby('libelle_region')[['nucleaire', 'thermique', 'bioenergies']].sum().sum(axis=1).reset_index()


  gdf_conso = gdf.merge(consommation_par_region, how='left', on='libelle_region')
  gdf_renouv = gdf.merge(production_renouvelable_par_region, how='left', on='libelle_region')
  gdf_non_renouv = gdf.merge(production_non_renouvelable_par_region, how='left', on='libelle_region')


  def plot_map(gdf, column, title, cmap='RdYlGn_r'):
      fig, ax = plt.subplots(1, 1, figsize=(12, 10))
      norm = mcolors.Normalize(vmin=gdf[column].min(), vmax=gdf[column].max())
      gdf.plot(column=column, ax=ax, legend=True,
               cmap=cmap, norm=norm, legend_kwds={'label': title, 'orientation': "horizontal"})
      ax.set_title(title, fontsize=15)
      ax.set_axis_off()
      st.pyplot(fig)


  option = st.selectbox(
      "Sélectionnez l'indicateur à afficher sur la carte :",
      ("Consommation électrique par région",
       "Production électrique renouvelable par région",
       "Production électrique non renouvelable par région")
)


  if option == "Consommation électrique par région":
      plot_map(gdf_conso, 'consommation', "Consommation Électrique par Région en France (en MW) - 2022", cmap='RdYlGn_r')
  elif option == "Production électrique renouvelable par région":
      plot_map(gdf_renouv, 0, "Production Électrique Renouvelable par Région en France (en MW) - 2022", cmap='YlGn')
  else:
      plot_map(gdf_non_renouv, 0, "Production Électrique Non Renouvelable par Région en France (en MW) - 2022", cmap='OrRd')
  
  
  
  
  





  st.write ("Dans la suite du projet nous nous sommes concentrés sur 2 régions : L'Île-de-France et la Bourgogne-Franche-Comté")


  region=df_ml['libelle_region'].unique()

  selection_region=st.selectbox(label="Région",options= region)

   
  annee=df_ml['Année'].unique()
  selection_annee=st.multiselect(label="Année",options= annee)

  filtered_data = df_ml.loc[df_ml['libelle_region'] ==  selection_region]
  filtered_data=filtered_data[filtered_data['Année'].isin (selection_annee)]

  st.write ("** DataViz secteur d'activité**")

  secteur=filtered_data.groupby(['Année','libelle_region']).agg({'conso_totale_mwh_tertiaire_annuel':'mean','conso_moyenne_mwh_tertiaire_annuel':'mean','conso_totale_mwh_agriculture_annuel':'mean','conso_moyenne_mwh_agriculture_annuel':'mean','conso_totale_mwh_industrie_annuel':'mean','conso_moyenne_mwh_industrie_annuel':'mean'}).reset_index()
  
  plt.figure(figsize=(14, 8))
  plt.plot(secteur['Année'].astype(str), secteur['conso_moyenne_mwh_agriculture_annuel'], label='Agriculture', color='blue', linestyle='-', marker='o')
  plt.plot(secteur['Année'].astype(str),secteur['conso_moyenne_mwh_industrie_annuel'], label='Industrie', color='r', linestyle='-', marker='o')
  plt.plot(secteur['Année'].astype(str),secteur['conso_moyenne_mwh_tertiaire_annuel'], label='Tertiaire', color='green', linestyle='-', marker='o')
  plt.title(f"Consommation electrique moyenne par secteur d'activité en {selection_annee}")
  plt.xlabel("Année")
  plt.ylabel("Consommation (MWh)")
  plt.legend()
  st.pyplot(plt)
    
  st.write ("**Existe t'il une corrélation entre la consommation électrique et la température ? **")

  
  selection_a=st.selectbox(label="Année",options= annee)
  filtered_data2 = df_ml.loc[df_ml['libelle_region'] ==  selection_region]
  filtered_data2=filtered_data2[filtered_data2['Année']==selection_a]


  consoM=filtered_data2.groupby(pd.Grouper(key='date_heure_simplifiée', freq='W'))[['consommation','tmoy','tmax','tmin']].mean()
 

  corr, p_value = pearsonr(consoM["consommation"], consoM["tmoy"])

  st.write ("Nous allons procéder à un test statistique de PearsonR pour déterminer s'il existe une corrélation entre la consommation électrique et la température.")
  st.write(f"La P-value est : {p_value:.2e}. La P_value est inférieure à 5%, nous pouvons donc confirmer l'hypothèse de l'existence d'une corrélation entre la température moyenne et la consommation électrique.")
  st.write(f"Le Coefficient de corrélation de Pearson est: {corr:.2f}.Nous pouvons voir l'existence d'une forte corrélation négative pour la {selection_region} entre la consommation et la température de l'année {selection_a}. ")

   
  plt.figsize=(5, 5) 
  sns.relplot(x = "tmoy", y = "consommation", kind = "line", data = consoM)
  plt.title (f"Consommation moyenne par semaine en {selection_region} en fonction des températures moyenne en  {selection_a}")
  plt.xlabel("Température moyenne")
  plt.ylabel("Consommation moyenne")
  st.pyplot(plt)

  st.write ("Le graphique nous permet de valider la corrélation négative entre la température moyenne et la consommation électrique. En effet nous pouvons voir que plus il fait froid, plus nous consommons d'électricité.")

  

if page == pages[3] :

  st.write ("Le jeu de donnée que nous allons utilisées pour le machine learning est le suivant :")
  st.dataframe(df_ml.head())

  st.write ('**Analyse des series temporelles**')

  st.write("Depuis le début de notre étude, nous avons clairement identifié une saisonnalité marquée dans la consommation électrique. Nous allons utilisés les modéles SARIMAX et PROPHET afin de prédire les consommations électriques futures. Notre étude ce porte sur 2 régions distincte.")
  
  model_choisi=st.selectbox(label="Model",options= {'Sarimax','Prophet'})

  region=df_ml['libelle_region'].unique()
  selection_region=st.selectbox(label="Région",options= region)


#SARIMAX
  filtered_data = df.loc[df['libelle_region'] ==  selection_region]

  filtered_data['date'] = pd.to_datetime(filtered_data['date'])

  sarima_data=filtered_data.groupby(pd.Grouper(key='date', freq='M'))['consommation'].mean()
   

  X_train_sarima = sarima_data[:-24]
  y_test_sarima = sarima_data[-24:]
   
   
  pickle_in= open('sarimax_model.pkl', 'rb') 
  loaded_results = pickle.load(pickle_in)

  start=len(X_train_sarima)
  end=len(X_train_sarima)+len(y_test_sarima)-1
 
  y_pred_sarima =np.exp(loaded_results.predict(start = start, end = end))
  

  y_test_a=y_test_sarima[:12]
  
  end_annuel=len(X_train_sarima)+len(y_test_a)-1

  #Prediction sur l'ensemble du jeu de test

  y_pred_sarima_annuelle =np.exp(loaded_results.predict(start = y_test_a.index[0], end = y_test_a.index[-1]))


  #Prophet------------------------------------------------------------------------------------------------------------------

  #@title Regroupement par mois de la conso et temperature moyenne
   
  filtered_data_prophet = df_ml.loc[df_ml['libelle_region'] ==  selection_region]

  consoMensuelle=filtered_data_prophet.groupby(pd.Grouper(key='date_heure_simplifiée', freq='M'))[['consommation','tmoy','tmax','tmin']].mean()


  #@title Prepa DateFrame Prophet MULTIVARIE

  #Rename the columns to 'ds' and 'y'
  consoMensuelle = consoMensuelle.reset_index().rename(columns={'date_heure_simplifiée':'ds', 'consommation':'y'})


  # @title Separation jeu de train et test

  df_train = consoMensuelle.loc[consoMensuelle["ds"]<"2021-12-31"]
  df_test  = consoMensuelle.loc[consoMensuelle["ds"]>="2021-12-31"]

  from prophet import Prophet

  model_prophet= Prophet(seasonality_mode='multiplicative', yearly_seasonality=3)

  model_prophet.add_regressor('tmoy')
  model_prophet.add_regressor('tmax')
  model_prophet.add_regressor('tmin')

  model_prophet.fit(df_train)


  # @title Affichage des dates futures concerné par la prévision
  future = model_prophet.make_future_dataframe(periods=12,freq='M')
  future['tmoy']=consoMensuelle['tmoy']
  future['tmax']=consoMensuelle['tmax']
  future['tmin']=consoMensuelle['tmin']
  future.tail()

  forecast = model_prophet.predict(future)






  from prophet.diagnostics import cross_validation, performance_metrics

  # Perform cross-validation to generate forecasts with a 'cutoff' column
  df_cv = cross_validation(model_prophet, initial='1000 days', period='30 days', horizon = '365 days')

  #@title Metrique de performance PROPHET a divers Horizon

  from prophet.diagnostics import performance_metrics
  df_performance = performance_metrics(df_cv)

 
  perf=df_performance.loc[df_performance['horizon'] == '365 days']   



    

  score = r2_score(y_test_a, y_pred_sarima_annuelle)
  mae = mean_absolute_error(y_test_a, y_pred_sarima_annuelle)
  mse= mean_squared_error(y_test_a, y_pred_sarima_annuelle)
  rmse= np.sqrt(mean_squared_error(y_test_a, y_pred_sarima_annuelle))
  data = {'Metric': ['MAE', 'MSE', 'RMSE'], 'Durée' : ['12 mois','12 mois','12 mois'],  'SARIMA': [mae, mse, rmse]}

#Dataviz SARIMAX------------------------------------------------------------------------------------


  end_pred=len(X_train_sarima)+len(y_test_sarima)-1

  import datetime
  pred = np.exp(loaded_results.predict(start=end, end=end+12))#Prédiction et passage à l'exponentielle
  pred_res = loaded_results.get_prediction(start=end, end=end+12)



  pred_ci = pred_res.conf_int(alpha=0.05) #Intervalle de confiance
  pred_ci=np.exp(pred_ci)
  pred_ci.index = pd.date_range(pred_ci.index[0], periods=len(pred_ci), freq='M')


  pred_low=pred_ci['lower consommation']
  pred_high=pred_ci['upper consommation']


  fig = model_prophet.plot_components(forecast)

  sarima= plt.figure(figsize=(10,8))
  plt.plot(X_train_sarima, label='Données d\'entrainement')
  plt.plot(y_test_sarima, label='Données de test')
  plt.axvline(x=y_test_sarima.index[-1], color='red', linestyle='--', label='Début des Prédictions')
  plt.axvline(x=X_train_sarima.index[-1], color='green', linestyle='--', label='Début des Test')
  plt.plot(y_pred_sarima, label='Prédiction sur les données de test')
  plt.plot(pred, label='Prédiction sur les données futures')
  plt.fill_between(pred_ci.index, pred_low, pred_high, alpha=0.5, color="y", label="Intervalle de confiance")
  plt.ylim(min(X_train_sarima.min(),y_test_sarima.min()),max(X_train_sarima.max(),y_test_sarima.max()))
  plt.xlabel('Date')
  plt.ylabel('Consommation')
  plt.legend()
  plt.title('Prédiction de la consommation électrique')


  fig1 = model_prophet.plot(forecast)
  plt.xlabel('Date')
  plt.ylabel('Consommation')
  plt.title('Prédiction et consommation électrique')
  plt.legend()
 




  if model_choisi=="Prophet" :
    st.write('Les résultats des 5 premières estimation future sont :',forecast.head())

    st.write ("Les métriques sont:" ,df_performance.head(12))
    st.markdown("Les résultats des métriques montrent que le modèle devient moins précis à mesure que l'horizon de prédiction s'allonge, ce qui est une tendance attendue dans les prévisions de séries temporelles.")

    st.pyplot(fig1)
    st.markdown(' Le graphique montre que le modèle capture efficacement les cycles saisonniers, avec des pics en hiver et des baisses en été. Les données réelles (points noirs) sont proches des prévisions, démontrant la précision du modèle.')

  elif model_choisi=="Sarimax" :
    st.write(loaded_results.summary())
    st.write("Les pvalues sont pour l'essentiel inférieur à 0.05.Le test de Ljung-Box est un test de blancheur des résidus. C'est un test statistique qui vise à rejeter ou non l'hypothèse 𝐻0 : Le résidu est un bruit blanc. Ici on lit sur la ligne Prob(Q) que la p-valeur de ce test est de 0.90 , donc on ne rejette pas l'hypothèse.Le test de Jarque-Bera est un test de normalité. C'est un test statistique qui vise à rejeter ou non l'hypothèse 𝐻0 : Le résidu suit une distribution normale. Ici on lit sur la ligne Prob (JB) que la p-valeur du test est de 0.00 . On rejette donc l'hypothèse.Les résidus confirme les hypothéses que nous avons faite initialement, ce qui conforte notre modèle.")

    st.write ("Le score est:" ,score)
    st.write("Les métriques sont les suivantes :")
    st.dataframe(data)
    st.write("Les résultats nous montrent ici une bonne capacité du modèle à prédire la consommation énergétique, nous avons un score très proche de 1 et des MAE, MSE, RMSE tout a fait acceptable.")

    st.pyplot(sarima)


  
  st.write("### Comparaison des 2 modèles")
 
  st.write('Les métriques sur 12 mois de prophet sont :',perf)
  st.write('Les métriques de SARIMAX sur 12 mois sont :')
  st.dataframe(data)

  st.write("Nous pouvons constater que les métriques du modèle SARIMAX sont meilleures à l'horizon 12 mois que le modèle Prophet. Cependant, comme nous pouvons le voir dans la modélisation Prophet, plus l'horizon est proche, plus les métriques Prophet s'améliorent. Nous allons donc privilégier SARIMA pour des prévisions sur le moyen, long terme et Prophet sur le court terme.")

  model_prophet.plot(forecast)
  plt.plot(y_pred_sarima,label='prediction SARIMA',color='green')
  plt.legend()
  plt.title("Prediction SARIMA vs PROPHET")
  

  st.pyplot(plt)
  st.markdown ('Le graphique compare les prédictions des deux modèles et confirme notre précédent comparatif :● SARIMA capture très bien les cycles saisonniers avec des prédictions régulières en étant très bon sur des horizons à long terme.● Prophet suit également les tendances mais semble plus efficace à court terme.')


if page==pages[4] :

 st.write("### Synthèse")

 st.write("Pour résumer, dans le cadre de notre projet de fin de formation en analyse de données, cette étude approfondie sur l'estimation de la consommation électrique future en France nous a permis de comprendre les tendances de consommation afin de contribuer à assurer une transition énergétique réussie. Notre travail s'est appuyé sur la collecte et l'analyse de divers jeux de données, notamment les données éCO2mix régionales sur la consommation et la production électrique par source d'énergie, les données météorologiques (températures, rayonnement solaire, vitesse du vent) et des informations sur les secteurs d'activité liés à la consommation électrique. Un effort significatif a été consacré au nettoyage et à la préparation de ces données pour garantir la fiabilité de nos analyses. Des tests statistiques, tels que les coefficients de corrélation de Pearson, ont permis d'identifier les variables significatives influençant la consommation électrique. L'analyse a révélé une saisonnalité marquée dans la consommation électrique, avec des pics en hiver et des creux en été. Pour modéliser ces tendances, nous avons utilisé des modèles de séries temporelles, notamment le modèle SARIMA, adapté pour capturer la saisonnalité et les tendances à long terme. Les prédictions sur 12 mois ont montré une excellente adéquation avec les données réelles, avec un score de 0,94. Parallèlement, nous avons employé la librairie Prophet, qui permet d'intégrer des variables externes comme la température pour affiner les prévisions. Prophet a démontré une meilleure performance sur les prévisions à court terme. Le comparatif des deux modèles a mis en évidence que SARIMA est plus robuste pour les prévisions à long terme, tandis que Prophet offre une précision accrue à court terme.")

 st.write("Notre étude a mis en évidence une tendance générale à la baisse de la consommation électrique en France. Cette diminution, confirmée par nos analyses statistiques et nos modèles de prévision, s'inscrit dans un contexte de transition énergétique et de prise de conscience accumulée des enjeux environnementaux. Plusieurs facteurs expliquent cette tendance : l'augmentation des tarifs d'électricité incite les consommateurs à réduire leur consommation ; les technologies avancées ont conduit à l'adoption d'équipements plus efficaces et moins énergivores ; le changement climatique entraîne des hivers plus doux, notamment la demande en chauffage électrique ; une sensibilisation environnementale croissante conduit la population à adopter des comportements plus responsables ; enfin, les politiques gouvernementales mettent en place des mesures incitatives pour réduire la consommation et promouvoir les énergies renouvelables.")

 st.write("Les implications de cette baisse sont significatives. Elle facilite l'atteinte des objectifs de décarbonation fixés lors d'accords internationaux tels que la COP22, en particulier les émissions de gaz à effet de serre liées à la production d'électricité. De plus, elle diminue la pression sur le réseau électrique national, améliorant sa résilience face aux variations de la demande et aux aléas climatiques. Toutefois, cette tendance pose également des défis aux producteurs d'énergie, qui doivent adapter leurs modèles économiques et investir dans les énergies renouvelables et les technologies de stockage.")

 st.write("Bien que notre étude ait apporté des éclairages significatifs sur l'évolution de la consommation électrique, plusieurs pistes méritent d'être explorées pour approfondir cette analyse. Nous aurions aimé affiner notre modélisation en travaillant sur des données hebdomadaires, voire journalières, notamment en utilisant la librairie Prophet, ce qui permet de capturer les fluctuations à court terme et d'identifier des schémas de consommation plus précis. Une analyse à une échelle plus locale, par exemple au niveau des villes, offrirait une compréhension détaillée des variations régionales. De même, étudier l'impact de la densité de population ou distinguer entre les villes industrielles et tertiaires permettra d'évaluer l'influence des activités économiques sur la consommation énergétique.")

 st.write("En somme, ces perspectives ouvrent la voie à une compréhension plus fine et nuancée de la consommation électrique en France. Elles soulignent l'importance d'une approche multidimensionnelle, combinant analyses techniques approfondies et prise en compte des facteurs socio-économiques. Poursuivre dans cette direction contribuera non seulement à optimiser la gestion énergétique, mais aussi à soutenir les efforts de transition vers une société plus durable et résiliente face aux défis climatiques.")

  
