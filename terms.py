import random


medical_terms = set([
    "abdominal-aortic-aneurysm-screening", "abdominal-aortic-aneurysm", "abdominal-aortic-aneurysm-screening", "abortion", "abscess",
    "acanthosis-nigricans", "achalasia", "acid-and-chemical-burns", "reflux-in-babies", "acne", "acoustic-neuroma", "acromegaly", "actinic-keratoses", 
    "actinomycosis", "acupuncture", "acute-cholecystitis", "acute-kidney-injury", "acute-lymphoblastic-leukaemia", "acute-myeloid-leukaemia", "acute-pancreatitis", 
    "acute-respiratory-distress-syndrome", "addisons-disease", "adenoidectomy", "age-related-cataracts", "age-related-macular-degeneration-amd", "agoraphobia", 
    "air-embolism", "albinism", "alcohol-misuse", "alcohol-poisoning", "alcohol-related-liver-disease", "alexander-technique", "alkaptonuria", "allergic-rhinitis", 
    "allergies", "altitude-sickness", "alzheimer's-disease", "lazy-eye", "memory-loss-amnesia", "amniocentesis", "amputation", "amyloidosis", "anabolic-steroid-misuse", 
    "iron-deficiency-anaemia", "vitamin-B12-or-folate-deficiency-anaemia", "anaesthesia", "anal-cancer", "anal-fissure", "anal-fistula", "anal-pain", "anaphylaxis", 
    "androgen-insensitivity-syndrome", "abdominal-aortic-aneurysm", "brain-aneurysm", "angelman-syndrome", "angina", "angioedema", "angiography", "coronary-angioplasty-and-stent-insertion", 
    "animal-and-human-bites", "ankle-pain", "ankylosing-spondylitis", "anorexia-nervosa", "lost-or-changed-sense-of-smell", "antacids", "antibiotics", "anticoagulant-medicines", "antidepressants", 
    "antifungal-medicines", "antihistamines", "antiphospholipid-syndrome", "antisocial-personality-disorder", "itchy-anus", "anxiety-disorders-in-children", "aortic-valve-replacement", "aphasia", 
    "appendicitis", "arrhythmia", "arterial-thrombosis", "arthritis", "arthroscopy", "asbestosis", "autism", "aspergillosis", "aspirin", "asthma", "astigmatism", "ataxia", "atherosclerosis", "athletes-foot", 
    "atopic-eczema", "atrial-fibrillation", "attention-deficit-hyperactivity-disorder-adhd", "auditory-processing-disorder", "autism", "autosomal-dominant-polycystic-kidney-disease-adpkd", "autosomal-recessive-polycystic-kidney-disease-arpkd",

    "baby", "back-pain", "bacterial-vaginosis", "bad-breath", "bakers-cyst", "balanitis", "barium-enema", "bartholins-cyst", "non-melanoma-skin-cancer", "bedbugs", "bedwetting-in-children", "behcets-disease", "diarrhoea-and-vomiting",
    "bells-palsy", "benign-brain-tumour", "prostate-enlargement", "beta-blockers", "bile-duct-cancer", "schistosomiasis", "binge-eating", "biopsy", "bipolar-disorder", "bird-flu", "birthmarks", "animal-and-human-bites", "black-eye",
    "bladder-cancer", "interstitial-cystitis", "bladder-stones", "post-menopausal-bleeding", "bleeding-from-the-bottom-rectal-bleeding", "blepharitis", "vision-loss", "blisters", "bloating", "blood-clots", "blood-groups", "blood-in-semen",
    "blood-in-urine", "sepsis", "high-blood-pressure-hypertension", "low-blood-pressure-hypotension", "blood-pressure-test", "blood-tests", "blood-transfusion", "blue-skin-or-lips-cyanosis", "blushing", "body-dysmorphic", "body-odour-bo", 
    "boils", "bone-cancer", "bone-cyst", "dexa-scan", "borderline-personality-disorder", "botulism", "bowel-cancer", "bowel-cancer-screening", "bowel-incontinence", "bowel-polyps", "small-bowel-transplant", "bowen's-disease", "braces-and-orthodontics",
    "plagiocephaly-brachycephaly", "brain-abscess", "brain-aneurysm", "brain-death", "subarachnoid-haemorrhage", "benign-brain-tumour", "malignant-brain-tumour", "brain-tumours", "breast-abscess", "breast-cancer-in-men", "breast-cancer-in-women", 
    "breast-lumps", "breast-pain", "breast-reduction-on-the-nhs", "breast-screening-mammogram", "breath-holding-in-babies-and-children", "broken-ankle", "broken-arm-or-wrist", "broken-collarbone", "broken-finger", "broken-leg", "broken-nose", 
    "broken-or-bruised-ribs", "broken-toe", "bronchiectasis", "bronchiolitis", "bronchitis", "bronchodilators", "brucellosis", "brugada-syndrome", "teeth-grinding-bruxism", "bulging-eyes", "bulimia", "bullous-pemphigoid", "bunions", "burns-and-scalds", "bursitis", "sciatica",

    "coronary-artery-bypass-graft-cabg", "caesarean-section", "cancer", "medical-cannabis", "carbon-monoxide-poisoning", "cea-test", "coronary-angiography", "cardiomyopathy", "cardiovascular-disease", "carotid-endarterectomy", "carpal-tunnel-syndrome", "cataract-surgery", 
    "cataracts", "childhood-cataracts", "catarrh", "cavernoma", "cavernous-sinus-thrombosis", "cellulitis", "cerebral-palsy", "cervical-cancer", "cervical-rib", "cervical-screening", "cervical-spondylosis", "charcot-marie-tooth-disease", "charles-bonnet-syndrome", "chemotherapy", 
    "chest-infection", "chest-pain", "chiari-malformation", "chickenpox", "chilblains", "chipped-broken-or-cracked-tooth", "chiropractic", "chlamydia", "bile-duct-cancer", "acute-cholecystitis", "cholera", "cholesteatoma", "high-cholesterol", "chorionic-villus-sampling-cvs", 
    "chronic-fatigue-syndrome-cfs", "chronic-kidney-disease", "chronic-lymphocytic-leukaemia", "chronic-myeloid-leukaemia", "chronic-obstructive-pulmonary-disease-copd", "chronic-pancreatitis", "chronic-traumatic-encephalopathy", "circumcision-in-boys", "circumcision-in-men",
    "cirrhosis", "creutzfeldt-jakob-disease-cjd", "claustrophobia", "cleft-lip-and-palate", "clinical-depression", "clinical-trials", "(c-difficile)", "club-foot", "cluster-headaches", "tailbone-coccyx-pain", "coeliac-disease", "cold-sores", "colic", "bowel-cancer", "colonoscopy", 
    "colostomy", "colour-vision-deficiency", "colposcopy", "coma", "common-cold", "compartment-syndrome", "complementary-and-alternative-medicine", "complex-regional-pain-syndrome", "concussion", "confusion", "congenital-heart-disease", "developmental-dysplasia-of-the-hip", "conjunctivitis", 
    "consent-to-treatment", "constipation", "contact-dermatitis", "cornea-transplant", "corns-and-calluses", "coronary-angioplasty-and-stent-insertion", "coronary-artery-bypass-graft", "coronary-heart-disease", "coronavirus-covid-19", "corticobasal-degeneration", "topical-corticosteroids", 
    "steroids", "cosmetic-procedures", "costochondritis", "cough", "coughing-up-blood", "counselling", "cradle-cap", "craniosynostosis", "crohns-disease", "croup", "ct-scan", "cushings-syndrome", "cuts-and-grazes",  "cyclical-vomiting-syndrome", "cyclospora", "cyclothymia", "cystic-fibrosis", 
    "cystitis", "cystoscopy", "cytomegalovirus-cmv",

    "dandruff", "deaf-blindness", "hearing-loss", "air-embolism", "decongestants", "dehydration", "frontotemporal-dementia", "vascular-dementia", "dementia-with-lewy-bodies", "dengue", "dental-abscess", "toothache", "dentures", "depression", "detached-retina-retinal-detachment", 
    "developmental-coordination-disorder-dyspraxia", "developmental-dysplasia-of-the-hip", "diabetes", "type-1-diabetes", "type-2-diabetes", "gestational-diabetes", "diabetes-insipidus", "diabetic-eye-screening", "diabetic-ketoacidosis", "diabetic-retinopathy", "dialysis", 
    "differences-in-sex-development", "digeorge-syndrome", "diphtheria", "discoid-eczema", "dislocated-kneecap", "dislocated-shoulder", "disorders-of-consciousness", "dissociative-disorders", "diverticular-disease-and-diverticulitis", "dizziness", 
    "do-not-attempt-cardiopulmonary-resuscitation-dnacpr-decisions", "double-vision", "downs-syndrome", "dry-eyes", "sore-or-dry-lips", "dry-mouth", "dupuytrens-contracture", "deep-vein-thrombosis-dvt", "restricted-growth", "dysarthria", "dyslexia", "swallowing-problems- dysphagia", 
    "developmental-coordination-disorder-dyspraxia-in-adults", "developmental-coordination-disorder-dyspraxia", "dystonia",

    "ear-infections", "earache", "perforated-eardrum", "early-menopause", "early-or-delayed-puberty", "earwax-build-up", "eating-disorders", "ebola-virus-disease", "echocardiogram", "heart-palpitations", "ectopic-pregnancy", "ectropion", "atopic-eczema", "contact-dermatitis", "discoid-eczema", 
    "varicose-eczema", "edwards-syndrome-(trisomy-18)", "ehlers-danlos-syndromes", "ejaculation-problems", "elbow-and-arm-pain", "electrocardiogram", "electroencephalogram", "electrolyte-test", "embolism", "emollients", "empyema", "encephalitis", "endocarditis", "womb-cancer", "endometriosis", 
    "endoscopy", "enhanced-recovery", "epidermolysis-bullosa", "epididymitis", "epidural", "epiglottitis", "epilepsy", "erection-problems-erectile-dysfunction", "erythema-multiforme", "erythema-nodosum", "erythromelalgia", "tremor-or-shaking-hands", "euthanasia-and-assisted-suicide", "ewing-sarcoma", 
    "excessive-daytime-sleepiness-hypersomnia", "excessive-hair-growth-hirsutism", "excessive-sweating-hyperhidrosis", "excessive-thirst", "eye-cancer", "floaters-and-flashes-in-the-eyes", "herpes-simplex-eye-infections", "eye-injuries", "eye-tests-for-children", "eyelid-problems",

    "fabricated-or-induced-illness", "face-blindness", "fainting", "falls", "flatulence", "febrile-seizures", "feeling-sick-nausea", "female-genital-mutilation-fgm", "femoral-hernia-repair", "fever-in-adults", "fever-in-children", "fibroids", "fibromyalgia", "finger-pain", "first-aid", "febrile-seizures", 
    "what-to-do-if-someone-has-a-seizure", "flat-feet", "plagiocephaly-and-brachycephaly", "floaters-and-flashes-in-the-eyes", "flu", "fluoride", "foetal-alcohol-spectrum-disorder", "food-allergy", "food-colours-and-hyperactivity", "food-intolerance", "food-poisoning", "foot-drop", "foot-pain", "foreskin-problems", 
    "phimosis", "frontotemporal-dementia", "frostbite", "frozen-shoulder", "medically-unexplained-symptoms", "fungal-nail-infection",

    "gallbladder-cancer", "acute-cholecystitis", "gallbladder-removal", "gallstones", "ganglion-cyst", "gangrene", "gastrectomy", "gastritis", "heartburn-and-acid-reflux", "gastroparesis", "gastroscopy", "gender-dysphoria", "general-anaesthesia", "genetic-and-genomic-testing", "predictive-genetic-tests-cancer", 
    "genital-herpes", "genital-warts", "rubella", "gestational-diabetes", "temporal-arteritis", "giardiasis", "acromegaly", "gilberts-syndrome", "glaucoma", "glomerulonephritis", "glue-ear", "glutaric-aciduria", "goitre", "gonorrhoea", "gout", "granuloma-annulare", "granulomatosis-with-polyangiitis", "group-b-strep", 
    "growing-pains", "guillain-barre-syndrome", "gum-disease",

    "haemochromatosis", "haemophilia", "hib", "piles-haemorrhoids", "hair-dye-reactions", "hair-loss", "hairy-cell-leukaemia", "bad-breath", "hamstring-injury", "hand-pain", "hand-tendon-repair", "hand-foot-and-mouth-disease", "having-surgery", "hay-fever", "head-and-neck-cancer", "head-injury-and-concussion", "head-lice-and-nits", 
    "headaches", "hormone-headaches", "tension-headaches", "hearing-aids-and-implants", "hearing-loss", "hearing-tests", "hearing-tests-for-children", "heart-attack", "heart-block", "coronary-artery-bypass-graft-cabg", "coronary-heart-disease", "heart-failure", "chest-pain", "heart-palpitations", "arrhythmia", "heart-transplant", 
    "mitral-valve-problems", "aortic-valve-replacement", "heart-lung-transplant", "heartburn-and-acid-reflux", "heat-exhaustion-and-heatstroke", "heat-rash-prickly-heat", "heavy-periods", "heel-pain", "henoch-schönlein-purpura-hsp", "hepatitis", "hepatitis-a", "hepatitis-b", "hepatitis-c", "herbal-medicines", "herceptin", 
    "hereditary-haemorrhagic-telangiectasia", "hereditary-neuropathy", "hereditary-spastic-paraplegia", "hernia", "femoral-hernia-repair", "hiatus-hernia", "inguinal-hernia-repair", "umbilical-hernia-repair", "genital-herpes", "neonatal-herpes", "herpes-simplex-eye-infections", " herpetic-whitlow", "hiatus-hernia", "hiccups",
    "hidradenitis-suppurativa", "high-blood-pressure-hypertension", "high-blood-sugar-hyperglycaemia", "high-cholesterol", " fever-in-adults", "fever-in-children", "developmental-dysplasia-of-the-hip", "hip-fracture", "hip-pain", "hip-pain-in-children-irritable-hip", "hip-replacement", "hirschsprungs-disease", "hirsutism", "hiv-and-aids",
    "hives", "hoarding-disorder", "hodgkin-lymphoma", "home-oxygen-therapy", "homeopathy", "homocystinuria", "worms-in-humans", "hormone-headaches", "hormone-replacement-therapy-(hrt)", "hrt,-see-hormone-replacement-therapy-hrt", "antiphospholipid-syndrome", "human-papilloma-virus-hpv", "huntingtons-disease", "hydrocephalus", "hydronephrosis", 
    "hyperacusis", " excessive-sweating-hyperhidrosis", "hyperparathyroidism", "excessive-daytime-sleepiness-hypersomnia", "overactive-thyroid-hyperthyroidism", "hypnotherapy", "low-blood-sugar-hypoglycaemia", "hypoparathyroidism", "low-blood-pressure-hypotension", "hypothermia", " underactive-thyroid-hypothyroidism", "hysterectomy", "hysteroscopy",

    "irritable-bowel-syndrome-ibs", "ichthyosis", "idiopathic-pulmonary-fibrosis", "ileostomy", "impetigo", "erection-problems-erectile-dysfunction", "urinary-incontinence", "indigestion", "infected-piercings", "infertility", "inflammatory-bowel-disease", "flu", "ingrown-hairs", "ingrown-toenail", "inguinal-hernia-repair", "insect-bites-and-stings", 
    "insomnia", "intensive-care", " differences-in-sex-development", "interstitial-cystitis", "intracranial-hypertension", "intrauterine-insemination", "iron-deficiency-anaemia", "irregular-periods", "irritable-bowel-syndrome-ibs", "isovaleric-acidaemia", "itchy-bottom", "itchy-skin", "ivf",

    "japanese-encephalitis", "jaundice", "jaundice-newborn", "temporomandibular-disorder-tmd", "jellyfish-and-other-sea-creature-stings", "jet-lag", "joint-hypermobility-syndrome", "joint-pain",

    "kaposis-sarcoma", "kawasaki-disease", "keloid-scars", "keratosis-pilaris", "kidney-cancer", "kidney-disease", "kidney-infection", "kidney-stones", "kidney-transplant", "klinefelter-syndrome", "meniscus-tear", "knee-ligament-surgery", "knee-pain", "knee-replacement", "knock-knees", "knocked-out-tooth", "kwashiorkor", "kyphosis",

    "labial-fusion", "labyrinthitis-and-vestibular-neuritis", "ldh-test", "lactose-intolerance", "lambert-eaton-myasthenic-syndrome", "laparoscopy", "laryngeal-cancer", "laryngitis", "laser-eye-surgery-and-lens-surgery", "laxatives", "lazy-eye", "learning-disabilities", "leg-cramps", "leg-ulcer", "legionnaires-disease", "leptospirosis", 
    "acute-lymphoblastic-leukaemia", "acute-myeloid-leukaemia", "chronic-lymphocytic-leukaemia", "chronic-myeloid-leukaemia", "hairy-cell-leukaemia", "leukoplakia", "lichen-planus", "lichen-sclerosus", "limping-in-children", "lipoedema", "lipoma", " sore-or-dry-lips", "listeriosis", "liver-cancer", "liver-disease", "alcohol-related-liver-disease",
    "liver-transplant", "local-anaesthesia", "long-qt-syndrome", "long-sightedness", "lost-or-changed-sense-of-smell", "loss-of-libido", "low-sperm-count", "low-white-blood-cell-count", "lumbar-decompression-surgery", "lumbar-puncture", "lumps", "lung-cancer", "lung-transplant", "lupus", "lyme-disease", "lymphoedema",

    "age-related-macular-degeneration-(amd)", "macular-hole", "magnesium-test", "malaria", "male-menopause", "malignant-brain-tumour-(brain-cancer)", "mallet-finger", "malnutrition", "breast-screening-mammogram", "maple-syrup-urine-disease", "marfan-syndrome", "mastectomy", "mastitis", "mastocytosis", "mastoiditis", "mcadd", "measles", "medical-cannabis",
    "medically-unexplained-symptoms", "medicines-information", "memory-loss-amnesia", "meningitis", "menopause", "early-menopause", "period-pain", "mesothelioma", "metabolic-syndrome", "metallic-taste", "foot-pain", "middle-east-respiratory-syndrome-mers", "migraine", "miscarriage", "mitral-valve-problems", "molar-pregnancy", "moles", "molluscum-contagiosum", 
    "monkeypox", "morton's-neuroma", "motion-sickness", "motor-neurone-disease", "mouth-cancer", "oral-thrush-mouth-thrush", "mouth-ulcers", "mri-scan", "mrsa", "mucositis", "multiple-myeloma", "multiple-sclerosis", "multiple-system-atrophy", "mumps", "munchausen-syndrome", "muscular-dystrophy", "chronic-fatigue-syndrome-cfs", "myasthenia-gravis",
    "mycobacterium-chimaera-infection", " myelodysplasia", "multiple-myeloma", "short-sightedness", "myositis", "menieres-disease",

    "fungal-nail-infection", "nail-patella-syndrome", "nail-problems", "nappy-rash", "narcolepsy", "nasal-and-sinus-cancer", "nasal-polyps", "nasopharyngeal-cancer", "feeling-sick-nausea", "neck-pain", "necroting-fasciitis", "neonatal-herpes", "nephrotic-syndrome", "neuroblastoma", "neuroendocrine-tumours", "carcinoid-syndrome", "neurofibromatosis-type-1", 
    "neurofibromatosis-type-2", "neuromyelitis-optica", "newborn-jaundice", "newborn-respiratory-distress-syndrome", "nhs-screening", "night-sweats", "night-terrors ", "nipple-discharge", "hyperacusis", "non-alcoholic-fatty-liver-disease", "non-allergic-rhinitis", "non-gonococcal-urethritis", "non-hodgkin-lymphoma", "noonan-syndrome", "norovirus", "nasal-and-sinus-cancer", 
    "nosebleed", "nsaids",

    "obesity", "sleep-apnoea", "occupational-therapy", "oesophageal-atresia", "oesophageal-cancer", "orf", "orthodontics", "osteoarthritis", "rickets-and-osteomalacia", "osteomyelitis", "osteopathy", "osteophyte", "osteoporosis", "otosclerosis", "ovarian-cancer", "ovarian-cyst", "overactive-thyroid-hyperthyroidism", "ovulation-pain", "home-oxygen-therapy",

    "pacemaker-implantation", "pagets-disease-bone", "pagets-disease-nipple", "testicles-pain", " hand-pain",  "interstitial-cystitis", "heart-palpitations", "pancreas-transplant", "pancreatic-cancer", "acute-pancreatitis", "pancreatitis-chronic", "panic-disorder", "paralysis", "parkinsons-disease", "pataus-syndrome", "peak-flow-test", "pelvic-inflammatory-disease", "pelvic-organ-prolapse",
    "pelvic-pain", "pemphigus-vulgaris", "penile-cancer", "perforated-eardrum", "pericarditis", "menopause", "period-pain", "periods", "heavy- periods", "irregular-periods", "stopped-or-missed- periods", "peripheral-arterial-disease-pad", "peripheral-neuropathy", "peritonitis", "persistent-trophoblastic-disease-and-choriocarcinoma", "personality-disorders", "pet-scan", "phaeochromocytoma", 
    "phenylketonuria", "tight-foreskin", "phlebitis", "phobias", "phosphate-test", "photodynamic-therapy", "physiotherapy", "piles-haemorrhoids", "pilonidal-sinus", "pins-and-needles", "PIP-breast-implants", "pityriasis-rosea", "pityriasis-versicolor", "plagiocephaly-brachycephaly", "plantar-fasciitis", "plastic-surgery", "pleurisy", "pre-menstrual-syndrome)", "pneumonia", "poisoning", "polio", 
    "autosomal-dominant-polycystic-kidney-disease-adpkd", "autosomal-recessive-polycystic-kidney-disease-arpkd", "polycystic-ovary-syndrome", "polycythaemia", "polyhydramnios", "polymorphic-light-eruption", "polymyalgia-rheumatica", "pompholyx", "bakers-cyst", "post-herpetic-neuralgia", "post-mortem", "post-polio-syndrome", "postmenopausal-bleeding", "postnatal-depression", "postpartum-psychosis", 
    "postural-tachycardia-syndrome", "potassium-test", "prader-willi-syndrome", "pre-eclampsia", "predictive-genetic-tests-for-cancer-risk-genes", "ejaculation-problems", "pressure-sores", "priapism-painful-erections", "heat-rash-prickly-heat", "primary-biliary-cholangitis-pbc", "probiotics", "problems-swallowing-pills", "anal-pain", "progressive-supranuclear-palsy", "pelvic-organ-prolapse", "face-blindness", 
    "prostate-cancer", "benign-prostate-enlargement", "prostate-problems", "prostatitis", "psoriasis", "psoriatic-arthritis", "psychiatry", "psychosis", "psychotic-depression", "early-or-delayed-puberty", "pubic-lice", "pudendal-neuralgia", "pulmonary-embolism", "idiopathic-pulmonary-fibrosis", "pulmonary-hypertension", "pyoderma-gangrenosum",

    "q-fever", "tonsillitis",

    "rabies", "radiotherapy", "rashes-in-babies-and-children", "raynaud's", "reactive-arthritis", "rectal-bleeding", "rectal-examination", "red-blood-cell-count", "red-eye", "reflux-in-babies", "repetitive-strain-injury-rsi", "respiratory-tract-infections", "restless-legs-syndrome", "restricted-growth", "detached-retina-retinal-detachment", "retinal-migraine", "retinoblastoma", "rett-syndrome", "reyes-syndrome", 
    "rhesus-disease", "rheumatic-fever", "rheumatoid-arthritis", "allergic-rhinitis", "rickets-and-osteomalacia", "ringworm", "root-canal-treatment", "rosacea", "roseola", "rubella",

    "salivary-gland-stones", "sarcoidosis", "scabies", "scarlet-fever", "scars", "schistosomiasis-(bilharzia)", "schizophrenia", "sciatica", "scleroderma", "scoliosis", "scurvy", "febrile-seizures", " what-to-do-if-someone-has-a-seizure-(fit)", "selective-mutism", "see-lost-or-changed-sense-of-smell", "sepsis", "septic-arthritis", "severe-head-injury", "sexually-transmitted-infections-stis", " tremor-or-shaking-hands", 
    "shin-splints", "shin-splints", "shingles", "short-sightedness-myopia", "shortness-of-breath", "shoulder-impingement", "shoulder-pain", "sick-building-syndrome", "sickle-cell-disease", "silicosis", "sinusitis-sinus-infection", "sjogrens-syndrome", "skin-cyst", "skin-picking-disorder", "skin-tags", "slapped-cheek-syndrome", "sleep-apnoea", "sleep-paralysis", "sleepwalking", "slipped-disc", "small-bowel-transplant", 
    "cervical-screening", "smelly-feet", "smelly-urine", "stop-stop-smoking-treatments", "snake-bites", "snoring", "soft-tissue-sarcomas", "soiling-child-pooing-their-pants", "actinic-keratoses", "sore-or-white-tongue", "sore-throat", "spina-bifida", "spinal-muscular-atrophy", "spirometry", "spleen-problems-and-spleen-removal", "spondylolisthesis", "sports-injuries", "sprains-and-strains", "squint", "stammering", 
    "staph-infection", "statins", "stem-cell-and-bone-marrow-transplants", "coronary-angioplasty", "topical-steroids", "steroid-inhalers", "steroid-injections", "anabolic-steroid-misuse", "steroid-nasal-sprays", "steroid-tablets", "steroids", "stevens-johnson-syndrome", "stillbirth", "insect-bites-and-stings", "stomach-ache", "stomach-cancer", "stomach-ulcer", "stop-smoking-treatments", "stopped-or-missed-periods", 
    "strep-A", "stretch-marks", "stroke", "stammering", "stye", "subarachnoid-haemorrhage", "subdural-haematoma", "confusion", "sudden-infant-death-syndrome-sids", "sunburn", "phlebitis", "supraventricular-tachycardia-svt", "having-surgery", "problems-swallowing-pills", "swallowing-problems-dysphagia", "night-sweats", "oedema", "swollen-arms-and-hands-oedema", "swollen-glands", "syphilis",

    "tailbone-coccyx-pain", "worms-in-humans", "tay-sachs-disease", "teeth-grinding", "teeth-whitening", "temporal-arteritis", "temporomandibular-disorder-tmd", "tendonitis", "tennis-elbow", " transcutaneous-electrical-nerve-stimulation- tens", "tension-headaches", "testicle-lumps-and-swellings", "testicle-pain", "testicular-cancer", "tetanus", "thalassaemia", "male-menopause", " excessive-thirst", "cervical-rib",
    "threadworms", "sore-throat", "thrombophilia", "thrush-in-men-and-women", "thumb-pain", "thyroid-cancer", "thyroiditis", "transient-ischemic-attack-tia", "tick-borne-encephalitis", "tics", "phimosis", "tinnitus", "toe-pain", "sore-or-white-tongue", "mouth-cancer", "tongue-tie", "tonsillitis", "chipped,-broken-or-cracked-tooth", "tooth-decay", "knocked-out-tooth", "toothache", "topical-corticosteroids", "tibc-test",
    "total-protein-test", "tourettes-syndrome", "toxic-shock-syndrome", "toxocariasis", "toxoplasmosis", "tracheostomy", "transient-ischemic-attack-tia", "transurethral-resection-of-the-prostate-turp", "travel-vaccinations", "tremor-or-shaking-hands", "trichomoniasis", "trigeminal-neuralgia", "trigger-finger", "trimethylaminuria", "tuberculosis-tb", "tuberous-sclerosis", "stomach-ache", "turner-syndrome", "twitching-eyes-and-muscles", 
    "type-1-diabetes", "type-2-diabetes", "typhoid-fever", "typhus",

    "ulcerative-colitis", "ultrasound-scan", "umbilical-hernia-repair", "underactive-thyroid-(hypothyroidism)", "undescended-testicles", "unintentional-weight-loss", "non-gonococcal-urethritis", "urinary-catheter", "urinary-incontinence", "urinary-tract-infections-utis", "smelly-urine", "acr-test", "womb-cancer", "uveitis",

    "vaginal-cancer", "vaginal-discharge", "vaginal-dryness", "vulvodynia", "vaginismus", "vaginitis", "varicose-eczema", "varicose-veins", "vascular-dementia", "vasculitis", "disorders-of-consciousness-vegetative-state", "venous-leg-ulcer", "vertigo", "labyrinthitis-and-vestibular-neuritis-vestibular-neuritis", "acoustic-neuroma-vestibular-schwannoma", "vitamin-b12-or-folate-deficiency-anaemia", "vitamins-and-minerals", "vitiligo", 
    "vomiting-blood", "norovirus ", "von-willebrand-disease", "vulval-cancer",

    "warts-and-verrucas", "watering-eyes", "unintentional-weight-loss", "unintentional-weight-loss", "weight-loss-surgery", "leptospirosis", "west-nile-virus", "what-to-do-if-someone-has-a-seizure-fit", "whiplash", "low-white-blood-cell-count", "herpetic-whitlow", "whooping-cough", "flatulence", "norovirus", "wisdom-tooth-removal", "wolff-parkinson-white-syndrome", "womb-cancer", "worms-in-humans", "wrist-pain",

    "x-ray",

    "yellow-fever",

    "zika-virus"

])

medicines_terms = set(["aciclovir", "acrivastine", "adalimumab", "alendronic-acid", "allopurinol", "alogliptin", "amitriptyline-for-depression", "amitriptyline-for-pain", "amlodipine", "amoxicillin", "anastrozole", "apixaban", "aspirin-for-pain-relief", "low-dose-aspirin", "atenolol", "atorvastatin", "azathioprine", "azithromycin",

                       "baclofen", "beclometasone-inhalers", "beclometasone-nasal-spray", "beclometasone-skin-creams", "beclometasone-tablets", "bendroflumethiazide", "benzoyl-peroxide", "benzydamine", "betahistine", "betamethasone-eyes-ears-and-nose", "betamethasone-skin", "betamethasone-tablets", "bimatoprost", "bisacodyl", "bisoprolol", "brinzolamide", "budesonide-inhalers", "budesonide-nasal-spray", 
                       "budesonide-rectal-foam-and-enemas", "budesonide-tablets-capsules-and-granules", "bumetanide", "buprenorphine-for-pain", "buscopan-hyoscine-butylbromide",

                       "calcipotriol", "candesartan", "carbamazepine", "carbimazole", "carbocisteine", "carmellose-sodium", "carvedilol", "cefalexin", "cetirizine", "champix-varenicline", "chloramphenicol", "chlorhexidine", "chlorphenamine-including-piriton", "cinnarizine", "ciprofloxacin", "citalopram", "clarithromycin", "clobetasol", "clobetasone", "clonazepam", "clopidogrel", "clotrimazole", 
                       "clotrimazole-for-thrush", "co-amoxiclav", "co-beneldopa", "co-careldopa", "co-codamol-for-adults", "co-codamol-for-children", "co-codaprin", "co-dydramol", "coal-tar", "codeine", "colchicine", "colecalciferol", "cyanocobalamin", "cyclizine",

                       "dabigatran", "dapagliflozin", "dexamethasone-eye-drops", "dexamethasone-tablets-and-liquid", "diazepam", "diclofenac", "digoxin", "dihydrocodeine", "diltiazem", "diphenhydramine", "dipyridamole", "docusate", "domperidone", "donepezil", "dosulepin", "doxazosin", "doxycycline", "duloxetine",

                       "edoxaban", "empagliflozin", "enalapril", "eplerenone", "erythromycin", "escitalopram", "esomeprazole", "ezetimibe",

                       "felodipine", "fentanyl", "ferrous-fumarate", "ferrous-sulfate", "fexofenadine", "finasteride", "flucloxacillin", "fluconazole", "fluoxetine-prozac", "fluticasone-inhalers", "fluticasone-nasal-spray-and-drops", "fluticasone-skin-creams", "folic-acid", "furosemide", "fusidic-acid", "fybogel-ispaghula-husk",

                       "gabapentin", "gaviscon", "gliclazide", "glimepiride", "glyceryl-trinitrate-gtn",

                       "heparinoid", "hydrocortisone", "hydrocortisone-buccal-tablets", "hydrocortisone-for-piles-and-itchy-bottom", "hydrocortisone-for-skin", "hydrocortisone-injections", "hydrocortisone-rectal-foam", "hydrocortisone-tablets", "hydroxocobalamin", "hydroxychloroquine", "hyoscine-hydrobromide",

                       "ibuprofen-and-codeine", "ibuprofen-for-adults", "ibuprofen-for-children", "indapamide", "irbesartan", "isosorbide-mononitrate-dinitrate", "isotretinoin-capsules", "isotretinoin-gel",

                       "ketoconazole",

                       "labatalol", "lactulose", "lamotrigine", "lansoprazole", "latanoprost", "lercanidipine", "letrozole", "levetiracetam", "levothyroxine", "lidocaine-for-mouth-and-throat", "lidocaine-for-piles-and-itchy-bottom", "lidocaine-skin-cream", "linagliptin", "lisinopril", "lithium", "loperamide", "loratadine", "lorazepam", "losartan", "low-dose-aspirin", "lymecycline",

                       "macrogol", "mebendazole", "mebeverine", "melatonin", "memantine", "mesalazine", "metformin", "methadone", "methotrexate", "methylphenidate-for-adults", "methylphenidate-for-children", "metoclopramide", "metoprolol", "metronidazole", "mirabegron", "mirtazapine", "molnupiravir", "mometasone-for-skin", "mometasone-inhalers", "mometasone-nasal-spray", "montelukast", "morphine",

                       "naproxen", "nefopam", "nicorandil", "nifedipine", "nitrofurantoin", "nortriptyline", "nystatin",

                       "olanzapine", "olmesartan", "omeprazole", "oxybutynin", "oxycodone",

                       "pantoprazole", "paracetamol-for-adults", "paracetamol-for-children", "paroxetine", "paxlovid", "peppermint-oil", "pepto-bismol", "perindopril", "phenoxymethylpenicillin", "phenytoin", "pioglitazone", "pravastatin", "prednisolone", "pregabalin", "prochlorperazine", "promethazine", "propranolol", "pseudoephedrine",

                       "quetiapine",

                       "rabeprazole", "ramipril", "ranitidine", "remdesivir-veklury", "risedronate", "risperidone", "rivaroxaban", "ropinirole", "rosuvastatin",

                       "salbutamol-inhaler", "saxagliptin", "senna", "sertraline", "sildenafil-viagra", "simeticone", "simvastatin", "sitagliptin", "sodium-cromoglicate-capsules", "sodium-cromoglicate-eye-drops", "sodium-valproate", "solifenacin", "sotalol", "sotrovimab", "spironolactone", "sulfasalazine", "sumatriptan",

                       "tadalafil", "tamsulosin", "temazepam", "terbinafine", "thiamine-vitamin-b1", "ticagrelor", "timolol-eye-drops", "timolol-tablets", "tolterodine", "topiramate", "tramadol", "tranexamic-acid", "trazodone", "trimethoprim",

                       "valproic-acid", "valsartan", "champix-varenicline", "venlafaxine", "verapamil",

                       "warfarin",

                       "zolpidem", "zopiclone"

                       ])

medical_terms_list = list(medical_terms)
choose = random.choice(medical_terms_list)
print(choose)
