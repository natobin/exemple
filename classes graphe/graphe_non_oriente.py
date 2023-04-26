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
        a_explorer = self.dic_adj[sommet].copy()
        vus = {sommet : True}
        while len(a_explorer) > 0:
            for voisin in a_explorer:
                if not voisin in vus:
                    parcours.append(voisin)
                    vus[voisin] = True
                    for suivant in self.dic_adj[voisin]:
                        if not suivant in vus:
                            a_explorer.append(suivant)
                a_explorer.remove(voisin)
        return parcours
      
    def parcours_en_largeur(self, sommet):
        parcours = [sommet]
        vus = {sommet:True}
        a_explorer = self.dic_adj[sommet].copy()
        while len(a_explorer) > 0:
            voisin =a_explorer.pop(0)
            if not voisin in vus:
                parcours.append(voisin)
                vus[voisin] = True
                for suivant in self.dic_adj[voisin]:
                    if not suivant in vus:
                        a_explorer.append(suivant)                            
        return parcours 
    
    def parcours_en_profondeur(self, sommet, parcours = None, vus = None):
        if parcours is None:
            parcours = [sommet]
            vus = {sommet: True}
        else:
            parcours.append(sommet)
            vus[sommet] = True
        for voisin in self.dic_adj[sommet]:
            if not voisin in vus:
                self.parcours_en_profondeur(voisin, parcours, vus)
        return parcours
    
    def sont_relies(self, sommet1, sommet2):
        if sommet1 == sommet2:
            return True
        vus = {sommet1: True}
        a_explorer = self.dic_adj[sommet1].copy()
        while len(a_explorer) > 0:
            voisin = a_explorer.pop(0)
            if voisin == sommet2:
                return True
            if not voisin in vus:
                vus[voisin] = True
                for suivant in self.dic_adj[voisin]:
                    if not suivant in vus:
                        a_explorer.append(suivant)                            
        return False
    
    def composantes_connexes(self):
        composantes = []
        vus = {s:False for s in self.dic_adj}
        for sommet in self.dic_adj:
            if not vus[sommet]:
                vus[sommet] = True
                une_composante = self.parcours_en_largeur(sommet)
                for coso in une_composante:
                    vus[coso] = True
                composantes.append(une_composante)
        return composantes
        
            
          
    def trouve_chemin(self, depart, arrivee):
        if self.sont_relies(depart, arrivee):
            a_explorer = self.dic_adj[depart].copy()
            vus = {voisin : depart for voisin in a_explorer}
            vus[depart] = None
            while len(a_explorer) > 0 and not arrivee in vus:
                voisin =a_explorer.pop(0)
                for suivant in self.dic_adj[voisin]:
                    if not suivant in vus:
                        a_explorer.append(suivant)   
                        vus[suivant] = voisin
            parcours = []
            but = arrivee
            while but is not None:
                parcours.append(but)
                but = vus[but]
            parcours.reverse()
            return parcours        
        
      
      
g = { "1" : ["2", "3"],
      "2" : ["1", "3", "4", "5"],
      "3" : ["1", "2", "5",  "7", "8"],
      "4" : ["2", "5"],
      "5" : ["2", "3", "4", "6"],
      "6" : ["5"],
      "7" : ["3", "8"],
      "8" : ["3", "7"],
      "9" : ["10"],
      "10" : ["9"],
      "11" : ["12"],
      "12" : ["11", "13"],
      "13" : ["12"]
     }
    
un_graphe = Graphe(g)

print("parcours", un_graphe.parcours_simple('1'))
print("parcours en largeur", un_graphe.parcours_en_largeur('1'))
print("parcours en profondeur", un_graphe.parcours_en_profondeur('1'))
for s in un_graphe.parcours_en_largeur('1'):
    assert un_graphe.sont_relies("1", s)
assert not un_graphe.sont_relies("1","11")
print(un_graphe.trouve_chemin("4","8"))
print(un_graphe.trouve_chemin("4", "9"))
print(un_graphe.composantes_connexes())



