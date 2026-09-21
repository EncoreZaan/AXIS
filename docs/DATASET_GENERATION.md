# Protocole de Génération et d'Ingestion Scalable (ARCHI-AI)

## 1. Objectif du Protocole

Ce guide définit les règles strictes pour passer de 25 exemples à 5 000, 10 000 et 50 000+ exemples sans introduire de pollution, d'hallucinations ou de doublons artificiels.

---

## 2. Invariants de Génération et d'Ingestion

1. **Pas de génération synthétique non vérifiée :** Tout exemple généré par LLM/VLM doit être pré-validé par le validateur QA avant d'être admis dans le Master Dataset.
2. **Attribution obligatoire de scène (`scene_id`) et projet (`project_name`) :** Essentiel pour éviter que plusieurs photos d'un même projet ne se retrouvent à la fois dans le train et dans la validation.
3. **Diversité des types de documents :** Ne pas se limiter à la photographie de salon contemporain ; intégrer systématiquement :
   - Plans 2D cotés
   - Coupes architecturales
   - Croquis d'intention
   - Renders 3D
   - Moodboards matériaux
4. **Équilibre des Learning Types :** Veiller à répartir les exemples entre observation pure, raisonnement sous contraintes, détection d'erreurs, critique et pédagogie.

---

## 3. Workflow d'Admission d'un Nouvel Exemple

```
[Nouvelle Image + Annotation]
            │
            ▼
[Calcul SHA-256 et pHash]  ──>  [Vérification Doublons / Collisions]
            │
            ▼
[Validation Pydantic / Schema]
            │
            ▼
[Contrôle Anti-Hallucination] ──> Statut = REVIEW si doute
            │
            ▼
[Insertion dans dataset/master/annotations/]
            │
            ▼
[Re-calcul des Splits & Détection de Leakage]
            │
            ▼
[Export vers Qwen2-VL Format]
```
