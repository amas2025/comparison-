import streamlit as st
import pandas as pd

# Streamlit app title
st.title("Excel Sales Comparison App")

# Upload two Excel files
file1 = st.file_uploader("Upload the first Excel file", type="xlsx")
file2 = st.file_uploader("Upload the second Excel file", type="xlsx")

if file1 and file2:
    try:
        # Read the Excel files using openpyxl engine
        df1 = pd.read_excel(file1, engine='openpyxl')
        df2 = pd.read_excel(file2, engine='openpyxl')

        st.write("### Preview of the first file")
        st.write(df1.head())

        st.write("### Preview of the second file")
        st.write(df2.head())

        # Input boxes for specifying sales quantities
        st.sidebar.header("Specify Sales Quantities")
        quantity1 = st.sidebar.number_input("Minimum sales quantity for the first file", min_value=0, value=50)
        quantity2 = st.sidebar.number_input("Maximum sales quantity for the second file", min_value=0, value=100)

        # Ensure the DataFrame has the required columns
        if "quantity" in df1.columns and "item" in df1.columns and \
           "quantity" in df2.columns and "item" in df2.columns:

            # Filter data based on sales quantities
            df1_filtered = df1[df1["quantity"] >= quantity1]

            # Filter the second file for items matching the first file's filtered results
            matched_items = df1_filtered["item"].unique()
            df2_filtered = df2[(df2["item"].isin(matched_items)) &
                               (df2["quantity"] <= quantity2)]

            # Display results
            st.write("### Filtered items from the first file")
            st.write(df1_filtered)

            st.write("### Matched items in the second file")
            st.write(df2_filtered)

        else:
            st.error("Ensure both files have 'item' and 'quantity' columns.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload both Excel files to proceed.")
