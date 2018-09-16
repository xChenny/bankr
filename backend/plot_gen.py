import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt, mpld3
import csv

from io import BytesIO

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

AVAILABLE_CITIES = ['NEW YORK', 'SAN FRANCISCO', 'SEATTLE', 'HOUSTON', 'WASHINGTON DC']

def generate_city_plots(city_name, offer_compensations=None, offer_details=None):
    figfile = generate_city_average_salaries(city_name, offer_compensations, offer_details)
    figdata_svg = figfile.getvalue()
    return figdata_svg

def generate_city_average_salaries(city_name, offer_compensations=None, offer_details=None):
    if city_name.upper() not in AVAILABLE_CITIES:
        raise ValueError('The city name provided is not in the set of available cities.')

    snakecase_city_name = "_".join(city_name.split(',')[0].split()).lower()
    csv_location = './csv/{0}_salaries.csv'.format(snakecase_city_name)
    svg_name = './svg/{0}_avg_salary.svg'.format(snakecase_city_name)
    df = pd.read_csv(csv_location, delimiter='|')

    fig, ax = plt.subplots(figsize=(8,4)) 
    dd = pd.melt(df,id_vars=['position'],value_vars=['salaries'])
    figure = sns.boxplot(y='position', x='value', data=dd.loc[dd.position.isin(dd.position.value_counts().nlargest(5).keys())], orient="h")
    plt.title("Boxchart of Compensation vs. Role for Most Frequent Roles in {0} (Glassdoor)".format(city_name))

    
    colors = ['black', 'blue', 'brown', 'violet', 'grey']
    if offer_compensations and offer_details:
        x_coords = [offer_compensation for offer_compensation in offer_compensations]
        lines = [plt.axvline(x=x_coord, color=colors[index], linewidth=3, linestyle="dashed") for index, x_coord in enumerate(x_coords)]
        plt.legend(lines, offer_details)

    figfile = BytesIO()
    plt.savefig(figfile, format='svg')
    return figfile

def generate_individualized_plots():
    line = plt.axvline(x=126000, color='black', linewidth=3, linestyle="dashed")
    plt.legend([line], ["Your Google Offer"])
