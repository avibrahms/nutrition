import matplotlib.pyplot as plt
import numpy as np
from utils import calculate_recommended_values_v2, calculate_averages, define_average_range

def spider(info, data):
    
    n, m = define_average_range(info, data)
    
    # Calculate recommended daily intake for each nutrient
    recommended_protein, recommended_fat, recommended_carbs, recommended_calories = calculate_recommended_values_v2(info)

    # Calculate the average intake and divide by the recommended value
    average_protein, average_fat, average_carbs, average_calories = calculate_averages(data, recommended_protein, recommended_fat, recommended_carbs, recommended_calories, n, m)

    # The data to plot
    data_to_plot = [average_protein, average_fat, average_carbs, average_calories]
    data_to_plot_numbers = [average_protein*recommended_protein, average_fat*recommended_fat, average_carbs*recommended_carbs, average_calories*recommended_calories]

    # Number of variables we're plotting
    num_vars = len(data_to_plot)

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # The plot is a circle, so we need to "complete the loop"
    # and append the start value to the end.
    data_to_plot += data_to_plot[:1]
    angles += angles[:1]

    # Customize colors
    colors = ['skyblue', 'salmon', 'limegreen', 'gold']

    # Customize fonts
    font = {'family' : 'DejaVu Sans',
            'weight' : 'bold',
            'size'   : 14}

    plt.rc('font', **font)

    # Create the spider chart
    fig, ax = plt.subplots(figsize=(6, 5), subplot_kw=dict(polar=True))
    fig.subplots_adjust(right=0.89, left=0.2, top=1, bottom=-0.0)

    # Draw the outline and lines for each nutrient.
    for i in range(num_vars):
        data = data_to_plot[i:i+2]
        angle = angles[i:i+2]
        ax.fill(angle, data, color=colors[i], alpha=0.25)
        ax.plot(angle, data, color=colors[i], linewidth=1)

    # Fix axis to go in the right order and start at 12 o'clock.
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Draw axis lines for each angle and label.
    labels = ['Proteins', 'Fats', 'Carbs', 'Calories']
    ax.set_thetagrids(np.degrees(angles[:-1]), [])
    # Add labels with different colors
    # Add labels with different colors
    for i, label in enumerate(labels):
        angle_rad = i / float(num_vars) * 2 * np.pi

        if angle_rad == 0 or angle_rad == np.pi:
            ha, distance_ax = "center", 1
        elif 0 < angle_rad < np.pi:
            ha, distance_ax = "left", 1
        else:
            ha, distance_ax = "right", 1

        ax.text(angle_rad, distance_ax, label, size=14, color=colors[i],
                horizontalalignment=ha, verticalalignment="center")


    # Go through labels and adjust alignment based on where
    # it is in the circle.
    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')

    # Remove y tick labels
    ax.yaxis.set_ticklabels([])

    # Add percentages for each nutrient
    # if info['AverageValues']:
    #     for angle, value, value_number, label in zip(angles, data_to_plot, data_to_plot_numbers, labels):
    #         ax.text(angle, value, f'{int(value * 100)}%\n({int(round(value_number))}{"g"*int(label!="Calories")})', ha='center', va='bottom', color=colors[labels.index(label)], fontsize=14, weight='bold')
    # else:
    for angle, value, label in zip(angles, data_to_plot, labels):
            ax.text(angle, value, f'{int(value * 100)}%', ha='center', va='bottom', color=colors[labels.index(label)], fontsize=14, weight='bold')

    # Set facecolor and title color
    ax.set_facecolor('black')

    # Set tick colors
    ax.tick_params(axis='x', colors='white')

    # Set figure background color
    fig.patch.set_facecolor('black')

    # Save the figure
    plt.savefig('/Users/avi/Documents/personal code/nutrients/spider_charts.png', facecolor='black')
    plt.close()