import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Carreguem les dades
df = pd.read_csv("dades_covid_numeric.csv")

# L'atribut 'region' té caràcters buits, aquests s'han d'emplenar utilitzant la moda (valor més comú)
most_common_region = df['region'].mode()[0]
print(f"Moda per a 'region': {most_common_region}")
df['region'] = df['region'].fillna(most_common_region)

# L'atribut 'charges' també té valors buits. L'emplenarem amb la mitjana dels valors
mean_charges = df['charges'].mean()
print(f"Mitjana per a 'charges': {mean_charges}")
df['charges'] = df['charges'].fillna(mean_charges)

# Comprovació: número de valors nuls
print("\nValors nuls per columna després de la imputació:")
print(df[['region', 'charges']].isnull().sum())

# Comprovació: número de valors no nuls
print("\nValors NO nuls per columna després de la imputació:")
print(df[['region', 'charges']].notnull().sum())

# ---------- Càlcul d'importància de característiques per 'PREGNANT' ----------
print("\nImportància de les variables predictors per predir 'PREGNANT':")

df_preg = df[df['PREGNANT'].notnull()]
X = df_preg.drop(columns=['PREGNANT'])
y = df_preg['PREGNANT']

clf = DecisionTreeClassifier(random_state=0)
clf.fit(X, y)

importances = pd.Series(clf.feature_importances_, index=X.columns)
importances = importances.sort_values(ascending=False)
print(importances.head(5))

# ---------- Imputació de valors buits a 'PREGNANT' amb arbre de decisió ----------

print("\nImputant valors buits a 'PREGNANT'...")

# Definim els predictors més rellevants
top_features = ['AGE', 'bmi', 'charges', 'USMER', 'OBESITY']

# Dades per entrenar el model
df_train = df[df['PREGNANT'].notnull()]
X_train = df_train[top_features]
y_train = df_train['PREGNANT']

# Proporció abans de la imputació
prop_before = df_train['PREGNANT'].value_counts(normalize=True)
print("\nProporció d'embarassades abans de la imputació:")
print(prop_before)

# Entrenem l'arbre de decisió
clf_preg = DecisionTreeClassifier(random_state=0)
clf_preg.fit(X_train, y_train)

# Predicció per les files amb PREGNANT nul
df_missing = df[df['PREGNANT'].isnull()]
X_missing = df_missing[top_features]

if not X_missing.empty:
    predicted = clf_preg.predict(X_missing)
    df.loc[df_missing.index, 'PREGNANT'] = predicted
    print(f"\nS'han imputat {len(predicted)} valors a 'PREGNANT'")
else:
    print("\nNo hi ha valors nuls a 'PREGNANT'. No cal imputar.")

# Correcció de casos impossibles:
df.loc[(df['SEX'] == 0) & (df['PREGNANT'] == 1), 'PREGNANT'] = 0
df.loc[(df['DATE_DIED'] == 1) & (df['PREGNANT'] == 1), 'PREGNANT'] = 0

# Comprovació final de valors nuls
print("\nValors nuls a 'PREGNANT' després de la imputació i correcció:")
print(df['PREGNANT'].isnull().sum())

# Proporció després de la imputació
prop_after = df['PREGNANT'].value_counts(normalize=True)
print("\nProporció d'embarassades després de la imputació:")
print(prop_after)

# Validació de casos impossibles
invalid_men = df[(df['SEX'] == 0) & (df['PREGNANT'] == 1)].shape[0]
invalid_dead = df[(df['DATE_DIED'] == 1) & (df['PREGNANT'] == 1)].shape[0]
print(f"\nNombre d'homes embarassats (hauria de ser 0): {invalid_men}")
print(f"Nombre de morts embarassats (hauria de ser 0): {invalid_dead}")

# Guardem el fitxer modificat
df.to_csv("dades_covid_modificat.csv", index=False)
