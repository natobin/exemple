import graphviz


class Graphe:
   # exemple de graphe non orienté sans boucle
    def __init__(self, dic_adj = None):
        if dic_adj is None:
            self.dic_adj = {}
        else:
            assert Graphe.est_valide(dic_adj), "Dictionnaire d\'adjacence invalide"
            self.dic_adj = dic_adj

    def est_valide(dic_adj):
        for som in dic_adj:
            for voisin in dic_adj[som]:
                if voisin not in dic_adj or som not in dic_adj[voisin]:
                    return False
        return True

    def est_vide(self):
        return self.dic_adj is {}

    def liste_sommets(self):
        return list(self.dic_adj.keys())
        #return list(self.dic_adj) #equivalent

    def ajoute_sommet(self, etiquette):
        if etiquette not in self.dic_adj:
            self.dic_adj[etiquette] = []

    def ajoute_arete(self, som1, som2):
        if som1 == som2:
            return
        if som1 not in self.dic_adj:
            self.ajoute_sommet(som1)
        if som2 not in self.dic_adj:
            self.ajoute_sommet(som2)
        if som2 not in self.dic_adj[som1]:
            self.dic_adj[som1].append(som2)
        if som1 not in self.dic_adj[som2]:
            self.dic_adj[som2].append(som1)

    def supprime_arete(self, som1, som2):
        if som2 in self.dic_adj[som1]:
            self.dic_adj[som1].remove(som2)
        if som1 in self.dic_adj[som2]:
            self.dic_adj[som2].remove(som1)

    def supprime_sommet(self, sommet):
        for autre_sommet in self.dic_adj[sommet]:
            self.dic_adj[autre_sommet].remove(sommet)
        del self.dic_adj[sommet]



    def matrice_adjacence(self):
        ''' dictionnaires supposés non ordonnées
        la fonction renvoie un tuple (liste d'étiquettes, matrice) où l'indice dans la liste d'étiquettes est le même que dans la matrice
        '''
        etiquettes = list(self.dic_adj.keys())
        matrice = [[False for s in range(len(etiquettes))] for st in range(len(etiquettes))]
        for index_sommet1 in range(len(etiquettes)):
            for sommet2 in self.dic_adj[etiquettes[index_sommet1]]:
                matrice[index_sommet1][etiquettes.index(sommet2)] = True
        return etiquettes, matrice



    def liste_aretes(self):
        aretes = []
        for sommet in self.dic_adj:
            for sommet2 in self.dic_adj[sommet]:
                if (sommet2, sommet) not in aretes:
                    aretes.append((sommet, sommet2))
        return aretes


    def parcours_simple(self, sommet):
        parcours = [sommet]
        autres = self.dic_adj[sommet].copy()
        while len(autres) > 0:
            for voisin in autres:
                if voisin not in parcours:
                    parcours.append(voisin)
                    for suivant in self.dic_adj[voisin]:
                        if suivant not in parcours:
                            autres.append(suivant)
                autres.remove(voisin)
        return parcours

    def parcours_en_largeur(self, sommet):
        parcours = [sommet]
        autres = self.dic_adj[sommet].copy()
        while len(autres) > 0:
            voisin = autres.pop(0)
            if voisin not in parcours:
                parcours.append(voisin)
                for suivant in self.dic_adj[voisin]:
                    if suivant not in parcours:
                        autres.append(suivant)
        return parcours

g = { "a" : ["d"],
          "b" : ["c"],
          "c" : ["b", "d", "e"],
          "d" : ["a", "c"],
          "e" : ["c"],
          "f" : []
    }

un_graphe = Graphe(g)
print(un_graphe.parcours_simple('e'))




