# AXIS — Spécification Formelle des Relations Spatiales (`SPATIAL_RELATION_DEFINITIONS.md`)

> **Document Identifier:** `RUN-021-SPATIAL-RELATION-DEFINITIONS`  
> **Date:** 2026-09-23  
> **Auteur:** AXIS Dataset Engineering & Scientific Preparation Agent  
> **Statut Invariant:** DÉTERMINISTE & MATHÉMATIQUEMENT FONDÉ (0 seuil arbitraire)

---

## 1. Principes Fondamentaux de Dérivation

Chaque relation spatiale est dérivée de façon strictement algorithmique à partir des masques physiques du plan rasterisé 256x256 px.
Aucune inférence par modèle de langage, estimation heuristique non vérifiée ou étiquetage visuel subjectif n'est admis comme vérité terrain (`DERIVED_GROUND_TRUTH`).

Soit un plan d'étage matriciel $I \in \{0, \dots, 255\}^{H \times W \times 3}$ ($H = W = 256$) :
- Masque des pièces : $M_{\text{rooms}} = \{(y, x) \mid I(y, x) = (255, 255, 255)\}$
- Masque des parois : $M_{\text{walls}} = \{(y, x) \mid I(y, x) = (255, 0, 0)\}$
- Masque des portes : $M_{\text{doors}} = \{(y, x) \mid I(y, x) = (0, 255, 0)\}$

Les pièces sont définies comme l'ensemble des composantes 4-connexes $\{R_1, \dots, R_N\}$ de $M_{\text{rooms}}$ ayant une surface $|R_i| \ge 50$ pixels (seuil géométrique éliminant les artéfacts de compression de tracé).
Chaque pièce $R_i$ possède :
- Une surface en pixels : $A(R_i) = |R_i|$
- Une boîte englobante : $\text{BBox}(R_i) = [ymin_i, xmin_i, ymax_i, xmax_i]$
- Une largeur et hauteur : $w_i = xmax_i - xmin_i$, $h_i = ymax_i - ymin_i$
- Un centroïde : $c_i = (\bar{x}_i, \bar{y}_i) = \left( \frac{1}{|R_i|} \sum_{(y, x) \in R_i} x, \; \frac{1}{|R_i|} \sum_{(y, x) \in R_i} y \right)$

---

## 2. Définitions des Relations Directionnelles

Pour deux pièces distinctes $R_A$ et $R_B$ de centroïdes $c_A = (cx_A, cy_A)$ et $c_B = (cx_B, cy_B)$, on pose :
$$\Delta x = cx_B - cx_A, \quad \Delta y = cy_B - cy_A$$
$$\bar{w} = \frac{w_A + w_B}{2}, \quad \bar{h} = \frac{h_A + h_B}{2}$$

### 2.1 `LEFT_OF(A, B)` et `RIGHT_OF(A, B)`
$R_A$ est dit **`LEFT_OF`** $R_B$ (et symétriquement $R_B$ est **`RIGHT_OF`** $R_A$) si et seulement si :
1. **Séparation horizontale stricte :** $\Delta x > 0$ ($c_A$ est à gauche de $c_B$).
2. **Dominance horizontale :** $|\Delta x| > |\Delta y|$ (l'axe est principalement horizontal, non vertical).
3. **Seuil d'écartement géométrique justifié :** $\Delta x \ge 0.4 \times \bar{w}$ (garantit que l'écart horizontal est significatif par rapport à la taille des pièces et ne résulte pas d'une infime variation d'alignement).
4. **Cohérence d'élévation :** L'écart vertical $|\Delta y| \le \max(h_A, h_B)$ (les pièces partagent une bande d'élévation commune).

### 2.2 `ABOVE(A, B)` et `BELOW(A, B)`
Dans le repère image matriciel (l'origine $(0, 0)$ est en haut à gauche, $y$ croît vers le bas) :
$R_A$ est dit **`ABOVE`** $R_B$ (et symétriquement $R_B$ est **`BELOW`** $R_A$) si et seulement si :
1. **Séparation verticale stricte :** $\Delta y > 0$ ($c_A$ est au-dessus de $c_B$ dans l'espace physique).
2. **Dominance verticale :** $|\Delta y| > |\Delta x|$.
3. **Seuil d'écartement géométrique justifié :** $\Delta y \ge 0.4 \times \bar{h}$.
4. **Cohérence latérale :** L'écart horizontal $|\Delta x| \le \max(w_A, w_B)$.

---

## 3. Définitions Topologiques : Connectivité et Adjacence

Soit l'opérateur de dilatation morphologique $\mathcal{D}_r(M)$ avec un élément structurant carré de rayon $r$ pixels :
$$\mathcal{D}_r(M) = \{p \in \mathbb{Z}^2 \mid \exists q \in M, \; \|p - q\|_\infty \le r\}$$

### 3.1 `CONNECTED_TO(A, B)` (Liaison par Porte)
Soit $\{D_1, \dots, D_M\}$ l'ensemble des composantes connexes du masque des portes $M_{\text{doors}}$.
Deux pièces $R_A$ et $R_B$ sont dites **`CONNECTED_TO`** s'il existe une porte $D_k$ telle que :
$$\mathcal{D}_2(D_k) \cap R_A \neq \emptyset \quad \text{ET} \quad \mathcal{D}_2(D_k) \cap R_B \neq \emptyset$$
Une porte physique relie directement l'espace $A$ à l'espace $B$ à travers le passage ouvert.

### 3.2 `NOT_CONNECTED_TO(A, B)` (Exemple Négatif Contrastif)
Deux pièces $R_A$ et $R_B$ sont dites **`NOT_CONNECTED_TO`** si :
$$\forall k \in \{1, \dots, M\}, \quad \neg \left( \mathcal{D}_2(D_k) \cap R_A \neq \emptyset \land \mathcal{D}_2(D_k) \cap R_B \neq \emptyset \right)$$
Cette relation négative formelle empêche le modèle d'apprendre un raccourci lexical selon lequel "toutes les pièces voisines sont connectées".

### 3.3 `ADJACENT_TO(A, B)` (Mitoyenneté Murale)
Deux pièces $R_A$ et $R_B$ sont dites **`ADJACENT_TO`** si elles partagent une cloison commune :
$$\mathcal{D}_3(R_A) \cap R_B \neq \emptyset$$
La dilatation de 3 pixels permet de franchir l'épaisseur de la cloison rouge (1 à 2 pixels) pour attester du contact mitoyen.

### 3.4 `NOT_ADJACENT_TO(A, B)` (Disjonction Spatiale)
Deux pièces sont dites **`NOT_ADJACENT_TO`** si $\mathcal{D}_3(R_A) \cap R_B = \emptyset$.

---

## 4. Définitions des Relations de Proximité et Extrémales

Soit la distance euclidienne de centroïdes :
$$d(c_A, c_B) = \sqrt{(cx_A - cx_B)^2 + (cy_A - cy_B)^2} \quad (\text{en pixels})$$

### 4.1 `NEAREST_TO(A, S)`
Soit $S = \{R_1, \dots, R_N\}$. La pièce $R_B \in S \setminus \{R_A\}$ est dite **`NEAREST_TO`** $R_A$ si :
$$R_B = \arg\min_{R \in S \setminus \{R_A\}} d(c_A, c(R))$$
La relation est valide si et seulement si l'argmin est unique (marge minimale de 2 pixels avec le deuxième plus proche pour lever toute ambiguïté).

### 4.2 `FARTHEST_FROM(A, S)`
La pièce $R_B \in S \setminus \{R_A\}$ est dite **`FARTHEST_FROM`** $R_A$ si :
$$R_B = \arg\max_{R \in S \setminus \{R_A\}} d(c_A, c(R))$$
avec une marge minimale de 2 pixels garantissant l'unicité.

### 4.3 `LARGEST_ROOM` et `SMALLEST_ROOM`
- $R_{\text{max}} = \arg\max_{R_i \in S} |R_i|$ (pièce de surface maximale).
- $R_{\text{min}} = \arg\min_{R_i \in S} |R_i|$ (pièce de surface minimale).

---

## 5. Représentation Graphique Formelle (`ROOM_GRAPH`)

Chaque plan d'étage $P$ est modélisé par un graphe topologique architectural non orienté :
$$G_P = (V_P, E_P, W_P)$$
- **Nœuds ($V_P$) :** Chaque nœud $v_i$ représente une pièce $R_i$, dotée de ses attributs géométriques $\{id, bbox, center, pixel\_area\}$.
- **Arêtes ($E_P$) :** Une arête $(v_i, v_j)$ existe si et seulement si $\text{CONNECTED\_TO}(R_i, R_j) = \text{TRUE}$.
- **Poids ($W_P$) :** Distance euclidienne $d(c_i, c_j)$ entre les centroïdes des pièces connectées.

### 5.1 Raisonnement Multi-Hop (Difficulté HARD)
Grâce à $G_P$, des tâches de raisonnement spatial complexe sont calculées de manière exacte :
- **Plus court chemin (Shortest Path Length) :** Nombre minimal de portes à traverser entre deux pièces distantes $R_i$ et $R_j$.
- **Accessibilité conditionnelle :** Existe-t-il un chemin entre $R_i$ et $R_j$ ne traversant pas un nœud de distribution donné $R_k$ ?
- **Nœud central de distribution (Circulation Hub) :** Le nœud $v^* = \arg\max_{v \in V} \text{deg}(v)$, correspondant à l'espace de circulation ou de séjour distribuant les autres pièces.
