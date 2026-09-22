# -*- coding: utf-8 -*-
"""
Script de reconstruction intégrale du dataset AXIS réaligné sur les 25 images réelles.
Source de vérité : chaque photographie dans dataset/images/archi_*.jpg (racine du dépôt)
"""

import json
import os

TRAIN_DATA = [
    # ---------------------------------------------------------
    # 1. ANALYSE D'ESPACE (archi_001 à archi_004)
    # ---------------------------------------------------------
    {
        "id": "archi_001",
        "category": "ANALYSE D'ESPACE",
        "space_type": "salon",
        "style": "contemporain",
        "image": "images/archi_001.jpg",
        "context": "Salon de séjour contemporain baigné de lumière naturelle, ouvert sur l'extérieur par une grande baie vitrée toute hauteur.",
        "question": "Analysez l'organisation spatiale, la hiérarchie des zones et l'apport lumineux de ce salon contemporain à partir de la photographie.",
        "answer": (
            "OBSERVATION\n"
            "La pièce présente un salon structuré autour d'un grand tapis clair posé sur un parquet en bois clair. À droite, un canapé droit en cuir marron cognac fait face à deux fauteuils bas blancs à structure métallique tubulaire noire situés à gauche. Au centre trône une table basse circulaire en bois clair. Le mur du fond accueille une enfilade basse blanche surmontée d'une grille régulière de seize cadres carrés avec photos noir et blanc et de deux lampes de table. Sur la droite, une baie vitrée toute hauteur fait entrer une lumière solaire directe créant des ombres franches au sol. Plusieurs végétaux en pot, dont un arbuste dans un panier tressé, ponctuent l'espace.\n\n"
            "ANALYSE\n"
            "L'organisation spatiale repose sur une disposition en vis-à-vis favorisant la conversation sans cloisonnement physique. Le tapis délimite visuellement le sous-espace de détente dans le volume de la pièce. L'orientation latérale par rapport à la grande ouverture vitrée baigne l'espace de lumière naturelle tout en dégageant les vues. La circulation principale semble s'effectuer librement entre les assises et vers le fond de la pièce.\n\n"
            "POINTS FORTS\n"
            "- Excellente luminosité naturelle apportée par la baie vitrée latérale.\n"
            "- Équilibre des masses entre le canapé en cuir chaleureux et les assises blanches plus légères.\n"
            "- Structuration visuelle claire de l'espace conversationnel par le tapis et la table basse centrale.\n\n"
            "POINTS DE VIGILANCE\n"
            "- L'exposition directe au rayonnement solaire peut générer un inconfort thermique ou un éblouissement selon l'heure de la journée.\n"
            "- Les cotes de passage réelles entre la table basse et les assises ne peuvent être certifiées sans plan métré.\n\n"
            "RECOMMANDATION\n"
            "Prévoir des stores filtrants ou des voilages légers sur la baie vitrée pour moduler la lumière directe en cas de fort ensoleillement sans occulter le panorama extérieur."
        )
    },
    {
        "id": "archi_002",
        "category": "ANALYSE D'ESPACE",
        "space_type": "espace extérieur",
        "style": "contemporain",
        "image": "images/archi_002.jpg",
        "context": "Maison contemporaine vue depuis le jardin au crépuscule, mettant en valeur la terrasse abritée et les relations dedans-dehors.",
        "question": "Analysez l'organisation spatiale et les relations entre l'architecture bâtie, la terrasse extérieure et le jardin visibles sur cette photographie.",
        "answer": (
            "OBSERVATION\n"
            "La photographie montre la façade arrière d'une maison contemporaine au crépuscule. La construction associe un volume principal à étage sombre et un rez-de-chaussée combinant bardage en lattes de bois verticales et larges baies vitrées. Une terrasse couverte surélevée en bois prolonge l'habitation vers le jardin engazonné, délimitée par un garde-corps vitré. Un grand arbre au tronc clair est conservé à la jonction immédiate de la terrasse et de la pelouse. Sur la terrasse sont visibles une table avec plusieurs chaises et un module de cuisson extérieur. À travers les vitrages éclairés, on aperçoit une cuisine et la volée d'un escalier intérieur.\n\n"
            "ANALYSE\n"
            "L'espace est conçu selon une transition graduelle entre intérieur, espace intermédiaire abrité (terrasse sous auvent) et extérieur paysager (jardin). L'intégration de l'arbre mature crée une articulation organique forte qui adoucit les lignes orthogonales du bâti. La transparence des baies coulissantes assure une continuité visuelle totale entre la zone de vie intérieure et la terrasse de réception.\n\n"
            "POINTS FORTS\n"
            "- Continuité spatiale intérieur-extérieur remarquable permise par les baies vitrées toute hauteur et le prolongement du niveau de sol sous l'auvent.\n"
            "- Valorisation paysagère de l'arbre existant au cœur du projet.\n"
            "- Polyvalence de la terrasse abritée utilisable par météos variées.\n\n"
            "POINTS DE VIGILANCE\n"
            "- La proximité immédiate du tronc de l'arbre avec la structure et la terrasse nécessite de surveiller le développement racinaire et la croissance du végétal dans le temps.\n"
            "- L'épaisseur et la résistance thermique des parois ne sont pas évaluables à l'œil nu.\n\n"
            "RECOMMANDATION\n"
            "Veiller à réserver un joint de dilatation suffisant autour de la base du tronc au niveau du plancher de la terrasse pour permettre la croissance naturelle de l'arbre sans contraindre la structure."
        )
    },
    {
        "id": "archi_003",
        "category": "ANALYSE D'ESPACE",
        "space_type": "salon",
        "style": "scandinave",
        "image": "images/archi_003.jpg",
        "context": "Salon séjour aux tonalités claires et douces, associant inspirations scandinaves et touches décoratives bohèmes.",
        "question": "Analysez la volumétrie, l'organisation spatiale et la composition décorative de ce salon d'inspiration scandinave et bohème.",
        "answer": (
            "OBSERVATION\n"
            "Le salon est aménagé autour d'un canapé d'angle beige avec méridienne positionnée à droite, complété par un fauteuil bas en bois clair et cannage sur la gauche. Au centre, une table basse ronde en bois à deux niveaux repose sur un grand tapis clair. Un pouf tricoté et deux tables d'appoint complètent les assises. Le mur du fond, teinté d'un vert sauge doux, présente une composition murale dense mêlant vanneries plates, tissage textile, cadres d'art, horloge blanche et crâne décoratif. Deux fenêtres habillées de rideaux beiges apportent une lumière naturelle latérale. Le sol est un parquet d'aspect bois clair.\n\n"
            "ANALYSE\n"
            "L'espace salon est structuré en fer à cheval autour de la table basse, favorisant le rassemblement convivial. La méridienne du canapé délimite l'espace côté fenêtres sans bloquer la vue ni la pénétration de la lumière. Le mur du fond fait office de plan focal décoratif, équilibrant la neutralité apaisante des textiles clairs par la multiplicité des textures artisanales.\n\n"
            "POINTS FORTS\n"
            "- Atmosphère chaleureuse et feutrée générée par la palette chromatique cohérente (écru, sable, bois clair, vert d'eau).\n"
            "- Distribution claire des fonctions de repos et de réception.\n"
            "- Excellente exploitation de la lumière naturelle provenant des deux baies latérales.\n\n"
            "POINTS DE VIGILANCE\n"
            "- La densité d'objets décoratifs muraux et d'éléments d'appoint au sol peut compliquer le dépoussiérage et l'entretien courant.\n"
            "- Les largeurs de circulation entre le pouf, le fauteuil et la table basse semblent confortables mais ne peuvent être mesurées précisément sans plan d'exécution.\n\n"
            "RECOMMANDATION\n"
            "Conserver dégagée la trajectoire de passage entre la porte visible à gauche et la baie vitrée de droite pour ne pas entraver le cheminement naturel à travers la pièce."
        )
    },
    {
        "id": "archi_004",
        "category": "ANALYSE D'ESPACE",
        "space_type": "salon",
        "style": "contemporain",
        "image": "images/archi_004.jpg",
        "context": "Zone de repos épurée adossée à une paroi blanche, combinant assise sobre, commode vintage et éléments végétaux.",
        "question": "Analysez l'organisation de ce coin repos contre paroi et l'équilibre des masses visuelles dans la composition spatiale.",
        "answer": (
            "OBSERVATION\n"
            "La scène montre un alignement mobilier contre une paroi murale blanche unie, sur un sol d'aspect parquet clair. Au centre se trouve un canapé compact deux places de couleur noire garni de deux coussins clairs. À sa droite est installée une commode ancienne peinte en gris-bleu pâle à poignées métalliques ouvragées, surmontée d'un vase de graminées séchées et d'un petit cadre. À gauche du canapé, un arbuste d'intérieur est disposé dans un panier tressé près d'une porte blanche entrouverte. À l'extrémité droite se dresse un lampadaire droit noir à tête orientable.\n\n"
            "ANALYSE\n"
            "L'aménagement fonctionne comme une séquence linéaire d'appoint adossée au mur. La masse visuelle dense et sombre du petit canapé noir est compensée par la teinte très claire de la commode adjacente et par les touches végétales. La verticalité du lampadaire noir à droite fait écho à la verticalité de l'arbuste et de la porte à gauche, créant un cadrage équilibré autour du mobilier central.\n\n"
            "POINTS FORTS\n"
            "- Composition sobre et lisible ne saturant pas le plancher.\n"
            "- Contraste graphique net entre le noir mat du canapé et la clarté du mur et de la commode.\n"
            "- Présence végétale apportant une respiration organique.\n\n"
            "POINTS DE VIGILANCE\n"
            "- La disposition linéaire stricte le long d'un seul pan de mur ne constitue pas un espace salon complet et ne permet pas d'évaluer la fonction de la pièce dans son ensemble.\n"
            "- Le débattement de la porte battante à gauche doit être vérifié pour s'assurer qu'il n'entre pas en contact avec la plante.\n\n"
            "RECOMMANDATION\n"
            "Si cet espace doit servir de lieu de lecture régulier, il serait judicieux d'associer une petite table d'appoint basse ou un tapis de sol pour délimiter plus nettement cette zone d'assise et améliorer son confort d'usage."
        )
    },

    # ---------------------------------------------------------
    # 2. STYLE / MATERIAUX / AMBIANCE (archi_006 à archi_009)
    # ---------------------------------------------------------
    {
        "id": "archi_006",
        "category": "STYLE / MATERIAUX / AMBIANCE",
        "space_type": "salon",
        "style": "contemporain",
        "image": "images/archi_006.jpg",
        "context": "Vaste salon contemporain à haut plafond, rythmé par des ouvertures paysagères et un choix de matières chaleureuses.",
        "question": "Identifiez les matériaux perceptibles, les éléments de finition et l'ambiance lumineuse de ce salon contemporain.",
        "answer": (
            "OBSERVATION\n"
            "Le salon rassemble un canapé trois places tapissé d'un tissu gris texturé, une table basse rectangulaire centrale en bois massif ou aspect bois brut, et deux poufs cubiques revêtus d'un cuir de couleur cognac. À droite, deux fauteuils bas associent une assise en cuir marron à un piètement métallique fin noir. Un grand lampadaire arc tubulaire en métal aspect laiton doré brossé se déploie au-dessus du salon. Au-dessus du canapé, une longue fenêtre bandeau horizontale étirée avec encadrement intérieur en bois offre une vue sur la cime des arbres, tandis qu'une baie vitrée toute hauteur éclaire la pièce depuis la droite. Un grand tapis texturé clair recouvre un sol à lames d'aspect bois.\n\n"
            "ANALYSE\n"
            "L'ambiance stylistique est contemporaine et chaleureuse, articulée autour de contrastes de matières : la douceur du tissu gris du canapé, le caractère chaleureux des cuirs cognac et du bois de la table basse, et la finesse graphique des éléments métalliques noirs et dorés. La fenêtre bandeau constitue une césure architecturale forte qui fait entrer la nature sous forme de tableau panoramique tout en préservant l'intimité de la pièce.\n\n"
            "POINTS FORTS\n"
            "- Harmonie équilibrée des teintes chaudes (cuir cognac, laiton, bois) et froides (tissu gris, parois neutres).\n"
            "- Apport de lumière naturelle double par la baie latérale et la fente vitrée supérieure.\n"
            "- Présence végétale soignée en pots et applique murale.\n\n"
            "POINTS DE VIGILANCE\n"
            "- La nature exacte du revêtement de sol (parquet en bois véritable ou carrelage effet lattes de bois) et la composition des enduits muraux ne peuvent être affirmées avec certitude sur la seule base visuelle.\n"
            "- Les dégagements de circulation autour des fauteuils en cuir ne peuvent être mesurés sans plan côté.\n\n"
            "RECOMMANDATION\n"
            "Maintenir la simplicité des accessoires pour ne pas concurrencer les lignes fortes du lampadaire en arc et de la baie bandeau panoramique."
        )
    },
    {
        "id": "archi_007",
        "category": "STYLE / MATERIAUX / AMBIANCE",
        "space_type": "salon",
        "style": "scandinave",
        "image": "images/archi_007.jpg",
        "context": "Coin séjour d'ambiance naturelle douce, centré sur un mur vert sauge et un ensemble de mobilier artisanal.",
        "question": "Décrivez la palette chromatique, les textures perceptibles et le style décoratif de cette composition de séjour.",
        "answer": (
            "OBSERVATION\n"
            "La scène met en valeur un mur peint dans une teinte vert sauge unie. Au centre est fixé un grand miroir circulaire à cerclage fin sombre, encadré par deux appliques murales ovales métalliques de teinte verte diffusant un halo lumineux vers le bas. Sous le miroir prend place une enfilade basse en bois clair équipée de trois portes en cannage ou rotin ajouré et de niches de rangement. À gauche, un panier tressé accueille une grande plante verte tropicale à larges feuilles. À droite, un fauteuil bas en cuir ou simili beige à structure métallique dorée est associé à un tabouret en bois tourné en forme de sablier. Un grand tapis tissé clair à motifs graphiques géométriques losangés couvre le sol.\n\n"
            "ANALYSE\n"
            "Le style emprunte aux codes du design scandinave et de la tendance bohème contemporaine. La palette chromatique repose sur une harmonie naturelle entre le vert sauge mat, les nuances boisées douces et la texture du cannage. Le grand miroir rond capte la lumière ambiante et agrandit visuellement l'espace perçu tout en brisant l'orthogonalité du buffet bas.\n\n"
            "POINTS FORTS\n"
            "- Choix cohérent de matériaux organiques (cannage, fibres végétales, bois clair, cuir).\n"
            "- Douceur de l'éclairage d'ambiance assuré par les deux appliques murales.\n"
            "- Graphisme soigné du grand miroir et du tapis à motifs géométriques.\n\n"
            "POINTS DE VIGILANCE\n"
            "- L'essence exacte du bois du buffet (chêne clair, frêne ou placage) et la matière exacte des parois ne peuvent être identifiées sans fiche produit.\n"
            "- La profondeur exacte de l'enfilade n'est pas mesurable sur l'image.\n\n"
            "RECOMMANDATION\n"
            "Privilégier des ampoules à température chaude (environ 2700 K) dans les appliques pour sublimer la tonalité vert sauge du mur sans la rendre terne en soirée."
        )
    },
    {
        "id": "archi_008",
        "category": "STYLE / MATERIAUX / AMBIANCE",
        "space_type": "salle de bain",
        "style": "contemporain",
        "image": "images/archi_008.jpg",
        "context": "Salle de bain contemporaine lumineuse avec meuble double vasque, cabine de douche vitrée et baignoire encastrée.",
        "question": "Quels sont les matériaux, les contrastes de textures et les choix de robinetterie identifiables dans cette salle de bain ?",
        "answer": (
            "OBSERVATION\n"
            "La salle de bain comporte sur la droite un meuble sous-vasque linéaire à façades gris-bleu foncé et poignées étriers noires, surmonté d'un plan blanc intégrant deux vasques et de mitigeurs noirs mats. Au-dessus est fixé un large miroir rectangulaire encadré de bois foncé à texture rustique. À gauche, une cabine de douche fermée par des parois en verre transparent présente un carrelage mural rectangulaire blanc type carreaux de métro et un sol en petites mosaïques hexagonales sombres, complétée d'une pomme de douche noire. Au premier plan à gauche se trouve une baignoire encastrée blanche munie de robinets noirs. Le sol de la pièce est revêtu de carreaux gris à motif rappelant des lattes de bois.\n\n"
            "ANALYSE\n"
            "Le projet combine une base contemporaine nette (carrelage métro blanc, meubles géométriques gris foncé, robinetterie noire mate graphique) avec des accents plus texturés apportés par le cadre de miroir en bois brut et les petites étagères murales. Ce contraste atténue la rigueur clinique souvent associée aux carreaux blancs et confère une atmosphère de bain soignée.\n\n"
            "POINTS FORTS\n"
            "- Lisibilité des volumes et zonage fonctionnel net entre bain, douche et plan vasque.\n"
            "- Finition noire mate de la robinetterie créant une ponctuation graphique sur les surfaces blanches.\n"
            "- Apport de lumière naturelle direct par la fenêtre translucide de la douche.\n\n"
            "POINTS DE VIGILANCE\n"
            "- La mosaïque hexagonale foncée et les nombreux joints de carrelage en milieu humide exigent un entretien régulier contre les dépôts calcaires.\n"
            "- La nature exacte du plan de travail (quartz composite, marbre ou résine synthétique) ne peut être certifiée visuellement.\n\n"
            "RECOMMANDATION\n"
            "Appliquer un traitement anticalcaire régulier sur les parois de douche vitrées et s'assurer d'une ventilation mécanique efficace pour préserver le cadre de miroir en bois de l'humidité."
        )
    },
    {
        "id": "archi_009",
        "category": "STYLE / MATERIAUX / AMBIANCE",
        "space_type": "salon",
        "style": "éclectique",
        "image": "images/archi_009.jpg",
        "context": "Détail d'une composition murale décorative sur paroi blanche unie, associant objets d'artisanat, cadres et végétation.",
        "question": "Identifiez les matières, les objets décoratifs et l'approche stylistique observables sur cette composition murale.",
        "answer": (
            "OBSERVATION\n"
            "La photographie cadre une composition murale d'art et d'objets sur une paroi peinte en blanc lisse. On identifie un masque allongé en bois sculpté, deux caissons étagères en bois patiné évoquant des tiroirs anciens reconvertis, un cadre illustrant des branchages bleus et un petit cadre à gauche représentant un poisson multicolore. Des éléments végétaux en pots de terre cuite (plante retombante, petit cactus, jeune arbuste) sont disposés sur l'étagère aux côtés d'une carafe en céramique vernissée vert émeraude ornée d'un motif solaire et de petites figurines. À droite est suspendu un appareil photo argentique noir par sa bandoulière.\n\n"
            "ANALYSE\n"
            "La composition relève d'une scénographie murale éclectique et poétique, associant objets artisanaux ethniques (masque, céramique), mobilier d'upcycling (tiroirs en bois brut transformés en étagères), art graphique et végétation vivante. L'asymétrie de l'agencement et la diversité des matières (bois brut, terre cuite, céramique émaillée, papier d'art) animent le mur blanc sans recourir à un mobilier lourd.\n\n"
            "POINTS FORTS\n"
            "- Variété sensorielle et richesse texturale des objets présentés.\n"
            "- Présence végétale apportant de la fraîcheur contre la paroi blanche.\n"
            "- Personnalité décorative singulière évitant la standardisation.\n\n"
            "POINTS DE VIGILANCE\n"
            "- La résistance des fixations murales pour supporter des pots de terre cuite et objets décoratifs ne peut être vérifiée sur l'image.\n"
            "- La paroi blanche sous les pots de plantes présente un risque de salissure lors des arrosages en cas de débordement.\n\n"
            "RECOMMANDATION\n"
            "Utiliser des sous-coupes étanches sous chaque pot en terre cuite afin de protéger le bois patiné des étagères et le mur blanc de toute infiltration d'humidité lors de l'arrosage."
        )
    },

    # ---------------------------------------------------------
    # 3. ERGONOMIE / CIRCULATION (archi_011 à archi_014)
    # ---------------------------------------------------------
    {
        "id": "archi_011",
        "category": "ERGONOMIE / CIRCULATION",
        "space_type": "cuisine",
        "style": "contemporain",
        "image": "images/archi_011.jpg",
        "context": "Poste de cuisson au gaz sur îlot ou plan de travail central dans une cuisine contemporaine, cadré pendant la préparation d'un repas.",
        "question": "Que peut-on observer de l'ergonomie du poste de travail et de l'accessibilité des ustensiles sur cette prise de vue d'une cuisine en activité ?",
        "answer": (
            "OBSERVATION\n"
            "La photographie montre en cadrage rapproché un poste de cuisson encastré dans un plan de travail en pierre ou composite veiné clair. Une cocotte en fonte émaillée orange est posée sur la grille en fonte d'une plaque de cuisson au gaz. À proximité immédiate sur le plan sont disposés un pot d'ustensiles contenant des cuillères et spatules, des boîtes de conservation étanches avec couvercles en bois, ainsi qu'un bol de citrons et des herbes aromatiques. En arrière-plan se déploie un linéaire de meubles hauts blancs sans poignées saillantes, une crédence grise avec zone d'évier sur la gauche, et une colonne verticale à droite intégrant un micro-ondes et un four encastrés en inox.\n\n"
            "ANALYSE\n"
            "L'ergonomie du plan de préparation visible est optimisée pour la tâche culinaire : les outils de manipulation et les condiments usuels sont positionnés dans le rayon de préhension direct de l'utilisateur, évitant les gestes parasites. L'implantation du four et du micro-ondes en colonne à hauteur intermédiaire participe au confort d'utilisation en limitant les flexions pour surveiller la cuisson.\n\n"
            "POINTS FORTS\n"
            "- Accessibilité immédiate des ustensiles et ingrédients sur la surface de travail.\n"
            "- Façades de meubles épurées limitant les aspérités.\n"
            "- Intégration en hauteur des appareils de cuisson visible à droite.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Le cadrage serré ne montre pas le sol ni les couloirs de circulation de la cuisine : il est impossible d'évaluer les largeurs de passage, les dégagements entre meubles ou la fluidité des flux généraux sans vue d'ensemble ou plan coté.\n"
            "- Aucun problème ergonomique évident ne peut être établi pour les zones non visibles de la pièce.\n\n"
            "RECOMMANDATION\n"
            "Veiller à conserver une zone libre d'au moins 30 à 40 cm de chaque côté de la plaque de cuisson pour déposer sans encombre les récipients chauds en cours de préparation."
        )
    },
    {
        "id": "archi_012",
        "category": "ERGONOMIE / CIRCULATION",
        "space_type": "espace ouvert",
        "style": "contemporain",
        "image": "images/archi_012.jpg",
        "context": "Espace lounge ou zone d'accueil partagée dans un environnement de travail contemporain ou de coworking.",
        "question": "Analysez la fluidité des circulations, le positionnement du mobilier et l'ergonomie d'assise dans cet espace d'accueil et de détente.",
        "answer": (
            "OBSERVATION\n"
            "La scène présente un espace d'attente ou de détente partagé. Au premier plan, deux fauteuils bas tapissés de tissu gris clair à pieds en bois sont disposés autour d'une petite table basse ronde claire. En retrait, deux fauteuils vert sapin sont orientés vers un canapé modulaire d'angle gris clair placé sous une grande baie vitrée à châssis blanc. Un meuble bas à casiers ouverts en bois clair borde l'espace sur la droite. Un lampadaire sur pied noir articulé à deux bras métalliques surplombe la zone. Le fond est bordé par une cloison vitrée à ossature en bois clair munie d'une porte avec bloc de secours. Des tapis vert d'eau reposent sur un sol clair uni.\n\n"
            "ANALYSE\n"
            "L'implantation du mobilier organise deux sous-groupes d'assises (fauteuils individuels au premier plan et canapé lounge d'angle au fond) tout en laissant un couloir central visuellement dégagé menant vers la porte de circulation au fond. La hauteur d'assise basse et les dossiers inclinés privilégient une posture décontractée d'attente ou d'échange informel.\n\n"
            "POINTS FORTS\n"
            "- Cheminement central libre permettant le passage sans contournement complexe.\n"
            "- Disposition modulaire favorisant des interactions en petits groupes.\n"
            "- Luminosité naturelle abondante provenant des baies vitrées latérales.\n\n"
            "POINTS DE VIGILANCE\n"
            "- L'envergure des bras du grand lampadaire noir doit être surveillée pour ne pas empiéter sur le gabarit de passage d'une personne debout.\n"
            "- Les largeurs exactes des couloirs de circulation entre les assises ne peuvent être certifiées sans plan d'aménagement coté.\n\n"
            "RECOMMANDATION\n"
            "S'assurer que le positionnement du lampadaire laisse une hauteur libre minimale de 2 mètres sous ses réflecteurs au niveau de la zone de marche pour éliminer tout risque de heurt de tête."
        )
    },
    {
        "id": "archi_013",
        "category": "ERGONOMIE / CIRCULATION",
        "space_type": "salon",
        "style": "contemporain",
        "image": "images/archi_013.jpg",
        "context": "Grand salon sous plafond cathédrale à double hauteur avec escalier monumental desservant une mezzanine et ouverture sur cuisine.",
        "question": "Analysez la hiérarchie des circulations verticales et horizontales ainsi que l'organisation des flux dans cette vaste pièce de vie avec mezzanine.",
        "answer": (
            "OBSERVATION\n"
            "La pièce développe un grand volume à double hauteur intégrant un escalier avec rampe en bois sombre et barreaux blancs, menant à une mezzanine ouverte à l'étage. L'espace salon est meublé de deux grands canapés en tissu blanc cassé se faisant face, complétés par deux fauteuils assortis et une table basse rectangulaire en bois et métal noir posée sur un tapis gris. Le sol est un parquet sombre. Au fond, une large baie libre sans porte ouvre sur une cuisine équipée comprenant un îlot central sombre à tabourets hauts. Des fenêtres à persiennes intérieures blanches habillent le mur de droite.\n\n"
            "ANALYSE\n"
            "L'espace articule une double circulation : un flux vertical majeur via l'escalier visible dès l'entrée du salon et un flux horizontal direct reliant la zone de repos à la cuisine ouverte. La disposition des deux canapés en parallèle encadre la table basse tout en ménageant de larges couloirs de passage latéraux qui préservent la fluidité des cheminements entre les différents pôles de la maison.\n\n"
            "POINTS FORTS\n"
            "- Clarté et lisibilité des parcours de circulation entre l'étage, le séjour et la cuisine.\n"
            "- Dégagements au sol très généreux autour du groupe d'assises.\n"
            "- Continuité spatiale et visuelle amplifiée par le vide sur séjour.\n\n"
            "POINTS DE VIGILANCE\n"
            "- La hauteur de chute depuis la mezzanine impose une conformité rigoureuse du garde-corps (hauteur minimale et espacement des barreaux) impossible à mesurer sur la photo.\n"
            "- L'absence de plan métré interdit de quantifier la largeur exacte des marches de l'escalier et des passages.\n\n"
            "RECOMMANDATION\n"
            "Veiller à maintenir la zone de départ de l'escalier parfaitement libre de tout petit mobilier d'appoint ou tapis glissant pour garantir une montée et une descente en toute sécurité."
        )
    },
    {
        "id": "archi_014",
        "category": "ERGONOMIE / CIRCULATION",
        "space_type": "salon",
        "style": "scandinave",
        "image": "images/archi_014.jpg",
        "context": "Salon lumineux avec parquet en chêne posé en chevrons, privilégiant un aménagement périphérique aéré.",
        "question": "Évaluez la liberté de circulation au sol et le dégagement des passages dans ce salon contemporain.",
        "answer": (
            "OBSERVATION\n"
            "La pièce présente un salon revêtu d'un sol en bois posé en chevrons (motif point de Hongrie). Le mobilier se répartit en périphérie : à gauche, un canapé droit tapissé de velours bleu profond ; au centre, un fauteuil blanc à coque sur piètement métallique fin garni d'une peau lainée claire ; à droite, un meuble bas linéaire blanc supporte un écran de télévision, des bougeoirs et des plantes en pot. Une fenêtre à trois vantaux avec radiateur en allège et rideaux à motifs végétaux habille le mur du fond. Un lampadaire blanc sur pied complète l'ensemble.\n\n"
            "ANALYSE\n"
            "L'organisation spatiale fait le choix de dégager entièrement l'aire centrale de la pièce en s'abstenant d'installer une table basse imposante au milieu. Cette décision libère une zone de circulation particulièrement fluide et continue entre le canapé, le meuble télévision et l'accès à la fenêtre, tout en mettant en valeur la continuité graphique du parquet en chevrons.\n\n"
            "POINTS FORTS\n"
            "- Circulation au sol totalement dégagée et sans entrave matérielle.\n"
            "- Excellente liberté de mouvement pour les déplacements du quotidien.\n"
            "- Dégagement complet de l'accès à la fenêtre et au radiateur.\n\n"
            "POINTS DE VIGILANCE\n"
            "- L'absence de table basse centrale, si elle optimise le flux piéton, impose d'ajouter un petit support d'appoint près du canapé pour déposer une tasse ou un livre.\n"
            "- Les cotes réelles de passage ne peuvent être validées sans plan d'architecte coté.\n\n"
            "RECOMMANDATION\n"
            "Intégrer une petite table d'appoint légère de type bout de canapé glissée sous l'assise bleue afin d'offrir une surface de pose sans encombrer le couloir de circulation central."
        )
    },

    # ---------------------------------------------------------
    # 4. CRITIQUE DE PROJET (archi_016 à archi_019)
    # ---------------------------------------------------------
    {
        "id": "archi_016",
        "category": "CRITIQUE DE PROJET",
        "space_type": "salon",
        "style": "contemporain",
        "image": "images/archi_016.jpg",
        "context": "Coin lecture et détente contemporain agencé autour d'un fauteuil jaune moutarde, d'un lampadaire tubulaire et d'un tableau géométrique.",
        "question": "Réalisez une critique architecturale et décorative de ce coin lecture en évaluant ses partis-pris graphiques, ses qualités et ses limites potentielles.",
        "answer": (
            "OBSERVATION\n"
            "La composition met en scène un fauteuil d'appoint jaune moutarde à pieds métalliques noirs, adossé à une paroi blanche sur laquelle est accroché un tableau d'art abstrait géométrique figurant un disque noir et des lignes fines dans un cadre noir. À gauche, un lampadaire d'architecte minimaliste en laiton doré brossé déploie son montant vertical et son bras coudé. À droite du fauteuil, une sellette fine avec plateau en marbre et socle en pierre accueille un vase garni de branchages. Sur la droite, un meuble bas blanc linéaire supporte des éléments sous un écran noir, tandis qu'à gauche s'élève un meuble haut sombre à moulures. Le sol est un parquet en bois clair bordé d'un tapis à motifs graphiques.\n\n"
            "ANALYSE\n"
            "Le parti-pris décoratif repose sur un contraste visuel maîtrisé : la silhouette jaune lumineuse du fauteuil agit comme accent chromatique fort face à la rigueur bicolore noir et blanc de l'art mural et des menuiseries sombres. L'équilibre géométrique est rigoureusement composé, le lampadaire doré apportant une ligne graphique aérienne qui verticalise l'espace sans l'alourdir.\n\n"
            "POINTS FORTS\n"
            "- Choix affirmé d'une couleur d'accent (jaune moutarde) rompant avec succès la monotonie des teintes neutres.\n"
            "- Dialogue visuel réussi entre le tableau d'art géométrique et le lampadaire tubulaire.\n"
            "- Finitions soignées des matériaux (laiton brossé, marbre, bois).\n\n"
            "POINTS DE VIGILANCE\n"
            "- La sellette d'appoint présente une surface de dépose très restreinte, déjà occupée par le vase à fleurs, limitant la possibilité d'y poser un livre ou une tasse sans risque d'instabilité.\n"
            "- La source lumineuse du lampadaire, très directive et tubulaire, semble conçue pour une lecture ponctuelle plutôt que pour éclairer l'ambiance globale du coin.\n\n"
            "RECOMMANDATION\n"
            "Déplacer le grand vase sur le meuble bas voisin pour libérer la sellette en marbre à des fins d'usage pratique lors des moments de lecture dans le fauteuil."
        )
    },
    {
        "id": "archi_017",
        "category": "CRITIQUE DE PROJET",
        "space_type": "chambre",
        "style": "contemporain",
        "image": "images/archi_017.jpg",
        "context": "Chambre contemporaine lumineuse aux teintes neutres grises et blanches, équipée d'un lit capitonné et d'un coin fauteuil.",
        "question": "Formulez une critique constructive de l'aménagement de cette chambre parentale en examinant le confort perçu, les proportions et l'équilibre des teintes.",
        "answer": (
            "OBSERVATION\n"
            "La chambre est organisée autour d'un lit double doté d'une tête de lit capitonnée en tissu gris et d'une literie blanche texturée avec coussins d'ornement gris et noirs. Au-dessus de la tête de lit est fixé un tableau horizontal représentant un mouton en noir et blanc. À gauche se trouve une table de chevet au plateau clair et piétement en métal doré surmontée d'une lampe de table. À droite, sous une fenêtre à double vantail avec store enrouleur, est installé un fauteuil bas d'appoint gris foncé accompagné d'un guéridon tripode doré. Le plafond blanc plat accueille un plafonnier circulaire simple. Le sol est revêtu d'un parquet brun foncé partiellement couvert par un tapis gris chiné.\n\n"
            "ANALYSE\n"
            "L'aménagement applique un parti-pris chromatique sobre et apaisant, dominé par une déclinaison de blancs, de gris et de textures textiles propices au repos. La symétrie habituelle de la chambre est ici brisée par le choix d'installer un coin lecture avec fauteuil côté fenêtre, apportant une fonction complémentaire à la pièce.\n\n"
            "POINTS FORTS\n"
            "- Atmosphère calme et reposante créée par la palette monochrome neutre.\n"
            "- Luminosité naturelle directe bien orientée sur le coin fauteuil.\n"
            "- Cohérence des détails métalliques dorés entre le chevet et le guéridon d'appoint.\n\n"
            "POINTS DE VIGILANCE\n"
            "- L'ambiance générale peut sembler légèrement impersonnelle ou standardisée en raison de l'absence de touches de couleurs plus chaleureuses.\n"
            "- L'espace de passage entre le pied du lit et le mur opposé n'est pas mesurable sur cette prise de vue.\n\n"
            "RECOMMANDATION\n"
            "Introduire des textiles aux tonalités chaudes naturelles (plaid en laine ocre, coussins terracotta ou rideaux en lin naturel de part et d'autre de la fenêtre) pour réchauffer subtilement l'ambiance sans altérer sa sérénité."
        )
    },
    {
        "id": "archi_018",
        "category": "CRITIQUE DE PROJET",
        "space_type": "salle de bain",
        "style": "minimaliste",
        "image": "images/archi_018.jpg",
        "context": "Salle de bain contemporaine épurée avec baignoire îlot, meuble vasque suspendu laqué et fente vitrée verticale.",
        "question": "Portez un regard critique sur le choix des équipements, l'organisation spatiale et le traitement minimaliste de cette salle de bain contemporaine.",
        "answer": (
            "OBSERVATION\n"
            "La salle de bain met en scène une baignoire îlot ovale d'un blanc mat ou satiné, équipée d'un mitigeur et d'une douchette murale chromés encastrés dans la paroi blanche. Un pont de baignoire en bois clair supporte des flacons de soin. Sur la gauche sont fixées deux barres porte-serviettes métalliques chromées. Sur la droite au premier plan, un meuble vasque suspendu blanc à tiroirs intégrés supporte une vasque ovale à poser et un mitigeur mural chromé, surmonté d'un grand miroir affleurant. Dans l'angle se dresse une haute fenêtre verticale étroite cadrant la lumière extérieure, devant laquelle est installée une plante verte à feuillage large. Le sol est composé de grands carreaux gris.\n\n"
            "ANALYSE\n"
            "Le projet revendique une esthétique minimaliste inspirée de l'hôtellerie haut de gamme. Le meuble suspendu décolle les volumes du sol, amplifiant l'impression d'espace et facilitant l'entretien. L'insertion d'une meurtrière vitrée toute hauteur apporte une percée visuelle poétique vers l'extérieur sans compromettre la pudeur de l'occupant. La présence végétale au pied de l'ouverture humanise la rigueur des surfaces lisses.\n\n"
            "POINTS FORTS\n"
            "- Lignes architecturales épurées et intégration soignée de la robinetterie encastrée murale.\n"
            "- Excellent meuble suspendu à tiroirs offrant un volume de rangement discret mais généreux.\n"
            "- Valorisation de la lumière naturelle par la fente vitrée verticale.\n\n"
            "POINTS DE VIGILANCE\n"
            "- L'absence de paroi de douche dédiée dans ce cadrage suggère soit une baignoire servant aussi de douche (ce qui générerait des projections d'eau sur le sol carrelé sans rideau), soit une zone de douche séparée hors champ non vérifiable.\n"
            "- La glissance du carrelage gris lorsqu'il est mouillé doit être surveillée.\n\n"
            "RECOMMANDATION\n"
            "Prévoir un tapis de bain absorbant et antidérapant au pied de la baignoire îlot pour sécuriser la sortie du bain et protéger le sol des éclaboussures."
        )
    },
    {
        "id": "archi_019",
        "category": "CRITIQUE DE PROJET",
        "space_type": "espace extérieur",
        "style": "contemporain",
        "image": "images/archi_019.jpg",
        "context": "Terrasse d'une villa contemporaine de plain-pied avec piscine privée, auvent en béton et baies vitrées coulissantes.",
        "question": "Analysez de manière critique la conception architecturale de cette terrasse avec piscine et son dialogue avec le pavillon contemporain.",
        "answer": (
            "OBSERVATION\n"
            "La photographie montre l'espace extérieur d'une villa contemporaine sous un ciel ensoleillé. Au premier plan apparaît l'eau turquoise d'une piscine bordée par une large terrasse revêtue de grands carreaux clairs à joints réguliers. Le bâtiment de plain-pied se caractérise par des façades blanches, un débord de toiture plat en béton et de larges baies vitrées coulissantes aux montants gris anthracite. À travers les vitres sont visibles une table de salle à manger et des chaises contemporaines. À gauche se trouvent une colonne de douche extérieure métallique et de la végétation méditerranéenne (palmiers). À l'étage, un toit-terrasse est sécurisé par un garde-corps vitré.\n\n"
            "ANALYSE\n"
            "Le projet exprime un langage architectural moderne net (style balnéaire contemporain). Le débord de toiture joue un rôle bioclimatique essentiel en assurant une protection solaire passive (casquette) sur les baies vitrées pour limiter les apports thermiques directs en été. La terrasse de plain-pied supprime les seuils de franchissement vers le salon, matérialisant une transition continue entre l'eau, la terrasse et l'intérieur.\n\n"
            "POINTS FORTS\n"
            "- Cohérence des lignes pures et géométriques de la toiture en auvent.\n"
            "- Continuité de niveau fluide entre la plage de piscine et les pièces de vie intérieures.\n"
            "- Clarté générale du dallage valorisant la teinte azurée du bassin.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Le dallage extérieur blanc très clair, bien qu'élégant et limitant l'accumulation de chaleur sous les pieds, peut provoquer un fort éblouissement par temps très ensoleillé.\n"
            "- Le coefficient d'adhérence antidérapant (norme pieds nus mouillés) du carrelage n'est pas vérifiable à l'image.\n\n"
            "RECOMMANDATION\n"
            "Vérifier la conformité de la classe antidérapante des dalles autour de la piscine (classe C / R11 minimum recommandée en bord de bassin) pour prévenir tout risque de glissade sur sol mouillé."
        )
    },

    # ---------------------------------------------------------
    # 5. PROPOSITION D'AMÉLIORATION (archi_021 à archi_024)
    # ---------------------------------------------------------
    {
        "id": "archi_021",
        "category": "PROPOSITION D'AMÉLIORATION",
        "space_type": "cuisine",
        "style": "industriel",
        "image": "images/archi_021.jpg",
        "context": "Poste de cuisson chaud en cuisine professionnelle de restaurant, immortalisé pendant une opération de flambage à la poêle.",
        "question": "Quelles propositions d'amélioration pouvez-vous formuler pour optimiser la sécurité, l'organisation spatiale et la gestion des flux d'air au niveau de ce poste de cuisson professionnel ?",
        "answer": (
            "OBSERVATION\n"
            "La photographie montre un chef cuisinier réalisant un flambage à la poêle au-dessus d'un piano de cuisson professionnel au gaz en acier inoxydable. Une flamme vive s'élève au-dessus du brûleur. Le cuisinier tient de la main gauche une bouteille d'alcool entourée d'un linge. Le poste comprend une crédence murale en tôle d'acier inoxydable, une étagère haute supportant des casseroles et récipients, ainsi qu'une marmite posée sur un feu arrière. L'éclairage est chaud et directionnel.\n\n"
            "ANALYSE\n"
            "En cuisine de restauration, le poste de cuisson vif est une zone à haut niveau d'exigence ergonomique et sécuritaire. La manipulation simultanée d'une bouteille inflammable et d'une poêle embrasée présente des risques inhérents de brûlure ou de projection. L'aménagement de l'espace doit impérativement garantir un dégagement suffisant autour du cuisinier et une extraction thermique performante.\n\n"
            "POINTS FORTS\n"
            "- Robustesse et hygiène irréprochable des surfaces en acier inoxydable faciles à désinfecter.\n"
            "- Espace de travail adapté aux manipulations culinaires intenses.\n"
            "- Étagère haute maintenant les ustensiles à portée de main.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Risque d'inflammation accidentelle lors de la manipulation directe d'une bouteille d'alcool près d'une flamme ouverte.\n"
            "- L'absence d'une vue sur le groupe d'extraction (hotte professionnelle et filtres) ne permet pas de contrôler visuellement la capacité d'évacuation des fumées.\n\n"
            "RECOMMANDATION\n"
            "1. Observation : La bouteille d'alcool est manipulée à la main directement au-dessus des feux vifs.\n"
            "PROBLÈME POTENTIEL : Risque de retour de flamme ou de chute de la bouteille sur le plan chaud.\n"
            "ACTION PROPOSÉE : Définir un protocole de portionnement préalable dans un petit godet doseur inox posé sur une tablette latérale réfractaire.\n"
            "EFFET ATTENDU : Élimination du risque d'embrasement du contenant en verre et sécurisation du geste.\n\n"
            "2. Observation : Présence de flammes hautes lors du flambage.\n"
            "PROBLÈME POTENTIEL : Encrassement rapide des éléments hauts par les vapeurs grasses.\n"
            "ACTION PROPOSÉE : Contrôler la présence d'une hotte à induction compensée avec filtres à chocs en inox nettoyés quotidiennement et système d'extinction automatique intégré.\n"
            "EFFET ATTENDU : Évacuation immédiate des fumées et conformité aux normes de sécurité incendie en cuisine professionnelle."
        )
    },
    {
        "id": "archi_022",
        "category": "PROPOSITION D'AMÉLIORATION",
        "space_type": "salon",
        "style": "vintage",
        "image": "images/archi_022.jpg",
        "context": "Salon de style vintage éclectique caractérisé par un mur d'accent vert canard, une galerie photo et un canapé en cuir cognac.",
        "question": "Quelles améliorations spatiales, ergonomiques et d'éclairage proposez-vous pour enrichir ce salon au mur d'accent vert canard ?",
        "answer": (
            "OBSERVATION\n"
            "La pièce met en valeur un mur d'accent peint en vert canard foncé, décoré d'une composition centrale de six cadres noirs avec photographies en noir et blanc et de deux têtes de cerfs décoratives blanches sculptées. Devant ce mur est installé un canapé en cuir couleur cognac garni de coussins et d'un plaid. Une table basse circulaire noire à deux niveaux repose sur un tapis clair à motifs graphiques noirs. Sur la gauche, un tabouret en métal et une grande plante en pot bordent une fenêtre habillée d'un rideau blanc. Sur la droite se trouvent un fauteuil vintage à structure bois et cuir noir, une table d'appoint noire, un lampadaire arc en métal doré et une plante sur pied doré. Le sol est un parquet clair.\n\n"
            "ANALYSE\n"
            "L'ambiance associe avec succès l'intensité du vert foncé et la chaleur du cuir camel dans un esprit rétro-chic affirmé. Toutefois, le regroupement de plusieurs meubles d'appoint et luminaires sur le côté droit crée une asymétrie de densité visuelle par rapport au côté gauche plus aéré.\n\n"
            "POINTS FORTS\n"
            "- Contraste chromatique puissant et élégant entre le vert profond du mur et le cuir cognac du canapé.\n"
            "- Rythme rigoureux apporté par la grille de cadres photos.\n"
            "- Qualité de la lumière naturelle provenant de la grande fenêtre latérale.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Concentration d'éléments sur le flanc droit (fauteuil, table d'appoint, lampadaire et plante en pot) pouvant encombrer le passage.\n"
            "- La puissance lumineuse du lampadaire orientable ne peut être testée de jour.\n\n"
            "RECOMMANDATION\n"
            "1. Observation : Accumulation sur le flanc droit d'un fauteuil, d'une sellette, d'un lampadaire doré et d'un cache-pot haut.\n"
            "PROBLÈME POTENTIEL : Sensation de saturation spatiale et circulation contrainte dans l'angle droit.\n"
            "ACTION PROPOSÉE : Déplacer la plante sur pied doré vers un autre angle de la pièce pour donner plus de respiration autour du fauteuil noir et du lampadaire.\n"
            "EFFET ATTENDU : Circulation fluidifiée et valorisation accrue des lignes du lampadaire doré.\n\n"
            "2. Observation : Le mur d'accent sombre absorbe naturellement une partie importante de la lumière ambiante.\n"
            "PROBLÈME POTENTIEL : Risque d'assombrissement marqué de la pièce une fois la nuit tombée.\n"
            "ACTION PROPOSÉE : Ajouter un éclairage indirect discret (ruban LED blanc chaud ou appliques orientables) pour souligner la texture du mur vert sans éblouissement.\n"
            "EFFET ATTENDU : Mise en valeur nocturne de la galerie photographique et confort visuel renforcé."
        )
    },
    {
        "id": "archi_023",
        "category": "PROPOSITION D'AMÉLIORATION",
        "space_type": "salle de bain",
        "style": "naturel",
        "image": "images/archi_023.jpg",
        "context": "Salle de bain d'inspiration spa tropical associant une baignoire îlot en pierre sur lit de galets, une paroi minérale rugueuse et une douche ouverte.",
        "question": "Quelles solutions d'aménagement et d'optimisation d'usage préconisez-vous pour parfaire cette salle de bain d'inspiration spa minéral ?",
        "answer": (
            "OBSERVATION\n"
            "La photographie montre une salle de bain de style spa naturel. Au centre trône une grande baignoire îlot ovale monolithique en pierre ou béton de teinte sable, posée au-dessus d'un lit de galets blancs de rivière. Le mur arrière est recouvert d'un enduit texturé rugueux gris minéral, agrémenté d'un palmier d'intérieur. La robinetterie métallique est montée au niveau de la bordure arrière avec des flacons de cosmétiques sur plateau en bois. À gauche repose une échelle porte-serviettes en bois sombre avec des draps de bain blancs. À droite, un espace de douche ouverte de plain-pied est revêtu de grands carreaux beiges unis du sol au mur. La lumière naturelle diffuse semble provenir d'un éclairage zénithal.\n\n"
            "ANALYSE\n"
            "La conception privilégie une expérience sensorielle immersive axée sur la matière brute, le végétal et l'eau. L'association de l'enduit granuleux, des galets lisses et de la pierre polie de la baignoire compose une atmosphère de sanctuaire de bien-être. Néanmoins, la gestion de l'eau et l'entretien des zones de galets constituent des enjeux techniques majeurs.\n\n"
            "POINTS FORTS\n"
            "- Esthétique biophilique et minérale d'une remarquable cohérence.\n"
            "- Transition de plain-pied fluide vers l'espace douche.\n"
            "- Luminosité zénithale douce mettant en valeur les reliefs de la paroi.\n\n"
            "POINTS DE VIGILANCE\n"
            "- L'accumulation d'eau, de calcaire et de savon dans le lit de galets de rivière sous la baignoire pose des difficultés d'hygiène et de nettoyage à long terme si une bonde d'évacuation dédiée n'est pas prévue dessous.\n"
            "- La glissance des carreaux de douche mouillés doit être contrôlée.\n\n"
            "RECOMMANDATION\n"
            "1. Observation : La baignoire repose sur un encaissement rempli de galets de rivière naturels.\n"
            "PROBLÈME POTENTIEL : Stagnation d'eau savonneuse et formation d'humidité ou de moisissures sous les galets lors des sorties de bain.\n"
            "ACTION PROPOSÉE : S'assurer que le lit de galets est installé sur un bac étanche démontable raccordé à une évacuation siphonnée, ou surélever légèrement les galets sur une grille inox amovible pour faciliter le rinçage régulier.\n"
            "EFFET ATTENDU : Maintien d'une hygiène irréprochable sans altérer l'esthétique zen.\n\n"
            "2. Observation : Absence de niche ou de tablette de rangement dédiée aux produits d'hygiène dans la zone de douche visible à droite.\n"
            "PROBLÈME POTENTIEL : Pose des flacons directement au sol, encombrant la zone de douche de plain-pied.\n"
            "ACTION PROPOSÉE : Intégrer une niche encastrée étanche dans la paroi de carrelage beige de la douche.\n"
            "EFFET ATTENDU : Rangement fonctionnel discret respectant l'épure minérale du projet."
        )
    },
    {
        "id": "archi_024",
        "category": "PROPOSITION D'AMÉLIORATION",
        "space_type": "petit espace",
        "style": "contemporain",
        "image": "images/archi_024.jpg",
        "context": "Mur galerie graphique très dense associant plus d'une vingtaine de cadres d'art, deux étagères cimaises et de petites touches végétales.",
        "question": "Quelles recommandations structurelles et esthétiques proposez-vous pour restructurer et mettre en valeur ce mur galerie d'art graphique particulièrement dense ?",
        "answer": (
            "OBSERVATION\n"
            "L'image cadre un mur blanc entièrement habillé d'une composition galerie dense comprenant de multiples cadres aux dimensions et finitions variées (bois clair, laiton doré, blanc et noir). Deux étagères murales pour tableaux (cimaises) sont fixées au mur : une étagère supérieure blanche portant de petits cadres et un pot doré de fleurs, et une étagère intermédiaire noire accueillant deux cadres et une plante verte en pot doré. Les œuvres affichées mêlent des visuels botaniques (grande feuille de monstera verte), des motifs géométriques à dorures, des représentations animales (oiseau, papillon) et une inscription typographique « HOME ». Ni le sol ni le mobilier bas ne sont visibles dans ce cadrage.\n\n"
            "ANALYSE\n"
            "Ce mur galerie mise sur un effet de foisonnement visuel joyeux et coloré. La combinaison de cadres posés sur cimaises et de cadres fixés directement au mur crée du relief. Toutefois, l'absence de ligne de force ou de respiration visuelle claire entre les œuvres peut générer une sensation de surcharge et brouiller la lisibilité des pièces maîtresses.\n\n"
            "POINTS FORTS\n"
            "- Grande fraîcheur et dynamisme apportés par la palette de couleurs vives (vert végétal, turquoise, doré, rose).\n"
            "- Flexibilité de mise en scène offerte par les deux étagères cimaises pour renouveler les visuels sans percer le mur.\n\n"
            "POINTS DE VIGILANCE\n"
            "- L'alignement hétérogène des cadres et la proximité étroite des bordures peuvent fatiguer le regard.\n"
            "- L'ancrage mécanique des étagères murales doit être vérifié en fonction du poids cumulé des cadres et des pots.\n\n"
            "RECOMMANDATION\n"
            "1. Observation : La multiplicité des bordures et la proximité des cadres créent une sensation de saturation sans hiérarchie claire.\n"
            "PROBLÈME POTENTIEL : Perte d'impact des pièces maîtresses (comme la feuille de monstera ou l'oiseau).\n"
            "ACTION PROPOSÉE : Harmoniser les espacements en instaurant un écart régulier constant (entre 5 et 8 cm) entre les œuvres fixées au mur et aérer les cimaises en retirant un ou deux petits cadres.\n"
            "EFFET ATTENDU : Lisibilité visuelle nettement améliorée et valorisation accrue des illustrations principales.\n\n"
            "2. Observation : Absence de système d'éclairage dédié perceptible au-dessus de la composition.\n"
            "PROBLÈME POTENTIEL : Rendu terne des dorures et contrastes graphiques en lumière ambiante indirecte ou en soirée.\n"
            "ACTION PROPOSÉE : Installer en partie haute un rail de spots orientables de type galerie d'art à faisceau ajustable (IRC > 90).\n"
            "EFFET ATTENDU : Révélation des reflets dorés et mise en scène scénographique de l'ensemble mural."
        )
    }
]

VAL_DATA = [
    # ---------------------------------------------------------
    # 1. ANALYSE D'ESPACE (archi_005)
    # ---------------------------------------------------------
    {
        "id": "archi_005",
        "category": "ANALYSE D'ESPACE",
        "space_type": "petit espace",
        "style": "contemporain",
        "image": "images/archi_005.jpg",
        "context": "Pièce de vie compacte associant salon convivial et poste de télétravail dans une ambiance végétale vivante.",
        "question": "Analysez la cohabitation fonctionnelle entre espace de détente et poste de travail au sein de cette pièce de vie.",
        "answer": (
            "OBSERVATION\n"
            "La photographie montre un espace de vie partagé intégrant plusieurs fonctions. Au fond, un canapé deux places en tissu gris chiné est installé sous une fenêtre équipée de stores à lamelles. Devant lui se trouvent une table basse en bois de forme triangulaire arrondie, un tapis clair et une chaise en contreplaqué courbé en bois foncé. Sur la gauche, un buffet bas blanc supporte une bibliothèque ouverte remplie de livres et de plantes en pot. Sur la droite au premier plan est implanté un espace de travail comprenant un bureau en bois avec ordinateur, une chaise de bureau pivotante à dossier résille et une banquette. La végétation d'intérieur est omniprésente, au sol, sur le mobilier et en suspension. Le sol est un parquet en bois.\n\n"
            "ANALYSE\n"
            "La pièce optimise un volume restreint en superposant coin détente (salon) et poste d'activité (bureau). L'implantation du canapé sous la fenêtre libère l'axe central pour la circulation. Le stockage vertical concentré sur le linéaire gauche maximise le rangement des livres sans multiplier les meubles hauts isolés. La profusion de plantes vertes crée une continuité visuelle qui lie harmonieusement les deux zones d'activité.\n\n"
            "POINTS FORTS\n"
            "- Utilisation dense et vivante de l'espace disponible.\n"
            "- Bonne luminosité naturelle au niveau de l'assise du canapé.\n"
            "- Rangement vertical efficace grâce à la bibliothèque murale intégrée.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Proximité immédiate entre le fauteuil de bureau et la zone centrale du salon, pouvant restreindre le recul lors des déplacements si la chaise est reculée.\n"
            "- Absence d'indication métrique pour valider la largeur des passages restants au sol.\n\n"
            "RECOMMANDATION\n"
            "Dégager légèrement la zone de circulation centrale en regroupant certaines plantes au sol sur des supports verticaux à plusieurs niveaux pour fluidifier le cheminement entre le bureau et le salon."
        )
    },

    # ---------------------------------------------------------
    # 2. STYLE / MATERIAUX / AMBIANCE (archi_010)
    # ---------------------------------------------------------
    {
        "id": "archi_010",
        "category": "STYLE / MATERIAUX / AMBIANCE",
        "space_type": "cuisine",
        "style": "classique",
        "image": "images/archi_010.jpg",
        "context": "Cuisine américaine de style farmhouse chic blanc, avec îlot central gris, plan de cuisson inox et crédence en pierre veinée.",
        "question": "Identifiez les matériaux nobles, les finitions et le registre stylistique perceptibles dans cette cuisine avec îlot central.",
        "answer": (
            "OBSERVATION\n"
            "La cuisine s'articule autour d'un grand îlot central peint en gris clair, coiffé d'un plan de travail blanc intégrant un évier sous plan et un mitigeur col de cygne métallique. Deux tabourets hauts en cuir noir à piètement circulaire chromé sont disposés devant le plan snack. Les linéaires d'armoires toute hauteur présentent des façades blanches à rainures horizontales type lambris, rehaussées de fines poignées droites en laiton doré. Le poste de cuisson comprend une cuisinière en inox surmontée d'un bandeau de hotte en bois grisé. La crédence et la paroi arrière sont revêtues d'une plaque minérale blanche veinée de gris d'aspect marbre, encadrée de deux appliques murales sombres. Deux lustres sphériques suspendus en perles de verre ou cristal surplombent l'îlot.\n\n"
            "ANALYSE\n"
            "Le style s'inscrit dans le registre néo-classique américain (Modern Farmhouse haut de gamme). L'association du blanc immaculé des menuiseries, du marbre veiné et des touches dorées confère une élégance lumineuse et intemporelle. L'îlot gris clair apporte une rupture chromatique douce qui ancre le meuble au centre de la composition sans alourdir l'espace.\n\n"
            "POINTS FORTS\n"
            "- Finitions raffinées perceptibles sur les menuiseries, la robinetterie et les luminaires sphériques.\n"
            "- Dialogue harmonieux entre les surfaces blanches, la pierre veinée et les poignées en laiton.\n"
            "- Excellent niveau d'éclairement combinant appliques de crédence, suspensions et spots encastrés.\n\n"
            "POINTS DE VIGILANCE\n"
            "- La porosité potentielle du panneau mural veiné (s'il s'agit de marbre naturel plutôt que de quartz ou grès cérame) nécessite des précautions contre les projections d'huile et d'acides de cuisson.\n"
            "- Les dimensions précises de passage autour de l'îlot ne sont pas mesurables directement.\n\n"
            "RECOMMANDATION\n"
            "Si le matériau de crédence s'avère être du marbre naturel calcaire, renouveler régulièrement un traitement hydro-oléofuge de surface pour prévenir les taches grasses persistantes près de la zone de cuisson."
        )
    },

    # ---------------------------------------------------------
    # 3. ERGONOMIE / CIRCULATION (archi_015)
    # ---------------------------------------------------------
    {
        "id": "archi_015",
        "category": "ERGONOMIE / CIRCULATION",
        "space_type": "bureau",
        "style": "minimaliste",
        "image": "images/archi_015.jpg",
        "context": "Espace de télétravail scandinave épuré aménagé en angle, avec bureau sur tréteaux réglables et écran monobloc surélevé.",
        "question": "Analysez l'ergonomie posturale, l'agencement du plan de travail et la circulation dans ce coin bureau de télétravail.",
        "answer": (
            "OBSERVATION\n"
            "L'espace de travail comprend un bureau droit composé d'un plateau gris clair reposant sur deux tréteaux en bois peint en blanc, dotés d'une tablette basse de rangement. Sur le plateau sont installés un ordinateur tout-en-un à grand écran surélevé par un socle support, un clavier fin blanc, une souris et un sous-main noir de protection. Une lampe à trépied avec abat-jour cylindrique et une plante en pot blanc complètent le bureau. L'utilisateur dispose d'un fauteuil de bureau pivotant en cuir gris à accoudoirs chromés monté sur un piétement à roulettes. Une fenêtre latérale sur la gauche apporte de la lumière naturelle sur un sol d'aspect parquet gris clair.\n\n"
            "ANALYSE\n"
            "L'ergonomie du poste de travail est soignée : la surélévation de l'écran permet de positionner le haut de la dalle au niveau de la ligne d'horizon du regard, limitant la flexion du cou. L'orientation latérale par rapport à la fenêtre évite à la fois les reflets directs sur la dalle vitrée et l'éblouissement frontal. Le fauteuil à roulettes permet un recul aisé pour s'asseoir et se lever.\n\n"
            "POINTS FORTS\n"
            "- Bonne orientation bioclimatique du poste de travail perpendiculaire à l'ouverture naturelle.\n"
            "- Réhausseur d'écran favorisant une posture cervicale neutre.\n"
            "- Surface de travail ordonnée avec périphériques sans fil dégagés.\n\n"
            "POINTS DE VIGILANCE\n"
            "- Les tréteaux occupent une emprise latérale au sol qui peut réduire l'espace pour les jambes lors de mouvements latéraux.\n"
            "- La hauteur exacte du plateau et la profondeur du plan de travail ne peuvent être vérifiées sans mesure physique.\n\n"
            "RECOMMANDATION\n"
            "Utiliser la tablette basse des tréteaux ou installer un caisson à tiroirs compact sous le plateau pour ranger les documents et chargeurs afin de maintenir la surface de travail totalement libre."
        )
    },

    # ---------------------------------------------------------
    # 4. CRITIQUE DE PROJET (archi_020)
    # ---------------------------------------------------------
    {
        "id": "archi_020",
        "category": "CRITIQUE DE PROJET",
        "space_type": "salon",
        "style": "classique",
        "image": "images/archi_020.jpg",
        "context": "Salon de réception à composition symétrique axiale, habillé d'un canapé clair, de deux fenêtres et d'accents bleu canard et turquoise.",
        "question": "Évaluez de manière critique la composition symétrique, le travail chromatique et les limites de cet aménagement de salon transitionnel.",
        "answer": (
            "OBSERVATION\n"
            "La vue frontale cadre un canapé deux places en tissu clair, adossé à un mur peint dans une nuance grège. Le canapé est garni d'un ensemble de coussins déclinés dans des teintes bleu pétrole et des motifs géométriques bleus et beiges. Au-dessus est accroché un tableau abstrait vertical aux touches turquoise, vert d'eau et dorées. Deux fenêtres à petits bois flanquent le canapé de façon symétrique, habillées de stores textiles blancs bordés de bleu. Sous chaque fenêtre, une table d'appoint supporte une lampe à poser en verre soufflé à abat-jour blanc et des accessoires décoratifs en verre coloré. Au premier plan apparaissent deux grands vases en céramique émaillée turquoise.\n\n"
            "ANALYSE\n"
            "L'aménagement applique les principes classiques de la symétrie axiale rigoureuse : l'axe central du tableau et du canapé est équilibré de part et d'autre par les fenêtres, les tables et les luminaires identiques. La cohérence chromatique est totale, le bleu canard et le turquoise servant de fil conducteur reliant les coussins, les stores, le tableau et les céramiques décoratives.\n\n"
            "POINTS FORTS\n"
            "- Grande maîtrise de l'harmonie des couleurs et sensation de sérénité ordonnée.\n"
            "- Apport de lumière naturelle bilatérale bien distribué de chaque côté du canapé.\n"
            "- Élégance intemporelle du mobilier aux lignes transitionnelles.\n\n"
            "POINTS DE VIGILANCE\n"
            "- La rigueur presque clinique de la symétrie peut conférer à l'espace une atmosphère figée de salon d'exposition, laissant peu de place à la spontanéité d'un lieu habité au quotidien.\n"
            "- La profondeur de passage devant le canapé ne peut être calculée sans vue en plan.\n\n"
            "RECOMMANDATION\n"
            "Briser subtilement la stricte gémellité des tables d'appoint en variant les objets posés (par exemple en remplaçant l'une des compositions par une pile de beaux livres ou une plante tombante) pour insuffler davantage de naturel et de vie à la pièce."
        )
    },

    # ---------------------------------------------------------
    # 5. PROPOSITION D'AMÉLIORATION (archi_025)
    # ---------------------------------------------------------
    {
        "id": "archi_025",
        "category": "PROPOSITION D'AMÉLIORATION",
        "space_type": "petit espace",
        "style": "contemporain",
        "image": "images/archi_025.jpg",
        "context": "Vaste pièce à vivre lumineuse avec baies vitrées d'angle panoramiques, cheminée centrale et espace salle à manger attenant.",
        "question": "Quelles propositions architecturales et décoratives préconisez-vous pour moderniser cette vaste pièce de vie et mieux connecter ses différentes zones à la vue panoramique ?",
        "answer": (
            "OBSERVATION\n"
            "La photographie montre un grand espace de vie ouvert à triple orientation fonctionnelle. Au premier plan à gauche, un coin salon composé de deux fauteuils beiges garnis de coussins turquoise et d'une table d'appoint en bois avec lampe prend place devant de larges baies vitrées d'angle offrant une vue panoramique sur un paysage urbain et un plan d'eau. Au centre se trouve une cheminée encastrée dans un coffrage blanc mouluré surmonté d'un tableau, flanquée d'une plante verte et d'un fauteuil bleu. Sur la droite est installé un espace repas avec table ronde en bois et chaises rembourrées beiges, précédant un salon plus sombre avec canapé d'angle brun. Le sol est intégralement revêtu d'une moquette claire uniforme. Le plafond présente des décrochés avec spots encastrés.\n\n"
            "ANALYSE\n"
            "Le volume dispose d'un potentiel spatial et lumineux remarquable grâce à son panorama extérieur d'angle et sa généreuse superficie. Toutefois, le traitement uniforme de la moquette au sol et la dispersion du mobilier créent une sensation de flottement des espaces sans véritable hiérarchie moderne. Le salon sombre du fond semble déconnecté de la clarté de la façade vitrée.\n\n"
            "POINTS FORTS\n"
            "- Exceptionnelle luminosité naturelle et qualité des vues dégagées sur l'extérieur.\n"
            "- Présence chaleureuse de la cheminée centrale.\n"
            "- Volume généreux permettant de multiples agencements sans sensation d'étouffement.\n\n"
            "POINTS DE VIGILANCE\n"
            "- La moquette claire globale est sensible aux taches, en particulier dans la zone de la salle à manger.\n"
            "- L'absence de plan coté ne permet pas de mesurer les distances réelles entre la table de repas et le coin salon vitré.\n\n"
            "RECOMMANDATION\n"
            "1. Observation : Le revêtement de moquette claire est continu sur l'ensemble de la pièce, y compris sous la table à manger.\n"
            "PROBLÈME POTENTIEL : Entretien contraignant face aux miettes et projections alimentaires, et absence de matérialisation des limites de zones.\n"
            "ACTION PROPOSÉE : Remplacer la moquette par un sol dur pérenne (parquet en chêne clair ou grand carrelage grès cérame clair) sur toute la pièce de vie, et délimiter les zones de repos par de grands tapis textiles distincts.\n"
            "EFFET ATTENDU : Modernisation radicale de l'esthétique générale, entretien facilité et zonage visuel clair.\n\n"
            "2. Observation : Le mobilier d'angle vitré (deux fauteuils séparés par une table) tourne en partie le dos à la perspective de la pièce.\n"
            "PROBLÈME POTENTIEL : Sous-exploitation de la connexion visuelle entre le panorama extérieur et la zone centrale de réception.\n"
            "ACTION PROPOSÉE : Réorienter le coin salon vitré avec une méridienne basse ou deux chauffeuses pivotantes orientables à volonté vers la vue extérieure ou vers la cheminée.\n"
            "EFFET ATTENDU : Flexibilité d'usage accrue et dialogue visuel renforcé entre l'intérieur et le paysage panoramique."
        )
    }
]

def format_record(item):
    user_text = f"Contexte : {item['context']}\n\nQuestion : {item['question']}"
    convs = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": item["image"]},
                {"type": "text", "text": user_text}
            ]
        },
        {
            "role": "assistant",
            "content": [
                {"type": "text", "text": item["answer"]}
            ]
        }
    ]
    return {
        "id": item["id"],
        "category": item["category"],
        "space_type": item["space_type"],
        "style": item["style"],
        "image": item["image"],
        "context": item["context"],
        "question": item["question"],
        "answer": item["answer"],
        "conversations": convs
    }

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(root_dir, "dataset")
    train_path = os.path.join(dataset_dir, "train.jsonl")
    val_path = os.path.join(dataset_dir, "validation.jsonl")

    print(f"Écriture de {train_path} ({len(TRAIN_DATA)} exemples)...")
    with open(train_path, "w", encoding="utf-8") as f:
        for item in TRAIN_DATA:
            rec = format_record(item)
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"Écriture de {val_path} ({len(VAL_DATA)} exemples)...")
    with open(val_path, "w", encoding="utf-8") as f:
        for item in VAL_DATA:
            rec = format_record(item)
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print("Reconstruction terminée avec succès.")

if __name__ == "__main__":
    main()
