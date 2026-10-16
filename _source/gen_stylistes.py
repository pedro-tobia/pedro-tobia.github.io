#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genere les deux versions de la page stylistes depuis une source unique.

    cd site-radice && python3 _source/gen_stylistes.py

Ecrit  stylistes/index.html      (francais)
       stylistes/en/index.html   (anglais)

Pour corriger un texte, modifier _source/textes.json et relancer.
Pour changer un fait ou une matiere, modifier _source/donnees.json.
Pour toucher a la structure ou au CSS, modifier _source/gabarit.html.
Ne jamais editer les deux index.html a la main : ils seront ecrases.

L'option --verifier regenere sans rien ecrire et signale toute difference
avec les fichiers en place. Utile avant de committer.
"""
import io, json, os, sys, difflib

ICI  = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(ICI)
CDN  = "https://cdn.shopify.com/s/files/1/0613/3982/8400/files/"

SORTIE = {"fr": "stylistes/index.html", "en": "stylistes/en/index.html"}


def lire(nom):
    return io.open(os.path.join(ICI, nom), encoding="utf-8").read()


def rendre_faits(faits, langue):
    """Le bandeau des six faits. Le troisieme element est facultatif."""
    lignes = []
    for f in faits:
        titre, valeur, detail = f[langue]
        appoint = "<span>%s</span>" % detail if detail else ""
        lignes.append('  <div class="fait"><dt>%s</dt><dd>%s%s</dd></div>'
                      % (titre, valeur, appoint))
    return '<dl class="faits">\n%s\n</dl>' % "\n".join(lignes)


def rendre_macros(macros, langue, gabarit_alt):
    """Le mur des matieres. Une tuile carree par macro, recadree par le CDN."""
    tuiles = []
    for m in macros:
        matiere = m[langue]
        alt = gabarit_alt.format(matiere=matiere.lower(), piece=m["piece"])
        tuiles.append(
            '    <figure><img src="%s%s&amp;width=520&amp;height=520&amp;crop=center" alt="%s"\n'
            '      width="520" height="520" loading="lazy">'
            '<figcaption>%s<span>%s</span></figcaption></figure>'
            % (CDN, m["fichier"], alt, matiere, m["piece"]))
    return "\n".join(tuiles)


def construire(langue, gabarit, textes, donnees):
    page = gabarit
    page = page.replace("{{faits}}",  rendre_faits(donnees["faits"], langue))
    page = page.replace("{{macros}}", rendre_macros(
        donnees["macros"], langue, textes[langue]["alt_macro"]))
    for cle, valeur in textes[langue].items():
        if cle == "alt_macro":
            continue
        page = page.replace("{{%s}}" % cle, valeur)
    reste = [m for m in ("{{",) if m in page]
    if reste:
        i = page.index("{{")
        raise SystemExit("cle non remplacee en %s : %s" % (langue, page[i:i + 40]))
    return page


def main():
    verifier = "--verifier" in sys.argv
    gabarit = lire("gabarit.html")
    textes  = json.loads(lire("textes.json"))
    donnees = json.loads(lire("donnees.json"))

    ecart = False
    for langue, chemin in SORTIE.items():
        page = construire(langue, gabarit, textes, donnees)
        dest = os.path.join(BASE, chemin)
        actuel = io.open(dest, encoding="utf-8").read() if os.path.exists(dest) else ""
        if verifier:
            if actuel == page:
                print("%s : identique" % chemin)
            else:
                ecart = True
                print("%s : DIFFERENT" % chemin)
                for l in list(difflib.unified_diff(
                        actuel.split("\n"), page.split("\n"),
                        "en place", "genere", lineterm=""))[:30]:
                    print("   " + l)
        else:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            io.open(dest, "w", encoding="utf-8").write(page)
            etat = "inchange" if actuel == page else "mis a jour"
            print("%-26s %s  (%d octets)" % (chemin, etat, len(page)))

    if verifier and ecart:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
