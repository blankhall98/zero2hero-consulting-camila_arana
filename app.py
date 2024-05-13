##### Importaciones #####
# importar bibliotecas externas
import matplotlib.pyplot as plt
import numpy as np

###### FUNCIONES ######
#eliminate forviden characters
def eliminate_forbidden_characters(string):
    #some strings end with '\r' character, this is a forbidden character
    if string[-2:] == '\r':
        string = string[:-2]
    #allowed characters
    allowed = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',' ']
    corrected_string = ''
    for char in string:
        if char in allowed:
            corrected_string += char
    return corrected_string

#read database
def read_base(route):
    ## leer la base de datos con pandas --> dataframe
    with open(route, 'r', newline='',encoding='ISO-8859-1') as file:
        db = file.read()
        db = db.split('\n')
        #processed database
        data = {}
        #extract columns
        columns = db[0].split(',')
        #clean columns
        for i in range(len(columns)):
            columns[i] = eliminate_forbidden_characters(columns[i])
        for c in columns:
            data[c] = []
        #extract rows
        for row in db[1:]:
            row = row.split(',')
            for i in range(len(row)):
                if type(row[i]) == str:
                    row[i] = eliminate_forbidden_characters(row[i])
                    try:
                        row[i] = float(row[i])
                    except:
                        pass
                data[columns[i]].append(row[i])

    return data

#graph relationship
def graph_relationship(data,var_x,var_y):
    plt.figure()
    plt.title(f'Relación entre {var_x} y {var_y}')
    plt.scatter(data[var_x],data[var_y])
    plt.xlabel(var_x)
    plt.ylabel(var_y)
    plt.show()

def summary(data,column,state=False):
    if state:
        data = data[data['Estado']==state]
    mean = np.mean(data[column])
    sd = np.std(data[column])
    print(f'La media de {column} es: {mean}'+'\n'+
          f'La desviación estándar de {column} es: {sd}')


###### MAIN ######
if __name__ == '__main__':

    #route and data
    ## ruta de la base de datos
    route = 'data/ENIGHDB.csv'
    data = read_base(route)

    print(data.keys())

    #action 1: graph relationship
    #graph_relationship(data,'Gastotri','personales')

    #action 2: summary
    summary(data,'limpieza',state='Yucatn')
    
    
    