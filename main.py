#packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.spatial import distance
import random
from random import sample

#fonctions
import calculObjectif 
import domination
import filterFront
import crossoverMutation

#########PARAMETRES A MODIFIER#############
#fonctionne uniquement pour deux variables et deux fonctions objectifs

#Définir les fonctions objectifs
def function1(x, y) :
    
    return x**2 -y 

 def function2(x, y) :
    
    return -np.exp(y) 

#Taille de la population
size = 200

#Définir les bornes (contraintes) de chaque variable
min_x1 = 0 #borne min de x1
max_x1 = 100 #borne max de x1
min_x2 = 0 #borne min de x2
max_x2 = 100 #borne max de x2

#Définir les paramètres de NSGA-G
nb_iter = 10 #Critère d'arrêt
alpha = 0.1 #chance qu'une mutation ait lieu
beta1 = 0.2 #si mutation, pourcentage de modificaiton du gene 1 (variable 1)
beta2 = 0.2 #si mutation, pourcentage de modificaiton du gene 2 (variable 2)

####NSGA-G#######
sampling_1 = (max_x1 - min_x1) * np.random.sample((size, 1)) + max_x1
sampling_2 = (max_21 - min_x2) * np.random.sample((size, 1)) + max_x2

sampling = np.concatenate((sampling1, sampling2), axis = 1)

def nsgag(pop, nb_iter, alpha, beta1, beta2) : 

	"""
	pop -> population aléatoire


	return : population tendant vers le front de Pareto
	"""

	cpt = 0
	while cpt < nb_iter :
	    
	    #tournois : création population
	    df_children = crossoverMutation.tournament(pop, alpha = alpha, beta1 = beta1, beta2 = beta2)
	    #Calcul des fonctions objectifs pour chaque observation
	    df_children = calculObjectif.calculObj(df_children, function1, function2)

	    #Nouvelle population complète : Pt + Et
	    pop = pd.concat([pop, df_children], axis = 0)
	    
	    #trie par Front de Non dominance
	    rank = domination.nonDominated(np.array(pop[['f1', 'f2']]))
	    #actualisation des nouveaux fronts
	    pop['rank'] = rank
	    
	    #Sélections des observations selon le rang (rank)
	    new_pop, rank = filterFront.selectObservations(pop, size)

	    #Filtrage du front n° rank pour compléter population
	    n_obs_select = size - new_pop.shape[0] #nombre d'observations à sélectionner(encore)
	    if n_obs_select == pop[pop['rank'] == rank].shape[0] :
	        add_pop = pop[pop['rank'] == rank]
	    elif n_obs_select < pop[pop['rank'] == rank].shape[0] :
	        n_obs_delete = pop[pop['rank'] == rank].shape[0] - n_obs_select #nb d'observations à supprimer

	        #print(pop[pop['rank'] == rank])
	        add_pop = filterFront.filterFront(pop[pop['rank'] == rank], n_obs_delete)

	        
	    #Concaténation des 2 populations pour avoir les meilleurs observations
	    pop = pd.concat([new_pop, add_pop])
	    
	    #compteur nombre itération (critère d'arrêt)
	    cpt+=1

	return pop


print("Population formant le front de Pareto")
print(nsgag(sampling, nb_iter, alpha, beta1, beta2))
