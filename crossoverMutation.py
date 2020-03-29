def mutation(x_child, alpha, beta1, beta2) :
    
    """
    Mutation des genes1 et genes2

    x1_child, x2_child <- genes 1 et 2
    alpha <- pourcentage de chance d'une mutation (entre 0 et 1)
    beta1, beta2 <- pourcentage de modificaiton du gene 1, gene 2

    return : genes mutés
    """
    
    alpha *= 100
    rand = random.randint(1,100)
    
    gene1, gene2 = x_child
    
    if rand <= alpha : #vecteur va être muté
        n_gene = random.randint(1,2) #mutation du premier ou du second gene
        
        if n_gene == 1 : #mutation gene1
            gene1 = gene1 + (beta1 * gene1)*random.sample([1,-1], 1)[0]
            
        elif n_gene == 2 : #mutation gene2
            gene2 = gene2 + (beta2 * gene2)*random.sample([1,-1], 1)[0]
    
    x_child = gene1, gene2
            
    return x_child

def crossOver(parent1, parent2) : 
    
    """
    Création de deux enfants à partir de deux parents

    parent1, parent2 <- tuple des genes(variables) des parents

    return : deux nouveaux enfants
    """
    
    n_var = random.randint(0,1) # interversion pour la première ou seconde variable
    
    if n_var == 0 : #interversion première variable
        child1 = (parent2[0], parent1[1])
        child2 = (parent1[0], parent2[1])
        
    elif n_var == 1 : #interversion seconde variable
        child1 = (parent1[0], parent2[1])
        child2 = (parent2[0], parent1[1])
        
    return child1, child2

def selectParents(pop) :
    
    
    """
    Sélection de deux parents aléatoirement, on garde le meilleur qui créera l'enfant avec un autre parent
    Sélection basée sur le rang (observation ayant le meilleur front sélectionné)

    pop <- population + rang pour chaque observation

    return : parent sélectionné
    """
    
    n_obs =  pop.shape[0]
    df_sample = pop.sample(n=2, replace = False) 
    
    
    rank_0 = df_sample['rank'].iloc[0]
    rank_1 = df_sample['rank'].iloc[1]
    
    if rank_1 < rank_0 :
        f1 = df_sample['x1'].iloc[1]
        f2 = df_sample['x2'].iloc[1]
    else : 
        f1 = df_sample['x1'].iloc[0]
        f2 = df_sample['x2'].iloc[0]
        
    return f1, f2

def tournament(pop, alpha, beta1, beta2) :

    """
    Création de la population enfant de taille n à partir de n parents

    pop -> population de parents
    alpha <- pourcentage de chance d'une mutation (entre 0 et 1)
    beta1, beta1 <- pourcentage de modificaiton du gene 1, gene 2

    return : population enfant créée
    """
    
    n = pop.shape[0]
    x1_children = list()
    x2_children = list()
    
    cpt = 0
    while cpt < n :  #génération de n enfants
    
        parent1 = selectParents(pop)
        parent2 = selectParents(pop)
        
        child1, child2 = crossOver(parent1, parent2)
        x1_children.append(child1)
        x2_children.append(child2)
        
        cpt+=2 #car deux enfants créés à chaque itération

        children = x1_children + x2_children #tous les nouveaux enfants
        
    for i in range(n) :
        children[i] = mutation(children[i], alpha, beta1, beta2)
    
    x1 = list()
    x2 = list()
    for i in range(len(children)) : 
        x1.append(children[i][0])
        x2.append(children[i][1])
        
    
    child_pop = pd.DataFrame()
    child_pop['x1'] = x1
    child_pop['x2'] = x2
    child_pop['rank'] = -1 #pas encore de rank
        
    return child_pop

