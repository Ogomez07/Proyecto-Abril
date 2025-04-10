from IPython.display import display
import pandas as pd

def explore_bank_data (df):
    """
    Carga el dataset de marketing bancario,
    """
    print(df.head())
    df = df.rename(columns={'y': 'fixed_term_deposit'})
    display(df.info())
    display(df.describe().round(2))
    display(df.isnull().sum())
    return df

def frequency_vars (df, columns):
    """ 
    Función que muestra cual es el valor que más y menos se repite de una variable
    """
    frequency = df[columns].value_counts()
    most_frequent_value = frequency.idxmax()
    least_frequent_value = frequency.idxmin()

    print(f'El valor más usual: {most_frequent_value}')
    print(f'El valor que menos se repite: {least_frequent_value}')

def info_cualitative_vars(df, columns):

    """ 
    Genera la media, moda y mediana de las variables cualitativas
    """
    mean =df[columns].mean()
    median = df[columns].median()
    mode = df[columns].mode()[0]

    print(f'Estadísticos para {columns}')
    print(f'Media: {mean}')
    print(f'Mediana: {median}')
    print(f'Moda: {mode}')

def ratio_vars(df, columns):
    """
    Devuelve los valores más y menos frecuentes de múltiples columnas categóricas.
    """
    result = {}
    for col in columns:
        ratios = (df[col].value_counts(normalize= True) * 100).round(2).sort_values(ascending= False)
        print(f'Las proporciones de la variable {col} son: ')
        display(ratios)
        most_frequent_ratio = ratios.idxmax()
        print(f'El ratio más alto es para: {most_frequent_ratio}')
        least_frequent_ratio = ratios.idxmin()
        print(f'El ratio más bajo es para {least_frequent_ratio}')
       
        result[col] = {
            'most_frequent': most_frequent_ratio,
            'least_frequent': least_frequent_ratio
        }

def acceptance_rate_multiple(df, columnas):

    """
    Calcula el porcentaje de aceptación del producto ('yes') 
    para cada categoría dentro de las columnas especificadas.

    Retorna un diccionario con un DataFrame por columna.
    """
    results = {}

    for col in columnas:
        result = {}
        for category in df[col].unique():
            subset = df[df[col] == category]
            valores = subset['fixed_term_deposit'].value_counts()
            porcentaje = (valores['yes'] / valores.sum()) * 100 if 'yes' in valores else 0
            result[category] = round(porcentaje, 2)

        result_df = pd.DataFrame.from_dict(result, orient='index', columns=['% aceptación'])
        result_df = result_df.sort_values(by='% aceptación', ascending=False).reset_index()
        result_df.rename(columns={'index': col}, inplace=True)

        results[col] = result_df

    return results
