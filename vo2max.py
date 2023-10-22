import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

def vo2max_male(distance_km):
    return (22.351 * distance_km) - 11.288

def vo2max_female(distance_km):
    return (21.097 * distance_km) - 8.41

# Mean and std dev values for VO2 max based on age and gender. 
# These are values from the provided table; real-world data may differ.
VO2_MEAN_STD = {
    'Male': {
        '20-29': (54.4, 8.4),
        '30-39': (49.1, 7.7),
        '40-49': (47.2, 7.7),
        '50-59': (42.6, 7.4),
        '60-69': (39.2, 6.7),
        '70+': (35.3, 6.5),
    },
    'Female': {
        '20-29': (43.0, 7.7),
        '30-39': (40.0, 6.8),
        '40-49': (38.4, 6.9),
        '50-59': (34.4, 5.7),
        '60-69': (31.1, 5.1),
        '70+': (28.3, 5.2),
    }
}

st.title("Cooper Test VO2 Max Estimator")

gender = st.selectbox("Select Gender", ["Male", "Female"])
age = st.number_input("Enter your age", 5, 99)
distance = st.number_input("Enter distance covered in 12 minutes (km)", 0.0, 20.0)

# Determine age group
if age < 30:
    age_group = '20-29'
elif age < 40:
    age_group = '30-39'
elif age < 50:
    age_group = '40-49'
elif age < 60:
    age_group = '50-59'
elif age < 70:
    age_group = '60-69'
else:
    age_group = '70+'

mean, std_dev = VO2_MEAN_STD[gender][age_group]

# Calculate VO2 max
if st.button("Calculate VO2 Max"):
    if gender == "Male":
        vo2 = vo2max_male(distance)
    else:
        vo2 = vo2max_female(distance)

    # Determine percentile
    percentile = stats.norm.cdf(vo2, mean, std_dev) * 100
    
    st.write(f"Your estimated VO2 max is: {vo2:.2f} ml/kg/min")
    st.write(f"Your percentile for your age group and gender is: {percentile:.2f}%")

    
    # Visualization
    x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 1000)
    y = stats.norm.pdf(x, mean, std_dev)
    
    fig, ax = plt.subplots()
    ax.plot(x, y, label=f"Age: {age_group}, Gender: {gender}")
    ax.axvline(x=vo2, color="red", linestyle="--", label="Your VO2 Max")
    ax.set_title("VO2 Max Distribution by Age and Gender")
    ax.set_ylabel("Probability Density")
    ax.set_xlabel("VO2 Max (ml/kg/min)")
    ax.legend()
    
    st.pyplot(fig)
