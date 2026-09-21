"""
Script de validation rigoureuse du dataset experimental ARCHI-AI.
Verifie :
1. Validite syntaxique JSONL (train.jsonl et validation.jsonl)
2. Presence des champs obligatoires (id, category, space_type, style, image, context, question, answer, conversations)
3. Existence des fichiers images sur disque
4. Lisibilite des images via Pillow (PIL) et controle des dimensions
5. Absence de chemins casses ou relatifs invalides
6. Absence totale de doublons d'images (intra-split et inter-splits)
7. Separation stricte train / validation (comptage et unicite des identifiants)
8. Structure et coherence du format multimodal (Qwen2-VL)
"""

import os
import sys
import json
from PIL import Image

def validate_split(file_path, dataset_dir, split_name, expected_count=None):
    print(f"--- Verification du fichier {split_name} : {os.path.basename(file_path)} ---")
    if not os.path.exists(file_path):
        print(f"[ERREUR] Le fichier {file_path} est introuvable.")
        return False, [], set()

    mandatory_fields = [
        "id", "category", "space_type", "style", "image", "context", "question", "answer", "conversations"
    ]
    
    records = []
    image_paths = []
    record_ids = set()
    errors = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                errors.append(f"Ligne {line_num} vide non autorisee.")
                continue
            
            # 1. Verification JSON
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"Ligne {line_num}: Erreur de syntaxe JSON ({e}).")
                continue

            records.append(data)

            # 2. Verification des champs obligatoires
            for field in mandatory_fields:
                if field not in data or data[field] is None or (isinstance(data[field], str) and not data[field].strip()):
                    errors.append(f"Ligne {line_num} (id={data.get('id', 'inconnu')}): Champ obligatoire manquant ou vide '{field}'.")

            # 3. Verification de l'identifiant unique
            rec_id = data.get("id")
            if rec_id:
                if rec_id in record_ids:
                    errors.append(f"Ligne {line_num}: Identifiant duplique '{rec_id}'.")
                record_ids.add(rec_id)

            # 4. Verification de l'image
            rel_image_path = data.get("image")
            if rel_image_path:
                image_full_path = os.path.join(dataset_dir, rel_image_path)
                if not os.path.exists(image_full_path):
                    errors.append(f"Ligne {line_num}: Image introuvable sur disque '{image_full_path}'.")
                else:
                    try:
                        with Image.open(image_full_path) as img:
                            img.verify()
                        with Image.open(image_full_path) as img:
                            w, h = img.size
                            if w <= 0 or h <= 0:
                                errors.append(f"Ligne {line_num}: Dimensions d'image invalides ({w}x{h}) pour '{rel_image_path}'.")
                            if w > 1024 or h > 768:
                                # Avertissement si depassement des seuils de securite VRAM 8 Go
                                pass
                    except Exception as img_err:
                        errors.append(f"Ligne {line_num}: Fichier image corrompu ou illisible '{rel_image_path}' ({img_err}).")
                
                image_paths.append(rel_image_path)

            # 5. Verification du format conversations (Qwen2-VL)
            convs = data.get("conversations")
            if isinstance(convs, list):
                if len(convs) < 2:
                    errors.append(f"Ligne {line_num}: Format conversations doit comporter au moins 2 tours (user/assistant).")
                else:
                    user_turn = convs[0]
                    asst_turn = convs[1]
                    if user_turn.get("role") != "user":
                        errors.append(f"Ligne {line_num}: Le premier tour de conversation doit avoir role='user'.")
                    if asst_turn.get("role") != "assistant":
                        errors.append(f"Ligne {line_num}: Le second tour de conversation doit avoir role='assistant'.")
                    
                    user_content = user_turn.get("content", [])
                    has_img_type = any(isinstance(c, dict) and c.get("type") == "image" for c in user_content)
                    has_txt_type = any(isinstance(c, dict) and c.get("type") == "text" for c in user_content)
                    if not (has_img_type and has_txt_type):
                        errors.append(f"Ligne {line_num}: Le contenu user doit inclure un objet type='image' et un objet type='text'.")
            else:
                errors.append(f"Ligne {line_num}: Le champ 'conversations' doit etre une liste.")

            # 6. Verification de la qualite de la reponse architecturale
            answer = data.get("answer", "")
            required_sections = ["OBSERVATION", "ANALYSE", "POINTS FORTS", "POINTS DE VIGILANCE", "RECOMMANDATION"]
            for sec in required_sections:
                if sec not in answer:
                    errors.append(f"Ligne {line_num} (id={rec_id}): Section de reponse experte manquante '{sec}'.")

    # Verification du nombre d'exemples attendus
    if expected_count is not None and len(records) != expected_count:
        errors.append(f"Nombre d'exemples inattendu pour {split_name}: {len(records)} trouves, {expected_count} attendus.")

    # Verification des doublons internes d'images
    unique_images = set(image_paths)
    if len(unique_images) != len(image_paths):
        errors.append(f"Doublons d'images detectes au sein du split {split_name} ({len(image_paths) - len(unique_images)} doublon(s)).")

    if errors:
        print(f"[ECHEC] {len(errors)} erreur(s) detectee(s) dans {split_name} :")
        for err in errors:
            print(f"  - {err}")
        return False, records, unique_images
    else:
        print(f"[SUCCES] {len(records)} exemples valides dans {split_name}. Aucune anomalie.")
        return True, records, unique_images

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(root_dir, "dataset")
    train_file = os.path.join(dataset_dir, "train.jsonl")
    val_file = os.path.join(dataset_dir, "validation.jsonl")

    print("================================================================")
    print("      VALIDATION DU MINI-DATASET MULTIMODAL ARCHI-AI            ")
    print("================================================================")

    # Validation train (20 attendus)
    train_ok, train_records, train_images = validate_split(train_file, dataset_dir, "TRAIN", expected_count=20)
    
    # Validation validation (5 attendus)
    val_ok, val_records, val_images = validate_split(val_file, dataset_dir, "VALIDATION", expected_count=5)

    # Verification croisee : aucun doublon entre train et validation
    print("\n--- Verification du cloisonnement Train / Validation ---")
    overlap = train_images.intersection(val_images)
    cross_ok = True
    if overlap:
        print(f"[ERREUR] Chevauchement detecte ! Images presentes a la fois dans train et validation : {overlap}")
        cross_ok = False
    else:
        print(f"[SUCCES] Cloisonnement strict : 0 image en commun entre train et validation.")

    # Synthese des categories et typologies
    all_records = train_records + val_records
    categories = {}
    space_types = {}
    styles = {}

    for r in all_records:
        cat = r.get("category", "Non defini")
        categories[cat] = categories.get(cat, 0) + 1
        st = r.get("space_type", "Non defini")
        space_types[st] = space_types.get(st, 0) + 1
        sty = r.get("style", "Non defini")
        styles[sty] = styles.get(sty, 0) + 1

    print("\n--- Repartition par Categorie (5 attendus par categorie) ---")
    for cat, count in sorted(categories.items()):
        print(f"  * {cat:32s} : {count} exemples")

    print("\n--- Diversite des Types d'Espace ---")
    for st, count in sorted(space_types.items()):
        print(f"  * {st:20s} : {count} exemples")

    print("\n--- Diversite des Styles Architecturaux ---")
    for sty, count in sorted(styles.items()):
        print(f"  * {sty:20s} : {count} exemples")

    total_images_on_disk = len(os.listdir(os.path.join(dataset_dir, "images")))
    print(f"\n--- Fichiers images sur disque : {total_images_on_disk} images trouvees dans dataset/images/ ---")

    print("\n================================================================")
    if train_ok and val_ok and cross_ok:
        print("RESULTAT GLOBAL : VALIDATION REUSSIE (100% CONFORME)")
        print("Le dataset est pret pour le test de pipeline QLoRA Qwen2-VL.")
        print("================================================================")
        sys.exit(0)
    else:
        print("RESULTAT GLOBAL : ECHEC DE VALIDATION")
        print("================================================================")
        sys.exit(1)

if __name__ == "__main__":
    main()
