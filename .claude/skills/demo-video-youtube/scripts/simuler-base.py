#!/usr/bin/env python3
"""Rend capturable hors de claude.ai un artefact qui lit sa base de données (capacité db).

Un tel artefact affiche « ouvre-moi depuis claude.ai » quand on l'ouvre en local : ses données
viennent de window.claude.use('db'). Ce script injecte une base simulée, remplie avec les
vraies données lues par ArtifactData (action list avec out_dir), pour pouvoir capturer la vraie
page avec capturer-page.cjs.

Usage :
  python3 -I simuler-base.py page.html donnees/ sortie.html [--etat 'JS exécuté avant la page']

- page.html : le HTML de l'artefact (Artifact read avec path "index.html").
- donnees/ : le dossier out_dir d'ArtifactData, avec un sous-dossier par collection
  (donnees/projects/*.json, donnees/steps/*.json…).
- --etat : du JavaScript facultatif exécuté avant la page, par exemple pour fixer l'onglet
  ouvert : "localStorage.setItem('cockpit.v2', JSON.stringify({project:'arteasy'}))".

La base simulée gère collection().onSnapshot / get, doc().get, et accepte les écritures
sans rien enregistrer. Elle sert à capturer, jamais à publier.
"""
import argparse, glob, json, os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("donnees")
    ap.add_argument("sortie")
    ap.add_argument("--etat", default="")
    a = ap.parse_args()
    D = {}
    for d in sorted(os.listdir(a.donnees)):
        p = os.path.join(a.donnees, d)
        if os.path.isdir(p):
            D[d] = [{"id": os.path.basename(f)[:-5], "data": json.load(open(f, encoding="utf-8"))}
                    for f in sorted(glob.glob(os.path.join(p, "*.json")))]
    mock = """<script>
/* base simulée (capture hors claude.ai) : vraies données lues par ArtifactData */
(function(){var D=%s;
function docs(c){return (D[c]||[]).map(function(d){return {id:d.id,exists:true,data:function(){return JSON.parse(JSON.stringify(d.data))}}})}
function snap(c){var x=docs(c);return {docs:x,size:x.length,empty:!x.length,forEach:function(f){x.forEach(f)}}}
function col(c){return {onSnapshot:function(cb){setTimeout(function(){cb(snap(c))},0);return function(){}},get:function(){return Promise.resolve(snap(c))},
  add:function(){return Promise.resolve({id:'x'})},where:function(){return col(c)},orderBy:function(){return col(c)},limit:function(){return col(c)}}}
function doc(path){var p=path.split('/'),c=p.slice(0,-1).join('/'),i=p[p.length-1],d=(D[c]||[]).filter(function(x){return x.id===i})[0];
  return {get:function(){return Promise.resolve({id:i,exists:!!d,data:function(){return d?JSON.parse(JSON.stringify(d.data)):undefined}})},
    onSnapshot:function(cb){setTimeout(function(){cb({id:i,exists:!!d,data:function(){return d?d.data:undefined}})},0);return function(){}},
    set:function(){return Promise.resolve()},update:function(){return Promise.resolve()},delete:function(){return Promise.resolve()}}}
var db={collection:col,doc:doc};
window.claude=window.claude||{};window.claude.use=function(){return Promise.resolve(db)};
try{%s}catch(e){}
})();
</script>
""" % (json.dumps(D, ensure_ascii=False).replace("</", "<\\/"), a.etat)
    s = open(a.page, encoding="utf-8").read()
    i = s.find("<script")
    s = s[:i] + mock + s[i:] if i >= 0 else mock + s
    open(a.sortie, "w", encoding="utf-8").write(s)
    print(f"{a.sortie} : {', '.join(f'{k} ({len(v)})' for k, v in D.items())}")


if __name__ == "__main__":
    main()
