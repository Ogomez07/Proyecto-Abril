import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from statsmodels.stats.proportion import proportions_ztest

def corr_vars(df): 
    df_corr = df.copy()
    df_corr['fixed_term_deposit'] = df_corr['fixed_term_deposit'].map({'no': 0, 'yes': 1})
    num_cols = ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous', 'fixed_term_deposit']

    corr_matrix = df_corr[num_cols].corr()
    # Visualizamos con un heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', square=True, fmt=".2f", linewidths=0.5)

    plt.title('Matriz de correlación entre variables numéricas y la variable objetivo (fixed_term_deposit)')
    plt.tight_layout()
    plt.show()

def corr_matrix_yes_clients(df_yes):
    """
    Calcula y muestra la matriz de correlación de las variables numéricas
    para los clientes que aceptaron el depósito a plazo fijo.
    """

    num_df = df_yes.select_dtypes(include='number')
    corr = num_df.corr()

    # Visualizamos con un heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", square=True, linewidths=0.5)
    plt.title("Matriz de correlación (clientes que aceptaron el depósito)")
    plt.tight_layout()
    plt.show()

def corr_matrix_no_clients(df_no):
    """
    Calcula y muestra la matriz de correlación de las variables numéricas
    para los clientes que NO aceptaron el depósito a plazo fijo.

    Parámetros:
    -----------
    df_no : pd.DataFrame
        DataFrame filtrado con clientes que dijeron 'no' en 'fixed_term_deposit'.
    """
    # Seleccionamos solo columnas numéricas
    num_df = df_no.select_dtypes(include='number')

    # Calculamos la matriz de correlación
    corr = num_df.corr()

    # Visualizamos la matriz como heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", square=True, linewidths=0.5)
    plt.title("Matriz de correlación (clientes que NO aceptaron el depósito)")
    plt.tight_layout()
    plt.show()

def normality_test(df, columns):
    """
    Aplica el test de normalidad (D’Agostino y Pearson) a  las columnas seleccionadas.
    Muestra el estadístico, p-valor y conclusión para cada una.
    """
    for col in columns:
        if df[col].dtype not in ['int64', 'float64']:
            print(f'{col} no es una variable númerica, no es válidad para el test de normalidad, se omite')
            continue
        
        stat, p = stats.normaltest(df[col])
        print(f'--Normalidad de la variable {col}--')
        print(f'Estadístico: {stat.round(2)}, p-valor: {p.round(4)}')

        if p > 0.05:
            print(f'✅ No se rechaza la hipótesis nula -> se comporta como una distribución normal')
        else: 
            print(f'❌ Se rechaza la hipótesis nula --> no se comporta como una normal')

def chi2_test_dependence(df, col1, col2):
    """ 
        Aplica el test de Chi-cuadrado para evaluar la independencia entre dos variables categóricas
    """
    table = pd.crosstab(df[col1], df[col2])
    chi2, p, dof, expected = stats.chi2_contingency(table)
    print(f'--Test Chi-cuadrado entre {col1} y {col2}--')
    print(f'Estadísico X^2: {chi2.round(2)}')
    print(f'Grados de libertad: {dof}')
    print(f'valor p: {p.round(6)}')

    if p < 0.05:
        print(f'Se rechaza la hipótesis nula: hay evidencia de que las variables no son independientes \n ✅ Por ello, la variable {col1} sí influye en la aceptación del producto')
    else:
        print(f'Se acepta la hipótesis nula: hay evidencia suficiente para decir que están relacionadas \n ❌ Por ello, la variable {col1} no influye en la aceptación del producto')

def t_test_mean_high(df, variable):
    """ 
     Compara si la media de 'variable' es mayor en quienes aceptaron el producto ('yes')
    frente a quienes no ('no'), usando un test t unilateral
    """
    yes = df[df['fixed_term_deposit'] == 'yes'][variable]
    no = df[df['fixed_term_deposit'] == 'no'][variable]

    t, p_dos_colas = stats.ttest_ind(yes, no, equal_var= False)
    p =p_dos_colas / 2 if t > 0 else 1 - (p_dos_colas / 2)  
    print(f'¿La media de {variable} es mayor de quienes aceptaron?')
    print(f'Estadístico t: {t.round(2)} | p-valor: {p.round(4)}')

    if p < 0.05:
        print(f'✅ Se rechaza la Hipótesis nula, a un nivel de significación del 5% podemos indicar que la media de {variable} es mayor en el grupo que aceptó')
    else:
        print('❌ No se puede rechazar la Hipótesis nula, la edad media es igual o similar a quienes no aceptaron')

def t_test_vars(df, variable):

    """ 
    A través del estadístico de t test compara si la variable influye o no en la aceptación del producto
    """

    yes = df[df['fixed_term_deposit'] == 'yes'][variable]
    no = df[df['fixed_term_deposit'] == 'no'][variable]

    stat_var, p = stats.ttest_ind(yes, no, equal_var=False)

    print(f'Test t para ver si la variable {variable} influye la aceptación del producto financierp')
    print(f'Estadístico t: {stat_var.round(3)}')
    print(f'Valor p: {p.round(4)}')

    if p < 0.05:
        print('✅ Se rechaza H₀: La duración de la llamada es significativamente diferente entre quienes aceptaron y quienes no.')
    else:
        print('❌ No se puede rechazar H₀: No hay evidencia de diferencia en duración entre los grupos.')

def t_test_compare_vars(df, column, group_1, group_2):

    """ 
    Compara si la proporción de aceptación del producto financiero (target) es mayor 
    en la categoría A que en la categoría B de una variable categórica (group_col) 
    mediante un test de proporciones Z.
    """

    g1 = df[df[column] == group_1]
    g2 = df[df[column] == group_2]

    yes_g1 = len(g1[g1['fixed_term_deposit'] == 'yes'])
    yes_g2 = len(g2[g2['fixed_term_deposit'] == 'yes'])

    total_g1 = len(g1)
    total_g2 = len(g2)

    z, p = proportions_ztest(count=[yes_g1, yes_g2], nobs=[total_g1, total_g2], alternative='larger')

    print(f"---¿{group_1} acepta más que {group_2} para la variable {column}?---")
    print(f"z: {z.round(2)} | p-valor: {p.round(4)}") 

    if p < 0.05:
        print(f"✅ Se rechaza H₀: los {group_1} tienen mayor probabilidad de aceptar el producto que {group_2}.")
    else:
        print(f"❌ No se rechaza H₀: no hay evidencia suficiente que indique que  acepten más los {group_1} que los {group_2}")

def test_compare_groups(df, col1, val1, col2, val2, col3, val3, col4, val4):
    """
    Compara si la tasa de aceptación del producto ('yes' en 'fixed_term_deposit')
    es mayor en un grupo A (col1=val1 y col2=val2) que en un grupo B (col3=val3 y col4=val4),
    usando un test de proporciones Z.

    Parámetros:
    -----------
    df : DataFrame
    col1, val1 : primera condición del grupo A
    col2, val2 : segunda condición del grupo A
    col3, val3 : primera condición del grupo B
    col4, val4 : segunda condición del grupo B
    """

    group_a = df[(df[col1] == val1) & (df[col2] == val2)]
    group_b = df[(df[col3] == val3) & (df[col4] == val4)]

    a_yes = (group_a['fixed_term_deposit'] == 'yes').sum()
    b_yes = (group_b['fixed_term_deposit'] == 'yes').sum()

    a_total = len(group_a)
    b_total =len(group_b)

    z, p = proportions_ztest([a_yes, b_yes], [a_total, b_total], alternative= 'larger')
    print(f"---Comparando:\n * A: {col1} = {val1}, {col2} = {val2}\n * B: {col3} = {val3}, {col4} = {val4}---")
    print(f"Z = {z.round(2)} | p = {p.round(4)}")

    if p < 0.05: 
        print(f'✅ Se rechaza la H0: El grupo {val1}, {val2} tiene una mayor probabilidad de aceptar que el grupo {val3}, {val4}')
    else:
        print(f'❌ Se acepta la H0: la aceptación del producto para el grupo {val1}, {val2} es igual o menor que para el grupo {val3}, {val4}')
