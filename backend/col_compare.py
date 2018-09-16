import matplotlib.pyplot as plt, mpld3
import pandas as pd
import numpy as np

col_df = pd.read_csv('./csv/col_index.csv', delimiter='|')
average_budget = [35, 27, 14, 10, 8, 6]
average_budget_labels = ['Cost of Living', 'Housing', 'Transportation', 'Food', 'Entertainment', 'Miscellaneous']

def compare_city_names(city1, city2):
    city_names = [city1, city2]
    average_total_difference = calculate_average_total_difference(city_names)
    return average_total_difference

def compare_offer(offer1, offer2):
    locations = [offer1["location"], offer2["location"]]
    compensation = [offer1["compensation"], offer2["compensation"]]
    
    col_index = get_col_index(locations)
    col_index_differences = calculate_col_index_difference(locations)
    average_difference = calculate_average_difference(locations)
    average_total_difference = calculate_average_total_difference(locations)
    
    desc = []
    desc.append('Offer one in ' + locations[0] + ' is approximately equal to ' +  "{0:.2f}".format(int(offer1['compensation']) / average_total_difference * 100) + ' in ' + locations[1] +  ' after cost of living adjustments.\n')
    desc.append('Offer two in ' + locations[1] + ' is approximately equal to ' +  "{0:.2f}".format(int(offer1['compensation']) * average_total_difference / 100) + ' in ' + locations[0] +  ' after cost of living adjustments.\n')

    desc.append(locations[0] + ' has a cost of living index of ' + str(col_index[0][2]) + ', where as ' + locations[1] + ' has a cost of living index of ' + str(col_index[1][2]) + ', which means it is ' + "{0:.2f}".format(col_index_differences[0] if col_index_differences[0] >= 0 else -col_index_differences[0]) + '% ' + ('more expensive' if col_index_differences[0] >= 0 else 'less expensive') + ' to live in the area.\n' )
    desc.append(locations[0] + ' has rent index of ' + str(col_index[0][3]) + ', where as ' + locations[1] + ' has a rent index of ' + str(col_index[1][3]) + ', which means it is ' + "{0:.2f}".format(col_index_differences[1] if col_index_differences[1] >= 0 else -col_index_differences[1]) + '% ' + ('more expensive' if col_index_differences[1] >= 0 else 'less expensive') + ' to rent in the area.\n' )
    desc.append(locations[0] + ' has combined rent and cost of living of ' + str(col_index[0][4]) + ', where as ' + locations[1] + ' has a combined rent and cost of living index of ' + str(col_index[1][4]) + ', which means it is ' + "{0:.2f}".format(col_index_differences[2] if col_index_differences[2] >= 0 else -col_index_differences[2]) + '% ' + ('more expensive' if col_index_differences[2] >= 0 else 'less expensive') + ' to rent/live in the area.\n' )
    desc.append(locations[0] + ' has a grocery index of ' + str(col_index[0][5]) + ', where as ' + locations[1] + ' has a grocery index of ' + str(col_index[1][5]) + ', which means it is ' + "{0:.2f}".format(col_index_differences[3] if col_index_differences[3] >= 0 else -col_index_differences[3]) + '% ' + ('more expensive' if col_index_differences[3] >= 0 else 'less expensive') + ' to buy groceries in the area.\n' )
    desc.append(locations[0] + ' has a restaurant price index of ' + str(col_index[0][6]) + ', where as ' + locations[1] + ' has a restaurant index of ' + str(col_index[1][6]) + ', which means it is ' + "{0:.2f}".format(col_index_differences[4] if col_index_differences[4] >= 0 else -col_index_differences[4]) + '% ' + ('more expensive' if col_index_differences[4] >= 0 else 'less expensive') + ' to eat out in the area.' )
    desc.append(locations[0] + ' has a local purchasing power index of ' + str(col_index[0][7]) + ', where as ' + locations[1] + ' has a purchasing power index of ' + str(col_index[1][7]) + ', which means it is ' + "{0:.2f}".format(col_index_differences[5] if col_index_differences[5] >= 0 else -col_index_differences[5]) + '% ' + ('cheaper' if col_index_differences[5] >= 0 else 'more expensive') + ' to buy things in the area.' )
    return desc

def get_col_index(city_names):
    cities = [col_df.loc[col_df['city'] == city] for city in city_names]
    cities = [np.ndarray.flatten(city.values).tolist() for city in cities]
    print(cities)
    return cities

def calculate_col_index_difference(city_names):
    cities = get_col_index(city_names)
    col_index_differences = [(cities[0][2+i] - cities[1][2+i]) for i in range(6)]
    return col_index_differences

def calculate_col_index_comparison(city_names):
    col_index_differences = calculate_col_index_difference(city_names)
    col_comparison = [(element + 100)/100 for element in col_index_differences]
    return col_comparison
    
def calculate_average_difference(city_names):
    col_differences = calculate_col_index_comparison(city_names)
    differences = [average_budget[index] * col_differences[index] for index in range(6)]
    return differences

def calculate_average_total_difference(city_names):
    differences = calculate_average_difference(city_names)
    total_difference = np.sum(differences)
    return total_difference
