# Dataset Quality Audit V2 : ARCHI-AI (train.jsonl & validation.jsonl)

**Date** : 21 Septembre 2026  
**Auditeur** : Pipeline d'Assurance Qualité ARCHI-AI / AEON-RWKV  
**Périmètre audité** : 
- `ARCHI_AI/dataset/train.jsonl` (20 exemples réécrits)
- `ARCHI_AI/dataset/validation.jsonl` (5 exemples réécrits)
- 25 photographies réelles dans `ARCHI_AI/dataset/images/`

---

## 1. Synthèse Exécutive

À la suite de l'audit V1 ayant diagnostiqué un taux de désynchronisation de 100% entre les descriptions textuelles et les photographies réelles, une refonte intégrale des annotations des **25 exemples** a été réalisée en prenant l'image comme **unique source de vérité**.

* **Nombre total d'exemples audités** : 25 (20 Train, 5 Validation)
* **Images réelles vérifiées sur disque** : 25 / 25
* **Validité syntaxique JSONL** : 100% conforme (`validate_dataset.py`)
* **Chevauchement Train / Validation** : 0 doublon (cloisonnement strict vérifié)
* **Équilibre des catégories** : 5 exemples par catégorie (4 Train, 1 Validation)
* **Exemples corrigés et réalignés sur l'image** : **25 / 25 (100%)**
* **Hallucinations restantes ou affirmations incompatibles** : **0**
* **Dimensions ou cotes inventées** : **0** (interdiction stricte respectée)
* **Distinction épistémique (Observation / Interprétation / Inconnu)** : 100% respectée

### Verdict global : **READY**
Le dataset expérimental multimodal est désormais totalement purgé de ses hallucinations. Chaque réponse repose strictement sur ce qui est observable sur la photographie, explicite les interprétations architecturales en tant que telles et stipule clairement les limites du mesurable en l'absence de plan coté métré.

---

## 2. Conformité Structurelle et Normative

Le script `ARCHI_AI/validate_dataset.py` a été exécuté avec succès :
- **Syntaxe JSONL** : Validée sans aucune ligne vide ni corruption.
- **Champs obligatoires** : Présents sur les 25 enregistrements (`id`, `category`, `space_type`, `style`, `image`, `context`, `question`, `answer`, `conversations`).
- **Format multimodal Qwen2-VL** : Structure `conversations` à 2 tours respectée (`user` avec objet `image` et objet `text`, `assistant` avec objet `text`).
- **Structure de réponse professionnelle** : Respect systématique des 5 sections normées :
  1. `OBSERVATION` : Inventaire objectif des volumes, agencements et matières visibles.
  2. `ANALYSE` : Interprétation spatiale et lumineuse raisonnée.
  3. `POINTS FORTS` : Qualités architecturales et fonctionnelles observables.
  4. `POINTS DE VIGILANCE` : Limites de perception, contraintes d'usage et mention de l'absence de plan coté métré.
  5. `RECOMMANDATION` : Prescriptions constructives réalistes (avec structure causale Observation $\to$ Problème $\to$ Action $\to$ Effet pour la catégorie Amélioration).

---

## 3. Contrôle Détaillé des 25 Exemples Réalignés

Le tableau et les fiches ci-dessous documentent pour chaque exemple :
- Le problème initial identifié dans l'audit V1
- L'ancienne annotation hallucinée
- La nouvelle annotation ancrée dans l'image
- La justification de correction

### Tableau Récapitulatif

| ID | Split | Catégorie | Contenu Réel de l'Image | Statut V1 | Statut V2 |
| :---: | :---: | :--- | :--- | :---: | :---: |
| **archi_001** | Train | ANALYSE D'ESPACE | Salon contemporain, canapé droit cuir cognac, 2 fauteuils blancs, parquet clair, baie vitrée toute hauteur, 16 cadres | Erroné (sol & canapé) | **CONFORME** |
| **archi_002** | Train | ANALYSE D'ESPACE | Façade extérieure crépuscule, terrasse surélevée bois, grand eucalyptus intégré, pelouse, baies coulissantes | Désynchronisation totale | **CONFORME** |
| **archi_003** | Train | ANALYSE D'ESPACE | Salon scandi-bohème, canapé d'angle beige, table ronde bois, mur vert d'eau, déco éclectique (crâne, macramé, horloge) | Erreur morphologique | **CONFORME** |
| **archi_004** | Train | ANALYSE D'ESPACE | Mur blanc, petit canapé noir 2 places, commode vintage gris-bleu, lampadaire noir, ficus en panier, porte moulurée | Désynchronisation totale | **CONFORME** |
| **archi_005** | Val | ANALYSE D'ESPACE | Salon compact habité, canapé gris sous fenêtre, coin bureau avec chaise résille/iMac, buffet bibliothèque blanc, plantes | Hallucination combles | **CONFORME** |
| **archi_006** | Train | STYLE / MATÉRIAUX | Grand salon contemporain, canapé gris, poufs cuir cognac, lampadaire arc laiton géant, baie bandeau horizontale, plantes | Teintes & éléments faux | **CONFORME** |
| **archi_007** | Train | STYLE / MATÉRIAUX | Coin séjour, mur vert sauge, grand miroir circulaire, enfilade basse cannage bois clair, appliques vertes, fauteuil cuir | Désynchronisation totale | **CONFORME** |
| **archi_008** | Train | STYLE / MATÉRIAUX | Salle de bain, meuble double vasque gris, miroir rectangulaire bois rustique, douche vitrée métro, baignoire d'angle | Hallucination sanitaires | **CONFORME** |
| **archi_009** | Train | STYLE / MATÉRIAUX | Mur blanc lisse, composition décorative : étagères tiroirs bois, masque africain, affiche branches bleues, appareil photo | Désynchronisation totale | **CONFORME** |
| **archi_010** | Val | STYLE / MATÉRIAUX | Cuisine farmhouse chic blanche à shiplap, îlot gris clair, tabourets noirs, piano cuisson inox, crédence marbre, lustres sphériques | Discordance stylistique | **CONFORME** |
| **archi_011** | Train | ERGONOMIE / FLUX | Cadrage moyen cuisine, femme cuisinant cocotte fonte orange sur feux gaz îlot, citrons, colonnes fours inox | Inadéquation cadrage | **CONFORME** |
| **archi_012** | Train | ERGONOMIE / FLUX | Lounge / accueil coworking, fauteuils crapauds gris et sapin, canapé angle, grand lampadaire noir articulé, cloison vitrée bois | Désynchronisation totale | **CONFORME** |
| **archi_013** | Train | ERGONOMIE / FLUX | Vaste séjour cathédrale double hauteur, escalier monumental bois/blanc, mezzanine, 2 canapés face-à-face, cuisine au fond | Désynchronisation totale | **CONFORME** |
| **archi_014** | Train | ERGONOMIE / FLUX | Salon avec parquet chêne en chevrons, canapé velours bleu, fauteuil coque blanc, meuble TV bas linéaire, sol central nu | Désynchronisation totale | **CONFORME** |
| **archi_015** | Val | ERGONOMIE / FLUX | Coin bureau scandinave épuré, plateau clair sur tréteaux blancs réglables, grand écran monobloc sur réhausseur, fauteuil cuir gris | Désynchronisation totale | **CONFORME** |
| **archi_016** | Train | CRITIQUE DE PROJET | Coin lecture épuré, fauteuil jaune moutarde, lampadaire potence laiton brossé, tableau art abstrait géométrique (cercle noir) | Contradiction frontale | **CONFORME** |
| **archi_017** | Train | CRITIQUE DE PROJET | Chambre moderne lumineuse, lit capitonné gris, tableau mouton noir et blanc, chevet marbre/laiton, coin fauteuil gris foncé | Hallucination mansarde | **CONFORME** |
| **archi_018** | Train | CRITIQUE DE PROJET | Salle de bain moderne blanche, baignoire îlot ovale, grand meuble vasque suspendu à tiroirs blancs, fente vitrée verticale | Contradiction frontale | **CONFORME** |
| **archi_019** | Train | CRITIQUE DE PROJET | Terrasse villa contemporaine, piscine turquoise, dallage blanc, auvent béton, baies vitrées coulissantes, palmiers | Désynchronisation totale | **CONFORME** |
| **archi_020** | Val | CRITIQUE DE PROJET | Salon réception symétrique axiale, canapé clair, coussins bleu canard/géométriques, tableau abstrait floral, 2 fenêtres/lampes | Désynchronisation totale | **CONFORME** |
| **archi_021** | Train | AMÉLIORATION | Cuisine pro restaurant en coup de feu, chef cuisinier flambant poêle vive, bouteille vodka, piano inox, étagère haute | Désynchronisation totale | **CONFORME** |
| **archi_022** | Train | AMÉLIORATION | Salon vintage éclectique, mur vert canard, grille 6 cadres N&B, 2 têtes de cerf blanches, canapé cuir camel, lampadaire doré | Désynchronisation totale | **CONFORME** |
| **archi_023** | Train | AMÉLIORATION | Salle de bain spa tropical minéral, baignoire monolithique ovale sur lit de galets blancs, mur crépi gris, palmier, douche plain-pied | Inversion totale | **CONFORME** |
| **archi_024** | Train | AMÉLIORATION | Mur galerie dense, vingtaine de cadres graphiques (monstera, oiseau, dorures), 2 étagères cimaises (blanche et noire) | Désynchronisation totale | **CONFORME** |
| **archi_025** | Val | AMÉLIORATION | Grande pièce de vie attique, coin fauteuils/coussins turquoise devant vue panoramique lac/toits, cheminée centrale, moquette | Désynchronisation totale | **CONFORME** |

---

## 4. Fiches de Contrôle Individuelles

### `archi_001` (Train) - ANALYSE D'ESPACE
* **Problème V1** : L'ancienne annotation affirmait la présence d'un "canapé d'angle" et d'un "carrelage grand format clair".
* **Ancienne annotation** : « On observe un espace salon structuré par un canapé d'angle... Le sol est revêtu d'un carrelage grand format... »
* **Nouvelle annotation** : Décrit fidèlement le canapé droit en cuir marron cognac, les deux fauteuils bas blancs à structure tubulaire noire, la table basse circulaire en bois clair et le véritable parquet en bois clair sous le grand tapis.
* **Raison de la correction** : Alignement strict sur les mobiliers et revêtements visibles.

### `archi_002` (Train) - ANALYSE D'ESPACE
* **Problème V1** : Désynchronisation critique. Le texte décrivait une cuisine intérieure avec îlot et tabourets hauts, alors que l'image montre une vue extérieure de façade crépusculaire avec terrasse et jardin.
* **Ancienne annotation** : « La cuisine s'articule autour d'un linéaire mural pleine hauteur abritant l'électroménager encastré et d'un îlot central monolithique... »
* **Nouvelle annotation** : Analyse la transition spatiale entre l'architecture contemporaine à étage, la terrasse couverte surélevée en bois avec son garde-corps vitré, l'intégration paysagère de l'eucalyptus préservé et le jardin engazonné.
* **Raison de la correction** : Reconversion complète du sujet d'analyse pour correspondre à la vue architecturale extérieure réelle.

### `archi_003` (Train) - ANALYSE D'ESPACE
* **Problème V1** : Discordance morphologique. Le texte parlait d'un canapé droit sur pieds hauts et de tables basses gigognes.
* **Ancienne annotation** : « un canapé aux pieds surélevés, une table basse gigogne ronde... »
* **Nouvelle annotation** : Identifie le véritable canapé d'angle beige à méridienne droite, la table basse ronde unique en bois à double plateau, le fauteuil en cannage, le pouf tricoté et la composition murale bohème au mur vert sauge.
* **Raison de la correction** : Correction des formes, des assises et prise en compte de la décoration murale caractéristique.

### `archi_004` (Train) - ANALYSE D'ESPACE
* **Problème V1** : Désynchronisation critique. Le texte inventait un grand loft industriel avec verrières d'atelier, poteaux et poutres métalliques, alors que l'image montre une sobre vignette murale d'un petit salon d'appoint.
* **Ancienne annotation** : « vaste plateau sans cloisons pleines, rythmé par des éléments structurels apparents (poteaux, poutres, menuiseries en acier sombre)... »
* **Nouvelle annotation** : Analyse l'alignement contre paroi blanche du canapé compact deux places noir, de la commode vintage gris-bleu pâle à poignées ouvragées, du lampadaire noir articulé et de la plante en panier tressé près de la porte blanche.
* **Raison de la correction** : Suppression des éléments de loft inexistants et ancrage dans la composition sobre visible.

### `archi_005` (Validation) - ANALYSE D'ESPACE
* **Problème V1** : Hallucination de mansarde. Le texte décrivait des combles urbains sous rampants avec fenêtres de toit de type Velux, alors que l'image montre un salon/coin bureau habité avec plafond horizontal et fenêtre classique droite.
* **Ancienne annotation** : « L'espace présente une configuration compacte avec sous-pentes et fenêtres de toit... L'aménagement tire parti de la sous-pente... »
* **Nouvelle annotation** : Décrit le véritable agencement associant un canapé deux places gris chiné sous la fenêtre à stores, une table basse en bois galet, une bibliothèque murale blanche garnie de livres et de plantes, et un coin bureau avec ordinateur et fauteuil ergonomique.
* **Raison de la correction** : Remplacement des sous-pentes imaginaires par l'analyse réelle de la cohabitation entre détente et télétravail.

### `archi_006` (Train) - STYLE / MATÉRIAUX / AMBIANCE
* **Problème V1** : Erreurs de colorimétrie et omissions majeures. Le texte décrivait un salon Japandi monochrome écru avec une seule plante, ignorant le canapé gris, les poufs cognac, l'immense lampadaire arc en laiton et la fenêtre bandeau.
* **Ancienne annotation** : « On observe un mobilier bas aux lignes sobres, des teintes écrues... Une plante verte sobre apporte une note vivante ponctuelle. »
* **Nouvelle annotation** : Décrit avec précision le canapé gris texturé, la table basse en bois massif, les poufs et fauteuils en cuir cognac, le spectaculaire lampadaire arc en laiton brossé et la fente vitrée bandeau horizontale cadrant les arbres.
* **Raison de la correction** : Rétablissement de l'ambiance matérielle réelle et des éléments architecturaux forts.

### `archi_007` (Train) - STYLE / MATÉRIAUX / AMBIANCE
* **Problème V1** : Désynchronisation critique. Le texte décrivait une chambre parentale avec un lit bas et des chevets suspendus, alors que l'image est un coin séjour avec buffet cannage et miroir rond.
* **Ancienne annotation** : « La chambre met en scène un lit bas avec tête de lit intégrée en panneau de bois... encadré de chevets suspendus monoblocs... »
* **Nouvelle annotation** : Analyse la paroi vert sauge, le grand miroir circulaire noir, l'enfilade basse en bois clair à portes de cannage, les appliques vertes coordonnées, la plante tropicale en vannerie et le fauteuil lounge cuir/laiton.
* **Raison de la correction** : Restitution intégrale du sujet réel de l'image.

### `archi_008` (Train) - STYLE / MATÉRIAUX / AMBIANCE
* **Problème V1** : Hallucination d'équipements clés. Le texte affirmait la présence d'une baignoire îlot ovale et d'un miroir circulaire rétroéclairé, alors que l'image montre une baignoire encastrée d'angle et un grand miroir rectangulaire à cadre en bois rustique.
* **Ancienne annotation** : « Une baignoire îlot ovale en résine mate blanche... Un large miroir circulaire rétroéclairé complète le meuble vasque. »
* **Nouvelle annotation** : Décrit le meuble double vasque gris foncé à poignées noires, le grand miroir rectangulaire en bois texturé, la cabine de douche carrelée de métro blanc avec sol mosaïque hexagonale et la baignoire d'angle encastrée.
* **Raison de la correction** : Remplacement des sanitaires fictifs par les équipements réellement installés.

### `archi_009` (Train) - STYLE / MATÉRIAUX / AMBIANCE
* **Problème V1** : Désynchronisation critique. Le texte inventait un salon industriel complet avec mur de briques rouges, canapé en cuir vieilli et table sur roulettes de fonte, alors que l'image est un détail de mur blanc décoré d'objets éclectiques.
* **Ancienne annotation** : « Le décor met en avant une paroi en briques de terre cuite rouge vieillie, une table basse sur roulettes industrielles... un canapé en cuir vieilli couleur tabac... »
* **Nouvelle annotation** : Analyse la scénographie murale sur fond blanc lisse : étagères tiroirs en bois patiné, masque africain sculpté, céramique vert émeraude à soleil en relief, cadres d'art et appareil photo vintage suspendu.
* **Raison de la correction** : Recadrage complet sur la réalité de la composition décorative murale.

### `archi_010` (Validation) - STYLE / MATÉRIAUX / AMBIANCE
* **Problème V1** : Discordance stylistique. Le texte parlait de meubles laqués vert sauge ou gris bleuté à cadres shaker et de poignées coquilles, alors que l'image montre une cuisine blanche à lambris horizontal shiplap et poignées droites dorées.
* **Ancienne annotation** : « Les façades de meubles sont laquées dans une teinte vert sauge ou gris bleuté avec des moulures à cadre traditionnel type shaker... poignées coquilles... »
* **Nouvelle annotation** : Décrit fidèlement l'ambiance farmhouse contemporaine blanche : armoires à rainures shiplap, îlot gris clair à plan blanc, tabourets en cuir noir, piano de cuisson inox sous hotte bois grisé, crédence marbre veiné et suspensions sphériques en perles de verre.
* **Raison de la correction** : Alignement chromatique et matériel rigoureux sur la photographie.

### `archi_011` (Train) - ERGONOMIE / CIRCULATION
* **Problème V1** : Inadéquation de cadrage et affirmation de cotes invisibles. Le texte prétendait analyser l'ensemble des couloirs de circulation au sol d'une cuisine familiale à partir d'un cadrage moyen centré sur une personne en train de cuisiner.
* **Ancienne annotation** : « L'espace présente une configuration linéaire avec îlot face au mur technique. L'évier est intégré dans l'îlot... La distance métrique du couloir central doit impérativement faire au minimum 90 cm... »
* **Nouvelle annotation** : Se concentre sur l'ergonomie observable du poste de travail : disposition de la cocotte orange sur la table de cuisson gaz de l'îlot, rayon de préhension des ustensiles et ingrédients, hauteur de la colonne de fours inox, et stipule explicitement que les circulations au sol ne sont pas visibles dans ce cadrage.
* **Raison de la correction** : Respect du cadrage effectif sans extrapolation sur les zones masquées.

### `archi_012` (Train) - ERGONOMIE / CIRCULATION
* **Problème V1** : Désynchronisation critique. Le texte décrivait un bureau individuel fermé avec bureau droit, écran informatique et fauteuil réglable, alors que l'image montre un grand salon lounge / attente de coworking.
* **Ancienne annotation** : « Le bureau est composé d'un plateau droit en bois clair... L'écran est disposé face à l'utilisateur... »
* **Nouvelle annotation** : Analyse la circulation fluide dans l'espace lounge : fauteuils bas gris clair, fauteuils vert sapin, canapé modulaire d'angle bas, meuble bas à casiers et grand lampadaire noir articulé surplombant la zone vers la cloison vitrée à montants bois.
* **Raison de la correction** : Réécriture conforme à la fonction d'accueil collectif et aux assises réelles.

### `archi_013` (Train) - ERGONOMIE / CIRCULATION
* **Problème V1** : Désynchronisation totale grotesque. Une photographie d'un immense séjour cathédrale avec escalier monumental vers mezzanine était légendée et analysée comme une salle d'eau avec douche à l'italienne !
* **Ancienne annotation** : « Salle d'eau contemporaine avec douche à l'italienne... receveur de plain-pied extra-plat... »
* **Nouvelle annotation** : Analyse les circulations réelles : flux vertical majeur par l'escalier vers la coursive d'étage, flux horizontal continu vers la cuisine ouverte du fond, et dégagements latéraux amples autour des deux grands canapés face-à-face.
* **Raison de la correction** : Élimination de l'aberration sémantique et analyse architecturale du volume double hauteur.

### `archi_014` (Train) - ERGONOMIE / CIRCULATION
* **Problème V1** : Désynchronisation critique. Le texte inventait une table de repas compacte avec chaises ajourées pour petit espace, alors que l'image montre un salon spacieux avec parquet en chevrons, canapé bleu et meuble TV bas.
* **Ancienne annotation** : « Petit espace repas avec table compacte et chaises ajourées... recul suffisant pour reculer les sièges... »
* **Nouvelle annotation** : Met en avant le parti-pris de libération totale du centre du salon, la mise en valeur de la continuité du parquet en chevrons, l'implantation périphérique du canapé bleu, du fauteuil coque blanc et du linéaire TV blanc.
* **Raison de la correction** : Suppression de la table imaginaire et analyse du flux central dégagé.

### `archi_015` (Validation) - ERGONOMIE / CIRCULATION
* **Problème V1** : Hallucination de typologie. Le texte décrivait un atelier de créatif avec un établi lourd en bois massif, du matériel d'échantillonnage et des étagères métalliques pour charges lourdes, alors que l'image montre un coin bureau scandinave épuré avec tréteaux blancs et iMac.
* **Ancienne annotation** : « Un large établi ou plan de travail en bois épais occupe le centre... étagères métalliques murales... matériel d'échantillonnage... »
* **Nouvelle annotation** : Analyse l'ergonomie posturale du poste informatique réel : écran tout-en-un surélevé sur socle, clavier compact et souris sur sous-main noir, tréteaux en bois blanc réglables avec étagère basse, fauteuil de bureau pivotant en cuir gris à roulettes et fenêtre latérale.
* **Raison de la correction** : Ancrage dans la réalité du poste de télétravail scandinave minimaliste.

### `archi_016` (Train) - CRITIQUE DE PROJET
* **Problème V1** : Contradiction frontale. Le texte affirmait que le mur était désespérément nu et recommandait d'ajouter un tableau d'art abstrait, alors qu'un grand tableau d'art abstrait géométrique (cercle noir) trône déjà en plein centre du mur derrière le fauteuil !
* **Ancienne annotation** : « Le mur blanc arrière souffre d'un vide trop important... Recommandation : accrocher un grand tableau d'art abstrait pour animer la paroi... »
* **Nouvelle annotation** : Formule une critique étayée sur la composition réellement présente : impact du fauteuil jaune moutarde face au tableau abstrait géométrique et au lampadaire potence en laiton, réserve sur l'encombrement de la sellette en marbre par un grand vase de fleurs et prescription de déplacer le vase.
* **Raison de la correction** : Élimination de la contradiction visuelle flagrante.

### `archi_017` (Train) - CRITIQUE DE PROJET
* **Problème V1** : Hallucination de mansarde et faux problème de sécurité. Le texte inventait une chambre sous mansarde avec des suspensions tombantes dangereuses créant des risques de choc de tête, alors que le plafond est parfaitement plat et les luminaires sont des lampes posées sur tables de chevet.
* **Ancienne annotation** : « Chambre sous combles avec suspensions tombant très bas au-dessus des chevets... risque de choc à la tête lors du lever nocturne... »
* **Nouvelle annotation** : Analyse la chambre contemporaine réelle aux tons neutres : lit capitonné gris, tableau de mouton au mur, chevet laiton et coin fauteuil d'appoint gris sous la fenêtre avec plafonnier affleurant, critique de l'ambiance pouvant sembler trop neutre et suggestion de textiles chauds.
* **Raison de la correction** : Suppression de la fausse alerte de sécurité et critique justifiée des matières.

### `archi_018` (Train) - CRITIQUE DE PROJET
* **Problème V1** : Contradiction frontale. Le texte critiquait l'absence totale de meuble et de rangement dans une salle de bain en béton ciré, alors qu'un imposant meuble sous-vasque suspendu blanc avec deux grands tiroirs occupe tout le premier plan !
* **Ancienne annotation** : « Salle de bain ultra-dépouillée en béton ciré dépourvue de tout meuble ou rangement... impossibilité de ranger les produits courants... »
* **Nouvelle annotation** : Reconnaît le meuble sous-vasque suspendu à tiroirs blancs intégrés, la vasque ovale, la baignoire îlot avec mitigeur encastré et la fente vitrée verticale, critique l'absence de paroi de douche dédiée dans le champ de vision et la glissance potentielle du carrelage gris.
* **Raison de la correction** : Correction de l'erreur factuelle sur la présence des rangements.

### `archi_019` (Train) - CRITIQUE DE PROJET
* **Problème V1** : Désynchronisation critique. Une prise de vue extérieure de villa contemporaine avec piscine turquoise et terrasse dallée sous ciel bleu était analysée comme un intérieur cathédrale souffrant d'écho et de réverbération phonique nécessitant un tapis !
* **Ancienne annotation** : « Grand volume intérieur sous verrière souffrant d'une réverbération acoustique intolérable... Recommandation : poser un grand tapis 3x4m... »
* **Nouvelle annotation** : Critique architecturale de l'espace extérieur : conception bioclimatique de l'auvent en béton protégeant les baies coulissantes, dialogue visuel entre le dallage clair et le plan d'eau turquoise, vigilance sur l'éblouissement solaire et contrôle de la classe antidérapante en bord de bassin.
* **Raison de la correction** : Remplacement de l'analyse acoustique intérieure absurde par une critique architecturale extérieure bioclimatique et sécuritaire.

### `archi_020` (Validation) - CRITIQUE DE PROJET
* **Problème V1** : Désynchronisation critique. Le texte décrivait une chambre de maître classique avec un lit imposant à montants et de lourdes draperies sombres, alors que l'image montre un salon de réception ordonné aux accents bleu canard et turquoise.
* **Ancienne annotation** : « Chambre de maître classique avec lit imposant à montants et boiseries peintes... massivité du mobilier qui sature la chambre... »
* **Nouvelle annotation** : Évalue de manière critique la stricte symétrie axiale du salon de réception : canapé clair centré sous un tableau floral turquoise, flanqué de deux fenêtres et deux tables d'appoint identiques avec lampes boules en verre, recommandation de briser la gémellité pour donner plus de naturel.
* **Raison de la correction** : Remplacement du mobilier de chambre fictif par l'analyse critique de la symétrie du salon.

### `archi_021` (Train) - PROPOSITION D'AMÉLIORATION
* **Problème V1** : Désynchronisation totale grotesque. Une scène dynamique de coup de feu dans un restaurant avec un chef cuisinier flambant une poêle avec des flammes vives était légendée comme une cuisine résidentielle zen avec îlot en bois clair et tabourets scandinaves !
* **Ancienne annotation** : « Cuisine résidentielle contemporaine avec îlot en chêne clair et plan en marbre blanc... »
* **Nouvelle annotation** : Structure causale stricte (Observation $\to$ Problème $\to$ Action $\to$ Effet) sur le poste de travail chaud professionnel : sécurisation de la manipulation d'alcool inflammable au-dessus des brûleurs (doseur inox déporté) et vérification du système d'extraction des fumées de flambage (hotte compensée et filtres chocs).
* **Raison de la correction** : Prise en compte de la scène réelle de cuisine professionnelle et conformité aux règles de sécurité incendie.

### `archi_022` (Train) - PROPOSITION D'AMÉLIORATION
* **Problème V1** : Désynchronisation critique. Le texte décrivait une chambre Japandi monacale avec sommier bas au sol, alors que l'image est un salon rétro-chic avec mur vert canard, trophées cerfs et canapé en cuir cognac.
* **Ancienne annotation** : « Chambre d'inspiration Japandi au sol minéral dépouillé et matelas bas posé au sol... »
* **Nouvelle annotation** : Structure causale proposant d'aérer le côté droit du salon (qui concentre fauteuil noir, table d'appoint, lampadaire doré et cache-pot haut) en déplaçant la plante, et d'ajouter un rétroéclairage indirect chaud sur le mur vert pour magnifier la galerie photo sans assombrir la pièce le soir.
* **Raison de la correction** : Propositions directement connectées aux déséquilibres de masse et d'éclairage observables.

### `archi_023` (Train) - PROPOSITION D'AMÉLIORATION
* **Problème V1** : Inversion critique. Le texte décrivait une salle de bain froide et clinique carrelée de blanc à réchauffer d'urgence, alors que l'image est déjà un spa tropical somptueux avec baignoire en pierre sur lit de galets de rivière blancs, mur crépi minéral et palmier vivant !
* **Ancienne annotation** : « Salle de bain carrelée de blanc froid façon hôpital... Recommandation : ajouter du bois et des plantes pour réchauffer... »
* **Nouvelle annotation** : Structure causale ciblée sur les vrais enjeux techniques de ce spa minéral : hygiène du lit de galets sous la baignoire (bac étanche drainé ou grille amovible pour éviter la stagnation d'eau savonneuse) et insertion d'une niche étanche dans la zone de douche pour supprimer les flacons au sol.
* **Raison de la correction** : Élimination de l'inversion et formulation de solutions d'usage expertes adaptées au luxe minéral de la pièce.

### `archi_024` (Train) - PROPOSITION D'AMÉLIORATION
* **Problème V1** : Désynchronisation critique. Le texte inventait un bureau bibliothèque toute hauteur avec un grand bureau de travail et des goulottes pour câbles informatiques, alors que l'image est un cadrage serré sur un mur galerie couvert de cadres d'art graphique.
* **Ancienne annotation** : « Bureau bibliothèque toute hauteur avec grande table de travail en chêne et passage de câbles... »
* **Nouvelle annotation** : Structure causale dédiée à la restructuration du mur galerie dense : régularisation des espacements entre cadres pour désaturer la lecture visuelle, allègement des deux cimaises et installation d'un rail de spots orientables à haut IRC pour valoriser les dorures et motifs botaniques.
* **Raison de la correction** : Alignement rigoureux sur le mur galerie observable.

### `archi_025` (Validation) - PROPOSITION D'AMÉLIORATION
* **Problème V1** : Désynchronisation critique. Le texte décrivait un petit studio urbain encombré de 35 m2 et proposait un meuble TV suspendu ultra-fin, alors que l'image montre une vaste pièce de vie lumineuse en attique avec panorama sur lac et cheminée centrale.
* **Ancienne annotation** : « Petit séjour d'appartement compact de 35 m2 manquant d'espace... remplacer le meuble TV posé au sol par un meuble suspendu de 30 cm... »
* **Nouvelle annotation** : Structure causale adaptée au volume généreux : remplacement de la moquette uniforme peu pratique sous la table à manger par un sol dur pérenne délimité par des tapis de zone, et réorientation du coin fauteuils vitré (assises pivotantes) pour valoriser simultanément la cheminée et la vue panoramique extérieure.
* **Raison de la correction** : Propositions adaptées aux vraies dimensions et qualités de la pièce de vie.

---

## 5. Bilan Qualité et Recommandation d'Étape

### Statistiques de Conformité :
- **Taux de conformité factuelle image $\leftrightarrow$ texte** : **100% (25/25)**
- **Hallucinations d'éléments d'aménagement** : **0**
- **Inventions de dimensions / cotes métriques** : **0**
- **Respect du protocole épistémique (Observation / Interprétation / Inconnu)** : **100%**
- **Validation technique automatique (`validate_dataset.py`)** : **PASS**

### Décision finale : **READY**

Le dataset `ARCHI_AI` est désormais rigoureusement aligné avec les pixels des photographies. Les gradients lors de l'entraînement multimodal viendront renforcer la capacité du modèle à analyser factuellement les scènes architecturales plutôt qu'à halluciner des templates prédéfinis.

**RAPPEL STRICT** : Conformément aux consignes, aucun entraînement, aucun fine-tuning et aucun script de backward n'ont été exécutés. La décision de procéder à l'entraînement relève désormais de la validation humaine.
