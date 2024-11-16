import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
  plt.title("Consommation electrique moyenne par secteur d'activité")
  plt.xlabel("Année")
  plt.ylabel("Consommation (MWh)")
  plt.legend()
  st.pyplot(plt)
    
  st.write ("**Existe t'il une corrélation entre la consommation électrique et la température ? **")

  # v01. Modification le 02112024-----------------------------------------------------------------------------------------------------------------------------------------------------
  selection_a=st.selectbox(label="Année",options= annee)
  filtered_data2 = df_ml.loc[df_ml['libelle_region'] ==  selection_region]
  filtered_data2=filtered_data2[filtered_data2['Année']==selection_a]


  consoM=filtered_data2.groupby(pd.Grouper(key='date_heure_simplifiée', freq='W'))[['consommation','tmoy','tmax','tmin']].mean()
  #Fin v01.-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

  corr, p_value = pearsonr(consoM["consommation"], consoM["tmoy"])
  st.write(f"Le Coefficient de corrélation de Pearson est: {corr:.2f}")
  st.write(f"La P-value est : {p_value:.2e}")

  st.write ("""Nous pouvons voir l'existence d'une forte corrélation négative entre la consommation et la température.""")
   
  plt.figsize=(5, 5) 
  sns.relplot(x = "tmoy", y = "consommation", kind = "line", data = consoM)
  plt.title ("Consommation moyenne par semaine en fonction des températures moyenne")
  plt.xlabel("Température moyenne")
  plt.ylabel("Consommation moyenne")
  st.pyplot(plt)

  

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

  
