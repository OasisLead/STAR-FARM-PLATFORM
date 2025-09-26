## Structure backend de l'ITK pour l'application

## Description LLM + structure (liste de string en général, ou liste de liste de string, ou dictionnaire 
## de listes de strings) ++ instruction (qui peut être la même chose que la description en soi)



#1

name_of_practice1=""
name_of_practice2=""


instru1 =""

crop1 = "Rice"
crop2 = "Rice"

description_llm_1 = "You are an agriculture expert, someone tells you they want to study"+name_of_practice1+" and "+name_of_practice2+" in the Mekong Delta, can you give multiple examples of crop rotations that are possible in these two practices ? Especially, for a given rotation, describe "


#2

### Triplet - Dates + contraintes sur les dates de ne pas s'overlap et d'être dans l'ordre

instru2 =""
date_début_cycle = ""
date_fin_cycle = ""

description_llm_2 = ""

"""Liste d'actions dynamique (type d'action + nom d'action)
à chaque fois qu'on ajoute une action on instantie une liste de couples de dates
dans la liste de couple de dates on fait en sorte qu'on ne puisse ajouter que du bon format (définir le format pour l'utilisateur)
et que dans une action les dates ne puissent pas s'overlap mais entre action si, et que les dates
soient dans l'ordre chronologique"""

"""Il y a un format de date"""


#3


date_semis_crop1 =""
date_semis_crop2=""

action1 =""
liste_date_action1=""

#Pour l'instant je simplifie et je met uniquement 1 seule période pour l'action, mais pour certain types
#d'action je peux répéter l'action plusieurs fois

#Semis - sowing
#Récolte - harvesting

#Binage
#Fauche
#Travail du sol

#Fertilisation
#Irrigation
#Traitement phytosanitaire




### ODD et code

# à chaque fois que je crée un ITK je dois: instancier un type d'agent (fermier_ITK_1), de préférence
# une classe abstraite pour la réutiliser pour d'autres gens mais cela peut être une classe concrète,
# et je dois également définir les actions possibles pour cet agent, ainsi que les périodes de temps associées,
#qui sont des conditions sur le temps dans l'année
# la question à ce moment là c'est est-ce que j'utilise le LLM pour générer cela et faire la jonction
# ou est-ce que je fais la jonction manuellement

#Je dois me familiariser avec le code ABM python et la structure ODD, ainsi que la structure GAMA au 
# fond



### Question de génération LLM

# 1) Générer en plusieurs layers ? -> Les actions, puis les premières dates, puis les périodes, puis les critères d'observation, etc...
# 1.1) Générer les actions 1 par 1 et ensuite s'assurer de la cohérence ? Faire une petite tache à la fois comme le fait Nicolas ?
# 2) Donc redonner en input du LLM à chaque fois la partie qui a déjà été générée avec une partie aditionnelle de contexte ?




