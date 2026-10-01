"""Pression sur le logement social dans 5 communes (données 2025, anonymisées)."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("logement_social_5_communes.csv")

# Pression = demandes en attente pour 1 logement attribué dans l'année
par_commune = df.groupby("commune")[["logements_2025", "demandes_attente_fin2025", "attributions_2025"]].sum()
par_commune["pression"] = par_commune["demandes_attente_fin2025"] / par_commune["attributions_2025"]
par_commune = par_commune.sort_values("pression")
print(par_commune.round(1))

# Pas de calcul possible quand il n'y a eu aucune attribution (division par zéro)
df = df[df["type"] != "T6"].copy()
df["pression"] = df["demandes_attente_fin2025"] / df["attributions_2025"].replace(0, np.nan)
par_type = df.pivot(index="type", columns="commune", values="pression")
print(par_type.round(1))

plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False, "font.size": 10})

fig, ax = plt.subplots(figsize=(8, 3.4))
ax.barh(par_commune.index, par_commune["pression"], color="#2a78d6", height=0.55)
for i, v in enumerate(par_commune["pression"]):
    ax.text(v + 0.4, i, f"{v:.0f} demandes", va="center")
ax.set_xlim(0, 36)
ax.set_xlabel("Demandes en attente pour 1 logement attribué en 2025")
ax.set_title("Pression sur le logement social, tous types confondus", loc="left")
ax.grid(axis="x", color="#e6e5e0")
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig("01_pression_par_commune.png", bbox_inches="tight")

fig, ax = plt.subplots(figsize=(8, 3.8))
valeurs = np.clip(par_type.values, 0, 50)
im = ax.imshow(np.ma.masked_invalid(valeurs), cmap="Blues", vmin=0, vmax=50, aspect="auto")
ax.set_facecolor("#e6e5e0")
ax.set_xticks(range(len(par_type.columns)), par_type.columns)
ax.set_yticks(range(len(par_type.index)), par_type.index)
for i in range(par_type.shape[0]):
    for j in range(par_type.shape[1]):
        v = par_type.values[i, j]
        texte = "aucune\nattribution" if np.isnan(v) else f"{v:.0f}"
        couleur = "white" if not np.isnan(v) and v > 28 else "#0b0b0b"
        ax.text(j, i, texte, ha="center", va="center", fontsize=9, color=couleur)
for bord in ax.spines.values():
    bord.set_visible(False)
ax.set_title("Nombre de demandes en attente pour 1 logement attribué en 2025\n(un nombre de demandes, pas une durée)", loc="left")
fig.colorbar(im, ax=ax, shrink=0.8, label="échelle plafonnée à 50")
fig.tight_layout()
fig.savefig("02_pression_par_type.png", bbox_inches="tight")
