import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Property Finder - HomeGuard", layout="wide")
st.title("🏠 Property Finder - HomeGuard Portfolio")

# Load Excel file automatically from repo
@st.cache_data
def load_data():
    return pd.read_excel("Property_Database_HomeGuard.xlsx", engine="openpyxl")

try:
    df = load_data()

    # Sidebar filters
    st.sidebar.header("🔽 Filters")

    # Primary filters
    st.sidebar.subheader("Basic Search")
    
    neighborhoods = ["All"] + sorted(df["Neighborhood"].dropna().unique().tolist())
    property_types = ["All"] + sorted(df["Property Type"].dropna().unique().tolist())
    bedrooms = ["All"] + sorted(df["Bedrooms"].dropna().astype(str).unique().tolist())
    bathrooms = ["All"] + sorted(df["Bathrooms"].dropna().astype(str).unique().tolist())
    
    neighborhood_sel = st.sidebar.selectbox("Neighborhood", neighborhoods)
    property_type_sel = st.sidebar.selectbox("Property Type", property_types)
    bedrooms_sel = st.sidebar.selectbox("Bedrooms", bedrooms)
    bathrooms_sel = st.sidebar.selectbox("Bathrooms", bathrooms)
    
    # Price range
    min_rent = int(df["Monthly Rent ($)"].min())
    max_rent = int(df["Monthly Rent ($)"].max())
    price_range = st.sidebar.slider("Monthly Rent ($)", min_rent, max_rent, (min_rent, max_rent))

    # Secondary filters
    st.sidebar.subheader("Additional Filters")
    
    availability_options = ["All"] + sorted(df["Availability Status"].dropna().unique().tolist())
    availability_sel = st.sidebar.selectbox("Availability Status", availability_options)
    
    section8_options = ["All"] + sorted(df["Section 8 Accepted"].dropna().unique().tolist())
    section8_sel = st.sidebar.selectbox("Section 8 Accepted", section8_options)
    
    pets_options = ["All"] + sorted(df["Pets Allowed"].dropna().unique().tolist())
    pets_sel = st.sidebar.selectbox("Pets Allowed", pets_options)

    # Apply filters
    df_filtered = df.copy()

    if neighborhood_sel != "All":
        df_filtered = df_filtered[df_filtered["Neighborhood"] == neighborhood_sel]

    if property_type_sel != "All":
        df_filtered = df_filtered[df_filtered["Property Type"] == property_type_sel]

    if bedrooms_sel != "All":
        df_filtered = df_filtered[df_filtered["Bedrooms"].astype(str) == bedrooms_sel]

    if bathrooms_sel != "All":
        df_filtered = df_filtered[df_filtered["Bathrooms"].astype(str) == bathrooms_sel]

    if availability_sel != "All":
        df_filtered = df_filtered[df_filtered["Availability Status"] == availability_sel]

    if section8_sel != "All":
        df_filtered = df_filtered[df_filtered["Section 8 Accepted"] == section8_sel]

    if pets_sel != "All":
        df_filtered = df_filtered[df_filtered["Pets Allowed"] == pets_sel]

    df_filtered = df_filtered[
        (df_filtered["Monthly Rent ($)"] >= price_range[0]) & 
        (df_filtered["Monthly Rent ($)"] <= price_range[1])
    ]

    # Results header
    st.subheader(f"Results: {len(df_filtered)} properties found")

    # Display properties as cards
    for i, row in df_filtered.iterrows():
        with st.container():
            st.markdown("---")
            
            # Property header with address and status
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### 📍 {row['Full Address']}")
            with col2:
                status = row['Availability Status']
                if status == "Available":
                    st.success(f"🟢 {status}")
                elif status == "Rented":
                    st.error(f"🔴 {status}")
                else:
                    st.warning(f"🟡 {status}")

            # Property details in columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**📋 Property Info**")
                st.markdown(f"""
                - **Neighborhood:** {row['Neighborhood']}
                - **ZIP Code:** {row['ZIP Code']}
                - **Property Type:** {row['Property Type']}
                - **Floor:** {row['Floor']}
                - **Year Built:** {row['Year Built']}
                - **Square Footage:** {row['Square Footage']}
                - **Condition:** {row['Property Condition']}
                """)

            with col2:
                st.markdown("**🛏️ Features**")
                st.markdown(f"""
                - **Bedrooms:** {row['Bedrooms']}
                - **Bathrooms:** {row['Bathrooms']}
                - **Pets Allowed:** {row['Pets Allowed']}
                - **Parking:** {row['Parking Available']} ({row['Parking Type']})
                - **Laundry:** {row['Laundry']}
                - **Utilities Included:** {row['Utilities Included']}
                """)

            with col3:
                st.markdown("**💰 Pricing & Requirements**")
                st.markdown(f"""
                - **Monthly Rent:** ${row['Monthly Rent ($)']:,}
                - **Security Deposit:** ${row['Security Deposit ($)']:,}
                - **Application Fee:** ${row['Application Fee ($)']}
                - **Pet Deposit:** ${row['Pet Deposit ($)']}
                - **Min. Income Required:** ${row['Minimum Income Required ($)']:,}
                - **Min. Credit Score:** {row['Minimum Credit Score']}
                - **Lease Term:** {row['Lease Term (months)']} months
                """)

            # Additional info row
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🏘️ Area Info**")
                st.markdown(f"""
                - **Public Transportation:** {row['Public Transportation']}
                - **Safety Level:** {row['Safety Level']}
                - **Noise Level:** {row['Noise Level']}
                """)

            with col2:
                st.markdown("**📞 Contact & Status**")
                st.markdown(f"""
                - **Section 8 Accepted:** {row['Section 8 Accepted']}
                - **Background Check:** {row['Background Check Required']}
                - **Eviction Policy:** {row['Eviction History Accepted']}
                - **Days on Market:** {row['Days on Market']}
                - **Available Date:** {row['Available Date']}
                """)

            # Special notes and contact
            if row['Special Notes'] and row['Special Notes'] != "None":
                st.info(f"📝 **Special Notes:** {row['Special Notes']}")
            
            st.markdown(f"**🏢 Property Manager:** {row['Property Manager']} | **📱 Contact:** {row['PM Contact']} | **🗓️ Last Updated:** {row['Last Updated']}")

    # Footer
    st.markdown("---")
    st.markdown("*HomeGuard Property Management - Ohio Rentals*")

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Please make sure the file 'Property_Database_HomeGuard.xlsx' is in the same directory as this app.")
