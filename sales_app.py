import streamlit as st
import pandas as pd
import pickle

# Load the trained Decision Tree model
@st.cache_resource
def load_model():
    with open('decision_tree_model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

DT_model = load_model()

st.title('Sales Prediction App')
st.write('Enter the features to predict sales high/low:')

# Define input fields based on the model's expected features
# Features: 'CompPrice', 'Income', 'Advertising', 'Population', 'Price',
# 'ShelveLoc', 'Age', 'Education', 'Urban', 'US'

CompPrice = st.slider('Competitor Price (CompPrice)', min_value=50, max_value=200, value=120)
Income = st.slider('Income', min_value=20, max_value=120, value=60)
Advertising = st.slider('Advertising Budget', min_value=0, max_value=30, value=10)
Population = st.slider('Population', min_value=0, max_value=500, value=250)
Price = st.slider('Price', min_value=50, max_value=200, value=100)

# ShelveLoc was label encoded: 0=Bad, 1=Good, 2=Medium
ShelveLoc_options = {'Bad': 0, 'Good': 1, 'Medium': 2}
selected_shelveloc = st.selectbox('Shelve Location', options=list(ShelveLoc_options.keys()))
ShelveLoc = ShelveLoc_options[selected_shelveloc]

Age = st.slider('Age', min_value=20, max_value=80, value=45)
Education = st.slider('Education Level', min_value=10, max_value=18, value=14)

# Urban was label encoded: 0=No, 1=Yes
Urban_options = {'No': 0, 'Yes': 1}
selected_urban = st.selectbox('Is it an Urban location?', options=list(Urban_options.keys()))
Urban = Urban_options[selected_urban]

# US was label encoded: 0=No, 1=Yes
US_options = {'No': 0, 'Yes': 1}
selected_us = st.selectbox('Is it in the US?', options=list(US_options.keys()))
US = US_options[selected_us]


if st.button('Predict Sales Level'):
    # Create a DataFrame from the inputs
    input_data = pd.DataFrame([{
        'CompPrice': CompPrice,
        'Income': Income,
        'Advertising': Advertising,
        'Population': Population,
        'Price': Price,
        'ShelveLoc': ShelveLoc,
        'Age': Age,
        'Education': Education,
        'Urban': Urban,
        'US': US
    }])

    # Make prediction
    prediction = DT_model.predict(input_data)

    # Display result
    if prediction[0] == 1:
        st.success('Predicted Sales Level: High (1)')
    else:
        st.error('Predicted Sales Level: Low (0)')

# Install localtunnel and run the Streamlit app
# !npm install -g localtunnel
# !streamlit run sales_app.py &>/dev/null& # Run in background
# !lt --port 8501 # Expose port 8501 (default for Streamlit)
