##### Importaciones #####
# importar bibliotecas externas
import matplotlib.pyplot as plt # para graficar
import numpy as np # para operaciones matemáticas
from scipy.stats import linregress # para regresión lineal
import scipy.stats # para pruebas estadísticas

###### FUNCIONES ######
#eliminate forviden characters
#navega por cada caracter de la cadena y si no es un caracter permitido lo elimina
def eliminate_forbidden_characters(string):
    #some strings end with '\r' character, this is a forbidden character
    if string[-2:] == '\r':
        string = string[:-2]
    #allowed characters
    allowed = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',' ','.']
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
        #clean columns names
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

#describe database
def describe_base(data):
    print('Descripción de la base de datos'+'\n')
    for key in data.keys():
        print(f'{key}: data type: {type(data[key][0])}')

#graph relationship
def graph_relationship(data, var_x, var_y, regression=False):
    plt.figure()
    plt.title(f'Relación entre {var_x} y {var_y}')
    plt.scatter(data[var_x], data[var_y], label='Data Points')
    
    if regression:
        # Calculate the linear regression
        slope, intercept, r_value, p_value, std_err = linregress(data[var_x], data[var_y])
        # Generate regression line based on slope and intercept
        x_vals = np.array(data[var_x])
        reg_line = slope * x_vals + intercept
        # Plotting the regression line
        plt.plot(data[var_x], reg_line, color='red', label=f'Linear Regression\ny={slope:.2f}x+{intercept:.2f}')
        # Display the equation and the r-squared value
        plt.legend(title=f'R-squared: {r_value**2:.2f}')
    
    plt.xlabel(var_x)
    plt.ylabel(var_y)
    plt.show()

#graph histogram
def graph_histogram(data,column):
    plt.figure()
    plt.title(f'Histograma de {column}')
    plt.hist(data[column],bins=200)
    plt.xlabel(column)
    plt.ylabel('Frecuencia')
    plt.show()

#graph boxplot
def graph_boxplot(data,column):
    plt.figure()
    plt.title(f'Boxplot de {column}')
    plt.boxplot(data[column])
    plt.ylabel(column)
    plt.show()

#graph distribution
def graph_distribution(data,column):
    plt.figure()
    plt.title(f'Distribución de {column}')
    plt.hist(data[column],bins=200,density=True)
    plt.xlabel(column)
    plt.ylabel('Densidad')
    plt.show()

def prueba_jarque_bera(datos, clave):
    # Extrae los datos asociados a la clave
    valores = datos[clave]
    # Realiza la prueba de Jarque-Bera
    estadistico, p_valor = scipy.stats.jarque_bera(valores)
    # Comprueba si la distribución se puede considerar normal (p > 0.05)
    if p_valor > 0.05:
        return True, p_valor  # Los datos siguen una distribución normal
    else:
        return False, p_valor  # Los datos no siguen una distribución normal

#statistical summary
def summary(data,column,histogram=False,boxplot=False,distribution=False,normality=False):
    obs = len(data[column])
    mean = np.mean(data[column])
    sd = np.std(data[column])
    print(f'Resumen estadístico: {column}'+'\n')
    print(f'Número de observaciones: {obs}'+'\n'+
          f'La media de {column} es: {mean}'+'\n'+
          f'La desviación estándar de {column} es: {sd}')
    if histogram:
        graph_histogram(data,column)
    if boxplot:
        graph_boxplot(data,column)
    if distribution:
        graph_distribution(data,column)
    if normality:
        print(f'Prueba de Jarque-Bera para {column}'+'\n')
        normal, p_value = prueba_jarque_bera(data,column)
        print(f'Normalidad: {normal}')
        print(f'P-valor: {p_value}')


###### MAIN ######
if __name__ == '__main__':

    #route and data
    ## ruta de la base de datos
    route = 'data/ENIGHDB.csv'
    ## leer la base de datos, limpiarla y guardarla en un diccionario
    data = read_base(route)

    #action 0: describe database
    describe_base(data)    

    #action 1: graph relationship
    #graph_relationship(data,'personales','gastomon')
    graph_relationship(data,'gastomon','personales',regression=True)

    #action 2: summary
    #histogram, boxplot and distribution functions are optional
    #summary(data,'personales')
    #summary(data,'gastomon',histogram=True)
    #summary(data,'personales',histogram=True,boxplot=True)
    #summary(data,'gastomon',histogram=True,boxplot=True,distribution=True)
    summary(data,'gastomon',histogram=True,distribution=True,normality=True)
    
    
    