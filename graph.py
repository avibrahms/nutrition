#!/usr/bin/env python3

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from utils import calculate_recommended_values_v2, calculate_averages, define_average_range

def set_x_labels(ax, dates):
    num_days = len(dates)
    if num_days <= 7:
        ax.set_xticks(dates)
    elif num_days <= 30:
        ax.set_xticks([dates[-1]] + [dates[-1 - i * 7] for i in range(1, num_days // 7 + 1) if (i * 7) < num_days])
    elif num_days <= 125:
        ax.set_xticks([dates[-1]] + [dates[-1 - i * 30] for i in range(1, num_days // 30 + 1) if (i * 30) < num_days])
    elif num_days <= 365:
        ax.set_xticks([dates[-1]] + [dates[-1 - i * 90] for i in range(1, num_days // 90 + 1) if (i * 90) < num_days])
    else:
        ax.set_xticks([dates[-1]] + [dates[-1 - i * 365] for i in range(1, num_days // 365 + 1) if (i * 365) < num_days])
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))



def plot_individual_chart(nutrient, recommended_nutrient, average_nutrient, title, filename, color1, dates):
    plt.figure(figsize=(10, 6), dpi=300)
    plot_chart(plt.gca(), nutrient, recommended_nutrient, average_nutrient, title, color1, dates, individual=True)
    plt.tight_layout()
    plt.savefig(filename, facecolor='#121212')
    plt.close()


def plot_chart(df, ax, nutrient, recommended_nutrient, average_nutrient, title, color1, dates, individual=False, average_nb_days=0):
    # Plot actual nutrient
    sns.lineplot(x='Days', y=nutrient, data=df, label=nutrient, linewidth=2.5, color=color1, ax=ax)
    # print(df[average_nutrient][0])
    # Plot recommended nutrient
    sns.lineplot(x='Days', y=recommended_nutrient, data=df, label=recommended_nutrient, linestyle='dashed', linewidth=2.5, color=color1, ax=ax)
    
    # Plot average nutrient
    if df[average_nutrient][0]:
        sns.lineplot(x='Days', y=average_nutrient, data=df, label=average_nutrient, linestyle='dotted', linewidth=2.5, color=color1, ax=ax)
    
    # Axis and title settings
    ax.set_title(title, color=color1, pad=20)
    ax.set_ylabel('Grams', color=color1)
    ax.set_xlabel('Days', color=color1)
    ax.tick_params(colors=color1)
    
    # Legend settings
    if df[average_nutrient][0]:
        space_above = 1.15 if individual else 1.3
        average_ratio = int(round(df[average_nutrient][0] / df[recommended_nutrient][0] * 100))
        values_to_display = [nutrient, recommended_nutrient, average_nutrient + ' - ' + str(average_ratio) + '%']
    else:
        space_above = 1.3 if individual else 1.45
        values_to_display = [nutrient, recommended_nutrient]
        
    legend = ax.legend(loc='upper left', fontsize=13)
    y_max = max(df[nutrient].max(), df[recommended_nutrient].max(), df[average_nutrient].max())
    for i, text in enumerate(values_to_display):
        legend.texts[i].set_text(text)
        legend.texts[i].set_color(color1)

    ax.set_ylim(0, y_max * space_above)
    # Custom function to set x-axis labels (assuming this function exists)
    set_x_labels(ax, dates)

    # Add y-label for the recommended value
    recommended_value = int(round(df[recommended_nutrient].iloc[0]))
    ax.text(0.0226, recommended_value, f'{recommended_value}', color=color1, backgroundcolor='#121212', transform=ax.get_yaxis_transform(), ha='right', va='center', fontsize=16, weight='bold')

    # Remove overlapping tick labels
    yticks = ax.get_yticks()
    yticks = [ytick for ytick in yticks if abs(ytick - recommended_value) > y_max * 0.14]
    ax.set_yticks(yticks)
    
    # Add y-label for the nutrient value
    value = int(round(df[nutrient].iloc[-1]))
    ax.text(1.01, value, f'{value}', color=color1, backgroundcolor='#121212', transform=ax.get_yaxis_transform(), ha='left', va='center', fontsize=16, weight='bold')
    
    if df[average_nutrient][0]:
        # Add y-label for the average value
        average_value = int(round(df[average_nutrient].iloc[-1]))
        average_nb_days = len(df) if average_nb_days == 0 else average_nb_days
        ax.text(max(0.05,1-average_nb_days/len(df)-0.037), average_value, f'{average_value}', color=color1, backgroundcolor='#121212', transform=ax.get_yaxis_transform(), ha='left', va='center', fontsize=10, weight='bold', bbox=dict(facecolor='black', edgecolor=color1, boxstyle='round,pad=0.2'))


def graph(info, df):

    df['Days'] = pd.to_datetime(df['Days'])
    n, m = define_average_range(info, df)
    recommended_proteins, recommended_fats, recommended_carbs, recommended_calories = calculate_recommended_values_v2(info)
    
    # Calculate the average intake and divide by the recommended value
    average_proteins, average_fats, average_carbs, average_calories = calculate_averages(df, recommended_proteins, recommended_fats, recommended_carbs, recommended_calories, n, m)
    
    num_days = len(df)
    df['Recommended Proteins'] = [recommended_proteins] * num_days
    df['Recommended Fats'] = [recommended_fats] * num_days
    df['Recommended Carbs'] = [recommended_carbs] * num_days
    df['Recommended Calories'] = [recommended_calories] * num_days
    df['Average Proteins'] = [recommended_proteins*average_proteins] * num_days
    df['Average Fats'] = [recommended_fats*average_fats] * num_days
    df['Average Carbs'] = [recommended_carbs*average_carbs] * num_days
    df['Average Calories'] = [recommended_calories*average_calories] * num_days
    
    if not info['AverageValues']:
        df['Average Proteins'] = df['Average Fats'] = df['Average Carbs'] = df['Average Calories'] = 0
    
    sns.set_theme(style="darkgrid")
    sns.set_context("notebook", font_scale=1.5)
    plt.rcParams['axes.facecolor'] = '#121212'
    plt.rcParams['figure.facecolor'] = '#121212'
    plt.rcParams['grid.color'] = '#404040'

    dates = df['Days'].dt.to_pydatetime()
    average_nb_days = int(info.get('LastDaysAverage', 0))
    _, axes = plt.subplots(2, 2, figsize=(16, 9), dpi=300)
    plot_chart(df, axes[0, 0], 'Proteins', 'Recommended Proteins', 'Average Proteins', r'$\bf{Protein}$' + f' Intake Over {num_days} Days', 'skyblue', dates, average_nb_days=average_nb_days)
    plot_chart(df, axes[0, 1], 'Fats', 'Recommended Fats', 'Average Fats', r'$\bf{Fat}$' + f' Intake Over {num_days} Days', 'salmon', dates, average_nb_days=average_nb_days)
    plot_chart(df, axes[1, 0], 'Carbs', 'Recommended Carbs', 'Average Carbs', r'$\bf{Carb}$' + f' Intake Over {num_days} Days', 'limegreen', dates, average_nb_days=average_nb_days)
    plot_chart(df, axes[1, 1], 'Calories', 'Recommended Calories', 'Average Calories', r'$\bf{Calorie}$' + f' Intake Over {num_days} Days', 'gold', dates, average_nb_days=average_nb_days)


    plt.tight_layout()
    plt.savefig('/Users/avi/Documents/personal code/nutrients/nutrients.png', facecolor='#121212')
    plt.close()
    

