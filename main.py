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

        # Date pickers for selecting date ranges
        st.sidebar.header("Select Date Ranges")
        date_range1 = st.sidebar.date_input("Select date range for the first file", [])
        date_range2 = st.sidebar.date_input("Select date range for the second file", [])

        if len(date_range1) == 2 and len(date_range2) == 2:
            start_date1, end_date1 = date_range1
            start_date2, end_date2 = date_range2

            # Ensure the DataFrame has the required columns
            if "date" in df1.columns and "quantity" in df1.columns and "item" in df1.columns and \
               "date" in df2.columns and "quantity" in df2.columns and "item" in df2.columns:

                # Filter data based on selected date ranges and sales quantities
                df1_filtered = df1[(df1["date"] >= pd.to_datetime(start_date1)) &
                                   (df1["date"] <= pd.to_datetime(end_date1)) &
                                   (df1["quantity"] >= quantity1)]

                df2_filtered = df2[(df2["date"] >= pd.to_datetime(start_date2)) &
                                   (df2["date"] <= pd.to_datetime(end_date2))]

                # Filter the second file for items matching the first file's filtered results
                matched_items = df1_filtered["item"].unique()
                df2_filtered = df2_filtered[(df2_filtered["item"].isin(matched_items)) &
                                             (df2_filtered["quantity"] <= quantity2)]

                # Display results
                st.write("### Filtered items from the first file")
                st.write(df1_filtered)

                st.write("### Matched items in the second file")
                st.write(df2_filtered)

            else:
                st.error("Ensure both files have 'date', 'item', and 'quantity' columns.")

        else:
            st.warning("Please select valid date ranges.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload both Excel files to proceed.")
