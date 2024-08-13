import joblib
import pandas as pd
import streamlit as st
from feature_mappings import peb_mapping, state_of_building_mapping, type_of_property_mapping, flooding_zone_mapping, default_values

# Load the model
model = joblib.load('model.pkl')

# List of feature names
feature_names = [
    'BathroomCount', 'BedroomCount', 'ConstructionYear', 'District', 'Fireplace',
    'Furnished', 'Garden', 'GardenArea', 'Kitchen', 'LivingArea', 'Locality',
    'MonthlyCharges', 'NumberOfFacades', 'PEB', 'PostalCode', 'PropertyId',
    'RoomCount', 'ShowerCount', 'StateOfBuilding', 'SubtypeOfProperty',
    'SurfaceOfPlot', 'SwimmingPool', 'Terrace', 'ToiletCount', 'TypeOfProperty',
    'SubtypeOfProperty_Numerical', 'TypeOfSale_Numerical', 'Kitchen_Numerical',
    'StateOfBuilding_Numerical', 'FloodingZone_Numerical',
    'FloodingZone_CIRCUMSCRIBED_FLOOD_ZONE', 'FloodingZone_CIRCUMSCRIBED_WATERSIDE_ZONE',
    'FloodingZone_NON_FLOOD_ZONE', 'FloodingZone_POSSIBLE_FLOOD_ZONE',
    'FloodingZone_POSSIBLE_N_CIRCUMSCRIBED_FLOOD_ZONE', 'FloodingZone_POSSIBLE_N_CIRCUMSCRIBED_WATERSIDE_ZONE',
    'FloodingZone_RECOGNIZED_FLOOD_ZONE', 'FloodingZone_RECOGNIZED_N_CIRCUMSCRIBED_FLOOD_ZONE',
    'FloodingZone_RECOGNIZED_N_CIRCUMSCRIBED_WATERSIDE_FLOOD_ZONE', 'TypeOfSale_annuity_lump_sum',
    'TypeOfSale_annuity_monthly_amount', 'TypeOfSale_annuity_without_lump_sum',
    'TypeOfSale_homes_to_build', 'TypeOfSale_residential_monthly_rent', 'TypeOfSale_residential_sale'
]

st.title('ImmoWeb Prediction App')

# Sidebar inputs
st.sidebar.header('Input Features')

num_rooms = st.sidebar.number_input('Rooms', min_value=0, max_value=100, value=1)
area = st.sidebar.number_input('Area (m²)', min_value=20, max_value=10000, value=20)
num_facades = st.sidebar.number_input('Facades', min_value=1, max_value=4, value=1)
num_bedrooms = st.sidebar.number_input('Bedrooms', min_value=1, max_value=5, value=1)

# Dynamic feature addition in the sidebar
feature_options = [ 
    'BathroomCount', 'ConstructionYear', 'Fireplace', 'Furnished', 'Garden', 'GardenArea', 
    'Kitchen', 'Locality', 'MonthlyCharges', 'PEB', 'PostalCode',
    'ShowerCount', 'StateOfBuilding', 'SurfaceOfPlot', 'SwimmingPool', 'Terrace', 
    'Toilet', 'TypeOfProperty', 'TypeOfSale_Numerical', 'FloodingZone_Numerical'
]
selected_features = st.sidebar.multiselect('Add Features', feature_options)

# Generate inputs for selected features
additional_features = {}
for feature in selected_features:
    if feature == 'BathroomCount':
        additional_features['BathroomCount'] = st.sidebar.number_input('Bathroom Count', min_value=1, value=1)
    elif feature == 'ConstructionYear':
        additional_features['ConstructionYear'] = st.sidebar.number_input('Construction Year', min_value=1800, max_value=2024, value=2000)
    elif feature == 'Fireplace':
        additional_features['Fireplace'] = st.sidebar.checkbox('Fireplace')
    elif feature == 'Furnished':
        additional_features['Furnished'] = st.sidebar.checkbox('Furnished')
    elif feature == 'Garden':
        additional_features['Garden'] = st.sidebar.checkbox('Garden')
        if additional_features['Garden']:
            additional_features['GardenArea'] = st.sidebar.number_input('Garden Area (m²)', min_value=0, max_value=20000, value=0)
    elif feature == 'Kitchen':
        additional_features['Kitchen'] = st.sidebar.checkbox('Kitchen')
    elif feature == 'Locality':
        additional_features['Locality'] = st.sidebar.number_input('Locality', min_value=0, max_value=10, value=0)
    elif feature == 'MonthlyCharges':
        additional_features['MonthlyCharges'] = st.sidebar.number_input('Monthly Charges', min_value=0, max_value=5000, value=0)
    elif feature == 'PEB':
        additional_features['PEB'] = st.sidebar.selectbox('PEB', options=list(peb_mapping.keys()), index=0)
    elif feature == 'PostalCode':
        additional_features['PostalCode'] = st.sidebar.number_input('Postal Code', min_value=1000, max_value=9999, value=1000)
    elif feature == 'ShowerCount':
        additional_features['ShowerCount'] = st.sidebar.number_input('Shower Count', min_value=1, max_value=5, value=1)
    elif feature == 'StateOfBuilding':
        additional_features['StateOfBuilding'] = st.sidebar.selectbox('State of Building', options=list(state_of_building_mapping.keys()), index=0)
    elif feature == 'SwimmingPool':
        additional_features['SwimmingPool'] = st.sidebar.checkbox('Swimming Pool')
    elif feature == 'Terrace':
        additional_features['Terrace'] = st.sidebar.checkbox('Terrace')
    elif feature == 'Toilet':
        additional_features['Toilet'] = st.sidebar.number_input('Toilet', min_value=1, max_value=5, value=1)
    elif feature == 'TypeOfProperty':
        additional_features['TypeOfProperty'] = st.sidebar.selectbox('Type of Property', options=list(type_of_property_mapping.keys()), index=0)
    elif feature == 'FloodingZone_Numerical':
        additional_features['FloodingZone_Numerical'] = st.sidebar.selectbox('Flooding Zone', options=list(flooding_zone_mapping.keys()), index=2)

# Feature mapping function
def map_categorical_features(data):
    if 'PEB' in data:
        data['PEB'] = peb_mapping.get(data['PEB'], 0)
    if 'StateOfBuilding' in data:
        data['StateOfBuilding'] = state_of_building_mapping.get(data['StateOfBuilding'], 0)
    if 'TypeOfProperty' in data:
        data['TypeOfProperty'] = type_of_property_mapping.get(data['TypeOfProperty'], 0)
    if 'FloodingZone_Numerical' in data:
        data['FloodingZone_Numerical'] = flooding_zone_mapping.get(data['FloodingZone_Numerical'], 0)
    return data

# Prediction function
def predict():
    user_data = {
        'RoomCount': num_rooms,
        'LivingArea': area,
        'NumberOfFacades': num_facades,
        'BedroomCount': num_bedrooms,
    }

    # Fill user data with additional features
    user_data.update(additional_features)
    
    # Fill missing features with default values
    for feature in feature_names:
        if feature not in user_data:
            user_data[feature] = default_values.get(feature, 0)

    # Map categorical features
    mapped_data = map_categorical_features(user_data)
    
    # Create DataFrame and make prediction
    input_data = pd.DataFrame([mapped_data], columns=feature_names)
    prediction = model.predict(input_data)[0]
    return prediction

# Button to trigger prediction
if st.sidebar.button('Predict'):
    result = predict()
    st.header(f'Predicted Price: {result:.2f} €')
    st.balloons()

st.markdown("""
    <style>
    .fade-in {
        animation: fadeIn 15s;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="fade-in">Gooood prices.</div>', unsafe_allow_html=True)

# Display the Immoweb logo
st.image('immologo.png', width=500)



joblib.dump(model, 'random_forest_model.joblib', compress=9)