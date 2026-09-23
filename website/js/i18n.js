/* AXIS — i18n dictionary (FR default, EN available).
   Keys mirror the data-i18n paths used in index.html.

   Every number and status claim in this dictionary is sourced from the
   repository root docs (PROJECT_STATUS.md, DATASET.md, EVALUATION.md,
   ROADMAP.md, ARCHITECTURE.md) and the RUN-019 through RUN-023 folders.
   If those documents change, this file must be updated to match —
   never the other way around. See website/README.md. */
(function (global) {
  "use strict";

  var STRINGS = {
    fr: {
      nav: { home: "Accueil", studio: "Studio", models: "Modèles", research: "Recherche", data: "Données", community: "Communauté" },
      hero: {
        kicker: "SYSTÈME D'INTELLIGENCE EXPERTE ARCHITECTURALE",
        title: { l1: "UNE INTELLIGENCE", l2: "ARCHITECTURALE,", l3: "CONSTRUITE SUR LA PREUVE" },
        desc: "AXIS est un projet de recherche qui développe des modèles capables de percevoir, représenter et raisonner sur l'espace architectural — et qui mesure précisément ce qui est déjà démontré de ce qui reste à prouver.",
        cta: { studio: "Explorer AXIS Studio", research: "Explorer la recherche", github: "Voir sur GitHub" },
        anno: {
          geometry: "GÉOMÉTRIE SPATIALE",
          vision: "VISION MULTIMODALE",
          bim: "BIM / IFC",
          reasoning: "RAISONNEMENT ARCHITECTURAL"
        },
        card: {
          eyebrow: "Projet résidentiel",
          title: "Analyse spatiale et fonctionnelle",
          plans: "Plans",
          model: "Modèle 3D",
          bim: "Données BIM (IFC)",
          relations: "Relations spatiales",
          cta: "Voir un exemple"
        }
      },
      about: {
        eyebrow: "QU'EST-CE QU'AXIS",
        title: "Architectural eXpert Intelligence System.",
        text: "AXIS est un projet de recherche qui développe des modèles capables de percevoir, représenter et raisonner sur l'espace architectural et ses données multimodales : plans 2D, modèles 3D, données BIM/IFC et texte normatif. Ces capacités ne sont pas toutes acquises — chacune est mesurée, publiée et classée selon son statut scientifique réel.",
        more: "Voir les preuves"
      },
      studio: {
        eyebrow: "AXIS STUDIO",
        badge: "PLANIFIÉ — NON DÉMARRÉ",
        title: "Un espace de travail, encore à l'état de projet.",
        text: "AXIS Studio désigne l'environnement prévu pour explorer, au même endroit, les sorties d'AXIS — plans, contexte, résultats de raisonnement. Aucune implémentation n'existe aujourd'hui dans ce dépôt : ni interface, ni fonctionnalité, ni maquette ne sont publiées. C'est une direction déclarée sur la feuille de route, pas un produit disponible.",
        note: "Cette section sera mise à jour dès qu'un premier composant réel existera — pas avant.",
        cta: "Suivre l'avancement sur GitHub"
      },
      models: {
        eyebrow: "AXIS MODELS",
        title: "Trois composants, trois statuts réels.",
        text: "AXIS ne repose pas sur un modèle unique. Trois composants distincts, à des stades de maturité très différents, forment aujourd'hui la famille AXIS Models.",
        m1: {
          status: "VALIDÉ",
          name: "AXIS-Clearance",
          role: "Régression géométrique 3D et vérification réglementaire de dégagement (Neufert, accessibilité PMR).",
          detail: "Architecture MLP (SpatialRelationMLP). Checkpoint validé sur le Gold Set V3 — MAE 0,0517 m."
        },
        m2: {
          status: "EXPÉRIMENTAL",
          name: "AXIS-Spatial",
          role: "Raisonnement spatial et topologique sur plans architecturaux (adjacence, connectivité, circulation).",
          detail: "Qwen2-VL-7B + adaptateur LoRA. RUN-023 : précision topologique 63,12 % (base 14,51 %). Dépendance visuelle non démontrée (VDI 1,28, seuil requis ≥ 3,0)."
        },
        m3: {
          status: "PLANIFIÉ",
          name: "AXIS-Unified",
          role: "Architecture multimodale unifiée : attention conjointe sur rasters 2D, coordonnées 3D et règles normatives textuelles.",
          detail: "Aucune implémentation n'existe à ce jour."
        },
        note: "« AXIS-Clearance », « AXIS-Spatial » et « AXIS-Unified » sont les noms publics donnés ici à trois composants internes documentés (respectivement SpatialRelationMLP, l'adaptateur Qwen2-VL-7B + LoRA de RUN-022, et l'Unified Architectural Transformer planifié dans ARCHITECTURE.md) — une couche de présentation, pas un renommage des identifiants scientifiques internes."
      },
      how: {
        eyebrow: "COMMENT AXIS FONCTIONNE",
        title: "De la perception au raisonnement.",
        step1: { title: "Architecture", text: "Plans 2D, modèles 3D, données BIM/IFC, rasters et vecteurs — la matière première brute." },
        step2: { title: "Perception", text: "Lire un plan ou un modèle sans halluciner d'échelle ni de dimension physique." },
        step3: { title: "Géométrie", text: "Extraire coordonnées, distances euclidiennes et volumes à partir des formes." },
        step4: { title: "Relations", text: "Reconstruire la topologie des espaces : adjacence, circulation, cloisonnement." },
        step5: { title: "Raisonnement", text: "Confronter la géométrie aux normes — dégagements, accessibilité PMR, Neufert." },
        step6: { title: "Action", text: "Produire un verdict falsifiable, vérifiable sur un benchmark immuable." }
      },
      research: {
        eyebrow: "RECHERCHE — RUN-023",
        title: "Mesurer, falsifier, recommencer.",
        text: "Les résultats scientifiques d'AXIS sont publiés au fil de l'eau, y compris lorsqu'ils invalident une hypothèse. RUN-020 a révélé qu'un premier pilote (RUN-019) avait appris des raccourcis textuels plutôt qu'un raisonnement visuel — ce qui a directement motivé la conception d'un nouveau protocole, de RUN-021 à RUN-023.",
        timeline: {
          eyebrow: "CHRONOLOGIE",
          r19: { title: "RUN-019 — Premier pilote QLoRA sur données réelles", text: "194 pas, 1 000 plans réels. Perte de validation −98,59 %.", tag: "ENTRAÎNEMENT — PASS" },
          r20: { title: "RUN-020 — Falsification scientifique", text: "85,3 % de reproduction de templates, 100 % d'hallucination d'identifiants, dépendance visuelle quasi nulle (VDI ≈ 1,0).", tag: "FALSIFIÉ" },
          r21: { title: "RUN-021 — Nouveau jeu de supervision spatiale", text: "1 000 assets / 7 950 exemples conçus pour éliminer les raccourcis identifiés en RUN-020. Zéro fuite.", tag: "VERROUILLÉ — PASS" },
          r22: { title: "RUN-022 — Entraînement sur le nouveau protocole", text: "2 310 pas (3 époques). Perte finale : 0,1218 (train) / 0,1397 (validation).", tag: "CHECKPOINT — PASS" },
          r23: { title: "RUN-023 — Évaluation de généralisation spatiale", text: "Évaluation complète sur 1 006 exemples de test verrouillés.", tag: "TERMINÉ" }
        },
        headline: {
          eyebrow: "RUN-023 — RÉSULTATS",
          n1: { value: "1 006", label: "exemples de test verrouillés" },
          n2: { value: "63,12 %", label: "précision de raisonnement topologique (base : 14,51 %)" },
          n3: { value: "100 %", label: "conformité de format de sortie" },
          n4: { value: "0 %", label: "taux d'hallucination d'identifiants" },
          n5: { value: "1,28", label: "indice de dépendance visuelle (VDI) — seuil requis ≥ 3,0" },
          conditions: "Modèle et adaptateur chargés en 4-bit NF4 + BF16, 392 tenseurs LoRA attachés, aucune mutation de poids détectée lors du smoke test. Reproductibilité vérifiée : 20/20 exécutions bit-exactes (seed 42).",
          verdict: "Verdict officiel : la dépendance visuelle du modèle n'est pas démontrée sous ce protocole. Tout entraînement supplémentaire est suspendu, dans l'attente d'une revue humaine avant la Phase 7."
        },
        track2: {
          eyebrow: "AXIS-CLEARANCE — GOLD SET V3",
          title: "Un second axe d'évaluation, déjà validé.",
          baseline: "Baseline 0",
          baselineSub: "Constante triviale — erreur moyenne",
          checkpoint: "AXIS-Clearance — checkpoint 005",
          checkpointSub: "CLEARANCE_CHECK — erreur moyenne (MAE)",
          reductionCaption: "de réduction relative de l'erreur (MAE), calculée sur n = 100 instances du Gold Set V3, tâche CLEARANCE_CHECK.",
          warning: "Résultat obtenu sur un benchmark spécifique et étroit (régression de dégagement 3D), sur un jeu de test à 99/1 instances déséquilibrées. Cette métrique ne constitue pas une preuve d'une compréhension architecturale générale.",
          goldTitle: "Un benchmark sanctuarisé, jamais modifié.",
          goldText: "Le checkpoint évalué a été sélectionné exclusivement sur la validation de Dataset A, avant toute exposition au Gold Set. Cette séparation stricte prévient la loi de Goodhart et protège la validité du benchmark.",
          certified: "instances certifiées, en lecture seule",
          negatives: "négatifs adversariaux (hard negatives)",
          goldNote: "Ni le manifeste du Gold Set ni les poids du checkpoint ne sont publiquement téléchargeables — seuls leurs empreintes SHA-256 et les métriques obtenues sont publiées, pour la traçabilité scientifique."
        }
      },
      evidence: {
        eyebrow: "EVIDENCE OVER CLAIMS",
        title: "Où en est AXIS, précisément ?",
        validated: {
          title: "Validé",
          i1: "Master Dataset v2 — 65 342 assets, zéro fuite",
          i2: "AXIS-Clearance — MAE 0,0517 m sur le Gold Set V3 (CLEARANCE_CHECK)",
          i3: "RUN-023 — raisonnement topologique 63,12 % vs 14,51 % base (+48,61 pts), format 100 %, hallucination 0 %",
          i4: "RUN-022 — intégrité du checkpoint : reprise déterministe, reproductibilité 20/20 bit-exacte"
        },
        experimental: {
          title: "Expérimental",
          i1: "AXIS-Spatial (Qwen2-VL-7B + LoRA) comme composant de raisonnement",
          i2: "Modèle vision 2D ROOM_TOPOLOGY — non évalué sur le Gold Set",
          i3: "Raisonnement multimodal 2D↔3D — 10 paires réelles seulement"
        },
        unproven: {
          title: "Non démontré",
          i1: "Dépendance visuelle du modèle (RUN-023) — VDI 1,28 sous le seuil requis de 3,0",
          i2: "Identification des hubs de circulation — 0 % de précision (RUN-023)",
          i3: "Évaluation humaine en aveugle — non encore réalisée"
        },
        blocked: {
          title: "Bloqué",
          i1: "FloorPlanCAD — exclusion permanente en attente de revue légale externe (0/65 342 admis)",
          i2: "ResPlan — quarantaine métrique (échelle non calibrée, 17 000 plans)",
          i3: "Pre-Training Gate — CONDITIONAL, entraînement suspendu avant revue humaine (Phase 7)"
        }
      },
      data: {
        eyebrow: "MASTER DATASET V2",
        caption: "assets consolidés dans le Master Dataset v2, issus de 19 sources indépendantes.",
        rawNote: "66 847 fichiers physiques passés en revue → 65 342 assets canoniques certifiés.",
        train: "Train", val: "Validation", test: "Test",
        review: "File de revue (isolée, non comptée)",
        note: "Partitionnement strict par project_group_id, seed fixe (42). Garantie de zéro fuite SHA256 et zéro fuite de projet entre les ensembles.",
        floorplancad: "FloorPlanCAD : 741 dessins quarantinés — exclusion permanente en attente de revue légale externe. Zéro exemplaire n'a jamais été utilisé pour l'entraînement, l'évaluation ou un checkpoint publié.",
        more: "Documentation complète du dataset"
      },
      roadmap: {
        eyebrow: "ROADMAP",
        title: "Progression par phases, sans date imposée.",
        done: "Terminé", current: "Actif", next: "Expérimental", future: "Planifié",
        p1: { title: "Fondation & développement du modèle", text: "Phases 0 à 6B : Master Dataset v2, moteur de supervision, pilote QLoRA réel (RUN-019), falsification scientifique (RUN-020), nouveau jeu de supervision spatiale (RUN-021), entraînement (RUN-022) et évaluation (RUN-023)." },
        p2: { title: "Revue humaine & gouvernance ouverte", text: "Revue humaine des résultats RUN-023 avant la Phase 7 ; dépôt public AXIS v0.1.0, licence MIT, gouvernance ouverte et infrastructure communautaire." },
        p3: { title: "Raffinement du protocole", text: "Retravailler le protocole d'ablation visuelle : supprimer la fuite de coordonnées dans les prompts textuels, introduire une tolérance IoU pour les hubs de circulation." },
        p4: { title: "Famille de modèles & AXIS Studio", text: "Acquisition de 50 à 100 modèles OpenBIM/IFC, extraction vectorielle millimétrée, benchmark vision 2D, AXIS Studio, AXIS-Unified, raisonnement réglementaire approfondi, optimisation d'inférence." }
      },
      oss: {
        eyebrow: "OUVERTURE",
        title: "Une recherche ouverte par défaut.",
        text: "Le code et la documentation originaux d'AXIS sont publiés sous licence MIT, afin de permettre à d'autres chercheurs, développeurs, architectes et passionnés d'explorer, modifier, expérimenter et construire à partir du projet. Les jeux de données tiers conservent leurs propres licences.",
        i1: "Licence du code AXIS",
        i2: "Dépôt GitHub public",
        i3: "Documentation scientifique complète",
        i4: "Ouvert à la contribution",
        i5: "Recherche reproductible et falsifiable"
      },
      community: {
        eyebrow: "COMMUNAUTÉ",
        title: "Construire AXIS à plusieurs.",
        text: "AXIS n'est pas conçu pour être construit par une seule personne. C'est une initiative interdisciplinaire, à la croisée de la recherche en IA et de la pratique architecturale.",
        p1: "Chercheur·se ML", p2: "Ingénieur·e ML", p3: "Développeur·se Python",
        p4: "Ingénieur·e GPU / inférence", p5: "Chercheur·se en vision par ordinateur",
        p6: "Architecte / designer", p7: "Évaluation & red-team", p8: "Documentation & rédaction technique",
        cta: "Contribuer au projet"
      },
      cta: {
        title: "L'architecture est un problème spatial.",
        sub: "AXIS apprend à raisonner sur cet espace — une capacité mesurée à la fois, jamais présumée.",
        github: "Explorer AXIS sur GitHub",
        docs: "Lire la recherche"
      },
      footer: {
        tagline: "Architectural eXpert Intelligence System",
        research: "Recherche", data: "Données", contributing: "Contribution", docs: "Documentation", license: "Licence MIT"
      }
    },

    en: {
      nav: { home: "Home", studio: "Studio", models: "Models", research: "Research", data: "Data", community: "Community" },
      hero: {
        kicker: "ARCHITECTURAL EXPERT INTELLIGENCE SYSTEM",
        title: { l1: "ARCHITECTURAL", l2: "INTELLIGENCE,", l3: "ENGINEERED WITH EVIDENCE" },
        desc: "AXIS is a research project developing models that can perceive, represent, and reason about architectural space — and measuring precisely what has already been demonstrated from what remains to be proven.",
        cta: { studio: "Explore AXIS Studio", research: "Explore Research", github: "View on GitHub" },
        anno: {
          geometry: "SPATIAL GEOMETRY",
          vision: "MULTIMODAL VISION",
          bim: "BIM / IFC",
          reasoning: "ARCHITECTURAL REASONING"
        },
        card: {
          eyebrow: "Residential project",
          title: "Spatial and functional analysis",
          plans: "Floor plans",
          model: "3D model",
          bim: "BIM data (IFC)",
          relations: "Spatial relations",
          cta: "See an example"
        }
      },
      about: {
        eyebrow: "WHAT IS AXIS",
        title: "Architectural eXpert Intelligence System.",
        text: "AXIS is a research project developing models that can perceive, represent, and reason about architectural space and its multimodal data: 2D plans, 3D models, BIM/IFC data, and normative text. Not all of these capabilities are already acquired — each one is measured, published, and labeled by its real scientific status.",
        more: "See the evidence"
      },
      studio: {
        eyebrow: "AXIS STUDIO",
        badge: "PLANNED — NOT STARTED",
        title: "A workspace, still on the drawing board.",
        text: "AXIS Studio names the environment planned to explore AXIS's outputs — plans, context, reasoning results — in one place. No implementation exists today in this repository: no interface, no feature, and no mockup has been published. It is a stated roadmap direction, not an available product.",
        note: "This section will be updated as soon as a first real component exists — not before.",
        cta: "Follow progress on GitHub"
      },
      models: {
        eyebrow: "AXIS MODELS",
        title: "Three components, three real statuses.",
        text: "AXIS does not rely on a single model. Three distinct components, at very different stages of maturity, currently make up the AXIS Models family.",
        m1: {
          status: "VALIDATED",
          name: "AXIS-Clearance",
          role: "3D geometric regression and regulatory clearance verification (Neufert, accessibility standards).",
          detail: "MLP architecture (SpatialRelationMLP). Checkpoint validated on Gold Set V3 — 0.0517 m MAE."
        },
        m2: {
          status: "EXPERIMENTAL",
          name: "AXIS-Spatial",
          role: "Spatial and topological reasoning over architectural plans (adjacency, connectivity, circulation).",
          detail: "Qwen2-VL-7B + LoRA adapter. RUN-023: 63.12% topological accuracy (base 14.51%). Visual dependency unproven (VDI 1.28, required threshold ≥3.0)."
        },
        m3: {
          status: "PLANNED",
          name: "AXIS-Unified",
          role: "Unified multimodal architecture: joint attention over 2D rasters, 3D coordinates, and normative textual rules.",
          detail: "No implementation exists to date."
        },
        note: "“AXIS-Clearance,” “AXIS-Spatial,” and “AXIS-Unified” are the public names given here to three documented internal components (respectively SpatialRelationMLP, the Qwen2-VL-7B + LoRA adapter from RUN-022, and the Unified Architectural Transformer planned in ARCHITECTURE.md) — a presentation layer, not a renaming of the internal scientific identifiers."
      },
      how: {
        eyebrow: "HOW AXIS WORKS",
        title: "From perception to reasoning.",
        step1: { title: "Architecture", text: "2D plans, 3D models, BIM/IFC data, rasters and vectors — the raw material." },
        step2: { title: "Perception", text: "Reading a plan or model without hallucinating scale or physical dimension." },
        step3: { title: "Geometry", text: "Extracting coordinates, Euclidean distances, and volumes from shapes." },
        step4: { title: "Relations", text: "Reconstructing spatial topology: adjacency, circulation, partitioning." },
        step5: { title: "Reasoning", text: "Checking geometry against standards — clearances, accessibility, Neufert." },
        step6: { title: "Action", text: "Producing a falsifiable verdict, verifiable against an immutable benchmark." }
      },
      research: {
        eyebrow: "RESEARCH — RUN-023",
        title: "Measure, falsify, repeat.",
        text: "AXIS's scientific results are published as they happen, including when they invalidate a hypothesis. RUN-020 revealed that an earlier pilot (RUN-019) had learned textual shortcuts rather than visual reasoning — which directly motivated the design of a new protocol, from RUN-021 through RUN-023.",
        timeline: {
          eyebrow: "TIMELINE",
          r19: { title: "RUN-019 — First real-data QLoRA pilot", text: "194 steps, 1,000 real plans. Validation loss −98.59%.", tag: "TRAINING — PASS" },
          r20: { title: "RUN-020 — Scientific falsification", text: "85.3% template reproduction, 100% ID hallucination, near-zero visual dependency (VDI ≈ 1.0).", tag: "FALSIFIED" },
          r21: { title: "RUN-021 — New spatial supervision dataset", text: "1,000 assets / 7,950 examples engineered to eliminate the shortcuts found in RUN-020. Zero leakage.", tag: "LOCKED — PASS" },
          r22: { title: "RUN-022 — Training on the new protocol", text: "2,310 steps (3 epochs). Final loss: 0.1218 (train) / 0.1397 (validation).", tag: "CHECKPOINT — PASS" },
          r23: { title: "RUN-023 — Spatial generalization evaluation", text: "Full evaluation on 1,006 locked test examples.", tag: "COMPLETE" }
        },
        headline: {
          eyebrow: "RUN-023 — RESULTS",
          n1: { value: "1,006", label: "locked test examples" },
          n2: { value: "63.12%", label: "topological reasoning accuracy (base: 14.51%)" },
          n3: { value: "100%", label: "output format adherence" },
          n4: { value: "0%", label: "ID hallucination rate" },
          n5: { value: "1.28", label: "Visual Dependency Index (VDI) — required threshold ≥3.0" },
          conditions: "Model and adapter loaded in 4-bit NF4 + BF16, 392 LoRA tensors attached, no weight mutation detected during the smoke test. Reproducibility verified: 20/20 bit-exact runs (seed 42).",
          verdict: "Official verdict: visual dependency has not been proven under this protocol. All further training is paused, pending human review before Phase 7."
        },
        track2: {
          eyebrow: "AXIS-CLEARANCE — GOLD SET V3",
          title: "A second evaluation track, already validated.",
          baseline: "Baseline 0",
          baselineSub: "Trivial constant — mean error",
          checkpoint: "AXIS-Clearance — checkpoint 005",
          checkpointSub: "CLEARANCE_CHECK — mean absolute error (MAE)",
          reductionCaption: "relative MAE reduction, computed on n = 100 instances of the Gold Set V3, task CLEARANCE_CHECK.",
          warning: "Result obtained on a specific, narrow benchmark (3D clearance regression), on a 99/1 class-imbalanced test set. This metric does not constitute proof of general architectural understanding.",
          goldTitle: "A sanctified benchmark, never modified.",
          goldText: "The evaluated checkpoint was selected exclusively on Dataset A validation loss, before any exposure to the Gold Set. This strict separation prevents Goodhart's law and protects the benchmark's validity.",
          certified: "certified, read-only instances",
          negatives: "adversarial hard negatives",
          goldNote: "Neither the Gold Set manifest nor the checkpoint weights are publicly downloadable — only their SHA-256 hashes and the resulting metrics are published, for scientific traceability."
        }
      },
      evidence: {
        eyebrow: "EVIDENCE OVER CLAIMS",
        title: "Where does AXIS actually stand?",
        validated: {
          title: "Validated",
          i1: "Master Dataset v2 — 65,342 assets, zero leakage",
          i2: "AXIS-Clearance — 0.0517 m MAE on Gold Set V3 (CLEARANCE_CHECK)",
          i3: "RUN-023 — topological reasoning 63.12% vs 14.51% base (+48.61pp), 100% format, 0% hallucination",
          i4: "RUN-022 — checkpoint integrity: deterministic resumption, 20/20 bit-exact reproducibility"
        },
        experimental: {
          title: "Experimental",
          i1: "AXIS-Spatial (Qwen2-VL-7B + LoRA) as a reasoning component",
          i2: "2D vision model ROOM_TOPOLOGY — not evaluated on the Gold Set",
          i3: "Multimodal 2D↔3D reasoning — only 10 genuine pairs"
        },
        unproven: {
          title: "Unproven",
          i1: "Model visual dependency (RUN-023) — VDI 1.28, below the required 3.0 threshold",
          i2: "Circulation-hub identification — 0% accuracy (RUN-023)",
          i3: "Human blind evaluation — not yet performed"
        },
        blocked: {
          title: "Blocked",
          i1: "FloorPlanCAD — permanent exclusion pending external legal review (0/65,342 admitted)",
          i2: "ResPlan — metric quarantine (uncalibrated scale, 17,000 plans)",
          i3: "Pre-Training Gate — CONDITIONAL, training paused before human review (Phase 7)"
        }
      },
      data: {
        eyebrow: "MASTER DATASET V2",
        caption: "assets consolidated in the Master Dataset v2, drawn from 19 independent sources.",
        rawNote: "66,847 physical files reviewed → 65,342 certified canonical assets.",
        train: "Train", val: "Validation", test: "Test",
        review: "Review queue (isolated, not counted)",
        note: "Strict partitioning by project_group_id, fixed seed (42). Guarantee of zero SHA256 leakage and zero project leakage across splits.",
        floorplancad: "FloorPlanCAD: 741 quarantined drawings — permanent exclusion pending external legal review. Zero examples have ever been used for training, evaluation, or a published checkpoint.",
        more: "Full dataset documentation"
      },
      roadmap: {
        eyebrow: "ROADMAP",
        title: "Phase-by-phase progress, with no imposed dates.",
        done: "Done", current: "Active", next: "Experimental", future: "Planned",
        p1: { title: "Foundation & model development", text: "Phases 0 through 6B: Master Dataset v2, supervision engine, first real-data QLoRA pilot (RUN-019), scientific falsification (RUN-020), new spatial supervision dataset (RUN-021), training (RUN-022), and evaluation (RUN-023)." },
        p2: { title: "Human validation & open governance", text: "Human review of RUN-023 results before Phase 7; public AXIS v0.1.0 repository, MIT license, open governance, and community infrastructure." },
        p3: { title: "Protocol refinement", text: "Reworking the visual ablation protocol: removing coordinate leakage from textual prompts, introducing IoU tolerance for circulation hubs." },
        p4: { title: "Model family & AXIS Studio", text: "Acquisition of 50–100 OpenBIM/IFC models, millimeter-scale vector extraction, 2D vision benchmark, AXIS Studio, AXIS-Unified, deeper regulatory reasoning, inference optimization." }
      },
      oss: {
        eyebrow: "OPENNESS",
        title: "Open research by default.",
        text: "AXIS's original code and documentation are published under the MIT License, so other researchers, developers, architects, and enthusiasts can explore, modify, experiment with, and build on the project. Third-party datasets keep their own licenses.",
        i1: "AXIS code license",
        i2: "Public GitHub repository",
        i3: "Complete scientific documentation",
        i4: "Open to contribution",
        i5: "Reproducible, falsifiable research"
      },
      community: {
        eyebrow: "COMMUNITY",
        title: "Building AXIS together.",
        text: "AXIS is not meant to be built by one person alone. It is an interdisciplinary initiative at the intersection of AI research and architectural practice.",
        p1: "ML Researcher", p2: "ML Engineer", p3: "Python Developer",
        p4: "GPU / Inference Engineer", p5: "Computer Vision Researcher",
        p6: "Architect / Designer", p7: "Evaluation & Red-Team", p8: "Documentation & Technical Writing",
        cta: "Contribute to the project"
      },
      cta: {
        title: "Architecture is a spatial problem.",
        sub: "AXIS is learning how to reason about it — one measured capability at a time, never assumed.",
        github: "Explore AXIS on GitHub",
        docs: "Read the research"
      },
      footer: {
        tagline: "Architectural eXpert Intelligence System",
        research: "Research", data: "Data", contributing: "Contributing", docs: "Documentation", license: "MIT License"
      }
    }
  };

  global.AXIS_I18N = STRINGS;
})(window);
