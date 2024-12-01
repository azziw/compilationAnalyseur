from ensembles import *

def analyseur_LL1():

    expression = list(map(str, input('\nVeuillez entrer la chaine à analyser, séparez les symboles par un espace et entrez un $ pour finir votre chaine \n').split(" ")))

    print(f"\nVous avez saisi la chaîne : {expression} \n")

    if(expression[-1] != '$'):
        print('il manque un $ à la fin de votre chaine veuillez réessayer')
        return


    #On initialise la pile
    pile = ['$'] 
    index = 0

    pile.append(nonTerminaux[0]) #on empile Programme pour débuter 

    while pile and expression[index]:

        print(f"pile = {pile}")

        if expression == ["main()", "{", "}", "$"]:
            print("Chaine acceptée pour l'expression fournie")
            break

        # print(f"On dépile {pile[-1]} et change la valeur du sommet de pile")
        X = pile.pop() #Soit X le symbole de sommet de pile

        while X == 'vide': #Si le sommet de pile est la chaine vide on continue de dépiler
            X = pile.pop()

        a = expression[index] #Soit a appartenant à VT le symbole courant de la chaine à analyser

        if(X in nonTerminaux): #Est-ce que X appartient a VN ?
            regle = table.get(X, {}).get(a)
            # print(regle)

            if regle: #est-ce que l'entrée de l'utilisateur est bien présente dans la table d'analyse
                print(f"Regle: {X} ::= {regle}") #emettre en sortie la règle X
                y = regle.split(" ")
                
                for n in range(len(y)):  #on empile de yn-1 à y1
                    pile.append((y[-n - 1]))
                # print(f"PIle après Empilation de {y} = {pile}")
            else:
                print("Erreur de syntaxe pour l'expression fournie")
                return

        else: #Sinon X appartient à VT
            # print(f"{X} est un terminal")
            if(X == "$"):
                if(a == "$"):
                    print("Chaine acceptée pour l'expression fournie")
                    accepte = True
                    break
                else:
                    print("Erreur de syntaxe pour l'expression fournie pour X == $")
                    break
            else:
                if(X == a):
                    # print(f"X = A -> {X} = {a}")
                    index += 1
                else:
                    print("Erreur de syntaxe le symbole Terminal n'est pas égal à l'expression")
                    break

analyseur_LL1()