 Mini-projet-Analyse exploratoire du catalogue Netflix

 Mini-Application Streamlit — Analyse du Catalogue Netflix

Ce projet est une mini-application interactive développée avec Streamlit, permettant d'explorer le dataset public de Netflix : films, séries, genres, durées, dates d’ajout, pays d’origine, etc.

L’application reprend les analyses du notebook Python (histogrammes, boxplots, genres, timeline…) et les rend interactives et filtrables.



 1. Contenu du projet

Le repository contient :

- app_streamlit.py: application Streamlit
- netflix_titles.csv: dataset Netflix 
- README.md
- Notebook_Adele_Dalle_Projet.ipynb: le notebook Jupyter contenant le code complet du projet
- Rapport_Adèle_Dalle.pdf: le rapport pdf avec les analyses
- requirements.txt: nécessaire pour le bon fonctionnement de l'application Streamlit


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

3. Accéder à l'application Streamlit
   
A taper dans Anaconda Prompt :

python -m pip install streamlit pandas plotly seaborn matplotlib wordcloud

Puis aller dans le dossier qui contient le code de l'application en utilisant:

cd "votre chemin contenant le code.../ app_streamlit"

Enfin donner cette dernière instruction: 

streamlit run app_streamlit.py

Ou ouvrir ce lien directement dans votre navigateur:

https://mini-projet-l2zs4xt3uxhnkgaj8c9mm5.streamlit.app/

