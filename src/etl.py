def drop_unknown(df, columns):
    """ 
    Elimina los valores unknown de las columnas elegidas
    """

    for col in columns:
        df= df[df[col] != 'unknown']
    return df
    
# df = drop_unknown(df, ['job', 'education'])

def map_education_level(df):
    """
    Crea una nueva columna 'education_level' que aclara el nivel de estudios
    a partir de la columna 'education'.
    """
    education_map = {
        'primary': 'Primary',
        'secondary': 'High School/VET',
        'tertiary': 'Grade/Higher VET',
        'unknown': 'unknown'
    }
    
    df['education_level'] = df['education'].map(education_map)
    return df

# df = map_education_level(df)

def group_ages(age):
    """ 
    Se encarga de agrupar rango de edades
    """
    if age <=30:
        return '18 - 30'
    elif age > 30 and age <= 45:
        return '31 - 45'
    elif age > 45 and age <= 65:
        return '46 - 65'
    else: 
        return '66+ '
    
# df['age_group'] = df['age'].apply(group_ages)

def yes_ftd(df):
    """ 
    Devuelve un nuevo DataFrame (df_fxt) con los registros de personas
    que aceptaron el depósito a plazo fijo (fixed_term_deposit == 'yes')
    """
    return df[df['fixed_term_deposit'] == 'yes']

def no_ftd(df):
    """ 
    Devuelve un nuevo DataFrame (df_fxt) con los registros de personas
    que no aceptaron el depósito a plazo fijo (fixed_term_deposit == 'no')
    """
    return df[df['fixed_term_deposit'] == 'no']

def remove_outliers(df, columns):
    """ 
    Función que se encarga de eliminar los valores atípicos de las columnas seleccionadas
    """

    for col in columns:
        q1= df[col].quantile(0.25)
        q3= df[col].quantile(0.75)
        iqr= q3 - q1

        lower = q1 - 1.5 * (iqr)
        upper = q3 + 1.5 * (iqr)
        df  = df[(df[col] >= lower) & (df[col] <= upper)]
    return df 