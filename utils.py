import pyperclip
import pandas as pd
import csv
import re
import os

def verify_csv_line(clipboard_content):
    # Verify the format "date,int/float,int/float,int/float,int/float"
    pattern = r"^\d{4}-\d{2}-\d{2},-?\d+(\.\d+)?,-?\d+(\.\d+)?,-?\d+(\.\d+)?,-?\d+(\.\d+)?$"
    return re.match(pattern, clipboard_content)

def process_csv_from_clipboard(csv_file_path):
    # 1. Take what is on the clipboard
    clipboard_content = pyperclip.paste()
    return process_csv(csv_file_path, clipboard_content)
    
def process_csv(csv_file_path, clipboard_content):
    print('Clipboard content:', clipboard_content)
    # 2. Verify the clipboard content
    if not verify_csv_line(clipboard_content):
        print("Clipboard content is not in the required CSV format.")
        return
    
    # 3. Open the CSV file
    if not os.path.exists(csv_file_path):
        print("CSV file does not exist.")
        return

    # Read all lines from the CSV
    with open(csv_file_path, 'r') as f:
        lines = list(csv.reader(f))

    # Remove empty or header lines from the end
    while lines and not lines[-1]:
        lines.pop()

    # 4. Check the last line's first column (date)
    last_line = lines[-1]
    last_date = last_line[0]
    clipboard_list = clean_elements(clipboard_content.split(','))
    print('Clipboard list:', clipboard_list)
    clipboard_date = clipboard_list[0]

    # 5 & 6. Replace or append the line
    if last_date == clipboard_date:
        lines[-1] = clipboard_list
    else:
        lines.append(clipboard_list)

    # Write back to the CSV
    with open(csv_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(lines)
        # close the file
        f.close()

def clean_elements(clipboard_list):
    return [re.sub(r'[^0-9\-,.]', '', element) for element in clipboard_list]

def calculate_averages(data, recommended_protein, recommended_fat, recommended_carbs, recommended_calories, n=None, m=None):
    average_protein = data['Proteins'][n:m].mean() / recommended_protein
    average_fat = data['Fats'][n:m].mean() / recommended_fat
    average_carbs = data['Carbs'][n:m].mean() / recommended_carbs
    average_calories = data['Calories'][n:m].mean() / recommended_calories
    return average_protein, average_fat, average_carbs, average_calories

def read_nutrients(file_path): 
    process_csv_from_clipboard(file_path)
    df = pd.read_csv(file_path)
    return df

def read_personal_info(file_path):
    info = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Skip empty lines
            if line.strip():
                key, value = line.strip().split(': ')
                info[key] = float(value) if key != 'Gender' else value
    return info

def calculate_recommended_values(info):
    weight = info['Weight']
    height = info['Height']
    age = info['Age']
    gender = info['Gender']
    workout_days = info['WorkoutDays']
    fasting_hours = info.get('FastingHours', 0)  # Default to 0 if not provided

    # Using the Mifflin-St Jeor equation for BMR calculation
    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Check if PAL is provided, otherwise calculate based on workout days
    pal = info.get('PAL')
    if pal is None:
        pal = 1.2 + (workout_days * 0.1)

    daily_calories = bmr * pal

    # Check if FastingCalorieDiminishingPercent is provided, otherwise use the fasting_hours calculation
    fasting_percent = info.get('FastingCalorieDiminishingPercent')
    if fasting_percent is not None:
        daily_calories -= daily_calories * (fasting_percent / 100)
    else:
        daily_calories -= fasting_hours * 10  # Adjusting for fasting

    # Protein (using the provided factor, or defaulting to 1.8 if not provided)
    protein_factor = info.get('ProteinFactor', 1.8)
    recommended_proteins = weight * protein_factor
    
    # Fat (using the provided percentage, or defaulting to 25% if not provided)
    fat_percentage = info.get('FatNeedPercentageFromCalories', 25)
    recommended_fats = daily_calories * (fat_percentage / 100) / 9
    
    # Carbohydrates
    carbohydrate_percentage = info.get('CarbohydratePercentageFromCalories', None)
    if carbohydrate_percentage is not None:
        recommended_carbs = (daily_calories * carbohydrate_percentage / 100) / 4
    else:
        # Initial formula: remaining calories after protein and fat
        recommended_carbs = (daily_calories - (recommended_proteins * 4 + recommended_fats * 9)) / 4


    return recommended_proteins, recommended_fats, recommended_carbs, daily_calories

def calculate_recommended_values_v2(info):
    weight = info['Weight']
    height = info['Height']
    age = info['Age']
    gender = info['Gender']
    AdaptiveThermogenesis = info.get('AdaptiveThermogenesis', 0)
    workout_days = info.get('WorkoutDays', 0)
    workoutDifficulty = info.get('WorkoutDifficulty', 1)
    fasting_hours = info.get('FastingHours', 0)  # Default to 0 if not provided

    # Using the Mifflin-St Jeor equation for BMR calculation
    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
    # Adjusting for adaptive thermogenesis
    bmr -= AdaptiveThermogenesis * 0.1 * bmr
    
    # Check if PAL is provided, otherwise calculate based on workout days
    pal = info.get('PAL')
    if pal is None:
        pal = 1.2 + (workout_days * 0.1 * workoutDifficulty)

    # Adjusting for adaptive thermogenesis
    pal -= 0.08 * pal * AdaptiveThermogenesis
    
    daily_calories = bmr * pal

    # Check if FastingCalorieDiminishingPercent is provided, otherwise use the fasting_hours calculation
    fasting_percent = info.get('FastingCalorieDiminishingPercent')
    if fasting_percent is not None:
        daily_calories -= daily_calories * (fasting_percent / 100)
    else:
        daily_calories -= fasting_hours * 10  # Adjusting for fasting
        
    daily_calories -= info.get('CalorieAdjustment', 0)

    # Protein (using the provided factor, or defaulting to 1.8 if not provided)
    protein_factor = info.get('ProteinFactor', 1.8)
    recommended_proteins = weight * protein_factor
    
    # Fat (using the provided factor, or defaulting to 0 if not provided)
    fat_factor = info.get('FatFactor', 1)
    recommended_fats = weight * fat_factor

    # Carbohydrates (using the provided factor, or defaulting to 0 if not provided)
    carb_factor = info.get('CarbFactor', 2)
    recommended_carbs = weight * carb_factor

    return recommended_proteins, recommended_fats, recommended_carbs, daily_calories

def define_average_range(info, data):
    
    days = int(info.get('LastDaysAverage', 0))
    if len(data) > 1:
        if days <= 0:
            n = None
            m = None
        elif days == 1:
            n = -1
            m = None
        elif days > 1 and days < len(data):
            n = -days - 1
            m = -1
        elif days >= len(data):
            n = None
            m = -1
    elif len(data) <= 1:
        n = None
        m = None
        
    return n,m