Voici un résumé des fonctionnalités que nous avons développées jusqu'à présent, avec une explication sur le fonctionnement du code :

date: 16 octobre 2024
 1. Inscription et Connexion
   - Fonctionnalité : Nous avons créé des formulaires d'inscription et de connexion permettant aux utilisateurs de s'enregistrer et de se connecter en utilisant leur prénom, nom de famille, email, numéro de téléphone et mot de passe.
   - Explication : Lorsqu'un utilisateur s'inscrit, ses informations sont enregistrées dans la base de données Snowflake. Lorsqu'il se connecte, ses identifiants sont vérifiés dans la base de données avant de lui permettre l'accès.

2. Vérification de l'Unicité des Données
   - Fonctionnalité : Nous avons ajouté une vérification pour s'assurer que les éléments suivants soient uniques :
     - L'email doit être unique.
     - Le numéro de téléphone doit être unique.
     - La combinaison prénom + nom de famille doit être unique.
   - Explication : Avant d'autoriser l'enregistrement d'un utilisateur, une vérification est effectuée dans la base de données pour s'assurer que personne n'a déjà utilisé la même adresse email, le même numéro de téléphone ou la même combinaison prénom et nom de famille.

3. Sélection du Rôle (Étudiant ou Enseignant)
   - Fonctionnalité : Nous avons ajouté un champ déroulant dans le formulaire d'inscription qui permet aux utilisateurs de choisir leur rôle : soit **Étudiant** (1-student) ou **Enseignant** (2-teacher).
   - Explication : Lors de l'inscription, l'utilisateur sélectionne son rôle, qui est ensuite enregistré dans la base de données avec ses autres informations.

4. Message de Bienvenue Personnalisé
   -Fonctionnalité : Après l'inscription ou la connexion d'un utilisateur, un message de bienvenue personnalisé est affiché.
     - Si l'utilisateur est un enseignant, le message est : "Bienvenue, Professeur [nom de famille]".
     - Si l'utilisateur est un étudiant, le message est : "Bienvenue, [prénom] [nom de famille]".
   -Explication : Le code vérifie le rôle de l'utilisateur (enseignant ou étudiant) et affiche le message correspondant.

5. Gestion de l'État de Session
   - Fonctionnalité : Nous avons utilisé `st.session_state` pour gérer l'état de connexion des utilisateurs.
   - Explication : Après une inscription ou une connexion réussie, les informations de l'utilisateur (prénom, nom de famille, rôle) sont stockées dans `st.session_state`, ce qui permet de personnaliser la page d'accueil et de maintenir l'utilisateur connecté tant que la session est active.

Conclusion :
Nous avons mis en place un système complet d'inscription et de connexion qui gère les rôles des utilisateurs, vérifie l'unicité des données et affiche des messages de bienvenue adaptés selon le profil.