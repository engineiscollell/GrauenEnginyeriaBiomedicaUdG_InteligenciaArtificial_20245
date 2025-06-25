import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# 1. Carreguem les dades
df = pd.read_csv('dades_covid_modificat.csv')

# -------- OBJECTIU A: Gravetat clínica --------
variables_a = ['AGE', 'ICU', 'INTUBED', 'DATE_DIED', 'DIABETES', 'COPD', 'RENAL_CHRONIC']
df_a = df[variables_a].copy()
df_a = df_a.fillna(0)

# Escalat per a gravetat clínica
scaler_a = StandardScaler()
scaled_a = scaler_a.fit_transform(df_a)

# KMeans amb k=3
kmeans_a = KMeans(n_clusters=3, random_state=0)
df['cluster_gravetat'] = kmeans_a.fit_predict(scaled_a)

# Visualització PCA
pca_a = PCA(n_components=2)
pca_a_result = pca_a.fit_transform(scaled_a)
plt.figure(figsize=(6, 5))
plt.scatter(pca_a_result[:, 0], pca_a_result[:, 1], c=df['cluster_gravetat'], cmap='viridis', alpha=0.6)
plt.title("Objectiu A – Clustering per gravetat clínica")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.show()

# -------- OBJECTIU B: Perfil econòmic --------
variables_b = ['AGE', 'bmi', 'charges', 'paid', 'children', 'region']
df_b = df[variables_b].copy()
df_b = df_b.fillna(0)

# Aplicació de pesos: més pes a 'charges' i 'AGE'
df_b['AGE'] *= 2
df_b['charges'] *= 3

# Escalat per a perfil econòmic
scaler_b = StandardScaler()
scaled_b = scaler_b.fit_transform(df_b)

# KMeans amb k=4
kmeans_b = KMeans(n_clusters=4, random_state=0)
df['cluster_economic'] = kmeans_b.fit_predict(scaled_b)

# Visualització PCA
pca_b = PCA(n_components=2)
pca_b_result = pca_b.fit_transform(scaled_b)
plt.figure(figsize=(6, 5))
plt.scatter(pca_b_result[:, 0], pca_b_result[:, 1], c=df['cluster_economic'], cmap='plasma', alpha=0.6)
plt.title("Objectiu B – Clustering per perfil econòmic")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.show()
