# Memo Fresque du Climat

Ce projet contient toutes les données pour construire le [mémo de la Fresque du Climat](https://fresqueduclimat.org/memo/) à partir du logiciel générique ["Memo-viewer"](https://framagit.org/memo-fresques/memo-viewer).

## Contributors

* @moniquevanmaare : Dutch Translations

## Développement

**La documentation complète et à jour est présente sur le site [memo.fresque.earth](https://memo.fresque.earth/#/dev/)**.

Pour travailler sur le projet, il faut suivre les étapes suivantes :

1. Cloner le projet ["fresque-du-climat"](https://framagit.org/memo-fresques/fresque-du-climat)

```
git clone https://framagit.org/memo-fresques/fresque-du-climat.git fresque-du-climat
```

2. Cloner le projet ["memo-viewer"](https://framagit.org/memo-fresques/memo-viewer) à l’intérieur de `fresque-du-climat` avec le nom `memo-viewer` ou bien le cloner ailleurs puis créer un lien symbolique.

```
ln -s <path to memoviewer> <path to fresque du climat>/<memo-viewer>
```

3. Mettre à jour les données "imagées" (cartes, miniatures, et pdf)

4. Installer les dépendances de `memo-viewer`, avec la commande `npm run install:app`

5. Lancer le mémo, en utilisant les données du projet _Fresque du Climat_ en exécutant `npm run dev:app`. Cette commande

6. Le mémo est alors accessible localement à l'url `localhost:6173`.

Pour lancer l'interface d'administration, installer les dépendances avec `npm run install:admin` et lancer l'interface avec `npm run dev:admin`.
