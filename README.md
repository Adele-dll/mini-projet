 Mini-projet-Analyse exploratoire du catalogue Netflix

 Mini-Application Streamlit — Analyse du Catalogue Netflix

Ce projet est une mini-application interactive développée avec Streamlit, permettant d'explorer le dataset public de Netflix : films, séries, genres, durées, dates d’ajout, pays d’origine, etc.

L’application reprend les analyses du notebook Python (histogrammes, boxplots, genres, timeline…) et les rend interactives et filtrables.

---

 1. Contenu du projet

Le repository contient :

- app_streamlit.py: application Streamlit
- netflix_titles.csv: dataset Netflix 
- README.md 
---

 2. Prérequis

Avant d’exécuter l’application, vous devez avoir :

- Python 3.8+ installé
- Les bibliothèques suivantes :  
  - streamlit  
  - pandas  
  - plotly  
  - seaborn  
  - matplotlib  
  - wordcloud  

A taper dans Anaconda Prompt :

python -m pip install streamlit pandas plotly seaborn matplotlib wordcloud

streamlit run app_streamlit.py

