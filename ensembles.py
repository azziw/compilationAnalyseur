# -------- CONSTRUCTION DES REGLES (GRAMMAIRE DU LANGAGE) -------- #
regles = {
    'Programme': [["main()", "{", "liste_declarations", "liste_instructions", "}"]],
    "liste_declarations": [["une_declaration", "liste_declarations"], ["vide"]],
    "une_declaration": [["type", "id"]],
    "liste_instructions": [["une_instruction", "liste_instructions"], ["vide"]],
    "une_instruction": [["affectation"], ["test"]],
    "type" : [["int"], ["float"]],
    "affectation": [["id", "=", "nombre", ";"]],
    "test": [["if", "condition", "une_instruction", "else", "une_instruction", ";"]],
    "condition": [["id", "operateur", "nombre"]],
    "operateur": [["<"], [">"], ["="]]
}

# -------- CONSTRUCTION DES SYMBOLES NON TERMINAUX -------- #
nonTerminaux = [key for key in regles.keys()] #on met dans nonTerminaux toutes les clés de regles car ce sont les non terminaux

# -------- CONSTRUCTION DES SYMBOLES TERMINAUX -------- #
terminaux = list({e for value in regles.values() for item in value for e in item if e not in nonTerminaux})

# EN COMMENTAIRE POUR MONTRER LE RAISONNEMENT QUI DONNE AU CODE CI-DESSUS
# terminaux = []
# for value in regles.values():
#     for item in value:
#         for e in item:
#             if e not in nonTerminaux and e not in terminaux: 
#                 terminaux.append(e)


# -------- ENSEMBLE PREMIER -------- #
def getPremier(element, inclureVide = True):
    premiers = set()  # Utilisation d'un set pour éviter les doublons
    #Pour chaque    
    for val in regles[element]:
        alpha = val[0]
        if alpha in terminaux:
            if inclureVide == True:
                premiers.add(alpha)
        elif alpha in nonTerminaux:
            premiers.update(getPremier(alpha)) 
    return premiers

    # -------- ENSEMBLE SUIVANT -------- #
def getSuivant(element):
    suivant = set()
    if(element == "Programme"):
        return "$"
    else:
        # pour chaque clé, valeur
        for key, value in regles.items():
            # pour chaque production d'une règle
            for val in value:
                # pour chaque element d'une production
                for i in range(len(val)):
                    #Si l'élement que je regarde est celui que je cherche
                    if val[i] == element:
                        #j'ajoute la valeur de suivant si c'est un terminal sinon j'ajoute la valeur du premier du non terminal trouvé, si le suivant n'existe pas on se refère au suivant de l'origine de production
                        #je vérifie qu'il existe un élément suivant.
                        if i < len(val) - 1:
                            #si mon suivant est un terminal
                            if val[i + 1] in terminaux:
                                #je l'ajoute à la liste
                                suivant.add(val[i + 1]) 
                            else:
                                #Si mon suivant n'est pas un terminal, j'ajoute l'ensemble premier du suivant
                                suivant.update(getPremier(val[i + 1], False)) 
                                #Si l'ensemble premier du suivant contient le mot vide
                                if 'vide' in getPremier(val[i + 1], True):
                                    #Je dois ajouter l'ensemble suivant de son origine de production
                                    #Si il contient le mot vide, je dois regarder le suivant de cette nouvelle production
                                    if(val[i+1]): 
                                        suivant.update(getSuivant(val[i+1]))                               
                        else:
                            # Si on est à la fin de la liste, on gère le symbole suivant avec l'origine de production
                            if key!=element: 
                                suivant.update(getSuivant(key))
    return suivant


# -------- CONSTRUCTION DES ENSEMBLES PREMIERS -------- #
premier = {key: getPremier(key) for key in regles} #On défini premier comme un dictionnaire avec le couple (clé, premiers)

# -------- CONSTRUCTION DES ENSEMBLES SUIVANTS -------- #
suivant = {key: getSuivant(key) for key in regles} #On défini premier comme un dictionnaire avec le couple (clé, Suivants)

# -------- CONSTRUCTION DE LA TABLE D'ANALYSE -------- #
table = {}
for non_terminal in nonTerminaux:
    table[non_terminal] = {}
    for regle in regles[non_terminal]:
        premiers = getPremier(non_terminal)
        premier_symbole = regle[0]
        
        if premier_symbole in terminaux:
            # Si le premier symbole est un terminal, on ajoute cette règle pour ce terminal
            table[non_terminal][premier_symbole] = " ".join(regle)
        elif premier_symbole in nonTerminaux:
            # Si le premier symbole est un non-terminal, on utilise son ensemble Premier
            premiers = getPremier(premier_symbole)
            for terminal in premiers:
                table[non_terminal][terminal] = " ".join(regle)
        if "vide" in premiers:
            # Si la production contient "vide", on ajoute cette règle pour les terminaux de l'ensemble Suivant
            for terminal in suivant[non_terminal]:
                table[non_terminal][terminal] = "vide"


# Affichage des règles
def printRegles():
    print("\nListe des règles:")
    for key, value in regles.items():
        print(f"{key} ::= ",end="")
        for sousliste in value:
            for symbole in sousliste:
                print(f"{symbole}", end=" ")
            if len(value) > 1:
                print(" | ", end="")
        print()

# Affichage des symboles terminaux
def printTerminaux():
    print("\nListe des terminaux:")
    print(terminaux)

# Affichage des symboles non terminaux
def printNonTerminaux():
    print("\nListe des non Terminaux: ")
    print(nonTerminaux)

# Affichage des ensembles premiers
def printPremiers():
    print("\nListe des ensembles Premiers :")
    for non_Terminal, terminal in premier.items():
        print(f"{non_Terminal} = {terminal}")

# Affichage des ensembles suivants
def printSuivants():
    print("\nListe des ensembles Suivants :")
    for non_Terminal, terminal in suivant.items():
        print(f"{non_Terminal} = {terminal}")

# Affichage de la table d'analyse
def printTableAnalyse():
    print("\nTable d'analyse LL(1) :")
    for non_terminal, rules in table.items():
        for terminal, regle in rules.items():
            print(f"({non_terminal}, {terminal}) : {non_terminal} -> {regle}")


printRegles()
printTerminaux()
printNonTerminaux()
printPremiers()
printSuivants()
printTableAnalyse()