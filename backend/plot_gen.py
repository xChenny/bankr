import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt, mpld3
import csv
import base64

from io import BytesIO

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

AVAILABLE_CITIES = ['NEW YORK', 'SAN FRANCISCO', 'SEATTLE', 'HOUSTON', 'WASHINGTON']

def generate_city_average_salaries(city_name, offer_compensations=None, offer_details=None):
    if city_name.upper() not in AVAILABLE_CITIES:
        raise ValueError('The city name provided is not in the set of available cities.')

    snakecase_city_name = "_".join(city_name.split(',')[0].split()).lower()
    csv_location = './csv/{0}_salaries.csv'.format(snakecase_city_name)
    svg_name = './svg/{0}_avg_salary.svg'.format(snakecase_city_name)
    df = pd.read_csv(csv_location, delimiter='|')

    fig, ax = plt.subplots(figsize=(10,5)) 
    dd = pd.melt(df,id_vars=['position'],value_vars=['salaries'])
    figure = sns.boxplot(y='position', x='value', data=dd.loc[dd.position.isin(dd.position.value_counts().nlargest(5).keys())], orient="h")
    plt.title("Boxchart of Compensation vs. Role for Most Frequent Roles in {0} (Glassdoor)".format(city_name))

    
    colors = ['black', 'blue', 'brown', 'violet', 'grey']
    if offer_compensations and offer_details:
        x_coords = [offer_compensation for offer_compensation in offer_compensations]
        lines = [plt.axvline(x=x_coord, color=colors[index], linewidth=3, linestyle="dashed") for index, x_coord in enumerate(x_coords)]
        plt.legend(lines, offer_details)

    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)

    figdata_png = figfile.getvalue()
    figdata_png = base64.b64encode(figdata_png)
    return figdata_png

def generate_companies_with_most_listings(city_name, offer_compensations=None, offer_details=None):
    if city_name.upper() not in AVAILABLE_CITIES:
        raise ValueError('The city name provided is not in the set of available cities.')

    snakecase_city_name = "_".join(city_name.split(',')[0].split()).lower()
    csv_location = './csv/{0}_salaries.csv'.format(snakecase_city_name)
    svg_name = './svg/{0}_avg_salary.svg'.format(snakecase_city_name)
    df = pd.read_csv(csv_location, delimiter='|')

    fig, ax = plt.subplots(figsize=(10,5))
    dd=pd.melt(df,id_vars=['company'],value_vars=['salaries'])
    figure = sns.boxplot(y='company',x='value',data=dd.loc[dd.company.isin(dd.company.value_counts().nlargest(5).keys())], orient="h")
    figure = figure.get_figure()
    plt.title("Boxchart of Compensation vs. Company for Top Hiring Companies in {0} (Glassdoor)".format(city_name))

    colors = ['black', 'blue', 'brown', 'violet', 'grey']
    if offer_compensations and offer_details:
        x_coords = [offer_compensation for offer_compensation in offer_compensations]
        lines = [plt.axvline(x=x_coord, color=colors[index], linewidth=3, linestyle="dashed") for index, x_coord in enumerate(x_coords)]
        plt.legend(lines, offer_details)

    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)

    figdata_png = figfile.getvalue()
    figdata_png = base64.b64encode(figdata_png)
    return figdata_png
