import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# 1. Carrega i clustering
df = pd.read_csv('dades_covid_modificat.csv')
if 'cluster' in df.columns:
    df = df.drop(columns=['cluster'])
variables = ['AGE', 'bmi', 'charges']
scaled = StandardScaler().fit_transform(df[variables])
df['cluster'] = KMeans(n_clusters=3, random_state=0).fit_predict(scaled)

# 2. PCA 2D
pca = PCA(n_components=2)
pcs = pca.fit_transform(scaled)
plt.figure(figsize=(8,5))
plt.scatter(pcs[:, 0], pcs[:, 1], c=df['cluster'], cmap='viridis', alpha=0.6)
plt.title('PCA 2D dels clústers')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()

# 3. Scatter plots
for x, y in [('AGE','bmi'), ('AGE','charges'), ('bmi','charges')]:
    plt.figure(figsize=(6,5))
    plt.scatter(df[x], df[y], c=df['cluster'], cmap='viridis', alpha=0.6)
    plt.title(f'{x} vs {y}')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()

# 4. Boxplots manual per variable
for var in variables:
    plt.figure(figsize=(6,5))
    grouped = [df[var][df['cluster'] == i] for i in sorted(df['cluster'].unique())]
    plt.boxplot(grouped)
    plt.xticks(range(1, len(grouped)+1), sorted(df['cluster'].unique()))
    plt.title(f'Boxplot de {var} per clúster')
    plt.xlabel('Clúster')
    plt.ylabel(var)
    plt.show()
