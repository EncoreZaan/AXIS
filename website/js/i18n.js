/* AXIS — i18n dictionary (FR default, EN available).
   Keys mirror the data-i18n paths used in index.html. */
(function (global) {
  "use strict";

  var STRINGS = {
    fr: {
      nav: { home: "Accueil", research: "Recherche", data: "Données", community: "Communauté", about: "À propos" },
      hero: {
        kicker: "SYSTÈME D'INTELLIGENCE EXPERTE ARCHITECTURALE",
        title: { l1: "UNE IA QUI", l2: "COMPREND", l3: "L'ARCHITECTURE" },
        desc: "AXIS est un projet de recherche open source qui explore comment l'intelligence artificielle peut comprendre, raisonner et travailler avec des données architecturales, géométriques et BIM.",
        cta: { discover: "Découvrir le projet", github: "Explorer sur GitHub" },
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
      problem: {
        eyebrow: "LE DÉFI",
        title: "L'architecture est plus complexe qu'un texte.",
        text: "Les modèles d'IA actuels excellent pour comprendre et générer du texte. Mais l'architecture repose aussi sur des relations spatiales, des géométries, des objets, des contraintes, des plans, des modèles 3D et des données structurées.",
        more: "En savoir plus"
      },
      vision: {
        eyebrow: "NOTRE APPROCHE",
        title: "De la perception au raisonnement.",
        step1: { title: "Architecture", text: "Plans 2D, modèles 3D, données BIM/IFC, rasters et vecteurs — la matière première brute." },
        step2: { title: "Perception", text: "Lire un plan ou un modèle sans halluciner d'échelle ni de dimension physique." },
        step3: { title: "Géométrie", text: "Extraire coordonnées, distances euclidiennes et volumes à partir des formes." },
        step4: { title: "Relations", text: "Reconstruire la topologie des espaces : adjacence, circulation, cloisonnement." },
        step5: { title: "Raisonnement", text: "Confronter la géométrie aux normes — dégagements, accessibilité PMR, Neufert." },
        step6: { title: "Action", text: "Produire un verdict falsifiable, vérifiable sur un benchmark immuable." }
      },
      domains: {
        eyebrow: "NOS DOMAINES DE RECHERCHE",
        title: "Une approche pluridisciplinaire à la croisée de l'IA et du monde architectural.",
        c1: { title: "IA & Machine Learning", text: "Modèles multimodaux et raisonnement spatial.", tag: "Recherche active" },
        c2: { title: "Vision par ordinateur", text: "Compréhension des plans et environnements 2D/3D.", tag: "Recherche active" },
        c3: { title: "Géométrie computationnelle", text: "Analyse et raisonnement sur les formes et les espaces.", tag: "Recherche active" },
        c4: { title: "BIM / IFC & OpenBIM", text: "Interopérabilité et exploitation des données structurées.", tag: "Recherche active" },
        c5: { title: "Architecture", text: "Cas d'usage réels et pertinence métier.", tag: "Recherche active" },
        c6: { title: "Évaluation & Benchmarks", text: "Mesure rigoureuse et falsifiable des performances.", tag: "Recherche active" }
      },
      dataset: {
        eyebrow: "MASTER DATASET V2",
        caption: "assets consolidés dans le Master Dataset v2, issus de 19 sources indépendantes.",
        train: "Train", val: "Validation", test: "Test",
        review: "File de revue (isolée, non comptée)",
        note: "Partitionnement strict par project_group_id, seed fixe (42). Garantie de zéro fuite SHA256 et zéro fuite de projet entre les ensembles.",
        more: "Documentation complète du dataset"
      },
      eval: {
        eyebrow: "GOLD SET V3 — CLEARANCE_CHECK",
        title: "Mesurer avant de prétendre comprendre.",
        baseline: "Baseline 0",
        baselineSub: "Constante triviale — erreur moyenne",
        checkpoint: "AXIS — checkpoint 005",
        checkpointSub: "CLEARANCE_CHECK — erreur moyenne (MAE)",
        reductionCaption: "de réduction relative de l'erreur (MAE), calculée sur n = 100 instances du Gold Set V3, tâche CLEARANCE_CHECK.",
        warning: "Résultat obtenu sur un benchmark spécifique et étroit (régression de dégagement 3D). Cette métrique ne constitue pas une preuve d'une compréhension architecturale générale, ni d'une capacité de raisonnement autonome."
      },
      gold: {
        eyebrow: "GOLD SET V3",
        title: "Un benchmark sanctuarisé, jamais modifié.",
        text: "Le checkpoint évalué a été sélectionné exclusivement sur la validation de Dataset A, avant toute exposition au Gold Set. Cette séparation stricte prévient la loi de Goodhart et protège la validité du benchmark.",
        certified: "instances certifiées, en lecture seule",
        negatives: "négatifs adversariaux (hard negatives)",
        note: "Les négatifs adversariaux se situent à ±0,02 m du seuil réglementaire, conçus pour déjouer les heuristiques de seuil superficielles. Ni le manifeste du Gold Set ni les poids du checkpoint ne sont publiquement téléchargeables — seuls leurs empreintes SHA-256 et les métriques obtenues sont publiées, pour la traçabilité scientifique."
      },
      status: {
        eyebrow: "TRANSPARENCE",
        title: "Où en est AXIS ?",
        validated: {
          title: "Validé",
          i1: "Master Dataset v2 — 65 342 assets, zéro fuite",
          i2: "Gold Set V3 — 200 instances + 200 négatifs",
          i3: "CLEARANCE_CHECK — MAE 0,0517 m sur le Gold Set",
          i4: "Sélection des tâches Phase 4 — 4/69 approuvées"
        },
        experimental: {
          title: "Expérimental",
          i1: "Preuve de concept VLM QLoRA (Qwen2-VL-7B, 6 pas)",
          i2: "Modèle vision 2D ROOM_TOPOLOGY — non évalué sur le Gold Set",
          i3: "Raisonnement multimodal 2D↔3D — 10 paires réelles seulement"
        },
        planned: {
          title: "Planifié",
          i1: "Extraction déterministe de plans vectoriels millimétrés",
          i2: "Benchmark vision 2D sur ROOM_TOPOLOGY / FLOORPLAN_READING",
          i3: "Piste d'accélération DSpark (aucune implémentation actuelle)"
        },
        blocked: {
          title: "Bloqué",
          i1: "ResPlan — quarantaine métrique (échelle non calibrée, 17 000 plans)",
          i2: "FloorPlanCAD — 741 dessins en revue légale",
          i3: "Pre-Training Gate — CONDITIONAL, entraînement non autorisé"
        }
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
      roadmap: {
        eyebrow: "ROADMAP",
        title: "Progression par phases, sans date imposée.",
        done: "Terminé", current: "En cours", next: "Prochain", future: "Futur",
        p1: { title: "Phases 0–4", text: "Master Dataset v2, moteur de supervision, audit red-team, forensic ResPlan, micro-pilote Gold Set V3." },
        p2: { title: "AXIS v0.1.0", text: "Dépôt public, licence MIT, gouvernance ouverte, infrastructure communautaire." },
        p3: { title: "Extension des données", text: "Acquisition de 50 à 100 modèles OpenBIM/IFC sous licence ouverte, extraction millimétrée, benchmark vision 2D." },
        p4: { title: "Raisonnement & échelle", text: "Pré-entraînement multimodal spécialisé, raisonnement normatif approfondi, optimisation d'inférence, piste DSpark." }
      },
      cta: {
        title: "Explore. Experiment. Build.",
        sub: "AXIS est ouvert à celles et ceux qui veulent explorer ce que pourrait être une intelligence artificielle capable de travailler avec le monde architectural.",
        github: "Explorer AXIS sur GitHub",
        docs: "Lire la documentation"
      },
      footer: {
        tagline: "Architectural eXpert Intelligence System",
        research: "Recherche", data: "Données", contributing: "Contribution", docs: "Documentation", license: "Licence MIT"
      }
    },

    en: {
      nav: { home: "Home", research: "Research", data: "Data", community: "Community", about: "About" },
      hero: {
        kicker: "ARCHITECTURAL EXPERT INTELLIGENCE SYSTEM",
        title: { l1: "AN AI THAT", l2: "UNDERSTANDS", l3: "ARCHITECTURE" },
        desc: "AXIS is an open-source research project exploring how artificial intelligence can understand, reason about, and work with architectural, geometric, and BIM data.",
        cta: { discover: "Discover the project", github: "Explore on GitHub" },
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
      problem: {
        eyebrow: "THE CHALLENGE",
        title: "Architecture is more complex than text.",
        text: "Current AI models excel at understanding and generating text. But architecture also relies on spatial relations, geometries, objects, constraints, floor plans, 3D models, and structured data.",
        more: "Learn more"
      },
      vision: {
        eyebrow: "OUR APPROACH",
        title: "From perception to reasoning.",
        step1: { title: "Architecture", text: "2D plans, 3D models, BIM/IFC data, rasters and vectors — the raw material." },
        step2: { title: "Perception", text: "Reading a plan or model without hallucinating scale or physical dimension." },
        step3: { title: "Geometry", text: "Extracting coordinates, Euclidean distances, and volumes from shapes." },
        step4: { title: "Relations", text: "Reconstructing spatial topology: adjacency, circulation, partitioning." },
        step5: { title: "Reasoning", text: "Checking geometry against standards — clearances, accessibility, Neufert." },
        step6: { title: "Action", text: "Producing a falsifiable verdict, verifiable against an immutable benchmark." }
      },
      domains: {
        eyebrow: "OUR RESEARCH DOMAINS",
        title: "A multidisciplinary approach at the intersection of AI and the built environment.",
        c1: { title: "AI & Machine Learning", text: "Multimodal models and spatial reasoning.", tag: "Active research" },
        c2: { title: "Computer Vision", text: "Understanding of 2D/3D plans and environments.", tag: "Active research" },
        c3: { title: "Computational Geometry", text: "Analysis and reasoning over shapes and spaces.", tag: "Active research" },
        c4: { title: "BIM / IFC & OpenBIM", text: "Interoperability and exploitation of structured data.", tag: "Active research" },
        c5: { title: "Architecture", text: "Real-world use cases and domain relevance.", tag: "Active research" },
        c6: { title: "Evaluation & Benchmarks", text: "Rigorous, falsifiable measurement of performance.", tag: "Active research" }
      },
      dataset: {
        eyebrow: "MASTER DATASET V2",
        caption: "assets consolidated in the Master Dataset v2, drawn from 19 independent sources.",
        train: "Train", val: "Validation", test: "Test",
        review: "Review queue (isolated, not counted)",
        note: "Strict partitioning by project_group_id, fixed seed (42). Guarantee of zero SHA256 leakage and zero project leakage across splits.",
        more: "Full dataset documentation"
      },
      eval: {
        eyebrow: "GOLD SET V3 — CLEARANCE_CHECK",
        title: "Measuring before claiming understanding.",
        baseline: "Baseline 0",
        baselineSub: "Trivial constant — mean error",
        checkpoint: "AXIS — checkpoint 005",
        checkpointSub: "CLEARANCE_CHECK — mean absolute error (MAE)",
        reductionCaption: "relative MAE reduction, computed on n = 100 instances of the Gold Set V3, task CLEARANCE_CHECK.",
        warning: "Result obtained on a specific, narrow benchmark (3D clearance regression). This metric does not constitute proof of general architectural understanding or autonomous reasoning ability."
      },
      gold: {
        eyebrow: "GOLD SET V3",
        title: "A sanctified benchmark, never modified.",
        text: "The evaluated checkpoint was selected exclusively on Dataset A validation loss, before any exposure to the Gold Set. This strict separation prevents Goodhart's law and protects the benchmark's validity.",
        certified: "certified, read-only instances",
        negatives: "adversarial hard negatives",
        note: "Adversarial negatives sit within ±0.02 m of the regulatory threshold, designed to defeat superficial threshold heuristics. Neither the Gold Set manifest nor the checkpoint weights are publicly downloadable — only their SHA-256 hashes and the resulting metrics are published, for scientific traceability."
      },
      status: {
        eyebrow: "TRANSPARENCY",
        title: "Where does AXIS stand?",
        validated: {
          title: "Validated",
          i1: "Master Dataset v2 — 65,342 assets, zero leakage",
          i2: "Gold Set V3 — 200 instances + 200 negatives",
          i3: "CLEARANCE_CHECK — 0.0517 m MAE on the Gold Set",
          i4: "Phase 4 task gating — 4/69 approved"
        },
        experimental: {
          title: "Experimental",
          i1: "VLM QLoRA proof of concept (Qwen2-VL-7B, 6 steps)",
          i2: "2D vision model ROOM_TOPOLOGY — not evaluated on the Gold Set",
          i3: "Multimodal 2D↔3D reasoning — only 10 genuine pairs"
        },
        planned: {
          title: "Planned",
          i1: "Deterministic extraction of millimeter-scaled vector plans",
          i2: "2D vision benchmark on ROOM_TOPOLOGY / FLOORPLAN_READING",
          i3: "DSpark acceleration track (no implementation yet)"
        },
        blocked: {
          title: "Blocked",
          i1: "ResPlan — metric quarantine (uncalibrated scale, 17,000 plans)",
          i2: "FloorPlanCAD — 741 drawings under legal review",
          i3: "Pre-Training Gate — CONDITIONAL, training not authorized"
        }
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
      roadmap: {
        eyebrow: "ROADMAP",
        title: "Phase-by-phase progress, with no imposed dates.",
        done: "Done", current: "Current", next: "Next", future: "Future",
        p1: { title: "Phases 0–4", text: "Master Dataset v2, supervision engine, red-team audit, ResPlan forensic, Gold Set V3 micro-pilot." },
        p2: { title: "AXIS v0.1.0", text: "Public repository, MIT license, open governance, community infrastructure." },
        p3: { title: "Data expansion", text: "Acquisition of 50–100 openly licensed OpenBIM/IFC models, millimeter-scale extraction, 2D vision benchmark." },
        p4: { title: "Reasoning & scale", text: "Specialized multimodal pre-training, deeper regulatory reasoning, inference optimization, DSpark track." }
      },
      cta: {
        title: "Explore. Experiment. Build.",
        sub: "AXIS is open to anyone who wants to explore what an artificial intelligence capable of working with the built environment could look like.",
        github: "Explore AXIS on GitHub",
        docs: "Read the documentation"
      },
      footer: {
        tagline: "Architectural eXpert Intelligence System",
        research: "Research", data: "Data", contributing: "Contributing", docs: "Documentation", license: "MIT License"
      }
    }
  };

  global.AXIS_I18N = STRINGS;
})(window);
