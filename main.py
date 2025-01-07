import streamlit as st
import pandas as pd

# Streamlit app title
st.title("Excel Sales Comparison App")

# Upload two Excel files
file1 = st.file_uploader("Upload the first Excel file", type="xlsx")
file2 = st.file_uploader("Upload the second Excel file", type="xlsx")

if file1 and file2:
    # Read the Excel files
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    st.write("### Preview of the first file")
    st.write(df1.head())

    st.write("### Preview of the second file")
    st.write(df2.head())

    # Date pickers for selecting date ranges
    st.sidebar.header("Select Date Ranges")

    date_range1 = st.sidebar.date_input(
        "Select date range for the first file", []
    )
    date_range2 = st.sidebar.date_input(
        "Select date range for the second file", []
    )

    if len(date_range1) == 2 and len(date_range2) == 2:
        start_date1, end_date1 = date_range1
        start_date2, end_date2 = date_range2

        # Ensure the DataFrame has the required columns
        if "date" in df1.columns and "quantity" in df1.columns and "date" in df2.columns:
            # Filter data based on selected date ranges
            df1_filtered = df1[(df1["date"] >= pd.to_datetime(start_date1)) &
                               (df1["date"] <= pd.to_datetime(end_date1)) &
                               (df1["quantity"] > 50)]

            df2_filtered = df2[(df2["date"] >= pd.to_datetime(start_date2)) &
                               (df2["date"] <= pd.to_datetime(end_date2))]

            # Compare the two dataframes to find items with no sales in the second file
            items_with_no_sales = df1_filtered[~df1_filtered["item"].isin(df2_filtered["item"])]

            # Display results
            st.write("### Items from the first file with no sales in the second file")
            st.write(items_with_no_sales)

        else:
            st.error("Ensure both files have 'date', 'item', and 'quantity' columns.")

    else:
        st.warning("Please select valid date ranges.")

else:
    st.info("Please upload both Excel files to proceed.")
