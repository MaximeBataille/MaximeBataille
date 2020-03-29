def selectObservations(pop, size) :
    
    """
    pop -> population
    size -> taille de la population à conserver
    
    retourne les observations sélectionnées et le front à analyser
    pour sélectionner les observations restantes
    """

    n_group = list(pop.groupby('rank').size())

    n = 0
    i = 0
    while n < size :
        memory_n = n
        memory_i = i
        
        n += n_group[i]
        i += 1
   
    selected_pop = pop[pop['rank'] <= memory_i]
        
    return selected_pop, memory_i+1


def euclideanDist(a, b) :
    
    """
    a, b -> tuples
    
    Calcul la distance euclidienne entre a et b
    """
    
    dist = np.sqrt( (a[0] -b[0])**2  +  (a[1] -b[1])**2)
    
    return dist

def rankInGroup(pop, grid, n_group) :
    
    """
    pop -> sous population de même groupe
    grid -> grille
    n_group -> numéro du groupe sélectionné
    """
    
    grid_min_f1 = grid[::-1][1:]
    grid_min_f2 = grid[:-1]
    
    dist = list()
    index = pop.index
    
    c_grid_min = (grid_min_f2[n_group-1], grid_min_f1[n_group-1])
    
    for f1, f2 in zip(pop["f1"], pop["f2"]) :
        c_obs = (f2, f1)
        
        dist.append( euclideanDist(c_obs, c_grid_min) )
    
    #observation ayant la distance la plus lointaine à grid_min
    iloc = np.argsort(dist)[-1]
    #index à supprimer
    del_loc = index[iloc]
    #suppression de cette observation
    pop = pop.drop([del_loc], axis = 0)
    
    return pop

def createGroups(pop, grid) : 
    
    '''
    pop -> fonction objectif pour chaque population
    grid -> balises de la grille
    '''
    print("grille", grid)
    groups = list()
    
    for f1, f2 in zip(pop[:, 0], pop[:, 1]) : 
        if (f1 == 1 and f2==0) or(f1 == 0 and f2 == 1) :
            groups.append(-1)
            
        else : 
            i = 0
            while f1 < grid[::-1][i] or f2 > grid[i] :
                i+=1
            if i > len(grid) :
                i-=1
            groups.append(i)
    
    return groups

def minMaxScaler(array, mini, maxi) : 
    
    return np.divide( (array - mini), maxi - mini)
    

def filterFront(pop, n_obs) :
    
    '''
    pop -> population
    n_obs -> observation to delete
    '''
    
    n_f = 2 #nombre de fonctions objectifs
    
    n_grids = n_obs ** (1/(n_f - 1))
    step = 1 / n_grids
    grid = list(np.arange(0,1.1,step))
    
    loc_qep1 = list(np.argsort(pop['f1']))[-1] #valeur la plus élevée
    loc_qep2 = list(np.argsort(pop['f2']))[-1] #valeur la plus élevée
    
    #qep2 = (pop[loc_qep1, 0], pop[loc_qep1, 1])
    #qep1 = (pop[loc_qep2, 0], pop[loc_qep2, 1])
    
    qep2 = (pop['f1'].iloc[loc_qep2], pop['f2'].iloc[loc_qep2])
    qep1 = (pop['f1'].iloc[loc_qep1], pop['f2'].iloc[loc_qep1])

    f1_max = qep1[0]
    f1_min = qep2[0]
    
    f2_max = qep2[1]
    f2_min = qep1[1]

    standard_pop = np.zeros((pop.shape[0], 2))
    #normalisation axe f1
    standard_pop[:, 0] = minMaxScaler(np.array(pop['f1']), f1_min, f1_max)
    #normalisation axe f2
    standard_pop[:, 1] = minMaxScaler(np.array(pop['f2']), f2_min, f2_max)

    #attribution d'un groupe à chaque observation
    groups = createGroups(standard_pop, grid)
    
    #valeurs des grid min sur f1 et f2
    grid_min_f1 = grid[::-1][1:]
    grid_min_f2 = grid[:-1]
    
    #Construction DataFrame
    df_pop = pd.DataFrame()
    df_pop["f1"] = standard_pop[:,0]
    df_pop["f2"] = standard_pop[:,1]
    df_pop["groups"] = groups
    df_pop['x1'] = list(pop['x1'])
    df_pop['x2'] = list(pop['x2'])
    
    while n_obs >= 1 : #tant que des observations à supprimer
        
        if df_pop.shape[0] == 1 : #cas où il reste uniquement qep1 ou qep2
            df_pop = df_pop.drop(list(df_pop.index))
            
        elif df_pop.shape[0] == 2 : #cas où il reste qep1 et qep2
            selected_qep = random.randint(0,1) #sélection de qep1 ou qep2
            df_pop = df_pop.drop(list(df_pop.index[selected_qep]))
            
        else : 
            #sélection d'un groupe au hasard
            selected_g = random.randint(1, n_grids)

            while selected_g not in list(df_pop['groups']) :  #cas où plus d'observation dans le groupe
                selected_g = random.randint(1, n_grids)

            df_group = df_pop[df_pop['groups'] == selected_g]
            #print('balba', grid)
            filtered_group = rankInGroup(df_group, grid, selected_g)

            #suppression puis maj du dataframe
            df_pop = df_pop.drop(list(df_group.index))
            df_pop = pd.concat([df_pop, filtered_group], axis = 0)
        
        #maj du compteur
        n_obs -=1
        
    #recalcul des fonctions objectifs pour 'casser' la normalisation
    df_pop = calculObj(df_pop, function1, function2)
    
    return df_pop