def calculObj(data, function1, function2) : 
    
    """
    Calcul des fonctions objectifs pour chaque observation

    data -> vecteurs d'entrée
    function1, function2 -> fonctions objectifs à minimiser

    return : même dataframe avec valeurs des fonctions objectifs pour chaque observation
    """
    
    x1 = data['x1']
    x2 = data['x2']

    f1 = list()
    f2 = list()

    for i, j in zip(x1, x2) : 
        f1.append(function1(i, j))
        f2.append(function2(i, j))

    data['f1'] = f1
    data['f2'] = f2
    
    return data