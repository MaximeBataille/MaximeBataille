def isDominated(w, t, arr_sort) :
    
    """
    Savoir si une observation domine l'autre

    w,t -> observations, avec valeurs des fonctions objectifs
    arr_sort -> rang de chaque observation pour chaque fonction objectif
    
    return : True si w est dominé par t, False sinon
    """
    
    arr_sort = arr_sort[:, 1:] #on ne compare pas la première colonne car w dominé par t pour cette fonction obj
    res = True #initialisation
    
    for v in range(arr_sort.shape[1]) :
        if np.where(arr_sort[:, v] == w) < np.where(arr_sort[:, v] == t) : #si rang de w meilleur que rang de t
                            #pour la variable v, alors w  n'est pas dominé
            res = False
            break #w n'est pas dominé par t
            
    return res

def nonDominated(pop) :
    
    """
    Donne le rang du front de chaque observation de la population


    pop --> population

    return : Même dataframe, population avec le rang pour chaque observation
    
    """
    
    n, var = pop.shape #n = nb observations, var = nb variables
    sort_arg = np.zeros((n, var)) #initialisation array tri
    
    
    for v in range(var) :
        sort_arg[:, v] = np.argsort(pop[:, v]) #tri des valeurs de chaque fonction objectif
    
    non_dominated_rank = np.inf * np.ones(n) #recevra le rang de chaque observation
    rank = 1 #initialisation rank
    working = list(sort_arg[:,0]) #les observations à ranker, dans ordre croissant de rank de la première fonction

    to_rank = working
    while len(working) > 0 : #tant que observations à ranker
        #print('classement des observations', sort_arg)
        #print('observation à ranker : ', working)
        non_dominated = list() #observations non dominées
        non_dominated.append(working[0]) #la 1° observation classée est forcément non dominée
        
        to_test = list()
        to_test.append(working[0]) #observations déjà traitées
        
        working = working[1:] #mis à jour, la première observation n'est plus à ranker
        
        
        for w in to_rank : #pour chaque observation à ranker
            
            if w in working : #si w est encore dans la liste en cours des observations à ranker
            
                cpt = 0
                for t in to_test : #comparaison aux observations déjà traitées

                    if isDominated(w, t, sort_arg) == False :
                        cpt += 1

                if cpt == len(to_test) :  #si w dominé par aucun t
                    non_dominated.append(w) #w non dominé
                    working.remove(w) #maj : w n'est plus à ranker

                to_test.append(w) #même si pas ranké, w est traité  

        #maj des rank
        for n_d in non_dominated :
            non_dominated_rank[int(n_d)] = rank
            
        rank += 1
                
    return non_dominated_rank