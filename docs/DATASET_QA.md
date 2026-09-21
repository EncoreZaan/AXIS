# Assurance Qualité et Détection Anti-Hallucination (ARCHI-AI)

## 1. Philosophie du Système QA

Contrairement à des approches naïves basées sur des filtres regex bloquants (qui risqueraient de rejeter de vraies analyses d'architecture formulées de façon nuancée), ARCHI-AI met en place un **système de drapeaux (Flags)** et de statuts gradués :

- `PASS` : Validité schématique totale, intégrité d'image certifiée, prudence épistémique présente si des métriques sont abordées.
- `WARNING` : Points d'attention non critiques (ex: image de résolution basse mais lisible, question concise).
- `REVIEW` : Présence d'affirmations quantitatives péremptoires sans clause de réserve ("mesure exactement 3,20 m", "isolant R=6"). Doit être inspecté par un architecte humain avant tout export d'entraînement.
- `FAIL` : Erreur de syntaxe JSON, champ requis manquant, image absente ou fichier corrompu, réponse anormalement courte (<50 caractères).

---

## 2. Détection Anti-Hallucination et Prudence Épistémique

Un modèle VLM entraîné sur des images d'architecture a naturellement tendance à halluciner des données invisibles :
- Hauteur exacte sous plafond
- Épaisseur de paroi
- Marque d'un mobilier
- Performance acoustique ou thermique

Le validateur QA (`dataset_tools/validation/qa_validator.py`) inspecte :
1. Les motifs à risque (`HALLUCINATION_RISK_PATTERNS`).
2. Les motifs vertueux de prudence épistémique (`EPISTEMIC_AWARENESS_PATTERNS`) : expressions telles que `sans plan métré`, `ne peut être certifié`, `semble`, `sous réserve`.
3. Si un exemple contient une assertion métrique sans prudence épistémique et sans section `unknowns`, il est automatiquement basculé en statut **`REVIEW`** et exclu des splits de production tant qu'il n'a pas été corrigé.
