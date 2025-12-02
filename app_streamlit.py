# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 13:11:54 2025

@author: adele
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.set_page_config(page_title="Streamlit Netflix", layout="wide")

st.title("Application Streamlit — Analyse Netflix")



def parse_duration_minutes(x):
    if isinstance(x, str) and "min" in x:
        try:
            return int(x.replace("min", "").strip())
        except:
            return np.nan
    return np.nan


def parse_duration_seasons(x):
    if isinstance(x, str) and "Season" in x:
        try:
            return int(x.split()[0])
        except:
            return np.nan
    return np.nan


def duration_to_numeric(x):
    # pour ordonner minutes d'abord, saisons après
    if pd.isna(x):
        return np.nan
    x = str(x)
    if "min" in x:
        try:
            return int(x.replace("min", "").strip())
        except:
            return np.nan
    if "Season" in x:
        try:
            n = int(x.split()[0])
            return 1000 + n
        except:
            return np.nan
    return np.nan

# ---------------- Chargement (upload ou fichier local) ----------------

st.sidebar.header("Chargement des données")
use_sample = st.sidebar.checkbox("Lire le fichier local 'netflix_titles.csv' si présent", value=False)
uploaded = None
if use_sample:
    try:
        df = pd.read_csv("netflix_titles.csv", encoding="latin1")
        st.sidebar.success("Fichier local chargé")
    except FileNotFoundError:
        st.sidebar.warning("Fichier local non trouvé. Utiliser l'uploader ci-dessous.")
        uploaded = st.sidebar.file_uploader("Ou importer fichier CSV", type=["csv"])
else:
    uploaded = st.sidebar.file_uploader("Importer fichier CSV", type=["csv"])
    df = None

if uploaded is not None and df is None:
    df = pd.read_csv(uploaded, encoding="latin1")

if df is None:
    st.info("Charger fichier netflix_titles.csv via la sidebar pour démarrer l'application.")
    st.stop()

# ---------------- Nettoyage  ----------------
st.sidebar.header("Nettoyage")
if st.sidebar.button("Appliquer nettoyage minimal"):
    # suppression NA 
    before = len(df)
    df.dropna(inplace=True)
    st.sidebar.write(f"Lignes supprimées (NA): {before - len(df)} — reste {len(df)}")

# suppression des doublons 
if st.sidebar.button("Supprimer les doublons" ):
    before = len(df)
    df.drop_duplicates(inplace=True)
    st.sidebar.write(f"Doublons supprimés: {before - len(df)} — reste {len(df)}")

# conversion des dates
df["date_added"] = pd.to_datetime(df.get("date_added"), errors="coerce")
# release_year -> numérique (années)
try:
    df["release_year"] = pd.to_numeric(df.get("release_year"), errors="coerce").astype('Int64')
except Exception:
    df["release_year"] = pd.to_numeric(df.get("release_year"), errors="coerce")

# durations
df["duration_minutes"] = df["duration"].apply(parse_duration_minutes)
df["duration_seasons"] = df["duration"].apply(parse_duration_seasons)
df["duration_numeric"] = df["duration"].apply(duration_to_numeric)

st.success("Nettoyage appliqué (date_added, release_year, duration_parsed)")

# ---------------- Sidebar filtres ----------------
st.sidebar.header("Filtres d'affichage")
all_types = df["type"].dropna().unique().tolist()
selected_types = st.sidebar.multiselect("Type (Movie / TV Show)", options=all_types, default=all_types)

min_year = int(df["release_year"].min()) if df["release_year"].notna().any() else 1900
max_year = int(df["release_year"].max()) if df["release_year"].notna().any() else 2025
year_range = st.sidebar.slider("Plage d'années (release_year)", min_year, max_year, (min_year, max_year))

# appliquer filtres
df_filtered = df[df["type"].isin(selected_types)]
df_filtered = df_filtered[df_filtered["release_year"].between(year_range[0], year_range[1], inclusive="both")]

# ---------------- Layout principal ----------------
st.header("Aperçu des données (filtrées)")
st.write(f"Titres affichés: {len(df_filtered)}")
st.dataframe(df_filtered.head(50))

col1, col2 = st.columns(2)

with col1:
    st.subheader("Histogramme durée (minutes et saisons)")
    # ordre des catégories basé sur duration_numeric
    ordered = (
        df_filtered.dropna(subset=["duration_numeric"])\
          .sort_values("duration_numeric")
          ["duration"]\
          .unique().tolist()
    )
    if len(ordered) == 0:
        st.info("Pas de données de durée pour le sous-ensemble filtré.")
    else:
        fig = px.histogram(df_filtered, x="duration", category_orders={"duration": ordered}, nbins=40,
                           title="Histogramme de la durée des contenus")
        fig.update_layout(xaxis_title="Durée (minutes ou saisons)", yaxis_title="Fréquence")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 20 genres (bar)" )
    genres = df_filtered["listed_in"].dropna().str.split(", ")
    genres_flat = [g for sub in genres for g in sub]
    if len(genres_flat) == 0:
        st.info("Pas de genres disponibles pour le filtrage actuel.")
    else:
        genres_series = pd.Series(genres_flat).value_counts().head(20).reset_index()
        genres_series.columns = ["genre", "count"]
        figg = px.bar(genres_series, x="genre", y="count", title="Top 20 genres")
        figg.update_layout(xaxis_tickangle=45)
        st.plotly_chart(figg, use_container_width=True)

with col2:
    st.subheader("Répartition classifications (rating)")
    if "rating" in df_filtered.columns:
        rating_counts = df_filtered["rating"].value_counts().reset_index()
        rating_counts.columns = ["rating", "count"]
        fig_r = px.bar(rating_counts, x="rating", y="count", title="Répartition des ratings")
        st.plotly_chart(fig_r, use_container_width=True)
    else:
        st.info("Colonne 'rating' absente.")

    st.subheader("Timeline des ajouts (mensuelle)")
    # timeline
    df_filtered["month_added"] = df_filtered["date_added"].dt.to_period("M").astype(str)
    timeline = df_filtered.groupby("month_added").size().reset_index(name="count")
    if timeline.empty:
        st.info("Pas assez de dates pour la timeline")
    else:
        fig_t = px.line(timeline, x="month_added", y="count", title="Ajouts par mois")
        st.plotly_chart(fig_t, use_container_width=True)

# ---------------- Boxplots Matplotlib (Films / Séries séparés) ----------------
st.header("Boxplots (Matplotlib) : Films vs Séries")
col3, col4 = st.columns(2)

with col3:
    df_films = df_filtered[df_filtered["type"] == "Movie"].dropna(subset=["duration_minutes"]) 
    if df_films.empty:
        st.info("Pas suffisamment de films avec durée en minutes pour afficher le boxplot.")
    else:
        figf, axf = plt.subplots(figsize=(6,5))
        sns.boxplot(y=df_films["duration_minutes"], ax=axf)
        axf.set_title("Durée des Films (minutes)")
        axf.set_ylabel("Durée (minutes)")
        st.pyplot(figf)

with col4:
    df_series = df_filtered[df_filtered["type"] == "TV Show"].dropna(subset=["duration_seasons"]) 
    if df_series.empty:
        st.info("Pas suffisamment de séries avec info de saisons pour afficher le boxplot.")
    else:
        figs, axs = plt.subplots(figsize=(6,5))
        sns.boxplot(y=df_series["duration_seasons"], ax=axs)
        axs.set_title("Durée des Séries (saisons)")
        axs.set_ylabel("Nombre de saisons")
        st.pyplot(figs)

# ---------------- Téléchargement ----------------
st.header("Exporter les données filtrées")
if st.button("Télécharger CSV filtré"):
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(label="Télécharger", data=csv, file_name='netflix_filtered.csv', mime='text/csv')

