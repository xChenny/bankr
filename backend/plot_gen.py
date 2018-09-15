import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt, mpld3
import csv

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

AVAILABLE_CITIES = ['NEW YORK', 'SAN FRANCISCO', 'SEATTLE', 'HOUSTON', 'WASHINGTON DC']

def generate_city_plots():
    ny = generate_city_average_salaries('New York')
    json_string = mpld3.fig_to_dict(ny)
    return json_string

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

    if offer_compensations and offer_details:
        x_coords = [offer_compensation for offer_compensation in offer_compensations]
        #for index, x_coord in enumerate(x_coords):
        #    element_color = 255 * index / len(x_coords)
        #    plt.axvline(x=x_coord, color=rgb(element_color, element_color, element_color), linewidth=3, linestyle="dashed")
        lines = [plt.axvline(x=x_coord, color=rgb(255 * index / len(x_coords), 255 * index / len(x_coords), 255 * index / len(x_coords)), linewidth=3, linestyle="dashed") for index, x_coord in enumerate(x_coords)]
        plt.legend([lines], offer_details)

    figure = figure.get_figure()
    figure.savefig(svg_name, format='svg')
    return fig

def generate_individualized_plots():
    line = plt.axvline(x=126000, color='black', linewidth=3, linestyle="dashed")
    plt.legend([line], ["Your Google Offer"])
