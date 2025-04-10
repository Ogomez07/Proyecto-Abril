import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

def plot_categorical_distributions(df):
    """
    Genera una visualización de la distribución de las variables categóricas
    en un DataFrame utilizando countplots de Seaborn.
    """
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns

    if len(categorical_cols) == 0:
        print("No se encontraron columnas categóricas en el DataFrame.")
        return

    plt.figure(figsize=(16, len(categorical_cols) * 4))

    for i, col in enumerate(categorical_cols, 1):
        plt.subplot(len(categorical_cols), 1, i)
        sns.countplot(
            data=df,
            x=col,
            hue=col,               
            palette='pastel',
            order=df[col].value_counts().index,
            legend=False           
        )
        plt.title(f'Distribución de valores en "{col}"')
        plt.xlabel('')
        plt.ylabel('Frecuencia')
        plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

def plot_numerical_distributions(df):
    """
    Genera una visualización de la distribución de las variables numéricas
    en un DataFrame utilizando histogramas de Seaborn.
    """
    numerical_cols = df.select_dtypes(include=['number']).columns

    if len(numerical_cols) == 0:
        print("No se encontraron columnas numéricas en el DataFrame.")
        return

    plt.figure(figsize=(16, len(numerical_cols) * 4))

    for i, col in enumerate(numerical_cols, 1):
        plt.subplot(len(numerical_cols), 1, i)
        sns.histplot(data=df, x=col, kde=True, color='skyblue')
        plt.title(f'Distribución de la variable numérica "{col}"')
        plt.xlabel('')
        plt.ylabel('Frecuencia')

    plt.tight_layout()
    plt.show()

def plot_individual_boxplots(df):
    """
    Genera boxplots individuales:
    - Uno por cada variable numérica (distribución simple).
    - Uno por cada variable categórica cruzada con 'age' (distribución por grupo).
    """
    numerical_vars = ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous']
    categorical_vars = ['job', 'marital', 'education', 'default', 'housing', 'loan',
                        'contact', 'poutcome', 'y']

    # 1. Boxplots de variables numéricas
    if len(numerical_vars) == 0:
        print("No se encontraron columnas numéricas en el DataFrame.")
    else:
        for col in numerical_vars:
            plt.figure(figsize=(8, 4))
            sns.boxplot(x=df[col], color='lightblue')
            plt.title(f'Boxplot de {col}')
            plt.xlabel(col)
            plt.tight_layout()
            plt.show()

    # 2. Boxplots cruzando categóricas con 'edad'
    if len(categorical_vars) == 0:
        print('No se encontraron columnas categóricas en el DataFrame')

    else:
        for cat in categorical_vars:
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=df, x=cat, y='age', hue=cat, palette='Set2')
            plt.title(f'Distribución de la edad según {cat}')
            plt.xlabel(cat)
            plt.ylabel('Edad')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

def plot_boxplot_with_y(df):
    """
    Genera boxplots individuales:
    - Uno por cada variable categórica cruzada con 'age' y la variable 'y'
    """
    categorical_vars = ['job', 'marital', 'education', 'default', 'housing', 'loan']
    
    if len(categorical_vars) == 0:
        print('No se encontraron columnas categóricas en el DataFrame')

    else:
        for cat in categorical_vars:
            plt.figure(figsize=(12, 6))
            sns.boxplot(data=df, x='y', y='age', hue=cat, palette='Set3')
            plt.title(f'Distribución de edad según y y segmentado por {cat}')
            plt.xlabel('y')
            plt.ylabel('Edad')
            plt.legend(title=cat, bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.show()

def plot_columns(df):
    """
    Crea gráficos de barras para cada columna puesta en la lista .
    """

    columnas_a_graficar = ['age', 'job', 'marital', 'education', 'default',
                           'housing', 'loan', 'contact', 'day']
    for col in columnas_a_graficar:
        conteo = df[col].value_counts()
        plt.figure(figsize=(8, 4))
        conteo.plot(kind='bar')
        plt.title(f'Distribución de {col}')
        plt.xlabel(col)
        plt.ylabel('Frecuencia')
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()

def plot_age_group(df, col):
    """
    Crea un gráfico de barras para una columna del DataFrame.
    """
    conteo = df[col].value_counts().sort_index()  
    plt.figure(figsize=(8, 4))
    conteo.plot(kind='bar')
    plt.title(f'Distribución de {col}')
    plt.xlabel(col)
    plt.ylabel('Frecuencia')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def plot_aceptation(results):
    """
    Recibe un diccionario de DataFrames y genera gráficos de barras
    para cada columna con el porcentaje de aceptación.
    """
    for columns, df_result in results.items():
        print(f"\n Porcentaje de aceptación por: {columns.upper()}")
        print(df_result)

        plt.figure(figsize=(10, 5))
        sns.barplot(data=df_result, x=columns, y='% aceptación', edgecolor='black', palette='Blues')
        plt.title(f'Porcentaje de aceptación por {columns}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def plot_job_education_gorup(df):
    
    """ 
    Genera un gráfico de barras que muestra la distribución de grupos de edad
    por tipo de trabajo y nivel educativo.
    """

    situation_group = df.groupby(['job', 'education_level'])['age_group'].value_counts().sort_values(ascending= False)
    situation_group = situation_group.reset_index(name= 'count')
    
    
    plt.figure(figsize=(16, 6))
    sns.barplot(
        data=situation_group,
        x='age_group',
        y='count',
        hue='job',
        dodge=True,
        errorbar=None,
        edgecolor='black',   
        width=0.8             
    )
    plt.title('Distribución de grupos de edad por tipo de trabajo')
    plt.xlabel('Grupo de edad')
    plt.ylabel('Cantidad')
    plt.legend(loc='upper right', bbox_to_anchor=(1.25, 1))
    plt.tight_layout()
    plt.show()

def plot_average_balance_by_job(df):
    """
    Genera un gráfico de barras con el balance promedio por tipo de trabajo.
    """
    plot_job_balance = df.groupby('job')['balance'].mean().sort_values(ascending=False)
    print(f'🔺El grupo con mayor renta media es: {plot_job_balance.idxmax()}')
    print(f'🔻El grupo con menor renta media es: {plot_job_balance.idxmin()}')    
    print(plot_job_balance.head())

    plt.figure(figsize=(10, 6))
    plot_job_balance.plot(kind='bar', color='skyblue', edgecolor='black')

    plt.title('Balance promedio por tipo de trabajo')
    plt.ylabel('Balance promedio (€)')
    plt.xlabel('Tipo de trabajo')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def scatter_balance_by_job(df):
    """
    Crea un gráfico de dispersión entre edad y balance, coloreando por tipo de trabajo (u otra variable).
    """

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='job', y='balance', hue='job') 
    plt.title('Relación entre trabajo y balance por tipo de trabajo')  
    plt.xlabel('Job')
    plt.ylabel('Balance (€)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_density(df, columns):
    """ 
    Gráfico que refleja la curva de densidad de las variables seleccionadas 
    """
    for column in columns:
        data = df[column]
        mean = data.mean()
        std = data.std()
        x_vals = np.linspace(data.min(), data.max(), 100)
        normal_curve = stats.norm.pdf(x_vals, loc=mean, scale=std)

        plt.figure(figsize=(10, 6))
        sns.kdeplot(data, label='Distribución real (KDE)', color='steelblue', linewidth=2)
        plt.plot(x_vals, normal_curve, label='Distribución normal teórica', color='red', linestyle='--')
        plt.title(f'Distribución de {column} vs Normal teórica')
        plt.xlabel(column.capitalize())
        plt.ylabel('Densidad')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()