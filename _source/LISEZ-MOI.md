# Page stylistes, source unique

La page existe en deux langues. **Ne jamais éditer les deux `index.html` à la
main** : ils sont régénérés depuis ce dossier et vos corrections seraient
écrasées au prochain passage.

```bash
cd site-radice
python3 _source/gen_stylistes.py              # écrit les deux pages
python3 _source/gen_stylistes.py --verifier   # compare sans rien écrire
```

## Où se trouve quoi

| Je veux changer | Fichier |
|---|---|
| Une phrase, un titre, un libellé de formulaire | `textes.json` |
| Un des six faits du bandeau | `donnees.json`, section `faits` |
| Une matière du mur, en ajouter ou en retirer une | `donnees.json`, section `macros` |
| La structure de la page, le CSS, le JavaScript | `gabarit.html` |

`textes.json` contient une entrée par langue pour la même clé. Corriger une
phrase française sans toucher à l'anglaise est possible, mais les deux pages
divergeront : c'est précisément ce que ce dossier sert à éviter.

Les clés préfixées `js_` sont des fragments de JavaScript, pas du texte
affiché. Elles portent les noms de jours et de mois, les messages de
validation de l'agenda, et le corps du courriel de rendez-vous. Leur syntaxe
doit rester valide : une apostrophe ou un guillemet mal placé casse la page.

## Les macros

Chaque entrée de `macros` porte le nom du fichier sur le CDN Shopify, la pièce
d'où il vient, et le nom de la matière dans les deux langues. Le recadrage
carré est fait par le CDN, pas par le navigateur.

Le mur est dessiné sur quatre colonnes sur écran, trois sur tablette, deux sur
téléphone. **Douze tuiles se répartissent sans trou dans les trois cas** ;
onze ou treize laisseraient une ligne incomplète. En ajouter ou en retirer
demande de revoir la grille dans `gabarit.html`, et le titre
« Six cuirs, trois fourrures, trois laines » dans `textes.json`.

## Le dossier n'est pas publié

Le workflow `.github/workflows/pages.yml` supprime `_source/` avant de
construire le site. Ces fichiers vivent dans le dépôt, pas sur le web.
