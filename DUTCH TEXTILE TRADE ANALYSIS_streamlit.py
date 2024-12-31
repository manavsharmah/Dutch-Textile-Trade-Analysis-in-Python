import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Dutch Textile Trade",
    page_icon=":bar_chart:",
)

@st.cache_data()
def load_data():
    df = pd.read_csv(r'C:\Users\manav\Desktop\miniproj\Dutchtrade1.csv')
    return df

df = load_data()


st.title("Dutch Textile Trade Analysis :bar_chart:")
st.markdown("Explore the Dutch Textile Trade dataset and gain insights.")

selected_option = st.sidebar.selectbox("Select an option",("Overview","Textiles and Values"))

if selected_option == "Overview":
    st.header("Dutch Textile Trade Overview")
    st.dataframe(df)

    # Summary statistics
    st.subheader("Summary Statistics  📈")
    st.write(df.describe())
    
    
    
    
    
    option = st.sidebar.selectbox(
        "Select option to see Data and Graph on:",
        ('Total Shipment starting each year',
         'Total Shipment endind each year',
         'Shipment by each Company',
         'Starting port of shipment',
         'Ending port of shipment',
         'Total quantity of textile shiped',
         'Total quantity of textile shiped of each type',
         'Total quantity of textile exported from each port',
         'Total quantity of textile shiped each year'))
    
    if option == 'Total Shipment starting each year':
        
        st.subheader("Total Shipment starting each year")
        bar_colors = [ '#F4E0B9' ]
        # How many shipments started for each year
        starting_shipment = df['orig_yr'].value_counts()
        st.write(starting_shipment)
        st.bar_chart(starting_shipment)
        
        
    elif option == 'Total Shipment endind each year':
        
        st.subheader("Total Shipment endind each year")
        
        # How many shpiments ended in each year
        ending_shipment = df['dest_yr'].value_counts()
        st.write(ending_shipment)
        st.bar_chart(ending_shipment)
        plot_colors = ['mediumblue']
        
        
    elif option == 'Shipment by each Company':
        
        st.subheader("Shipment by each Company")
        
        # How many shipments were made by each companies
        shiping_company = df['company'].value_counts()
        st.write(shiping_company)
        st.bar_chart(shiping_company)
        plot_colors = ['mediumblue']
        
    elif option == 'Starting port of shipment':
        
        st.subheader("Starting port of shipment")
        
        # How many shipments started in each port
        ship_orig = df['orig_loc_port_modern'].value_counts()
        st.write(ship_orig)
        st.bar_chart(ship_orig)
        plot_colors = ['mediumblue']
        
    elif option == 'Ending port of shipment':
        
        st.subheader("Ending port of shipment")
        
        # How many shipments ended in each port
        ship_dest = df['dest_loc_port'].value_counts()
        st.write(ship_dest)
        st.bar_chart(ship_dest)
        plot_colors = ['mediumblue']
        
    elif option == 'Total quantity of textile shiped':
        
        st.subheader("Total quantity of textile shiped")
        
        # Total quantity of textiles shipped
        df['textile_quantity'] = pd.to_numeric(df['textile_quantity'], errors='coerce')
        total_quantity = df['textile_quantity'].sum()
        st.write("Total quantity of textiles:", total_quantity)
            
    elif option == 'Total quantity of textile shiped of each type':
        
        st.subheader("Total quantity of textile shiped of each type")
        
        # Total quantity of textile of each type shipped
        total_quantity_shipped_of_each_type = df.groupby('textile_name')['textile_quantity'].sum()
        st.write(total_quantity_shipped_of_each_type)
        st.bar_chart(total_quantity_shipped_of_each_type)
        plot_colors = ['mediumblue']
        
    elif option == 'Total quantity of textile exported from each port':
        
        st.subheader("Total quantity of textile exported from each port")
        
        # Total quantity of textile exported from each port
        quantity_left_per_port = df.groupby('orig_loc_region_modern')['textile_quantity'].sum()
        pd.set_option('display.float_format', '{:.2f}'.format)
        st.write(quantity_left_per_port)
        st.bar_chart(quantity_left_per_port)
        plot_colors = ['mediumblue']
        
    elif option == 'Total quantity of textile shiped each year':
        
        st.subheader("Total quantity of textile shiped each year")
        
        # Total quantity of textile shipped every year
        quantity_left_per_year = df.groupby('orig_yr')['textile_quantity'].sum()
        pd.set_option('display.float_format', '{:.2f}'.format)
        st.write(quantity_left_per_year)
        st.bar_chart(quantity_left_per_year)
        plot_colors = ['mediumblue']

        
elif selected_option== "Textiles and Values":
    
    textile_names = df['textile_name'].drop_duplicates().sort_values()
    textile_type = st.sidebar.selectbox("Select a Textile Type:",textile_names)
    
    x_axis = st.sidebar.selectbox("Choose a variable for x-axis",("Year","Destination Port","Origin region"))
    y_axis = st.sidebar.selectbox("Choose a variable for y-axis",("Quantity Shipped","Total Value (Dutch guilders)"))
    
    plt.gca().set_facecolor('none')
    plt.gca().xaxis.grid(False)
    
    if x_axis == "Year":
        
        if y_axis == "Quantity Shipped":
            
            #Filtering textile type
            textile_type_to_plot = textile_type
            filtered_df = df[df['textile_name'] == textile_type]
            
            #Converting Orig_yr to int
            filtered_df['orig_yr'] = filtered_df['orig_yr'].astype(int)
            
            # Get unique years and sort them
            unique_years = filtered_df['orig_yr'].unique()
            unique_years.sort()
            
            # Group and sum quantities
            grouped_df = filtered_df.groupby('orig_yr')['textile_quantity'].sum().reset_index()
            grouped_df.sort_values('orig_yr', inplace=True)
            
            # Creating bar plot
            fig, ax = plt.subplots()
            ax.bar(grouped_df['orig_yr'], grouped_df['textile_quantity'])
            ax.set_xlabel('Year')
            ax.set_ylabel('Textile Quantity')
            ax.set_title(f'Graph for {textile_type}')
            
            # Setting x-axis tick labels and rotate them
            ax.set_xticks(unique_years)
            ax.set_xticklabels(unique_years, rotation='vertical')
            
            # Displaying the plot in Streamlit
            st.pyplot(fig)
            
            
        elif y_axis == "Total Value (Dutch guilders)":
            
            #filtering textile type
            textile_type_to_plot = textile_type
            filtered_df = df[df['textile_name'] == textile_type]
            
            #Converting orig_yr to int
            filtered_df['orig_yr'] = filtered_df['orig_yr'].astype(int)
            
            #get unique years and sort them
            unique_years = filtered_df['orig_yr'].unique()
            unique_years.sort()
            
            #Group and sum quantities
            grouped_df = filtered_df.groupby('orig_yr')['total_value'].sum().reset_index()
            grouped_df.sort_values('orig_yr', inplace=True)
            
            #Creating bar plot
            fig, ax = plt.subplots()
            ax.bar(grouped_df['orig_yr'], grouped_df['total_value'])
            ax.set_xlabel('Year')
            ax.set_ylabel('Total Value')
            ax.set_title(f'Graph for {textile_type}')
            
            # Setting x-axis tick labels and rotate them
            ax.set_xticks(unique_years)
            ax.set_xticklabels(unique_years, rotation='vertical')
            
            # Displaying the plot in Streamlit
            st.pyplot(fig)
        
        
    elif x_axis == "Destination Port":
        
        if y_axis == "Quantity Shipped":
            
            #Filtering textile type
            textile_type_to_plot = textile_type
            filtered_df = df[df['textile_name'] == textile_type]
            
            
            # Get unique Dest_loc
            unique_dest = filtered_df['dest_loc_port'].unique()
            
            # Group and sum quantities
            grouped_df = filtered_df.groupby('dest_loc_port')['textile_quantity'].sum().reset_index()
            grouped_df.sort_values('dest_loc_port', inplace=True)
            
            # Creating bar plot
            fig, ax = plt.subplots()
            ax.bar(grouped_df['dest_loc_port'], grouped_df['textile_quantity'])
            ax.set_xlabel('Destination')
            ax.set_ylabel('Textile Quantity')
            ax.set_title(f'Graph for {textile_type}')
            
            # Setting x-axis tick labels and rotate them
            ax.set_xticklabels(unique_dest, rotation='vertical')
            
            # Displaying the plot in Streamlit
            st.pyplot(fig)
            
            
        elif y_axis == "Total Value (Dutch guilders)":
            
            #filtering textile type
            textile_type_to_plot = textile_type
            filtered_df = df[df['textile_name'] == textile_type]
            
            
            #get unique dest_loc 
            unique_dest = filtered_df['dest_loc_port'].unique()
            
            #Group and sum quantities
            grouped_df = filtered_df.groupby('dest_loc_port')['total_value'].sum().reset_index()
            grouped_df.sort_values('dest_loc_port', inplace=True)
            
            #Creating bar plot
            fig, ax = plt.subplots()
            ax.bar(grouped_df['dest_loc_port'], grouped_df['total_value'])
            ax.set_xlabel('Destination')
            ax.set_ylabel('Total Value')
            ax.set_title(f'Graph for {textile_type}')
            
            # Setting x-axis tick labels and rotate them
            ax.set_xticklabels(unique_dest, rotation='vertical')
            
            # Displaying the plot in Streamlit
            st.pyplot(fig)
            
    elif x_axis == "Origin region":
        
        if y_axis == "Quantity Shipped":
            
        
            #Filtering textile type
            textile_type_to_plot = textile_type
            filtered_df = df[df['textile_name'] == textile_type]
        
        
            # Get unique Origin region
            unique_orig = filtered_df['orig_loc_region_modern'].unique()
        
            # Group and sum quantities
            grouped_df = filtered_df.groupby('orig_loc_region_modern')['textile_quantity'].sum().reset_index()
            grouped_df.sort_values('orig_loc_region_modern', inplace=True)
            
            # Creating bar plot
            fig, ax = plt.subplots()
            ax.bar(grouped_df['orig_loc_region_modern'], grouped_df['textile_quantity'])
            ax.set_xlabel('Origin')
            ax.set_ylabel('Textile Quantity')
            ax.set_title(f'Graph for {textile_type}')
        
            # Setting x-axis tick labels and rotate them
            ax.set_xticklabels(unique_orig, rotation='vertical')
        
            # Displaying the plot in Streamlit
            st.pyplot(fig)
        
        
        elif y_axis == "Total Value (Dutch guilders)":
        
            #filtering textile type
            textile_type_to_plot = textile_type
            filtered_df = df[df['textile_name'] == textile_type]
        
        
            #get unique Origin region
            unique_orig = filtered_df['orig_loc_region_modern'].unique()
        
            #Group and sum quantities
            grouped_df = filtered_df.groupby('orig_loc_region_modern')['total_value'].sum().reset_index()
            grouped_df.sort_values('orig_loc_region_modern', inplace=True)
        
            #Creating bar plot
            fig, ax = plt.subplots()
            ax.bar(grouped_df['orig_loc_region_modern'], grouped_df['total_value'])
            ax.set_xlabel('Origin')
            ax.set_ylabel('Total Value')
            ax.set_title(f'Graph for {textile_type}')
        
            # Setting x-axis tick labels and rotate them
            ax.set_xticklabels(unique_orig, rotation='vertical')
        
            # Displaying the plot in Streamlit
            st.pyplot(fig)
            
# ---- HIDE STREAMLIT STYLE ----
hide_st_style ="""
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown (hide_st_style, unsafe_allow_html=True)
        
        
        
    