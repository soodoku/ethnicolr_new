import streamlit as st
import pandas as pd
import ethnicolr
from ethnicolr import census_ln, pred_census_ln
import base64


# Define your sidebar options
sidebar_options = {
    'Append Census Data to Last Name': census_ln,
    'Florida VR Last Name Model': pred_census_ln
}

def download_file(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="results.csv">Download results</a>'
    st.markdown(href, unsafe_allow_html=True)

def app():
    # Set app title
    st.title("ethnicolr: Predict Race and Ethnicity From Name")

    # Generic info.
    st.write('We exploit the US census data, the Florida voting registration data, and the Wikipedia data collected by Skiena and colleagues, to predict race and ethnicity based on first and last name or just the last name.')
    st.write('[Github](https://github.com/appeler/ethnicolr)')

    # Set up the sidebar
    st.sidebar.title('Select Function')
    selected_function = st.sidebar.selectbox('', list(sidebar_options.keys()))

    # Upload CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    # Load data
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Data loaded successfully!")
    else:
        st.stop()

    if selected_function == "Append Census Data to Last Name": 
        lname_col = st.selectbox("Select column with last name", df.columns)
        year = st.selectbox("Select a year", [2000, 2010])
        function = sidebar_options[selected_function]
        if st.button('Run'):
            transformed_df = function(df, namecol=lname_col, year = year)
            st.dataframe(transformed_df)
            download_file(transformed_df)

    elif selected_function == "Florida VR Last Name Model":
        lname_col = st.selectbox("Select column with last name", df.columns)
        function = sidebar_options[selected_function]
        if st.button('Run'):
            transformed_df = function(df, namecol=lname_col)
            st.dataframe(transformed_df)
            download_file(transformed_df)

    


# Run the app
if __name__ == "__main__":
    app()