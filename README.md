# READ ME

## Preparez environnement
#### Dans le fichier /.env:
1. Modifier la variable DATA_PATH pour y mettre le chemin contenant les fichiers
des tweets

Pour tester commenter la ligne

    ENTRYPOINT=python3 /app/src/python/main.py

Et décommenter la ligne

    ENTRYPOINT=bash /app/scripts/pytest.sh
    
Pour lancer le server faire l'inverse

#### Dans le fichier /.config.yml
2. Ecrire le nom de chaque fichier des tweets à lire

3. (optionnel) Possible de modifier la taille du cache si besoin

## Lancer le container
A la racine du répertoire
### Construire l'image 
    
    docker-compose build

### Lancer le container
    docker-compose up

  
