import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt

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

        # File previews in collapsible sections
        with st.expander("Preview the first file"):
            st.write(df1.head())

        with st.expander("Preview the second file"):
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
            matched_items = df1_filtered["item"].unique()
            df2_filtered = df2[
                (df2["item"].isin(matched_items)) &
                ((df2["quantity"] <= quantity2) | (df2["quantity"] == 0))
            ]

            # Matched items display with pie chart
            st.write("### Matched items in the second file (All Rows Including Zeros)")
            st.dataframe(df2_filtered, height=1000, use_container_width=True)

            # Pie Chart Section
            st.write("### Visualization of Matched Items")

            # Toggle between visualizations
            chart_type = st.radio("Select Pie Chart Type:", ["By Item Count", "By Total Quantity"], horizontal=True)

            if chart_type == "By Item Count":
                item_counts = df2_filtered["item"].value_counts()
                fig, ax = plt.subplots()
                ax.pie(item_counts, labels=item_counts.index, autopct="%1.1f%%", startangle=90, colors=plt.cm.Paired.colors)
                ax.set_title("Distribution by Item Count")
                st.pyplot(fig)

            elif chart_type == "By Total Quantity":
                quantity_sums = df2_filtered.groupby("item")["quantity"].sum()
                fig, ax = plt.subplots()
                ax.pie(quantity_sums, labels=quantity_sums.index, autopct="%1.1f%%", startangle=90, colors=plt.cm.Paired.colors)
                ax.set_title("Distribution by Total Quantity")
                st.pyplot(fig)

            # Add a download button for full matched results
            def to_csv(df):
                return df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="Download Full Results as CSV",
                data=to_csv(df2_filtered),
                file_name="matched_items.csv",
                mime="text/csv"
            )

            # Notification for items sold less than 20 in the second file
            low_sales_items = df2[df2["quantity"] < 20]
            if not low_sales_items.empty:
                notification_message.warning("Items in the second file with sales less than 20:")
                if show_low_sales_button:
                    with st.expander("Items with sales less than 20"):
                        st.write(low_sales_items)

            # Export functionality
            def to_excel(df):
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Sheet1')
                    writer.close()
                return output.getvalue()

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
