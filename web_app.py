import pickle
import os
import numpy as np
import streamlit as st

# Load the trained model
model_path = r"C:\Users\chotu s\Desktop\crime rate projct\trained_model.sav"
loaded_model = pickle.load(open(model_path, "rb"))

if os.path.exists(model_path):
    try:
        with open(model_path, "rb") as file:
            loaded_model = pickle.load(file)
        print("Model loaded successfully!")
    except Exception as e:
        st.error(f"Error loading model: {e}")
else:
    st.error(f"Error: Model file not found at {model_path}")

# Dictionaries
city_names = {
    '0': 'Ahmedabad', '1': 'Bengaluru', '2': 'Chennai', '3': 'Coimbatore',
    '4': 'Delhi', '5': 'Ghaziabad', '6': 'Hyderabad', '7': 'Indore',
    '8': 'Jaipur', '9': 'Kanpur', '10': 'Kochi', '11': 'Kolkata',
    '12': 'Kozhikode', '13': 'Lucknow', '14': 'Mumbai', '15': 'Nagpur',
    '16': 'Patna', '17': 'Pune', '18': 'Surat'
}

crime_names = {
    '0': 'Crime Committed by Juveniles', '1': 'Crime against SC',
    '2': 'Crime against ST', '3': 'Crime against Senior Citizen',
    '4': 'Crime against children', '5': 'Crime against women',
    '6': 'Cyber Crimes', '7': 'Economic Offences',
    '8': 'Kidnapping', '9': 'Murder'
}

populations = {
    '0': 63.50, '1': 85.00, '2': 87.00, '3': 21.50, '4': 163.10,
    '5': 23.60, '6': 77.50, '7': 21.70, '8': 30.70, '9': 29.20,
    '10': 21.20, '11': 141.10, '12': 20.30, '13': 29.00, '14': 184.10,
    '15': 25.00, '16': 20.50, '17': 50.50, '18': 45.80
}

# Prediction function
def predict_crime(year, city_code, crime_code):
    try:
        year = int(year)
        city_code = str(city_code)
        crime_code = str(crime_code)
        base_pop = populations[city_code]
        adjusted_pop = base_pop * (1 + 0.01 * (year - 2011))

        input_data = np.array([[year, int(city_code), adjusted_pop, int(crime_code)]], dtype=np.float32)
        crime_rate = loaded_model.predict(input_data)[0]

        if crime_rate <= 1:
            status = "Very Low Crime Area"
        elif crime_rate <= 5:
            status = "Low Crime Area"
        elif crime_rate <= 15:
            status = "High Crime Area"
        else:
            status = "Very High Crime Area"

        estimated_cases = int(np.ceil(crime_rate * adjusted_pop))
        return city_names[city_code], crime_names[crime_code], adjusted_pop, crime_rate, status, estimated_cases

    except Exception as e:
        return None, None, None, None, None, f"Prediction error: {e}"

# Streamlit app
def main():
    st.title("Crime Rate Prediction Web App")

    # Input form
    city_code = st.selectbox("Select City", options=city_names.keys(), format_func=lambda x: city_names[x])
    crime_code = st.selectbox("Select Crime Type", options=crime_names.keys(), format_func=lambda x: crime_names[x])
    year = st.text_input("Enter Year", "2025")

    if st.button("Predict Crime Rate"):
        city, crime, pop, rate, status, cases = predict_crime(year, city_code, crime_code)
        if city:
            st.success(f"City: {city}")
            st.success(f"Crime Type: {crime}")
            st.success(f"Year: {year}")
            st.info(f"Population (estimated): {pop:.2f} Lakhs")
            st.info(f"Predicted Crime Rate: {rate:.2f}")
            st.warning(f"Crime Status: {status}")
            st.success(f"Estimated Number of Cases: {cases}")
        else:
            st.error(cases)

if __name__ == "__main__":
    main()