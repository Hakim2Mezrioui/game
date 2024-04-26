"""
    Auteur: MEZRIOUI Hakim
    date : décembre 2021
    preojet en bref :
    Ce projet est un petit jeu (escape game)
    dans lequel le joueur commande au clavier
    les déplacements d’un personnage au sein
    d’un « château » représenté en plan
"""
from CONFIGS import *
import turtle as t
wn = t.Screen()
chateau = t.Turtle()
chateau.speed(0)
chateau.color("WHITE")
ecrit = t.Turtle()
ecrit.hideturtle()
ecrit.up()
t.up()
t.hideturtle()
t.goto(POINT_AFFICHAGE_INVENTAIRE)
pai = [70, 210 , 0]
augmenter = 0
t.write('Inventaire :')


personnage = t.Turtle()
personnage.hideturtle()
personnage.shape('circle')
personnage.color('black','red')
personnage.shapesize(0.5)
personnage.up()

def lire_matrice(fichier):
    """
    recevra en argument le nom d’un fichier texte
    contenant le plan à tracer.
    Elle ouvrira ce fichier et renverra en sortie une matrice,
    c’est-à-dire une liste de listes
    """
    file = open(fichier)
    lines = file.readlines()
    lst1 = []
    lst2 = []
    for line in lines:
        for num in line:
            if ' ' not in num and '\n' not in num :
                lst1.append(num)
        lst2.append(lst1)
        lst1 = []
    return (lst2)

def calculer_pas(matrice):
    """
    calcule la dimension à donner aux cases
    pour que le plan tienne dans la zone
    de la fenêtre turtle
    """
    pas1 = 440/len(matrice)
    pas2 = 290/len(matrice[0])
    pas = 0
    if pas1 < pas2 :
        pas = pas1
    else :
        pas = pas2
    return pas

def cordonnes(case , pas):
    """
    Cette fonction calcule les coordonnées en pixels turtle
    du coin inférieur gauche d’une case définie
    par ses coordonnées
    """
    y = ZONE_PLAN_MINI[0]
    x = ZONE_PLAN_MINI[1]
    y += (27 - case[0]) * pas
    x += (case[1]) * pas 
    return x,y

def tracer_carre(dimension,pas,couleur):
    """
    cette fonction trace un carré dont la dimension
    en pixels turtle est donnée en argument
    """
    chateau.up()
    chateau.goto(dimension)
    chateau.down()
    chateau.fillcolor(couleur)
    chateau.begin_fill()
    for i in range(4):
        chateau.forward(pas)
        chateau.left(90)
    chateau.end_fill()

def tracer_case(case, couleur, pas):
    """
    cette fonction recevois en arguments un couple de coordonnées
    en indice dans la matrice contenant le plan, une couleur,
    et un pas (taille d'un côté) et qui va appeler la fonction
    tracer_carre pour tracer un carré d’une certaine couleur et taille
    à un certain endroit.
    """
    dimension = cordonnes(case, pas)
    if couleur == 'white':
        pass
    else:
        tracer_carre(dimension,pas,couleur)

def afficher_plan(matrice):
    """
    cette fonction va appeler la fonction tracer_case
    pour chaque ligne et chaque colonne du plan,
    par deux boucles imbriquées.
    """
    pas = calculer_pas(matrice)
    couleur = ''
    for i in range(len(matrice)):
        for j in range(len(matrice[0])):
            val = matrice[i][j]
            couleur = COULEURS[int(val)]
            tracer_case((i,j), couleur , pas)
    chateau.hideturtle()
    global position
    position = [0,1]
    pst = cordonnes(position,pas)
    personnage.goto(pst[0]+(pas/2),pst[1]+(pas/2))
    personnage.showturtle()
global matrice            
matrice = lire_matrice(fichier_plan)
afficher_plan(matrice)

def deplacer_gauche():
    "cette fonction oriente le personnage vers gauche"
    t.onkeypress(None,"Left")
    deplacer(matrice,position,"Left")
    pas = calculer_pas(matrice)
    pst = cordonnes(position,pas)
    personnage.goto(pst[0]+(pas/2),pst[1]+(pas/2))
    t.onkeypress(deplacer_gauche,"Left")

def deplacer_droite():
    "cette fonction oriente le personnage vers droite"
    t.onkeypress(None,"Right")
    deplacer(matrice,position,"Right")
    pas = calculer_pas(matrice)
    pst = cordonnes(position,pas)
    personnage.goto(pst[0]+(pas/2),pst[1]+(pas/2))
    t.onkeypress(deplacer_droite,"Right")

def deplacer_haut():
    "cette fonction oriente le personnage vers haut"
    t.onkeypress(None,"Up")
    deplacer(matrice,position,"Up")
    pas = calculer_pas(matrice)
    pst = cordonnes(position,pas)
    personnage.goto(pst[0]+(pas/2),pst[1]+(pas/2))
    t.onkeypress(deplacer_haut,"Up")

def deplacer_bas():
    "cette fonction oriente le personnage vers bas"
    t.onkeypress(None,"Down")
    deplacer(matrice,position,"Down")
    pas = calculer_pas(matrice)
    pst = cordonnes(position,pas)
    personnage.goto(pst[0]+(pas/2),pst[1]+(pas/2))
    t.onkeypress(deplacer_bas,"Down")

def creer_dictionnaire_des_objets(fichier_des_objets):
    """
    cette fonction va creer un dictionnair ,
    elle recevra en argument le nom du fichier_des_objets,
    et renverra un dictionnaire comportant 
    """
    file = open(fichier_des_objets, encoding='UTF-8')
    dct = {}
    val = ''
    for line in file:
        ln = line.strip('\n')
        cdn = ln[ln.find('(')+1:ln.find(')')]
        cdn = cdn.split(',')
        key = (int(cdn[0]),int(cdn[1]))
        simple , double = ln.find("'") , ln.find('"')
        if simple < double and simple != -1:
            val = ln[ln.find("'")+1:-1]
        elif simple == -1 :
            val = ln[ln.find('"')+1:-1]
        elif simple > double and double != -1:
            val = ln[ln.find('"')+1:-1]
        elif double == -1:
            val = ln[ln.find("'")+1:-1]
        dct[key] = val
    return dct
global les_objets
global les_questions
les_objets = creer_dictionnaire_des_objets(fichier_objets)
les_questions = creer_dictionnaire_des_objets(fichier_questions)

def ramasser_objet():
    """
    cette fonction ramasse les objets
    et elle affiche une annonce
    dans le bandeau d’affichage des annonces.
    """
    try:
        pai[1] -= 20
        pai[2] += 1
        t.goto(pai[0],pai[1])
        text = "N°"+str(pai[2])+":"+les_objets[(position[0],position[1])]
        t.write(text)
        ecrit.goto(POINT_AFFICHAGE_ANNONCES)
        ecrit.clear()
        ecrit.write('Vous avez trouvé : '+ les_objets[(position[0],position[1])], font=("Arial", 10, "bold"))
        matrice[position[0]][position[1]] = 0
    except:
        pass 


def deplacer(matrice, position, mouvement):
    """
    cette fonction est une fonction principla de getion 
    des déplacement et qui reçoit en arguments position (un couple définissant la position où se trouve le personnage)
    et mouvment (un couple définissant le mouvement demandé par le joueur)
    """
    pas = calculer_pas(matrice)
    x = position[0]
    y = position[1]
    if mouvement == "Left" :
        y -= 1  
        if int(matrice[x][y]) == 1 or y < 0 :
            pass
        elif int(matrice[x][y]) == 3 :
            poser_question(matrice,(x,y),"Left")
        else :
            position[1] -= 1
            tracer_case(position,COULEURS[5],pas)
            personnage.showturtle()
            
    elif mouvement == "Right" :
        y += 1
        if int(matrice[x][y]) == 1 or y > 17 :
            pass
        elif int(matrice[x][y]) ==  3 :
            poser_question(matrice,(x,y),"Right")
        else :
            position[1] += 1
            tracer_case(position,COULEURS[5],pas)
            personnage.showturtle()
            
    elif mouvement == "Up" :
        x -= 1
        if int(matrice[x][y]) == 1 or x < 0:
            pass
        elif int(matrice[x][y]) ==  3 :
            poser_question(matrice,(x,y),"Up")
        else :
            position[0] -= 1
            tracer_case(position,COULEURS[5],pas)
            personnage.showturtle()
            
    elif mouvement == "Down" :
        x += 1
        if x > 26:
            pass
        elif int(matrice[x][y]) == 1  :
            pass
        elif int(matrice[x][y]) ==  3 :
            poser_question(matrice,(x,y),"Down")
        else :
            position[0] += 1
            tracer_case(position,COULEURS[5],pas)
            personnage.showturtle()
    if int(matrice[position[0]][position[1]]) == 4:
        ramasser_objet()
        
    if int(matrice[position[0]][position[1]]) == 2 :
        pst = cordonnes(position,pas)
        personnage.goto(pst[0]+(pas/2),pst[1]+(pas/2))
        ecrit.goto(POINT_AFFICHAGE_ANNONCES)
        ecrit.clear()
        ecrit.write("Bravo ! Vous avez gagné.", font=("Arial", 16, "bold"))

t.listen()
t.onkeypress(deplacer_gauche,"Left")
t.onkeypress(deplacer_droite,"Right")
t.onkeypress(deplacer_haut,"Up")
t.onkeypress(deplacer_bas,"Down")

def poser_question(matrice, case, mouvement):
    "cette fonction affiche dans le bandeau d’affichage des annonces correspondant à l’emplacement de la porte"
    pas = calculer_pas(matrice)
    val ,reponse = les_questions[case] , ''
    ecrit.goto(POINT_AFFICHAGE_ANNONCES)
    ecrit.clear()
    ecrit.write("Cette porte est fermée.", font=("Arial", 10, "bold"))
    question = t.textinput('Question',val[:val.rindex('?')+1])
    reponse = val[val.rindex('?')+1:]
    reponse = reponse[reponse.index("'",2)+1:reponse.rindex("'")]
    if mouvement == "Left" :
        if question == reponse:
            position[1] -= 1
            tracer_case(position,COULEURS[5],pas)
            personnage.showturtle()
            ecrit.clear()
            ecrit.write("La porte s'ouvre !", font=("Arial", 10, "bold"))
            matrice[case[0]][case[1]] = 0
        else:
            ecrit.clear()
            ecrit.write("Movaise réponse", font=("Arial", 10, "bold"))
    elif mouvement == "Right" :
        if question == reponse:
            position[1] += 1
            tracer_case(position,COULEURS[5],pas)
            personnage.showturtle()
            ecrit.clear()
            ecrit.write("La porte s'ouvre !", font=("Arial", 10, "bold"))
            matrice[case[0]][case[1]] = 0
        else:
            ecrit.clear()
            ecrit.write("Movaise réponse", font=("Arial", 10, "bold"))
    elif mouvement == "Up" :
        if question == reponse:
            position[0] -= 1
            tracer_case(position,COULEURS[5],pas)
            personnage.showturtle()
            ecrit.clear()
            ecrit.write("La porte s'ouvre !", font=("Arial", 10, "bold"))
            matrice[case[0]][case[1]] = 0
        else:
            ecrit.clear()
            ecrit.write("Movaise réponse", font=("Arial", 10, "bold"))
    elif mouvement == "Down" :
        if question == reponse:
            position[0] += 1
            tracer_case(position,COULEURS[5],pas)
            personnage.showturtle()
            ecrit.clear()
            ecrit.write("La porte s'ouvre !", font=("Arial", 10, "bold"))
            matrice[case[0]][case[1]] = 0
        else:
            ecrit.clear()
            ecrit.write("Movaise réponse", font=("Arial", 10, "bold"))
    t.listen()
    t.onkeypress(deplacer_gauche,"Left")
    t.onkeypress(deplacer_droite,"Right")
    t.onkeypress(deplacer_haut,"Up")
    t.onkeypress(deplacer_bas,"Down")
