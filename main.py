import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Streamlit app title
st.title("Excel Sales Comparison App")

# Upload two Excel files
file1 = st.file_uploader("Upload the first Excel file", type="xlsx")
file2 = st.file_uploader("Upload the second Excel file", type="xlsx")

# Notification section below input boxes
st.sidebar.header("Notifications")
notification_message = st.sidebar.empty()

# Button to view items with sales less than 20
show_low_sales_button = st.sidebar.button("Show Items with Sales < 20")

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

            # Convert quantity columns to numeric, handling large integers
            df1["quantity"] = pd.to_numeric(df1["quantity"], errors='coerce').fillna(0).astype(np.int64)
            df2["quantity"] = pd.to_numeric(df2["quantity"], errors='coerce').fillna(0).astype(np.int64)

            # Filter data based on sales quantities
            df1_filtered = df1[df1["quantity"] >= quantity1]

            # Filter the second file for items matching the first file's filtered results
            matched_items = df1_filtered["item"].unique()
            df2_filtered = df2[(df2["item"].isin(matched_items)) &
                               ((df2["quantity"] <= quantity2) if quantity2 > 0 else (df2["quantity"] == 0))]

            # Display results
            st.write("### Filtered items from the first file")
            st.write(df1_filtered)

            st.write("### Matched items in the second file")
            st.write(df2_filtered)

            # Notification for items sold less than 20 in the second file
            low_sales_items = df2[df2["quantity"] < 20]
            if not low_sales_items.empty:
                notification_message.warning("Items in the second file with sales less than 20:")

                # Show the low sales items in a window when the button is clicked
                if show_low_sales_button:
                    st.write("### Items in the second file with sales less than 20")
                    st.write(low_sales_items)

            # Export functionality
            def to_excel(df):
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Sheet1')
                    writer.close()  # Correctly close the writer
                processed_data = output.getvalue()
                return processed_data

            st.sidebar.header("Export Filtered Data")
            if not df1_filtered.empty:
                df1_excel = to_excel(df1_filtered)
                st.sidebar.download_button(label="Download Filtered File 1", 
                                           data=df1_excel, 
                                           file_name="filtered_file1.xlsx", 
                                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            if not df2_filtered.empty:
                df2_excel = to_excel(df2_filtered)
                st.sidebar.download_button(label="Download Filtered File 2", 
                                           data=df2_excel, 
                                           file_name="filtered_file2.xlsx", 
                                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            if not low_sales_items.empty:
                low_sales_excel = to_excel(low_sales_items)
                st.sidebar.download_button(label="Download Low Sales Items", 
                                           data=low_sales_excel, 
                                           file_name="low_sales_items.xlsx", 
                                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        else:
            st.error("Ensure both files have 'item' and 'quantity' columns.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload both Excel files to proceed.")
