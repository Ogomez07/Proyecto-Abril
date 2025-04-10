import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from statsmodels.stats.proportion import proportions_ztest

import src.eda as eda
import src.etl as etl
import src.stats as statistic
import src.visualization as viz

if __name__ == "__main__":
    df = pd.read_csv('data/raw/bank-full.csv', sep= ';')
    df = df.rename(columns={'y': 'fixed_term_deposit'})
    eda.explore_bank_data (df)

    viz.plot_categorical_distributions(df)

    # proporción de unknowns en el dataset
    total = len(df)
    unknowns = (df['job'] == 'unknown').sum()
    percentage = round((unknowns / total) * 100, 2)
    print(f"'unknown' representa el {percentage}% de los datos.")

    df = etl.drop_unknown(df, ['job', 'education'])
    df = etl.map_education_level(df)
    df['age_group'] = df['age'].apply(etl.group_ages)

    # viz.plot_numerical_distributions(df)
    # viz.plot_individual_boxplots(df)
    # viz.plot_boxplot_with_y(df)

    statistic.corr_vars(df)

    df_yes_ftd =etl.yes_ftd(df)
    statistic.corr_matrix_yes_clients(df_yes_ftd)

    df_no_ftd =etl.no_ftd(df)
    statistic.corr_matrix_no_clients(df_no_ftd)

    # viz.plot_columns(df_yes_ftd)

    # viz.plot_age_group(df_yes_ftd, 'age_group') 
    # viz.plot_age_group(df_no_ftd, 'age_group')

    eda.info_cualitative_vars(df_yes_ftd, 'age')
    eda.info_cualitative_vars(df_no_ftd, 'age')

    eda.frequency_vars(df_yes_ftd, ['job', 'marital', 'education_level', 'month', 'loan', 'default'])
    eda.frequency_vars(df_no_ftd, ['job', 'marital', 'education', 'month', 'loan', 'default'])

    columns = ['job', 'marital', 'education_level', 'month', 'loan', 'default']
    eda.ratio_vars(df_yes_ftd, columns)

    columnas = columns
    eda.acceptance_rate_multiple(df, columnas)
    results = eda.acceptance_rate_multiple(df, columnas)
    # viz.plot_aceptation(results)

    # viz.plot_job_education_gorup(df_yes_ftd)
    # viz.plot_job_education_gorup(df_no_ftd)

    # viz.plot_average_balance_by_job(df_yes_ftd)
    # viz.plot_average_balance_by_job(df)
    # viz.plot_average_balance_by_job(df_no_ftd)

   #  viz.scatter_balance_by_job(df_yes_ftd)
    # viz.scatter_balance_by_job(df_no_ftd)

    statistic.normality_test(df, ['age', 'balance'])
    viz.plot_density(df, ['age', 'balance'])

    df_sin_outliers = etl.remove_outliers(df, ['age', 'balance'])
    statistic.normality_test(df_sin_outliers, ['age', 'balance'])
    viz.plot_density(df_sin_outliers, ['age', 'balance'])

    statistic.chi2_test_dependence(df, 'job', 'fixed_term_deposit')
    statistic.chi2_test_dependence(df, 'marital', 'fixed_term_deposit')
    statistic.chi2_test_dependence(df, 'education', 'fixed_term_deposit')
    statistic.chi2_test_dependence(df, 'default', 'fixed_term_deposit')
    statistic.chi2_test_dependence(df, 'housing', 'fixed_term_deposit')
    statistic.chi2_test_dependence(df, 'contact', 'fixed_term_deposit')

    statistic.t_test_mean_high(df, 'age')

    statistic.t_test_vars(df, 'duration')

    statistic.t_test_compare_vars(df, 'job', 'retired', 'unemployed')
    statistic.t_test_compare_vars(df, 'job', 'management', 'technician')
    statistic.t_test_compare_vars(df, 'job', 'student', 'unemployed')
    statistic.t_test_compare_vars(df, 'job', 'blue-collar', 'services')
    statistic.t_test_compare_vars(df, 'job', 'retired', 'student')
    statistic.t_test_compare_vars(df, 'job', 'student', 'retired')
    statistic.t_test_compare_vars(df, 'marital', 'single', 'married')
    statistic.t_test_compare_vars(df, 'housing', 'no', 'yes')
    statistic.t_test_compare_vars(df, 'loan', 'yes', 'no')

    statistic.test_compare_groups(df,
                        'marital', 'married',
                        'education_level', 'High School/VET',
                        'marital', 'single',
                        'education_level', 'Grade/Higher VET')

    statistic.test_compare_groups(df, 
                        'marital', 'married', 
                        'education_level', 'High School/VET',
                        'marital', 'divorced',
                        'education_level', 'Primary'
                        )

    statistic.test_compare_groups(df, 
                        'marital', 'divorced', 
                        'education_level', 'Primary',
                        'marital', 'married',
                        'education_level', 'High School/VET'
                        )

    statistic.test_compare_groups(df, 
                        'marital', 'married', 
                        'education_level', 'Grade/Higher VET',
                        'marital', 'divorced',
                        'education_level', 'Grade/Higher VET'
                        )

    statistic.test_compare_groups(df, 
                        'marital', 'married', 
                        'education_level', 'Grade/Higher VET',
                        'marital', 'divorced',
                        'education_level', 'Primary'
                        )

    statistic.test_compare_groups(df, 
                        'marital', 'married', 
                        'education_level', 'Grade/Higher VET',
                        'marital', 'single',
                        'education_level', 'Primary'
                        )

    statistic.test_compare_groups(df, 
                        'marital', 'married', 
                        'education_level', 'Grade/Higher VET',
                        'marital', 'married',
                        'education_level', 'Primary'
                        )
    statistic.test_compare_groups(df, 
                        'marital', 'single', 
                        'education_level', 'Grade/Higher VET',
                        'marital', 'single',
                        'education_level', 'Primary'
                        )
    
df.to_csv('data/processed/Bank_FTD.csv', index= False)