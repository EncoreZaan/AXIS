"""
Script de creation et telechargement du mini-dataset experimental ARCHI-AI.
Gere le telechargement securise des 25 images Unsplash (licence libre),
l'optimisation de resolution (capping <= 1024x768 pour compatibilite VRAM 8 Go),
et la generation de train.jsonl (20) et validation.jsonl (5).
"""

import os
import io
import json
import urllib.request
from PIL import Image

DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")
IMAGES_DIR = os.path.join(DATASET_DIR, "images")

# Definition des 25 exemples avec annotations architecturales rigoureuses
DATASET_EXAMPLES = [
    # =========================================================================
    # CATEGORIE 1 : ANALYSE D'ESPACE (5 exemples)
    # =========================================================================
    {
        "id": "archi_001",
        "category": "ANALYSE D'ESPACE",
        "split": "train",
        "space_type": "salon",
        "style": "contemporain",
        "unsplash_id": "photo-1600210492486-724fe5c67fb0",
        "image": "images/archi_001.jpg",
        "context": "Pièce de vie principale d'une maison contemporaine individuelle, orientée vers une baie vitrée donnant sur l'extérieur.",
        "question": "En tant qu'architecte d'intérieur, réalisez une analyse spatiale complète de cette pièce de vie en précisant l'organisation des zones et la gestion des flux.",
        "answer": (
            "OBSERVATION\n"
            "La pièce présente un grand volume traversant avec une généreuse hauteur sous plafond et de larges ouvertures vitrées. "
            "On observe un espace salon structuré par un canapé d'angle posé sur un grand tapis clair, une table basse centrale basse et un meuble bas linéaire. "
            "Le sol est revêtu d'un carrelage grand format de teinte neutre claire. La transition vers l'extérieur s'effectue sans rupture de niveau apparente.\n\n"
            "ANALYSE\n"
            "L'organisation spatiale repose sur un plan ouvert où les limites entre intérieur et extérieur sont visuellement gommées par les baies vitrées. "
            "Le tapis sert d'élément d'ancrage territorial pour délimiter la zone de repos et de conversation au sein du grand volume sans nécessiter de cloisonnement physique. "
            "La lumière naturelle pénètre en profondeur et crée une hiérarchie lumineuse mettant en valeur la zone de séjour.\n\n"
            "POINTS FORTS\n"
            "- Continuité visuelle fluide vers l'extérieur qui amplifie la sensation de volume.\n"
            "- Délimitation efficace du coin salon grâce au tapis et à l'orientation du mobilier.\n"
            "- Palette chromatique sobre favorisant la sérénité et la clarté spatiale.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Risque de réverbération acoustique élevé en raison de la prédominance de surfaces dures et vitrées.\n"
            "- Les dimensions exactes et dégagements au sol ne peuvent être garantis sans plan coté métré.\n"
            "- L'exposition directe aux baies vitrées peut engendrer des surchauffes estivales ou des reflets sur les écrans.\n\n"
            "RECOMMANDATION\n"
            "Intégrer des éléments d'absorption acoustique (rideaux en lin lourd ou velours, panneaux muraux acoustiques en tasseaux de bois sur feutre) "
            "et prévoir des stores d'occultation ou de filtration solaire pour maîtriser le confort thermique et l'éblouissement."
        )
    },
    {
        "id": "archi_002",
        "category": "ANALYSE D'ESPACE",
        "split": "train",
        "space_type": "cuisine",
        "style": "contemporain",
        "unsplash_id": "photo-1600585154340-be6161a56a0c",
        "image": "images/archi_002.jpg",
        "context": "Espace cuisine ouvert sur séjour dans une villa contemporaine, intégrant un îlot central multifonction.",
        "question": "Analysez l'agencement spatial de cette cuisine ouverte et la relation qu'elle entretient avec le reste de l'habitat.",
        "answer": (
            "OBSERVATION\n"
            "La cuisine s'articule autour d'un linéaire mural pleine hauteur abritant l'électroménager encastré et d'un îlot central monolithique. "
            "L'îlot intègre à la fois une surface de préparation et un espace repas rapide / comptoir avec tabourets hauts. "
            "Le rétroéclairage linéaire sous les meubles et des suspensions suspendues au-dessus de l'îlot scandent le volume.\n\n"
            "ANALYSE\n"
            "L'îlot central agit comme un filtre architectural : il sépare subtilement la circulation technique de la cuisine de l'espace de vie tout en maintenant la convivialité. "
            "L'implantation murale pleine hauteur maximise la capacité de rangement verticale sans empiéter sur l'emprise au sol centrale.\n\n"
            "POINTS FORTS\n"
            "- Zonage fonctionnel clair entre zone de stockage/préparation et zone de convivialité.\n"
            "- Dégagement visuel ouvert vers la pièce à vivre et l'extérieur.\n"
            "- Éclairage zoné efficace combinant lumière fonctionnelle directe et ambiance générale.\n\n"
            "POINTS DE VIGILANCE\n"
            "- L'absence de plan métré interdit d'affirmer si le recul autour de l'îlot respecte strictement les 90 à 100 cm réglementaires pour le croisement de deux personnes.\n"
            "- La hotte ou le système d'aspiration de l'îlot doit être performant pour éviter la diffusion des odeurs vers le séjour.\n\n"
            "RECOMMANDATION\n"
            "Vérifier sur plan d'exécution que les largeurs de passage autour de l'îlot permettent l'ouverture simultanée du lave-vaisselle et des tiroirs opposés."
        )
    },
    {
        "id": "archi_003",
        "category": "ANALYSE D'ESPACE",
        "split": "train",
        "space_type": "salon",
        "style": "scandinave",
        "unsplash_id": "photo-1616486338812-3dadae4b4ace",
        "image": "images/archi_003.jpg",
        "context": "Séjour d'un appartement lumineux avec parquet en chêne clair et mobilier d'inspiration nordique.",
        "question": "Procédez à une analyse de l'organisation spatiale et de la volumétrie de ce salon scandinave.",
        "answer": (
            "OBSERVATION\n"
            "L'espace est structuré de manière aérée avec un canapé aux pieds surélevés, une table basse gigogne ronde, un fauteuil d'appoint et des étagères murales légères. "
            "Le sol est un parquet bois clair aux lames orientées dans le sens de la lumière. Les murs sont peints dans une nuance blanc cassé mat.\n\n"
            "ANALYSE\n"
            "Le mobilier sur pieds fins décolle les masses du sol, augmentant la surface visible du plancher et donnant une impression de légèreté spatiale. "
            "L'orientation des lames de parquet guide le regard vers la source principale de lumière, amplifiant la profondeur de la pièce.\n\n"
            "POINTS FORTS\n"
            "- Excellente sensation de respiration visuelle grâce au choix de mobiliers aériens.\n"
            "- Harmonie des proportions entre le gabarit des assises et la surface au sol observable.\n"
            "- Circulation libre sans entrave dans la zone centrale.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Les cotes exactes de passage ne peuvent être validées que sur relevé d'état des lieux.\n"
            "- Faible présence de rangements fermés, ce qui peut poser des défis d'encombrement au quotidien.\n\n"
            "RECOMMANDATION\n"
            "Compléter par un meuble bas fermé en enfilade basse pour dissimuler les objets du quotidien sans obturer le champ de vision horizontal."
        )
    },
    {
        "id": "archi_004",
        "category": "ANALYSE D'ESPACE",
        "split": "train",
        "space_type": "espace ouvert",
        "style": "industriel",
        "unsplash_id": "photo-1513694203232-719a280e022f",
        "image": "images/archi_004.jpg",
        "context": "Loft réhabilité dans un ancien bâtiment industriel, caractérisé par un plan ouvert et de hautes fenêtres métalliques.",
        "question": "Comment l'espace de ce loft industriel est-il structuré pour concilier grand volume ouvert et sous-espaces fonctionnels ?",
        "answer": (
            "OBSERVATION\n"
            "On constate un vaste plateau sans cloisons pleines, rythmé par des éléments structurels apparents (poteaux, poutres, menuiseries en acier sombre). "
            "Les différentes fonctions (séjour, travail, repas) sont disposées par îlots distincts sur la surface de sol continue.\n\n"
            "ANALYSE\n"
            "La structuration ne recourt pas à des murs mais à un zonage par le mobilier et les tapis. "
            "La hauteur sous plafond remarquable crée un volume d'air important ; les lignes horizontales des meubles bas viennent contrebalancer la verticalité prononcée des verrières d'atelier.\n\n"
            "POINTS FORTS\n"
            "- Clarté et luminosité exceptionnelle offertes par les grandes baies industrielles.\n"
            "- Grande flexibilité d'usage permise par l'absence de refends intérieurs porteurs.\n"
            "- Rythme architectural affirmé par la trame des poutres.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Difficulté de gestion thermique (stratification de l'air chaud vers le haut) et phonique dans un tel volume.\n"
            "- Sans échelle métrique fournie, l'éloignement réel entre les pôles fonctionnels reste une estimation visuelle.\n\n"
            "RECOMMANDATION\n"
            "Créer des micro-zones plus intimes à l'aide de verrières intérieures coulissantes ou de claustras ajourés permettant de moduler l'espace sans perdre la continuité visuelle."
        )
    },
    {
        "id": "archi_005",
        "category": "ANALYSE D'ESPACE",
        "split": "validation",
        "space_type": "petit espace",
        "style": "contemporain",
        "unsplash_id": "photo-1502672260266-1c1ef2d93688",
        "image": "images/archi_005.jpg",
        "context": "Studio urbain sous les toits, combinant salon, coin bureau et zone de repos dans un gabarit compact.",
        "question": "Analysez la gestion des contraintes spatiales et volumétriques dans ce petit espace aménagé.",
        "answer": (
            "OBSERVATION\n"
            "L'espace présente une configuration compacte avec sous-pentes et fenêtres de toit. "
            "On identifie un canapé placé sous la pente, une table basse légère, un coin repos en retrait et un parquet ancien clair. "
            "Les teintes blanches dominent les parois verticales et la toiture rampante.\n\n"
            "ANALYSE\n"
            "L'aménagement tire parti de la sous-pente en y logeant les assises et les éléments bas, réservant la hauteur maximale sous faîtage aux cheminements de passage. "
            "Le traitement monochrome blanc maximise la réverbération de la lumière naturelle provenant du zénith.\n\n"
            "POINTS FORTS\n"
            "- Exploitation judicieuse des zones de faible hauteur pour les fonctions sédentaires (assise, détente).\n"
            "- Forte sensation de clarté malgré le volume restreint.\n"
            "- Mobilier aux lignes basses préservant le sentiment d'espace.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Hauteur d'échappée sous plafond à contrôler précisément pour éviter les chocs de tête au lever du canapé.\n"
            "- Les dimensions utiles au sol ne peuvent être calculées sans coupe d'architecture cotée.\n\n"
            "RECOMMANDATION\n"
            "Exploiter les parties les plus basses du rampant (moins de 1m80) pour insérer des caissons de rangements fermés sur mesure sur toute la longueur."
        )
    },

    # =========================================================================
    # CATEGORIE 2 : STYLE / MATERIAUX / AMBIANCE (5 exemples)
    # =========================================================================
    {
        "id": "archi_006",
        "category": "STYLE / MATERIAUX / AMBIANCE",
        "split": "train",
        "space_type": "salon",
        "style": "Japandi",
        "unsplash_id": "photo-1618221195710-dd6b41faaea6",
        "image": "images/archi_006.jpg",
        "context": "Salon conçu selon les principes du Japandi, fusionnant minimalisme japonais et chaleur scandinave.",
        "question": "Identifiez le style décoratif, détaillez la palette de matériaux et analysez l'ambiance lumineuse de cet intérieur.",
        "answer": (
            "OBSERVATION\n"
            "On observe un mobilier bas aux lignes sobres, des teintes écrues, du bois de chêne naturel et des éléments en céramique artisanale. "
            "Les parois présentent une texture minérale mate rappelant l'enduit à la chaux. Une plante verte sobre apporte une note vivante ponctuelle. "
            "La lumière naturelle diffuse pénètre latéralement de façon douce et feutrée.\n\n"
            "ANALYSE\n"
            "Le style correspond au courant Japandi, associant la simplicité formelle scandinave à la philosophie wabi-sabi japonaise qui célèbre les textures organiques et l'imperfection naturelle. "
            "La palette chromatique est volontairement restreinte à des tons sable, beige et bois brut pour éliminer toute distraction visuelle.\n\n"
            "POINTS FORTS\n"
            "- Grande cohérence tactile et matérielle invitant au calme et au repos mental.\n"
            "- Richesse texturale des enduits mats qui accrochent la lumière sans éblouir.\n"
            "- Équilibre remarquable entre minimalisme et chaleur sensorielle.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Fragilité des enduits minéraux clairs face aux taches ou frottements du quotidien.\n"
            "- L'ambiance peut sembler trop austère si l'éclairage artificiel nocturne n'est pas conçu avec plusieurs points chauds (2700K).\n\n"
            "RECOMMANDATION\n"
            "Prévoir un éclairage d'appoint chaleureux au niveau du sol (lampes en papier washi ou diffuseurs en lin) pour prolonger cette atmosphère enveloppante en soirée."
        )
    },
    {
        "id": "archi_007",
        "category": "STYLE / MATERIAUX / AMBIANCE",
        "split": "train",
        "space_type": "chambre",
        "style": "minimaliste",
        "unsplash_id": "photo-1616046229478-9901c5536a45",
        "image": "images/archi_007.jpg",
        "context": "Chambre parentale contemporaine minimaliste privilégiant les lignes épurées et les matériaux nobles.",
        "question": "Décrivez les choix de matériaux, l'harmonie des finitions et le traitement de la lumière dans cette chambre.",
        "answer": (
            "OBSERVATION\n"
            "La chambre met en scène un lit bas avec tête de lit intégrée en panneau de bois ou tissu tendu, encadré de chevets suspendus monoblocs. "
            "Le linge de lit présente des fibres naturelles (lin froissé, coton lavé) dans des teintes taupe et grège. "
            "Un ruban LED dissimulé fournit un rétroéclairage rasant sur la paroi murale.\n\n"
            "ANALYSE\n"
            "L'espace repose sur un minimalisme chaleureux (warm minimalism). L'absence de poignées visibles et l'intégration des luminaires "
            "dans l'architecture du mobilier épurent le champ visuel pour favoriser le repos. "
            "Le rétroéclairage rasant souligne le grain de la paroi et confère une légèreté flottante à la tête de lit.\n\n"
            "POINTS FORTS\n"
            "- Éclairage indirect doux parfaitement adapté à la fonction repos.\n"
            "- Choix de textiles naturels respirants offrant du confort sensoriel.\n"
            "- Lignes horizontales épurées qui élargissent visuellement la pièce.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Les dimensions exactes du couchage (160 ou 180 cm) et des dégagements latéraux nécessitent un relevé sur site.\n"
            "- Nécessité d'assurer une maintenance aisée des systèmes LED encastrés.\n\n"
            "RECOMMANDATION\n"
            "Ajouter des liseuses orientables à faisceau étroit pour la lecture nocturne individuelle sans altérer l'ambiance tamisée globale."
        )
    },
    {
        "id": "archi_008",
        "category": "STYLE / MATERIAUX / AMBIANCE",
        "split": "train",
        "space_type": "salle de bain",
        "style": "contemporain",
        "unsplash_id": "photo-1584622650111-993a426fbf0a",
        "image": "images/archi_008.jpg",
        "context": "Salle de bain contemporaine haut de gamme avec baignoire îlot et finitions minérales.",
        "question": "Analysez l'esthétique, le mariage des matériaux et l'ambiance lumineuse de cette salle de bain contemporaine.",
        "answer": (
            "OBSERVATION\n"
            "Une baignoire îlot ovale en résine mate blanche est mise en scène devant un mur habillé de carreaux de pierre naturelle ou grès cérame effet marbre. "
            "La robinetterie sur pied est en métal noir mat ou bronze brossé. Un large miroir circulaire rétroéclairé complète le meuble vasque.\n\n"
            "ANALYSE\n"
            "Le design adopte les codes du spa résidentiel de luxe. Le contraste graphique entre la blancheur pure de la baignoire et la texture veinée de la pierre "
            "crée une sensation de raffinement intemporel. La robinetterie noire ou bronze apporte une ponctuation visuelle contemporaine forte.\n\n"
            "POINTS FORTS\n"
            "- Forte valeur sculpturale de la baignoire îlot positionnée en pièce maîtresse.\n"
            "- Matériaux résistants à l'humidité et durables (grès cérame, résine haute densité).\n"
            "- Rétroéclairage du miroir qui élimine les ombres dures sur le visage.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Entretien régulier des finitions mates et de la robinetterie face aux dépôts de calcaire.\n"
            "- Le poids cumulé d'une baignoire îlot remplie impose une vérification de portance du plancher non mesurable visuellement.\n\n"
            "RECOMMANDATION\n"
            "Prévoir une niche murale encastrée à proximité de la baignoire pour poser les flacons sans rompre l'alignement minimaliste au sol."
        )
    },
    {
        "id": "archi_009",
        "category": "STYLE / MATERIAUX / AMBIANCE",
        "split": "train",
        "space_type": "salon",
        "style": "industriel",
        "unsplash_id": "photo-1534349762230-e0cadf78f5da",
        "image": "images/archi_009.jpg",
        "context": "Salon d'inspiration industrielle avec mur de parement en briques anciennes et mobilier en cuir patiné.",
        "question": "Quels sont les marqueurs stylistiques et les matériaux qui définissent l'ambiance industrielle de ce séjour ?",
        "answer": (
            "OBSERVATION\n"
            "Le décor met en avant une paroi en briques de terre cuite rouge vieillie, une table basse sur roulettes industrielles ou piétement fonte, "
            "un canapé en cuir vieilli couleur tabac et des luminaires à cage métallique avec ampoules à filament visible.\n\n"
            "ANALYSE\n"
            "L'espace s'inscrit directement dans le vocabulaire loft new-yorkais. L'authenticité découle de la mise à nu des matériaux structurels "
            "(brique, acier brut, bois de récupération). Les textures imparfaites et rugueuses apportent une dimension historique et chaleureuse.\n\n"
            "POINTS FORTS\n"
            "- Caractère visuel très affirmé et narratif grâce aux textures brutes.\n"
            "- Belle patine du cuir qui vieillit élégamment avec le temps.\n"
            "- Ambiance lumineuse intime générée par la température de couleur très chaude des ampoules décoratives.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Risque d'obscurité excessive si l'apport de lumière directe n'est pas suffisant pour la lecture ou les activités quotidiennes.\n"
            "- La brique brute est poreuse et nécessite un traitement hydrofuge/antipoussière.\n\n"
            "RECOMMANDATION\n"
            "Adjoindre un éclairage d'appoint indirect au niveau du plafond ou des corniches pour compenser l'absorption lumineuse des parois en briques sombres."
        )
    },
    {
        "id": "archi_010",
        "category": "STYLE / MATERIAUX / AMBIANCE",
        "split": "validation",
        "space_type": "cuisine",
        "style": "classique",
        "unsplash_id": "photo-1507089947368-19c1da9775ae",
        "image": "images/archi_010.jpg",
        "context": "Cuisine de style classique intemporel avec façades moulurées shaker et plan de travail en pierre noble.",
        "question": "Identifiez les matériaux, le travail de modénature et l'ambiance générale de cette cuisine classique revisitée.",
        "answer": (
            "OBSERVATION\n"
            "Les façades de meubles sont laquées dans une teinte vert sauge ou gris bleuté avec des moulures à cadre traditionnel type shaker. "
            "Les plans de travail et crédences présentent un marbre blanc carrare ou composite quartz veiné. "
            "Les poignées coquilles et mitigeurs sont en laiton doré brossé.\n\n"
            "ANALYSE\n"
            "Il s'agit d'une réinterprétation néo-classique contemporaine. L'élégance provient de la modénature discrète des cadres de portes "
            "qui accroche délicatement la lumière, combinée à la noblesse minérale du marbre. Le laiton apporte une touche d'orfèvrerie décorative.\n\n"
            "POINTS FORTS\n"
            "- Esthétique intemporelle qui résiste remarquablement aux effets de mode.\n"
            "- Contraste raffiné entre la laque mate pastel et les reflets chaleureux du laiton.\n"
            "- Finitions haut de gamme perçues.\n\n"
            "POINTS DE VIGILANCE\n"
            "- La porosité d'un marbre naturel face aux acides alimentaires (citron, vinaigre) requiert une étanchéité hydro-oléofuge régulière.\n"
            "- L'épaisseur exacte des plans de travail et les dimensions d'encastrement ne sont pas quantifiables à l'œil nu.\n\n"
            "RECOMMANDATION\n"
            "Si le matériau s'avère être du marbre naturel calcaire, appliquer un traitement protecteur oléofuge ou envisager un grès cérame marbré pour une insensibilité totale aux taches."
        )
    },

    # =========================================================================
    # CATEGORIE 3 : ERGONOMIE / CIRCULATION (5 exemples)
    # =========================================================================
    {
        "id": "archi_011",
        "category": "ERGONOMIE / CIRCULATION",
        "split": "train",
        "space_type": "cuisine",
        "style": "contemporain",
        "unsplash_id": "photo-1556911220-e15b29be8c8f",
        "image": "images/archi_011.jpg",
        "context": "Cuisine familiale contemporaine avec linéaire d'armoires et grand îlot de préparation.",
        "question": "Évaluez l'ergonomie fonctionnelle et les schémas de circulation de cette cuisine, notamment le triangle d'activité.",
        "answer": (
            "OBSERVATION\n"
            "L'espace présente une configuration linéaire avec îlot face au mur technique. L'évier est intégré dans l'îlot tandis que les colonnes "
            "avec fours encastrés à hauteur des yeux et réfrigérateur bordent le mur arrière. Un couloir de passage sépare les deux blocs.\n\n"
            "ANALYSE\n"
            "Le triangle d'activité (stockage, préparation/lavage, cuisson) est compact et fluide : le pivotement entre l'îlot et le linéaire mural est direct. "
            "L'implantation des fours en colonne à hauteur de buste évite les flexions lombaires répétées lors des manipulations de plats chauds.\n\n"
            "POINTS FORTS\n"
            "- Triangle d'activité ergonomique réduisant les pas inutiles.\n"
            "- Excellente posture de travail grâce aux appareils de cuisson surélevés.\n"
            "- Dégagement de plan de travail continu autour de l'évier pour le séchage et la découpe.\n\n"
            "POINTS DE VIGILANCE\n"
            "- La distance métrique du couloir central doit impérativement faire au minimum 90 cm (idéalement 110-120 cm) pour ouvrir le lave-vaisselle sans entraver le passage.\n"
            "- L'absence de plan métré ne permet pas de valider la cote exacte de ce dégagement.\n\n"
            "RECOMMANDATION\n"
            "S'assurer que la poubelle de tri sélectif sous évier et le lave-vaisselle sont positionnés de façon à pouvoir être ouverts simultanément sans créer de collision."
        )
    },
    {
        "id": "archi_012",
        "category": "ERGONOMIE / CIRCULATION",
        "split": "train",
        "space_type": "bureau",
        "style": "minimaliste",
        "unsplash_id": "photo-1524758631624-e2822e304c36",
        "image": "images/archi_012.jpg",
        "context": "Espace de télétravail aménagé dans une pièce dédiée, axé sur la clarté et l'ergonomie posturale.",
        "question": "Analysez l'ergonomie du poste de travail, le positionnement par rapport à la lumière et la fluidité de circulation.",
        "answer": (
            "OBSERVATION\n"
            "Le bureau est composé d'un plateau droit en bois clair sur piétement sobre, accompagné d'un fauteuil pivotant réglable. "
            "L'écran est disposé face à l'utilisateur, perpendiculairement à la fenêtre latérale. L'espace au sol autour du siège est entièrement dégagé.\n\n"
            "ANALYSE\n"
            "L'orientation du plan de travail perpendiculaire à la source lumineuse est idéale : elle évite l'éblouissement direct d'un travail face fenêtre "
            "et les reflets gênants d'un écran dos à la fenêtre. Le recul disponible derrière le siège permet un mouvement fluide sans frottement mural.\n\n"
            "POINTS FORTS\n"
            "- Excellent positionnement bioclimatique de l'écran par rapport à la lumière du jour.\n"
            "- Fauteuil ergonomique doté d'un soutien lombaire et d'accoudoirs.\n"
            "- Aire de manœuvre dégagée facilitant les déplacements assis-debout.\n\n"
            "POINTS DE VIGILANCE\n"
            "- La hauteur précise du plateau (standard recommandé : 72 à 75 cm) et la distance œil-écran ne sont pas vérifiables sans mesure physique.\n"
            "- Manque de caisson de rangement à portée de main immédiate pour les dossiers courants.\n\n"
            "RECOMMANDATION\n"
            "Ajouter un support d'écran réglable en hauteur pour aligner le haut de l'affichage avec la ligne d'horizon du regard, prévenant les tensions cervicales."
        )
    },
    {
        "id": "archi_013",
        "category": "ERGONOMIE / CIRCULATION",
        "split": "train",
        "space_type": "salle de bain",
        "style": "contemporain",
        "unsplash_id": "photo-1565182999561-18d7dc61c393",
        "image": "images/archi_013.jpg",
        "context": "Salle d'eau moderne avec grande douche à l'italienne de plain-pied et meuble double vasque suspendu.",
        "question": "Examinez l'agencement de cette salle d'eau sous l'angle de la sécurité, de la transition zone sèche/humide et des circulations.",
        "answer": (
            "OBSERVATION\n"
            "La pièce dispose d'une douche de plain-pied séparée par une paroi vitrée transparente fixe sans porte. "
            "Le receveur affleure parfaitement le sol de la pièce. En vis-à-vis ou en continuité, un meuble suspendu accueille une ou deux vasques. "
            "Le sol est un carrelage grand format antidérapant.\n\n"
            "ANALYSE\n"
            "L'absence de marche d'accès à la douche élimine les risques de trébuchement et répond aux principes de conception universelle. "
            "La séparation par paroi fixe assure une circulation directe sans manipulation de battants dans un espace confiné.\n\n"
            "POINTS FORTS\n"
            "- Accès de plain-pied sécurisé et ergonomique pour tous les âges.\n"
            "- Meuble suspendu libérant l'espace au sol pour un nettoyage facile et un passage des pieds fluide.\n"
            "- Linéarité de la circulation entre vasque et douche.\n\n"
            "POINTS DE VIGILANCE\n"
            "- L'avancée de la paroi vitrée doit être suffisante pour éviter les projections d'eau sur la zone sèche de sortie.\n"
            "- La pente d'évacuation (généralement 1,5 à 2%) est invisible à l'image et nécessite une conformité technique rigoureuse.\n\n"
            "RECOMMANDATION\n"
            "Positionner le sèche-serviettes ou une patère à la sortie immédiate de la zone de douche pour attraper son linge sans traverser la pièce mouillé."
        )
    },
    {
        "id": "archi_014",
        "category": "ERGONOMIE / CIRCULATION",
        "split": "train",
        "space_type": "petit espace",
        "style": "scandinave",
        "unsplash_id": "photo-1493809842364-78817add7ffb",
        "image": "images/archi_014.jpg",
        "context": "Appartement de taille réduite optimisé avec espace salon-salle à manger connecté.",
        "question": "Analysez la fluidité des flux de passage et l'ergonomie de l'encombrement dans ce petit espace de vie.",
        "answer": (
            "OBSERVATION\n"
            "La pièce concentre plusieurs fonctions : table de repas compacte à chaises légères et coin salon avec table basse. "
            "Les axes de passage entre la porte d'accès et la fenêtre longent le mobilier sans croisement frontal visible.\n\n"
            "ANALYSE\n"
            "Dans ce gabarit étroit, la priorité est de préserver un corridor de circulation principal rectiligne. "
            "Les chaises à dossier ajouré réduisent l'impact visuel et n'encombrent pas le champ optique. Le mobilier est adossé aux parois pour dégager le centre.\n\n"
            "POINTS FORTS\n"
            "- Alignement des flux de déplacement évitant les trajectoires en zigzag.\n"
            "- Mobilier aux gabarits proportionnés à l'échelle de la pièce.\n"
            "- Dégagement satisfaisant autour de la table pour reculer les chaises.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Les passages étroits peuvent devenir critiques si les chaises ne sont pas repoussées sous la table après usage.\n"
            "- Sans cotation millimétrée, la largeur exacte du couloir de circulation ne peut être certifiée conforme aux 80 cm de confort.\n\n"
            "RECOMMANDATION\n"
            "Opter pour une table à rallonges papillon ou plateau rabattable pour libérer 30 à 40 cm de passage supplémentaire en dehors des repas."
        )
    },
    {
        "id": "archi_015",
        "category": "ERGONOMIE / CIRCULATION",
        "split": "validation",
        "space_type": "bureau",
        "style": "industriel",
        "unsplash_id": "photo-1518455027359-f3f8164ba6bd",
        "image": "images/archi_015.jpg",
        "context": "Atelier-bureau de créatif avec grand plan de travail en bois massif et rangements verticaux.",
        "question": "Évaluez l'ergonomie de travail et l'organisation des flux dans cet atelier de travail créatif.",
        "answer": (
            "OBSERVATION\n"
            "Un large établi ou plan de travail en bois épais occupe le centre/bord de l'espace, entouré de rangements modulaires et d'étagères métalliques murales. "
            "Le matériel de travail et d'échantillonnage est disposé à proximité immédiate.\n\n"
            "ANALYSE\n"
            "L'ergonomie est pensée pour une activité dynamique alternant postures assise et debout. "
            "La grande profondeur du plan de travail permet d'étaler des plans ou maquettes sans empiéter sur la zone ordinateur. "
            "Le stockage vertical exploite toute la hauteur sous plafond pour désencombrer le plan utile.\n\n"
            "POINTS FORTS\n"
            "- Surface de travail continue généreuse propice aux manipulations créatives.\n"
            "- Accessibilité directe des outils et fournitures sans déplacement majeur.\n"
            "- Solidité apparente des supports adaptés aux charges lourdes.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Les étagères hautes nécessitent un escabeau ou marchepied dont le rangement doit être anticipé.\n"
            "- Risque de fatigue visuelle si la surface de bois foncé absorbe trop la lumière sans éclairage direct ponctuel.\n\n"
            "RECOMMANDATION\n"
            "Installer une lampe d'architecte articulée à fort IRC (Indice de Rendu des Couleurs > 90) avec fixation sur étau pour éclairer précisément la zone de précision."
        )
    },

    # =========================================================================
    # CATEGORIE 4 : CRITIQUE DE PROJET (5 exemples)
    # =========================================================================
    {
        "id": "archi_016",
        "category": "CRITIQUE DE PROJET",
        "split": "train",
        "space_type": "salon",
        "style": "contemporain",
        "unsplash_id": "photo-1586023492125-27b2c045efd7",
        "image": "images/archi_016.jpg",
        "context": "Salon design mettant en scène un fauteuil d'accentuation jaune moutarde face à une composition murale épurée.",
        "question": "Formulez une critique architecturale constructive de ce salon en évaluant ses partis-pris de composition, ses contrastes et son confort d'usage.",
        "answer": (
            "OBSERVATION\n"
            "L'espace est dominé par un fond neutre sobre sur lequel se détache un fauteuil d'accent de couleur jaune vive, accompagné d'une table basse d'appoint "
            "et d'une lampe sur pied design. Le mur de fond reste largement immaculé.\n\n"
            "ANALYSE\n"
            "Le projet mise sur une stratégie scénographique d'objet-icône : le fauteuil coloré focalise l'attention et dynamise l'espace par contraste chromatique. "
            "Cependant, la composition tend vers un minimalisme de catalogue qui semble privilégier la contemplation formelle sur la convivialité partagée.\n\n"
            "POINTS FORTS\n"
            "- Effet visuel percutant et mémorable grâce au contraste chromatique maîtrisé.\n"
            "- Lignes du mobilier contemporain bien dessinées et élégantes.\n"
            "- Absence totale de pollution visuelle.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Sous-dimensionnement de la capacité d'accueil si la pièce est destinée à une famille ou à recevoir.\n"
            "- La distance entre l'assise et la table d'appoint semble juste sur le plan ergonomique pour poser une tasse sans se pencher.\n"
            "- Les dimensions réelles de recul ne peuvent être affirmées sans plan d'aménagement coté.\n\n"
            "RECOMMANDATION\n"
            "Enrichir la composition d'une seconde assise complémentaire (chauffeuse ou pouf en tissu texturé) et d'un tableau d'art abstrait au mur pour rééquilibrer les masses visuelles."
        )
    },
    {
        "id": "archi_017",
        "category": "CRITIQUE DE PROJET",
        "split": "train",
        "space_type": "chambre",
        "style": "scandinave",
        "unsplash_id": "photo-1595526114035-0d45ed16cfbf",
        "image": "images/archi_017.jpg",
        "context": "Chambre à coucher scandinave sous mansarde avec suspensions tombantes et palette pastel.",
        "question": "Réalisez une critique objective de ce projet de chambre : relevez les réussites décoratives et les défauts fonctionnels potentiels.",
        "answer": (
            "OBSERVATION\n"
            "Le lit est adossé à un mur peint en tonalité sourde, flanqué de tables de chevet minimalistes et de suspensions légères retombant du plafond. "
            "Des textiles doux et des coussins superposés habillent le lit.\n\n"
            "ANALYSE\n"
            "L'ambiance cocooning et intime est indéniablement réussie grâce au travail sur les matières moelleuses et l'enveloppement chromatique. "
            "En revanche, les suspensions descendant très bas au-dessus des chevets peuvent constituer une gêne physique lors des mouvements nocturnes ou du nettoyage.\n\n"
            "POINTS FORTS\n"
            "- Belle sensibilité atmosphérique propice à l'apaisement et au sommeil.\n"
            "- Superposition textile créant de la profondeur et du relief tactile.\n"
            "- Libération de la surface du chevet par l'usage d'éclairages suspendus.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Risque d'accrochage ou d'impact avec les suspensions au lever du lit si la hauteur d'arrêt n'est pas millimétrée.\n"
            "- Absence de rangement fermé pour dissimuler les livres ou objets personnels de nuit.\n\n"
            "RECOMMANDATION\n"
            "Régler la hauteur basse des suspensions à au moins 45 cm au-dessus du plateau de chevet et équiper le circuit d'un variateur mural d'intensité lumineuse."
        )
    },
    {
        "id": "archi_018",
        "category": "CRITIQUE DE PROJET",
        "split": "train",
        "space_type": "salle de bain",
        "style": "minimaliste",
        "unsplash_id": "photo-1620626011761-996317b8d101",
        "image": "images/archi_018.jpg",
        "context": "Salle de bain ultra-minimaliste aux surfaces monochromes en béton ciré sans aucun rangement apparent.",
        "question": "Proposez une critique experte de cette salle de bain ultra-minimaliste : confrontez l'intention plastique aux contraintes de la vie réelle.",
        "answer": (
            "OBSERVATION\n"
            "Les parois, le sol et le plan vasque forment une continuité matérielle unifiée en béton ciré ou micro-ciment gris clair. "
            "La robinetterie encastrée est minimaliste. Aucun meuble à tiroirs ni étagère n'est visible dans le champ de la photo.\n\n"
            "ANALYSE\n"
            "D'un point de vue sculptural, l'espace offre une puissance monolithique remarquable qui sublime l'architecture brute. "
            "Toutefois, sur le plan fonctionnel, l'absence apparente de solutions de rangement pour les produits de toilette, cosmétiques et serviettes "
            "rend l'espace difficilement vivable sans créer un désordre visuel immédiat dès le premier usage quotidien.\n\n"
            "POINTS FORTS\n"
            "- Pureté géométrique et absence totale de joints créant une impression de sérénité sculpturale.\n"
            "- Entretien des surfaces planes aisé en l'absence de recoins.\n"
            "- Finitions encastrées témoignant d'une mise en œuvre technique soignée.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Rupture rapide de l'esthétique minimaliste dès que des flacons hétérogènes sont posés sur le plan vasque.\n"
            "- Comportement du micro-ciment dans le temps : vulnérabilité aux micro-fissures structurelles non visibles sur photo.\n\n"
            "RECOMMANDATION\n"
            "Intégrer une armoire de toilette affleurante dissimulée derrière un miroir pleine face avec système push-pull pour préserver le minimalisme tout en offrant le volume de stockage indispensable."
        )
    },
    {
        "id": "archi_019",
        "category": "CRITIQUE DE PROJET",
        "split": "train",
        "space_type": "espace ouvert",
        "style": "contemporain",
        "unsplash_id": "photo-1512917774080-9991f1c4c750",
        "image": "images/archi_019.jpg",
        "context": "Grand espace de vie décloisonné dans une villa contemporaine de grand gabarit.",
        "question": "Analysez de façon critique la gestion de l'échelle, de l'intimité et du confort dans ce grand volume décloisonné.",
        "answer": (
            "OBSERVATION\n"
            "Le volume rassemble sur une même surface continue salon, salle à manger et passages vers l'étage sous une hauteur libre importante. "
            "Les sols en pierre polie reflètent la lumière des baies vitrées panoramiques. Les groupes de mobilier semblent disséminés sur le plateau.\n\n"
            "ANALYSE\n"
            "Le projet exprime une générosité spatiale indéniable mais souffre d'un écueil fréquent dans les très grands plateaux : le sentiment d'agora impersonnelle. "
            "La disproportion entre l'échelle du corps humain et l'immensité du volume non sous-divisé peut générer une sensation de flottement et un inconfort acoustique majeur.\n\n"
            "POINTS FORTS\n"
            "- Vaste sentiment de liberté et de prestige architectural.\n"
            "- Luminosité naturelle abondante et vues dégagées.\n"
            "- Facilité de circulation globale d'un pôle à l'autre.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Écho et temps de réverbération certainement très défavorables aux conversations feutrées.\n"
            "- Zonage thermique complexe (zones froides près des vitrages, déperditions volumétriques).\n"
            "- Les portées exactes entre piliers nécessiteraient les plans d'ingénierie structurelle.\n\n"
            "RECOMMANDATION\n"
            "Créer des sous-espaces plus intimes grâce à des paravents architecturaux, des tapis de très grand format (3x4m) et des plafonds suspendus partiels avec éclairage acoustique intégré."
        )
    },
    {
        "id": "archi_020",
        "category": "CRITIQUE DE PROJET",
        "split": "validation",
        "space_type": "chambre",
        "style": "classique",
        "unsplash_id": "photo-1505691938895-1758d7feb511",
        "image": "images/archi_020.jpg",
        "context": "Chambre de maître classique avec lit imposant à montants et boiseries peintes.",
        "question": "Évaluez de manière critique le rapport d'échelle entre le mobilier classique et le volume de cette chambre.",
        "answer": (
            "OBSERVATION\n"
            "La chambre accueille un lit imposant en bois massif travaillé, flanqué de chevets massifs coordonnés. "
            "Les murs comportent des moulures d'encadrement et des rideaux généreux à embrasses tombent jusqu'au sol.\n\n"
            "ANALYSE\n"
            "Le projet respecte les canons du style classique bourgeois avec une grande rigueur dans la symétrie. "
            "Cependant, la massivité du mobilier a tendance à saturer visuellement l'espace au sol. Le lit devient une présence presque écrasante "
            "qui réduit la sensation de fluidité spatiale dans la pièce.\n\n"
            "POINTS FORTS\n"
            "- Respect scrupuleux de l'équilibre et de la symétrie axiale classique.\n"
            "- Belle facture artisanale des pièces d'ébénisterie.\n"
            "- Sentiment de confort feutré et sécurisant.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Lourdeur visuelle causée par l'accumulation de bois foncé et de draperies épaisses.\n"
            "- Difficulté d'évolution ou de réaménagement ultérieur compte tenu du gabarit fixe des meubles.\n\n"
            "RECOMMANDATION\n"
            "Alléger la perception de l'ensemble en introduisant du linge de lit en lin blanc lavé plus décontracté et en remplaçant les abat-jours sombres par des diffuseurs clairs."
        )
    },

    # =========================================================================
    # CATEGORIE 5 : PROPOSITION D'AMELIORATION (5 exemples)
    # =========================================================================
    {
        "id": "archi_021",
        "category": "PROPOSITION D'AMÉLIORATION",
        "split": "train",
        "space_type": "cuisine",
        "style": "contemporain",
        "unsplash_id": "photo-1600565193348-f74bd3c7ccdf",
        "image": "images/archi_021.jpg",
        "context": "Cuisine moderne avec îlot en bois clair et plan de travail marbré, manquant de touches de contraste et d'éclairage d'ambiance.",
        "question": "Quelles propositions concrètes d'amélioration architecturale et décorative formuleriez-vous pour optimiser cette cuisine ?",
        "answer": (
            "OBSERVATION\n"
            "La cuisine dispose d'armoires lisses en bois clair, d'un îlot assorti avec plan en marbre blanc et d'un sol en béton poli. "
            "L'éclairage repose principalement sur des spots encastrés au plafond. L'atmosphère est claire mais manque de relief et de points d'accroche visuels.\n\n"
            "ANALYSE\n"
            "La base architecturale est saine et contemporaine, mais l'uniformité des teintes crée une certaine monotonie visuelle. "
            "L'éclairage zénithal par spots est fonctionnel mais projette des ombres directes peu flatteuses sur le plan de travail lorsque l'on cuisine.\n\n"
            "POINTS FORTS\n"
            "- Excellente base de matériaux pérennes et chaleureux (bois et pierre naturelle).\n"
            "- Volumes bien proportionnés et circulation aérée.\n"
            "- Rangement abondant dissimulé derrière des façades uniformes.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Absence d'éclairage d'ambiance ou de balisage chaleureux pour les moments de convivialité en soirée.\n"
            "- Risque de monotonie chromatique sur le long terme.\n\n"
            "RECOMMANDATION\n"
            "1. Installer deux ou trois suspensions sculpturales en céramique ou verre strié au-dessus de l'îlot pour créer un point focal élégant.\n"
            "2. Intégrer un rétroéclairage LED 2700K sous le nez du plan de travail de l'îlot pour donner un effet de lévitation au bloc minéral.\n"
            "3. Remplacer les tabourets neutres par des modèles avec piétement noir mat et assise en cuir cognac pour apporter du contraste graphique."
        )
    },
    {
        "id": "archi_022",
        "category": "PROPOSITION D'AMÉLIORATION",
        "split": "train",
        "space_type": "chambre",
        "style": "Japandi",
        "unsplash_id": "photo-1615873968403-89e068629265",
        "image": "images/archi_022.jpg",
        "context": "Chambre Japandi très dépouillée avec sommier bas près du sol et teintes organiques.",
        "question": "En conservant l'esprit zen et épuré de cette chambre Japandi, quelles améliorations fonctionnelles et acoustiques recommandez-vous ?",
        "answer": (
            "OBSERVATION\n"
            "Un sommier bas en chêne clair est posé sur un sol minéral nu. Les parois sont nues et peintes en ton pierre. "
            "Un seul élément décoratif discret habille la pièce. L'espace paraît extrêmement calme mais résonnant.\n\n"
            "ANALYSE\n"
            "Si la quête de vacuité visuelle propre au bouddhisme zen est parfaitement atteinte, le confort tactile et acoustique d'une chambre à coucher "
            "requiert un traitement plus soigné de l'amortissement sonore et de la transition thermique au lever du lit.\n\n"
            "POINTS FORTS\n"
            "- Pureté esthétique exceptionnelle propice au désencombrement de l'esprit.\n"
            "- Respect fidèle des canons stylistiques traditionnels réinterprétés.\n"
            "- Belle circulation naturelle de l'air et de la lumière.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Sensation de froid au pied du lit sur sol dur nu le matin.\n"
            "- Résonance acoustique probable due à la vacuité des parois.\n\n"
            "RECOMMANDATION\n"
            "1. Disposer un grand tapis en fibres naturelles (jute souple, laine bouclée non teinte) débordant d'au moins 60 cm de part et d'autre du lit.\n"
            "2. Poser un claustra mural en tasseaux de chêne ajourés sur feutre acoustique noir derrière la tête de lit pour absorber les fréquences moyennes et habiller le mur sans surcharge.\n"
            "3. Prévoir un store bateau en lin lavé à la fenêtre pour tamiser délicatement la lumière matinale."
        )
    },
    {
        "id": "archi_023",
        "category": "PROPOSITION D'AMÉLIORATION",
        "split": "train",
        "space_type": "salle de bain",
        "style": "minimaliste",
        "unsplash_id": "photo-1507652313519-d4e9174996dd",
        "image": "images/archi_023.jpg",
        "context": "Salle de bain compacte avec carrelage blanc uniforme, fonctionnelle mais ressentie comme froide et clinique.",
        "question": "Comment réchauffer l'ambiance et optimiser la sensation de bien-être dans cette salle de bain sans engager de lourds travaux de démolition ?",
        "answer": (
            "OBSERVATION\n"
            "La pièce est entièrement carrelée de blanc avec des joints ton sur ton, sanitaire en céramique blanche et robinetterie chromée standard. "
            "L'éclairage provient d'un plafonnier central blanc froid. L'ensemble est propre et lumineux mais dégage une impression d'espace clinique.\n\n"
            "ANALYSE\n"
            "Le projet souffre d'un excès d'asepsie visuelle : le blanc total combiné au chrome froid et à un éclairage sans gradation crée une lumière crue. "
            "L'introduction ciblée de matériaux vivants et organiques permettrait d'humaniser l'espace sans modifier la plomberie existante.\n\n"
            "POINTS FORTS\n"
            "- Luminosité globale très élevée maximisant la clarté.\n"
            "- Facilité d'entretien hygiénique.\n"
            "- Base neutre idéale servant de toile de fond facile à accessoiriser.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Inconfort thermique perçu dû à la froideur des surfaces et de la lumière.\n"
            "- Absence de rangements d'agrément personnalisés.\n\n"
            "RECOMMANDATION\n"
            "1. Remplacer le miroir standard par un miroir rond cerclé de chêne avec rétroéclairage chaud (2700K).\n"
            "2. Ajouter des étagères ouvertes en teck ou chêne traité hydrofuge pour accueillir des paniers de rangement en fibres tressées et des plantes tropicales (ex. Pothos ou fougère) prospérant en milieu humide.\n"
            "3. Remplacer le plafonnier blanc froid par une source lumineuse diffuse IP44 à température de couleur chaleureuse."
        )
    },
    {
        "id": "archi_024",
        "category": "PROPOSITION D'AMÉLIORATION",
        "split": "train",
        "space_type": "bureau",
        "style": "contemporain",
        "unsplash_id": "photo-1513519245088-0e12902e5a38",
        "image": "images/archi_024.jpg",
        "context": "Espace bibliothèque / bureau contemporain avec rayonnages ouverts et table de travail centrale.",
        "question": "Formulez des recommandations d'amélioration pour perfectionner l'organisation fonctionnelle et la mise en lumière de cet espace bureau-bibliothèque.",
        "answer": (
            "OBSERVATION\n"
            "Une grande bibliothèque toute hauteur accueille des livres et objets décoratifs. Une table de travail sobre est installée au premier plan. "
            "L'éclairage ambiant est assuré par un luminaire central au plafond, laissant les fonds d'étagères dans une pénombre relative.\n\n"
            "ANALYSE\n"
            "La bibliothèque possède un fort potentiel décoratif et de stockage, mais l'absence d'éclairage intégré dans le meuble étouffe la profondeur "
            "des rayonnages. De plus, les câbles d'alimentation du matériel informatique sur le bureau risquent de perturber la pureté des lignes.\n\n"
            "POINTS FORTS\n"
            "- Forte capacité de stockage documentaire et d'exposition d'objets.\n"
            "- Ambiance studieuse et intellectuelle affirmée.\n"
            "- Mobilier aux finitions soignées.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Pénombre sur les livres due à l'éclairage zénithal projetant l'ombre de l'utilisateur sur les rayons.\n"
            "- Gestion des arrivées électriques et courants faibles à dissimuler rigoureusement.\n\n"
            "RECOMMANDATION\n"
            "1. Intégrer des réglettes micro-LED invisibles fraisées sous chaque tablette de la bibliothèque pour mettre en valeur les tranches de livres et objets d'art.\n"
            "2. Équiper le plateau de bureau d'une trappe passe-câbles encastrée affleurante avec goulotte sous plateau pour faire disparaître tout filage.\n"
            "3. Disposer un fauteuil lounge d'appoint avec liseuse orientable dans un angle pour créer une zone de lecture distincte du poste informatique."
        )
    },
    {
        "id": "archi_025",
        "category": "PROPOSITION D'AMÉLIORATION",
        "split": "validation",
        "space_type": "petit espace",
        "style": "contemporain",
        "unsplash_id": "photo-1560448204-e02f11c3d0e2",
        "image": "images/archi_025.jpg",
        "context": "Pièce à vivre d'un petit appartement moderne de 35 m2 nécessitant une optimisation spatiale et lumineuse.",
        "question": "Quelles solutions d'architecture d'intérieur proposez-vous pour agrandir visuellement ce petit séjour et démultiplier ses fonctionnalités ?",
        "answer": (
            "OBSERVATION\n"
            "L'appartement comprend un séjour compact regroupant salon et coin repas. Le canapé est adossé à un mur plein, face à une fenêtre latérale. "
            "Le mobilier au sol occupe une proportion notable de la surface utile.\n\n"
            "ANALYSE\n"
            "Dans les petits appartements, chaque meuble posé au sol grignote la perception de l'espace global. "
            "Pour amplifier le volume perçu, la stratégie architecturale consiste à libérer le plancher, guider la lumière naturelle et démultiplier les usages par du mobilier intelligent.\n\n"
            "POINTS FORTS\n"
            "- Bonne distribution naturelle de la lumière grâce à la fenêtre latérale.\n"
            "- Forme du plateau relativement régulière et facile à aménager.\n"
            "- Potentiel d'optimisation verticale élevé sur les murs porteurs.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Risque d'encombrement rapide si des meubles d'appoint s'accumulent au fil du temps.\n"
            "- Les cotes d'épaisseur des cloisons et contraintes de gaines techniques doivent être vérifiées avant toute fixation lourde.\n\n"
            "RECOMMANDATION\n"
            "1. Remplacer le meuble TV posé au sol par un meuble suspendu ultra-fin (profondeur 30 cm) laissant visible le carrelage/parquet sous le meuble.\n"
            "2. Installer un grand miroir d'atelier vertical sur le mur perpendiculaire à la fenêtre pour capter la lumière du jour et créer une perspective de fausse pièce en trompe-l'œil.\n"
            "3. Remplacer la table fixe par une console extensible modulable permettant de passer d'un meuble d'entrée discret de 40 cm à une table de réception pour 6 personnes."
        )
    }
]

def format_qwen2_vl_record(item):
    """
    Formate un exemple dans une structure riche et standardisee :
    1. Champs plats (id, category, space_type, style, image, context, question, answer)
    2. Format 'conversations' natif Qwen2-VL / LLaVA / HF multi-modal
    """
    image_rel_path = item["image"]
    user_text = f"Contexte : {item['context']}\n\nQuestion : {item['question']}"
    assistant_text = item["answer"]
    
    return {
        "id": item["id"],
        "category": item["category"],
        "space_type": item["space_type"],
        "style": item["style"],
        "image": image_rel_path,
        "context": item["context"],
        "question": item["question"],
        "answer": assistant_text,
        "conversations": [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image_rel_path},
                    {"type": "text", "text": user_text}
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": assistant_text}
                ]
            }
        ]
    }

def main():
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    print(f"=== TELECHARGEMENT ET VERIFICATION DES {len(DATASET_EXAMPLES)} IMAGES ===")
    
    train_records = []
    val_records = []
    
    for idx, item in enumerate(DATASET_EXAMPLES, start=1):
        filename = f"{item['id']}.jpg"
        filepath = os.path.join(DATASET_DIR, item["image"])
        url = f"https://images.unsplash.com/{item['unsplash_id']}?w=1024&q=80"
        
        print(f"[{idx:02d}/25] Image {filename} ({item['category']} - {item['space_type']})...")
        
        if not os.path.exists(filepath):
            req = urllib.request.Request(
                url, 
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
                img = Image.open(io.BytesIO(data)).convert("RGB")
                # Redimensionnement respectant les ratios tout en bridant a 1024x768
                img.thumbnail((1024, 768), Image.Resampling.LANCZOS)
                img.save(filepath, "JPEG", quality=85, optimize=True)
                file_size_kb = os.path.getsize(filepath) // 1024
                print(f"       -> Telechargee et optimisee: {img.size[0]}x{img.size[1]} ({file_size_kb} KB)")
        else:
            with Image.open(filepath) as img:
                print(f"       -> Deja presente: {img.size[0]}x{img.size[1]} ({os.path.getsize(filepath)//1024} KB)")

        record = format_qwen2_vl_record(item)
        if item["split"] == "train":
            train_records.append(record)
        else:
            val_records.append(record)

    # Ecriture des fichiers JSONL
    train_path = os.path.join(DATASET_DIR, "train.jsonl")
    val_path = os.path.join(DATASET_DIR, "validation.jsonl")

    with open(train_path, "w", encoding="utf-8") as f:
        for r in train_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\n[OK] Fichier train.jsonl genere : {len(train_records)} exemples ({train_path})")

    with open(val_path, "w", encoding="utf-8") as f:
        for r in val_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[OK] Fichier validation.jsonl genere : {len(val_records)} exemples ({val_path})")

    print("\nCreation terminee avec succes.")

if __name__ == "__main__":
    main()
