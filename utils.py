import pandas as pd

def read_nutrients(file_path):
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

