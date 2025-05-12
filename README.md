<h1 align="center">🎓 Portail Universitaire - Student Management System</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Backend-Django-blue.svg" />
  <img src="https://img.shields.io/badge/Frontend-AdminLTE%20%2B%20Bootstrap-green.svg" />
  <img src="https://img.shields.io/badge/Database-MariaDB-lightgrey.svg" />
  <img src="https://img.shields.io/badge/Architecture-MVT-purple.svg" />
</p>

<p align="center">
  Une application web complète pour la gestion universitaire : étudiants, professeurs, cours, notes et présence.
</p>

---

## 🌐 Description

Ce projet est un portail universitaire développé en **Django** (backend) avec un frontend basé sur **AdminLTE**, **Bootstrap**, **HTML** et **CSS**. Il permet aux administrateurs, professeurs et étudiants d’interagir via un système de rôles bien défini.

---

## 🧠 Fonctionnalités principales

- 🔐 Authentification & gestion des rôles :
  - Admin
  - Professeur
  - Étudiant
- 🧑‍🎓 Gestion des étudiants (création, modification, suppression)
- 📚 Gestion des matières, cours et notes
- 🗓️ Suivi de la présence
- 📁 Gestion des documents/cours
- 📊 Tableau de bord selon le rôle
- ✉️ Notifications internes

---

## 🛠️ Technologies utilisées

| Composant     | Technologie               |
|---------------|---------------------------|
| Backend       | Django                    |
| Frontend      | AdminLTE, Bootstrap, HTML, CSS |
| Base de données | MariaDB                |
| Architecture  | MVT (Model - View - Template) |
| Authentification | Django auth + rôles personnalisés |

---

## 🔧 Installation

### Prérequis

- Python 3.9+
- Django
- MariaDB
- Node.js (si besoin pour assets statiques)

### Étapes

```bash
# Cloner le dépôt
git clone https://github.com/othmane-tanji/student-management-system-pfa.git
cd student-management-system-pfa

# Créer un environnement virtuel
python -m venv env
source env/bin/activate  # ou env\Scripts\activate sous Windows

# Installer les dépendances
pip install -r requirements.txt

# Configuration de la base de données
# Mettre à jour les infos dans settings.py

# Appliquer les migrations
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
