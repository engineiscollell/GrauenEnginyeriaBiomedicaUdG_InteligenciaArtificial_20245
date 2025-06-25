import pandas as pd

# 0. Spec de tipus per a booleans i categories
bool_cols = [
    'INTUBED','PNEUMONIA','DIABETES','COPD','ASTHMA',
    'INMSUPR','HIPERTENSION','OTHER_DISEASE','CARDIOVASCULAR',
    'OBESITY','RENAL_CHRONIC','TOBACCO','ICU','PREGNANT','paid'
]
dtype_spec = {col: "string" for col in bool_cols}
dtype_spec.update({
    'DATE_DIED': "string",
    'region': "category",
    'CLASIFFICATION_FINAL': "category",
    'SEX': "category"
})

# 1. Llegim el CSV indicant que la coma és separador decimal
df = pd.read_csv(
    "dades_covid.csv",
    sep=";",
    dtype=dtype_spec,
    decimal=",",    # → 41,23  → 41.23
    thousands=None  # cap separador de milers
)

# Ara df["charges"] i df["bmi"] surten directament com a float64
print(df[["bmi","charges"]].dtypes)
# bmi       float64
# charges   float64

# 2. Helper per normalitzar + map
def map_column(col: pd.Series, mapper: dict, null_val=None, nullable_type=None):
    s = col.str.strip().str.lower()
    mapped = s.map(mapper)
    if null_val is not None:
        mapped = mapped.fillna(null_val)
    if nullable_type is not None:
        return mapped.astype(nullable_type)
    return mapped

# 3. Diccionaris de mapatge
mappings = {
    'SEX': {"male": 0, "female": 1},
    **{col: {"true":1, "false":0} for col in bool_cols},
    'region': {"northwest":0,"southwest":1,"northeast":2,"southeast":3},
    'DATE_DIED': { "":0 },    # ho tractarem a part
    'CLASIFFICATION_FINAL': {
        'covid_1':0,'covid_2':1,'covid_3':2,
        'inconcluse_1':3,'inconcluse_2':4,'inconcluse_3':5,
        'none_1':6,'none_2':7,'none_3':8
    }
}

# 4. Apliquem els mapatges i acumulem informe
report = []
for col, mapper in mappings.items():
    before = df[col].value_counts(dropna=False)
    if col == "DATE_DIED":
        mapped = df[col].notna().astype(int)
    else:
        nullable = "Int64" if col in bool_cols + ['region','CLASIFFICATION_FINAL'] else None
        mapped = map_column(df[col], mapper, null_val=None, nullable_type=nullable)
    df[col] = mapped
    after = df[col].value_counts(dropna=False)
    report.append((col, before.to_dict(), after.to_dict()))

# 5. Funció per imprimir l’informe
def print_report(r):
    for col, bef, aft in r:
        print(f"--- {col} ---")
        print("Before:", bef)
        print("After: ", aft, "\n")

print_report(report)

# 6. Quinze columnes tenen NaN?
cols_with_nans = df.isna().sum()[lambda x: x>0]
print("Columnes amb NaN:", list(cols_with_nans.index))

# 7. Desa el CSV final
df.to_csv("dades_covid_numeric.csv", index=False)
