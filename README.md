# Student Management System (Projet de fin d'année)

🎓 **Student Management System** est une application web développée avec Django destinée à la gestion complète des établissements scolaires et universitaires. Ce projet a pour objectif de faciliter la gestion des étudiants, du personnel, des cours, des absences et des résultats, tout en offrant une interface moderne, intuitive et sécurisée. Il intègre également un chatbot pédagogique basé sur l'IA pour accompagner les étudiants.

---

## Sommaire

- [Fonctionnalités](#fonctionnalités)
- [Architecture du projet](#architecture-du-projet)
- [Technologies utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Capture d'écran](#capture-décran)
- [Structure des rôles](#structure-des-rôles)
- [Limites et perspectives](#limites-et-perspectives)
- [Auteurs](#auteurs)

---

## Fonctionnalités

- **Gestion des étudiants** : inscription, modification, consultation du profil.
- **Gestion du personnel** : ajout/removal de professeurs et staff, attribution aux matières.
- **Gestion des cours et matières** : création, modification et affectation aux classes.
- **Gestion des absences** : pointage, suivi des absences par matière.
- **Gestion des résultats** : saisie et consultation des notes par matière.
- **Interface d'administration** : tableau de bord pour l’admin, gestion centralisée des ressources.
- **Chatbot pédagogique** : assistance aux étudiants (notes, absences, orientation, motivation, etc.) via une IA intégrée.
- **Gestion des rôles** : accès différencié pour les administrateurs, enseignants et étudiants.
- **Notifications** : alertes pour absences, résultats, nouveaux messages, etc.

---

## Architecture du projet

- **Backend** : Django (Python)
- **Base de données** : MySQL
- **Frontend** : HTML, CSS, JavaScript (Bootstrap pour le style)
- **Chatbot IA** : intégration d'une API IA externe pour l'assistant pédagogique

```
student-management-system-pfa/
│
├── student_management_system/      # Racine Django
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── student_management_app/         # App principale
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   ├── static/
│   └── ...
│
├── templates/
├── static/
├── requirements.txt
└── README.md
```

---

## Technologies utilisées

- Django 4.x (framework web Python)
- MySQL (gestion de base de données)
- HTML5, CSS3, JavaScript, Bootstrap (frontend)
- API OpenRouter ou équivalent (pour le chatbot IA)
- Autres : pandas, requests, etc.

---

## Installation

### Prérequis

- Python 3.8+
- MySQL Server
- pip (gestionnaire de paquets Python)
- (Optionnel) un environnement virtuel

### Étapes

1. **Cloner le dépôt**

   ```bash
   git clone https://github.com/othmane-tanji/student-management-system-pfa.git
   cd student-management-system-pfa
   ```

2. **Créer et activer un environnement virtuel (recommandé)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Ou .\venv\Scripts\activate sous Windows
   ```

3. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la base de données**

   - Créez une base de données MySQL (ex : `student_management_db`).
   - Configurez le fichier `settings.py` avec vos identifiants MySQL :
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'student_management_db',
             'USER': 'votre_utilisateur',
             'PASSWORD': 'votre_mot_de_passe',
             'HOST': 'localhost',
             'PORT': '3306',
         }
     }
     ```

5. **Appliquer les migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Créer un superutilisateur**

   ```bash
   python manage.py createsuperuser
   ```

7. **Lancer le serveur**

   ```bash
   python manage.py runserver
   ```

8. **Accéder à l’application**

   - Interface web : http://127.0.0.1:8000/
   - Interface d’administration : http://127.0.0.1:8000/admin

---

## Utilisation

- Connectez-vous selon votre rôle (admin, staff, étudiant).
- L’administrateur peut gérer les utilisateurs, matières, résultats, etc.
- Les enseignants peuvent consulter et saisir les notes, la présence.
- Les étudiants consultent leurs notes, absences, emploi du temps et peuvent interagir avec le chatbot via l’interface dédiée.

---

## Capture d’écran

> *(Ajoutez ici quelques captures d’écrans de l’interface principale, du dashboard admin, du chatbot, etc.)*

---

## Structure des rôles

- **Administrateur** : gestion complète du système (utilisateurs, matières, staff, résultats, configuration générale)
- **Staff (enseignant/professeur)** : gestion des notes, absences, consultation des listes d’étudiants de ses matières
- **Étudiant** : consultation de son profil, suivi des notes et absences, assistance via le chatbot

---

## Limites et perspectives

- Le système ne prend pas encore en charge la visioconférence ou les classes en ligne comme Microsoft Teams (fonctionnalité envisagée mais complexe à intégrer dans cette version).
- Possibilité d’étendre les fonctionnalités du chatbot (prise de rendez-vous, FAQ, etc.).
- Améliorer la sécurité et l’ergonomie mobile.
- Ajouter une gestion des emplois du temps dynamique.

---

## Auteurs

- [Othmane Tanji](https://github.com/othmane-tanji)
- Encadrants : *(À compléter)*

---

## Licence

Ce projet est publié sous une licence "Other". Voir le fichier LICENSE pour plus de détails.

---

*Projet réalisé dans le cadre du projet de fin d’année universitaire.*