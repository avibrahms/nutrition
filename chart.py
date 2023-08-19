import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from utils import calculate_recommended_values_v2


def chart(info, data):

    # Calculate recommended daily intake for each nutrient
    recommended_protein, recommended_fat, recommended_carbs, recommended_calories = calculate_recommended_values_v2(info)

    # Convert 'Days' column to datetime
    data['Days'] = pd.to_datetime(data['Days'])

    # Define major tick location based on data range
    days = (data['Days'].max() - data['Days'].min()).days

    if days <= 7:
        tick_locator = mdates.DayLocator()
    elif days <= 60:
        tick_locator = mdates.WeekdayLocator()
    elif days <= 365:
        tick_locator = mdates.MonthLocator()
    else:
        tick_locator = mdates.YearLocator()

    # Define the format for the major tick label
    tick_formatter = mdates.ConciseDateFormatter(tick_locator)

    # Plot the bar charts
    fig, ax = plt.subplots(2, 2, figsize=(16, 9), dpi=300, constrained_layout=False)
    fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)



    # Customize colors
    colors = ['skyblue', 'salmon', 'limegreen', 'gold']

    # Customize fonts
    font = {'family' : 'DejaVu Sans',
            'weight' : 'bold',
            'size'   : 16}

    plt.rc('font', **font)

    # Set figure and axes background color
    fig.patch.set_facecolor('black')
    for row in ax:
        for a in row:
            a.set_facecolor('black')
            a.grid(color='white', linestyle='--', linewidth=0.5)

    # Set title and label colors
    for row in ax:
        for a in row:
            a.title.set_color('white')
            a.xaxis.label.set_color('white')
            a.yaxis.label.set_color('white')

    # Set tick colors
    for row in ax:
        for a in row:
            a.tick_params(axis='x', colors='white')
            a.tick_params(axis='y', colors='white')
            a.xaxis.set_major_locator(tick_locator)
            a.xaxis.set_major_formatter(tick_formatter)

    # Proteins
    ax[0, 0].bar(data['Days'], data['Proteins'], color=colors[0])
    ax[0, 0].axhline(y=recommended_protein, color=colors[0], linestyle='--')
    ax[0, 0].set_ylabel('Proteins (g)', color=colors[0])
    ax[0, 0].set_title('Protein', color=colors[0], weight='bold')
    ax[0, 0].tick_params(axis='x', colors=colors[0])
    ax[0, 0].tick_params(axis='y', colors=colors[0])
    ax[0, 0].text(1.01, recommended_protein, f'{round(recommended_protein)}', va='center', ha="left", bbox=dict(facecolor='black', edgecolor=colors[0], boxstyle='round,pad=0.2'), transform=ax[0, 0].get_yaxis_transform(), color=colors[0], weight='bold')
    ax[0, 0].text(data['Days'].iloc[-1], data['Proteins'].iloc[-1], f'{round(data["Proteins"].iloc[-1])}', color=colors[0], weight='bold', ha='center', va='bottom')

    # Fats
    ax[0, 1].bar(data['Days'], data['Fats'], color=colors[1])
    ax[0, 1].axhline(y=recommended_fat, color=colors[1], linestyle='--')
    ax[0, 1].set_ylabel('Fats (g)', color=colors[1])
    ax[0, 1].set_title('Fat', color=colors[1], weight='bold')
    ax[0, 1].tick_params(axis='x', colors=colors[1])
    ax[0, 1].tick_params(axis='y', colors=colors[1])
    ax[0, 1].text(1.01, recommended_fat, f'{round(recommended_fat)}', va='center', ha="left", bbox=dict(facecolor='black', edgecolor=colors[1], boxstyle='round,pad=0.2'), transform=ax[0, 1].get_yaxis_transform(), color=colors[1], weight='bold')
    ax[0, 1].text(data['Days'].iloc[-1], data['Fats'].iloc[-1], f'{round(data["Fats"].iloc[-1])}', color=colors[1], weight='bold', ha='center', va='bottom')

    # Carbs
    ax[1, 0].bar(data['Days'], data['Carbs'], color=colors[2])
    ax[1, 0].axhline(y=recommended_carbs, color=colors[2], linestyle='--')
    ax[1, 0].set_ylabel('Carbs (g)', color=colors[2])
    ax[1, 0].set_title('Carbohydrate', color=colors[2], weight='bold')
    ax[1, 0].tick_params(axis='x', colors=colors[2])
    ax[1, 0].tick_params(axis='y', colors=colors[2])
    ax[1, 0].text(1.01, recommended_carbs, f'{round(recommended_carbs)}', va='center', ha="left", bbox=dict(facecolor='black', edgecolor=colors[2], boxstyle='round,pad=0.2'), transform=ax[1, 0].get_yaxis_transform(), color=colors[2], weight='bold')
    ax[1, 0].text(data['Days'].iloc[-1], data['Carbs'].iloc[-1], f'{round(data["Carbs"].iloc[-1])}', color=colors[2], weight='bold', ha='center', va='bottom')

    # Calories
    ax[1, 1].bar(data['Days'], data['Calories'], color=colors[3])
    ax[1, 1].axhline(y=recommended_calories, color=colors[3], linestyle='--')
    ax[1, 1].set_ylabel('Calories', color=colors[3])
    ax[1, 1].set_title('Calorie', color=colors[3], weight='bold')
    ax[1, 1].tick_params(axis='x', colors=colors[3])
    ax[1, 1].tick_params(axis='y', colors=colors[3])
    ax[1, 1].text(1.01, recommended_calories, f'{round(recommended_calories)}', va='center', ha="left", bbox=dict(facecolor='black', edgecolor=colors[3], boxstyle='round,pad=0.2'), transform=ax[1, 1].get_yaxis_transform(), color=colors[3], weight='bold')
    ax[1, 1].text(data['Days'].iloc[-1], data['Calories'].iloc[-1], f'{round(data["Calories"].iloc[-1])}', color=colors[3], weight='bold', ha='center', va='bottom')

    # Save the figure
    plt.savefig('/Users/avi/Documents/personal code/nutrients/nutrient_charts.png', facecolor='black')
