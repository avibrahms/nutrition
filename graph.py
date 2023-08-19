#!/usr/bin/env python3

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from utils import calculate_recommended_values_v2

def set_x_labels(ax, dates):
    num_days = len(dates)
    if num_days <= 7:
        ax.set_xticks(dates)
    elif num_days <= 60:
        ax.set_xticks([dates[-1]] + [dates[-1 - i * 7] for i in range(1, num_days // 7 + 1) if (i * 7) < num_days])
    elif num_days <= 365:
        ax.set_xticks([dates[-1]] + [dates[-1 - i * 60] for i in range(1, num_days // 60 + 1) if (i * 60) < num_days])
    else:
        ax.set_xticks([dates[-1]] + [dates[-1 - i * 365] for i in range(1, num_days // 365 + 1) if (i * 365) < num_days])
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))



def plot_individual_chart(nutrient, recommended_nutrient, title, filename, color1, dates):
    plt.figure(figsize=(10, 6), dpi=300)
    plot_chart(plt.gca(), nutrient, recommended_nutrient, title, color1, dates, individual=True)
    plt.tight_layout()
    plt.savefig(filename, facecolor='#121212')
    plt.close()

def plot_chart(df, ax, nutrient, recommended_nutrient, title, color1, dates, individual=False):
    sns.lineplot(x='Days', y=nutrient, data=df, label=nutrient, linewidth=2.5, color=color1, ax=ax)
    sns.lineplot(x='Days', y=recommended_nutrient, data=df, label=recommended_nutrient, linestyle='dashed', linewidth=2.5, color=color1, ax=ax)
    ax.set_title(title, color=color1, pad=20)
    ax.set_ylabel('Grams', color=color1)
    ax.set_xlabel('Days', color=color1)
    ax.tick_params(colors=color1)
    y_max = max(df[nutrient].max(), df[recommended_nutrient].max())
    space_above = 1.3 if individual else 1.45
    ax.set_ylim(0, y_max * space_above)
    legend = ax.legend(loc='upper left', fontsize='small')
    legend.texts[0].set_text(nutrient)
    legend.texts[0].set_color(color1)
    legend.texts[1].set_text(recommended_nutrient)
    legend.texts[1].set_color(color1)
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




def graph(info, df):

    df['Days'] = pd.to_datetime(df['Days'])

    recommended_proteins, recommended_fats, recommended_carbs, recommended_calories = calculate_recommended_values_v2(info)
    num_days = len(df)
    df['Recommended Proteins'] = [recommended_proteins] * num_days
    df['Recommended Fats'] = [recommended_fats] * num_days
    df['Recommended Carbs'] = [recommended_carbs] * num_days
    df['Recommended Calories'] = [recommended_calories] * num_days

    sns.set_theme(style="darkgrid")
    sns.set_context("notebook", font_scale=1.5)
    plt.rcParams['axes.facecolor'] = '#121212'
    plt.rcParams['figure.facecolor'] = '#121212'
    plt.rcParams['grid.color'] = '#404040'

    dates = df['Days'].dt.to_pydatetime()

    fig, axes = plt.subplots(2, 2, figsize=(16, 9), dpi=300)
    plot_chart(df, axes[0, 0], 'Proteins', 'Recommended Proteins', r'$\bf{Protein}$' + f' Intake Over {num_days} Days', 'skyblue', dates)
    plot_chart(df, axes[0, 1], 'Fats', 'Recommended Fats', r'$\bf{Fat}$' + f' Intake Over {num_days} Days', 'salmon', dates)
    plot_chart(df, axes[1, 0], 'Carbs', 'Recommended Carbs', r'$\bf{Carb}$' + f' Intake Over {num_days} Days', 'limegreen', dates)
    plot_chart(df, axes[1, 1], 'Calories', 'Recommended Calories', r'$\bf{Calorie}$' + f' Intake Over {num_days} Days', 'gold', dates)


    plt.tight_layout()
    plt.savefig('/Users/avi/Documents/personal code/nutrients/nutrients.png', facecolor='#121212')
    plt.close()
    

