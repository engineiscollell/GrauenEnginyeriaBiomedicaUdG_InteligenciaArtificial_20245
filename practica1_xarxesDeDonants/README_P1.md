# Pràctica 1 — Xarxes de Donants (IA 2024/25)

> Author: **Lluís F. Collell**  
> Curs **Intel·ligència Artificial** · Universitat de Girona

## 📜 Descripció

Algoritme per formar **4 xarxes de donació** a partir de **40 hospitals** combinant:

1. **Distància euclidiana** entre hospitals.  
2. **Semblança de la població** (XB `matchBN`) ponderada amb un paràmetre `µ` (0 ≤ µ ≤ 1).

L’objectiu és **minimitzar la distància interna** de cada xarxa mentre **maximitzem** la semblança (`µ·sim`) entre hospitals de la mateixa xarxa.

## ✏️ Algoritme

La solució es basa en **Local Beam Search (LBS)** amb veïnatge *swap* i *shift*.

- **Representació d’estat:** vector de longitud 40 amb valors `{0, 1, 2, 3}` que indica la xarxa assignada a cada hospital.
- **Estats inicials:** generem `B` assignacions aleatòries amb `creacio_beam_aleatories`.

### Veïnatge

- `swap(i, j)`: intercanvia dos hospitals de xarxes diferents.  
- `shift(i → j)`: mou un hospital a una altra xarxa.

### Funció objectiu

La funció a optimitzar és:

f(g) = dist(g) − µ·sim(g)

on:
- `dist(g)`: distància mitjana entre hospitals d'una mateixa xarxa (intra-xarxa).
- `sim(g)`: semblança mitjana entre hospitals d'una mateixa xarxa segons la xarxa bayesiana `matchBN`.
- `µ`: paràmetre de ponderació entre distància i semblança (0 ≤ µ ≤ 1).

### Criteri d’aturada

L'algoritme finalitza quan:

- No hi ha millora en una iteració, **o**
- S'han fet `K` iteracions com a màxim.

### Complexitat (pitjor cas)

| Pas                | Complexitat   |
|--------------------|---------------|
| Generar veïns      | B · N²        |
| Avaluar el beam    | B · N²        |
| Iteracions totals  | K · B · N²    |

## 🧠 Xarxes Bayesianes i Inferència

- `criticalBN` (donada): modela la probabilitat de casos crítics amb les variables `I`, `J`, `C`, `K`.
- `matchBN` (implementada): duplica l’estructura de `criticalBN` per a dos hospitals i hi afegeix la variable `M` (*match*).

### Regla principal

> Si `C₁ = C₂` aleshores `P(M = T) = 0.95`;  
> Altrament, `P(M = T) = 0.10`.

### Inferència

- **Exacta:** `variable_elimination`, cal triar un bon ordre d’eliminació.
- **Aproximada:**
  - `rejection_sampling`
  - `weighted_sampling` (amb *likelihood weighting*)

L’informe analitza quants mostres (`N`) calen perquè els resultats aproximats convergeixin als exactes.

Aquesta xarxa bayesiana ens permet incorporar la **similitud de poblacions** directament a la funció objectiu amb el terme `µ·sim(g)`.

---

## 🗂️ Estructura del projecte
```text
.
├── s1/                    # Materials de la 1a sessió
│   ├── main1.py
│   └── datapoints.csv
├── s2/                    # Materials de la 2a sessió / entrega final
│   ├── main2.py
│   ├── data.csv
│   ├── bn.py
│   ├── my_bns.py
│   └── inferencia.py
├── p1.py                  # Algoritme principal (Local Beam Search)
├── informe.pdf            # Informe complet de la pràctica
├── p1_enunciat.pdf        # Enunciat de la pràctica
└── README.md              # Aquesta guia
````

## Agraïments

- **Enunciat, dades i codi base:** Prof. **Jerónimo Hernández González**, Universitat de Girona (curs 2024/25).
- **Implementació inicial de** `criticalBN`, `bn.py` i `rejection_sampling`: equip docent de l’assignatura d’IA.
- **Inspiració dels veïnatges** *swap* i *shift*: apunts de classe i el llibre *Russell & Norvig*.
