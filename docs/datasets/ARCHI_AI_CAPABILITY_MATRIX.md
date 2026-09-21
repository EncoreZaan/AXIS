# ARCHI-AI — Matrice des Capacités & Compétences Visées (`ARCHI_AI_CAPABILITY_MATRIX`)

## 1. Objectifs Opérationnels & Demandes Utilisateurs Réelles

Ce document établit la grille d'audit et de validation des **13 cas d'usage majeurs** formulés par les utilisateurs réels d'ARCHI-AI (étudiants, architectes d'intérieur, enseignants, prescripteurs).

Pour chaque cas d'usage, la matrice détaille :
- L'intitulé type de la demande utilisateur ;
- Le niveau de compétence actuellement mesuré (Baseline post-QLoRA 25 ex.) ;
- Le niveau cible requis pour un système expert de référence ;
- Les sources de données et modalités mobilisées ;
- Le mode de traitement (VLM, RAG, Tool, Hybride) ;
- Le statut de maturité opérationnelle.

---

## 2. Matrice Complète des 13 Capacités Cibles

| # | Capacité Métier | Demande Utilisateur Type | Niveau Actuel (Micro 25 ex.) | Niveau Cible (Expert ARCHI-AI) | Datasets & Sources Mobilisés | Mode de Traitement | Statut de Maturité |
|---|---|---|---|---|---|---|---|
| **01** | **Analyse Visuelle de Pièce** | *"Analyse cette pièce."* | **2.5 / 5** : Description correcte du mobilier principal et des ouvertures. | **4.8 / 5** : Diagnostic complet des volumes, hauteurs perçues, calepinage, points focaux et équilibre plein/vide. | `Structured3D`, `StructScan3D`, `IL3D` | `FINE-TUNE` | **En Production** (Extension 25k planifiée) |
| **02** | **Circulation & Flux sur Plan** | *"Analyse ce plan et explique-moi les problèmes de circulation."* | **2.0 / 5** : Repère les portes et pièces principales, mais rate les goulots d'étranglement. | **4.9 / 5** : Analyse des lignes de désir, croisements de flux, couloirs sombres, dégagements réglementaires et sas. | `ResPlan`, `MSD`, `CubiCasa5K`, `Space Syntax` | `COMBINAISON` *(VLM + Tool Graphes)* | **En Conception** (Jeu 2D prioritaire) |
| **03** | **Ergonomie Fonctionnelle** | *"Est-ce que cet aménagement semble fonctionnel ?"* | **1.8 / 5** : Commentaires génériques sur l'espace sans vérification des cotes d'usage. | **4.8 / 5** : Audit précis du triangle d'activité cuisine, débattements de portes de placard, cotes d'assise et passages de lit. | `CHOrD`, `Panero & Zelnik`, `Neufert` | `COMBINAISON` *(VLM + Tool Collisions)* | **En Conception** (Données anthropo prêtes) |
| **04** | **Palette de Matériaux & Parti Pris** | *"Quelle palette de matériaux serait cohérente avec ce parti pris ?"* | **2.2 / 5** : Suggère des matériaux basiques (bois, blanc, marbre) sans justification. | **4.7 / 5** : Recommandation de textures contrastées (mat/brillant, lisse/rugueux), essences réelles, finitions et calepinages cohérents. | `MatSynth`, `ambientCG`, `MMIS` | `FINE-TUNE` + `RAG` | **En Conception** (Base PBR prête) |
| **05** | **Analyse de la Lumière** | *"Analyse l'éclairage de ce projet."* | **2.0 / 5** : Constate si la photo est claire ou sombre. | **4.6 / 5** : Distinction apports naturels (orientation des baies) / artificiels, gradation d'ambiance, températures en Kelvin, éblouissement. | `Laval Photometric HDR`, `OpenRooms`, `RE2020` | `COMBINAISON` *(VLM + Tool FLJ)* | **À Acquérir** (HDR à préprocesser) |
| **06** | **Style & Signature Décorative** | *"Quels éléments caractérisent cette ambiance ?"* | **3.0 / 5** : Reconnaît les styles évidents (scandinave, moderne). | **4.9 / 5** : Identification fine parmi 40 styles (Japandi, Haussmannien, Wabi-Sabi, Art Déco), avec analyse des marqueurs et détails ornementaux. | `MMIS`, `The Met Open Access`, `Cooper Hewitt` | `FINE-TUNE` + `RAG` | **En Production** (Jeu MMIS audité) |
| **07** | **Critique de Studio d'Architecture** | *"Fais-moi une critique comme en studio."* | **1.5 / 5** : Trop poli, ne relève pas les incohérences majeures de composition. | **4.9 / 5** : Diagnostic incisif, rigoureux et constructif : hiérarchie des espaces, force du parti pris, points de friction et pistes d'arbitrage. | `ARCHI-AI Expert Curated (Studios & Jurys)` | `FINE-TUNE` | **En Conception** (Curations expertes) |
| **08** | **Pédagogie & Maïeutique** | *"Explique-moi pourquoi mon choix ne fonctionne pas."* | **2.0 / 5** : Donne la solution directement sans expliquer le principe architectural. | **4.8 / 5** : Reformulation didactique, questionnement guidé, illustration par contre-exemples et référence aux grands principes de composition. | `ARCHI-AI Socratic Dialogues`, `Design Pedagogy` | `FINE-TUNE` | **En Conception** (Templates CoT) |
| **09** | **Comparaison d'Options** | *"Compare ces deux propositions d'aménagement."* | **1.8 / 5** : Description séquentielle sans réelle mise en balance multicritère. | **4.7 / 5** : Tableau comparatif rigoureux : gain de surface utile, luminosité, fluidité de circulation, coût relatif et confort d'usage. | `Structured3D (Variantes)`, `IL3D Multiview` | `FINE-TUNE` | **En Conception** |
| **10** | **Analyse des Manques d'un Projet** | *"Qu'est-ce que j'ai oublié dans ce projet ?"* | **1.5 / 5** : Propose des objets décoratifs secondaires (plantes, coussins). | **4.8 / 5** : Détection des oublis critiques : rangement de l'entrée, gaine technique, retour de porte, radiateurs/convecteurs, prises de chevet, trappes. | `BIM/IFC Checklists`, `ARCHI-AI Technical Audit` | `RAG` + `FINE-TUNE` | **En Conception** |
| **11** | **Vérifications Techniques Constructives**| *"Quels points techniques dois-je vérifier ?"* | **1.2 / 5** : Alertes génériques sur les murs porteurs. | **4.9 / 5** : Check-list second œuvre : colonnes d'évacuation gravitaire, épaisseur des faux-plafonds pour gaines VMC, étanchéité douche, garde-corps. | `DTU 25.41 / 52.1`, `CCH`, `Fiches CSTB` | `RAG` + `TOOL` | **En Conception** (Corpus technique prêt) |
| **12** | **Cohérence Plan ↔ Rendu 3D** | *"Compare le plan avec le rendu et trouve les incohérences."* | **1.0 / 5** : Non supporté par la baseline historique (mono-image). | **4.6 / 5** : Confrontation point par point : mobilier absent, sens d'ouverture de porte inversé, position d'une fenêtre divergente, cloisons déplacées. | `Structured3D (Plan+Rendu alignés)`, `ResBIM` | `FINE-TUNE` *(Multi-images)* | **En Conception** (Schéma Qwen2-VL validé) |
| **13** | **Cohérence Globale Multimodale** | *"Voici mon plan, mon moodboard et mon rendu. Analyse la cohérence globale."* | **0.8 / 5** : Non supporté par la baseline historique. | **4.7 / 5** : Analyse holistique du projet : alignement entre le parti pris annoncé, les matières du moodboard, l'organisation du plan et le rendu final. | `Structured3D + MatSynth + Curated Moodboards` | `FINE-TUNE` *(Multi-images 3+)* | **En Conception** (Architecture prête) |

---

## 3. Synthèse de l'Évolution de Performance

```text
Score Moyen par Axe de Compétence (Échelle 1 à 5)

Axe 1 : Vision & Enveloppe       [■■■□□] 2.5 ──► [■■■■■] 4.8  (+92%)
Axe 2 : Plans 2D & Circulations   [■■□□□] 2.0 ──► [■■■■■] 4.9  (+145%)
Axe 3 : Ergonomie & Cotes         [■■□□□] 1.8 ──► [■■■■■] 4.8  (+166%)
Axe 4 : Matériaux & PBR           [■■□□□] 2.2 ──► [■■■■■] 4.7  (+113%)
Axe 5 : Lumière & Photométrie     [■■□□□] 2.0 ──► [■■■■■] 4.6  (+130%)
Axe 6 : Styles & Histoire         [■■■□□] 3.0 ──► [■■■■■] 4.9  (+63%)
Axe 7 : Critique de Studio        [■□□□□] 1.5 ──► [■■■■■] 4.9  (+226%)
Axe 8 : Pédagogie & Maïeutique    [■■□□□] 2.0 ──► [■■■■■] 4.8  (+140%)
Axe 9 : Technique & DTU           [■□□□□] 1.2 ──► [■■■■■] 4.9  (+308%)
Axe 10: Multimodal Plan+Rendu     [■□□□□] 1.0 ──► [■■■■■] 4.6  (+360%)
──────────────────────────────────────────────────────────────────────────
Moyenne Globale ARCHI-AI          [■■□□□] 1.9 ──► [■■■■■] 4.8  (+152%)
```

---

## 4. Critères de Validation pour le Déploiement

Le système ARCHI-AI sera déclaré apte au service dès lors que :
1. **Zéro hallucination normative :** 100% des citations d'articles PMR ou ERP proviennent du RAG certifié avec référence légale exacte.
2. **Exactitude dimensionnelle :** Tout jugement de non-conformité sur une cote (largeur de passage, hauteur d'assise) est validé par un calcul de l'outil déterministe.
3. **Score Benchmark global $\ge 4.5 / 5$ :** Sur le jeu de test indépendant et scellé de 1 000 exemples non vus.
