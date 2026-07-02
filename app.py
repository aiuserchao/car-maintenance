import streamlit as st
import json
import os
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Initialize data files
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

VEHICLES_FILE = os.path.join(DATA_DIR, "vehicles.json")
MAINTENANCE_FILE = os.path.join(DATA_DIR, "maintenance.json")
FUEL_FILE = os.path.join(DATA_DIR, "fuel.json")
EXPENSES_FILE = os.path.join(DATA_DIR, "expenses.json")

def load_data(filename):
    """Load data from JSON file"""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def save_data(data, filename):
    """Save data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, default=str)

# Initialize data
vehicles = load_data(VEHICLES_FILE)
maintenance_records = load_data(MAINTENANCE_FILE)
fuel_records = load_data(FUEL_FILE)
expenses = load_data(EXPENSES_FILE)

def save_all():
    """Save all data files"""
    save_data(vehicles, VEHICLES_FILE)
    save_data(maintenance_records, MAINTENANCE_FILE)
    save_data(fuel_records, FUEL_FILE)
    save_data(expenses, EXPENSES_FILE)

# Page configuration
st.set_page_config(
    page_title="Car Maintenance Tracker",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🚗 Car Maintenance Tracker</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page",
    ["Dashboard", "Vehicles", "Maintenance", "Fuel", "Expenses", "Reports"]
)

# Dashboard Page
if page == "Dashboard":
    st.header("📊 Dashboard")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Vehicles", len(vehicles))
    
    with col2:
        total_maintenance = sum_maintenance_cost = sum(record.get('cost', 0) for record in maintenance_records)
        st.metric("Total Maintenance Cost", f"${_maintenance_cost:.2f}")
    
    with col3:
        total_fuel_cost = sum(record.get('cost', 0) for record in fuel_records)
        st.metric("Total Fuel Cost", f"${total_fuel_cost:.2f}")
    
    with col4:
        total_expenses = sum(expense.get('amount', 0) for expense in expenses)
        st.metric("Total Other Expenses", f"${total_expenses:.2f}")
    
    # Recent activity
    st.subheader("Recent Activity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Recent Maintenance**")
        recent_maintenance = sorted(maintenance_records, key=lambda x: x.get('date', ''), reverse=True)[:5]
        if recent_maintenance:
            for record in recent_maintenance:
                st.write(f"• {record.get('date', 'N/A')} - {record.get('description', 'N/A')} (${record.get('cost', 0):.2f})")
        else:
            st.write("No maintenance records yet")
    
    with col2:
        st.write("**Recent Fuel Fill-ups**")
        recent_fuel = sorted(fuel_records, key=lambda x: x.get('date', ''), reverse=True)[:5]
        if recent_fuel:
            for record in recent_fuel:
                st.write(f"• {record.get('date', 'N/A')} - {record.get('gallons', 0):.1f} gal @ ${record.get('price_per_gallon', 0):.2f}/gal")
        else:
            st.write("No fuel records yet")

# Vehicles Page
elif page == "Vehicles":
    st.header("🚙 Vehicle Management")
    
    tab1, tab2 = st.tabs(["View Vehicles", "Add Vehicle"])
    
    with tab1:
        if vehicles:
            df = pd.DataFrame(vehicles)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No vehicles added yet. Use the 'Add Vehicle' tab to add your first vehicle.")
    
    with tab2:
        st.subheader("Add New Vehicle")
        with st.form("vehicle_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                make = st.text_input("Make (e.g., Toyota, Honda)")
                model = st.text_input("Model (e.g., Camry, Civic)")
                year = st.number_input("Year", min_value=1900, max_value=datetime.now().year + 1, value=datetime.now().year)
                vin = st.text_input("VIN (Vehicle Identification Number)")
            
            with col2:
                license_plate = st.text_input("License Plate")
                color = st.text_input("Color")
                current_mileage = st.number_input("Current Mileage", min_value=0, value=0)
                purchase_date = st.date_input("Purchase Date", value=datetime.now())
            
            submitted = st.form_submit_button("Add Vehicle")
            
            if submitted:
                new_vehicle = {
                    "id": len(vehicles) + 1,
                    "make": make,
                    "model": model,
                    "year": year,
                    "vin": vin,
                    "license_plate": license_plate,
                    "color": color,
                    "current_mileage": current_mileage,
                    "purchase_date": purchase_date.isoformat(),
                    "created_at": datetime.now().isoformat()
                }
                
                vehicles.append(new_vehicle)
                save_all()
                st.success(f"Vehicle {make} {model} added successfully!")
                st.rerun()

# Maintenance Page
elif page == "Maintenance":
    st.header("🔧 Maintenance Records")
    
    tab1, tab2 = st.tabs(["View Maintenance", "Add Maintenance"])
    
    with tab1:
        if maintenance_records:
            df = pd.DataFrame(maintenance_records)
            # Format date for display
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No maintenance records yet. Use the 'Add Maintenance' tab to add your first record.")
    
    with tab2:
        st.subheader("Add Maintenance Record")
        
        if not vehicles:
            st.warning("Please add a vehicle first before adding maintenance records.")
        else:
            vehicle_options = {f"{v['make']} {v['model']} ({v['year']})": v['id'] for v in vehicles}
            
            with st.form("maintenance_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    selected_vehicle = st.selectbox("Select Vehicle", options=list(vehicle_options.keys()))
                    vehicle_id = vehicle_options = selected_vehicle
                    date = st.date_input("Service Date", value=datetime.now())
                    mileage = st.number_input("Mileage at Service", min_value=0, value=0)
                    service_type = st.selectbox("Service Type", [
                        "Oil Change", "Tire Rotation", "Brake Service", "Fluid Check",
                        "Engine Tune-up", "Transmission Service", "Battery Replacement",
                        "Other"
                    ])
                    description = st.text_area("Description")
                
                with col2:
                    cost = st.number_input("Cost ($)", min_value=0.0, step=0.01, format="%.2f")
                    service_provider = st.text_input("Service Provider (e.g., Dealership, Mechanic)")
                    parts_replaced = st.text_input("Parts Replaced (if any)")
                    next_service_mileage = st.number_input("Next Service Mileage (optional)", min_value=0, value=0)
                    next_service_date = st.date_input("Next Service Date (optional)", value=None)
                
                submitted = st.form_submit_button("Add Maintenance Record")
                
                if submitted:
                    new_record = {
                        "id": len(maintenance_records) + 1,
                        "vehicle_id": vehicle_id,
                        "date": date.isoformat(),
                        "mileage": mileage,
                        "service_type": service_type,
                        "description": description,
                        "cost": cost,
                        "service_provider": service_provider,
                        "parts_replaced": parts_replaced,
                        "next_service_mileage": next_service_mileage if next_service_mileage > 0 else None,
                        "next_service_date": next_service_date.isoformat() if next_service_date else None,
                        "created_at": datetime.now().isoformat()
                    }
                    
                    maintenance_records.append(new_record)
                    save_all()
                    st.success("Maintenance record added successfully!")
                    st.rerun()

# Fuel Tracking"
    ]
)
```

Let me continue with the rest of the application<tool_call>
<function=write>
<parameter=content>
# Fuel Page
elif page == "Fuel":
    st.header("⛽ Fuel Tracking")
    
    tab1, tab2 = st.tabs(["View Fuel Records", "Add Fuel Record"])
    
    with tab1:
        if fuel_records:
            df = pd.DataFrame(fuel_records)
            # Format date for display
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No fuel records yet. Use the 'Add Fuel Record' tab to add your first record.")
    
    with tab2:
        st.subheader("Add Fuel Record")
        
        if not vehicles:
            st.warning("Please add a vehicle first before adding fuel records.")
        else:
            vehicle_options = {f"{v['make']} {v['model']} ({v['year']})": v['id'] for v in vehicles}
            
            with st.form("fuel_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    selected_vehicle = st.selectbox("Select Vehicle", options=list(vehicle_options.keys()))
                    vehicle_id = vehicle_options[selected_vehicle]
                    date = st.date_input("Date", value=datetime.now())
                    mileage = st.number_input("Mileage", min_value=0, value=0)
                    gallons = st.number_input("Gallons Liters", min_value=0.0, step=0.1, value=0.0)
                
                with col2:
                    cost = st.number_input("Total Cost ($)", min_value=0.0, step=0.01, format="%.2f")
                    price_per_gallon = st.number_input("Price per Gallon ($)", min_value=0.0, step=0.01, format="%.2f")
                    fuel_type = st.selectbox("Fuel Type", ["Regular", "Mid-grade", "Premium", "Diesel", "Electric"])
                    station_name = st.text_input("Gas Station Name")
                
                submitted = st.form_submit_button("Add Fuel Record")
                
                if submitted:
                    # Calculate price per gallon if not provided
                    if price_per_gallon == 0.0 and gallons > 0 and cost > 0:
                        price_per_gallon = cost / gallons
                    elif price_per_gallon > 0.0 and gallons == 0 and cost > 0:
                        gallons = cost / price_per_gallon
                    elif price_per_gallon > 0.0 and gallons > 0 and cost == 0.0:
                        cost = price_per_gallon * gallons
                    
                    new_record = {
                        "id": len(fuel_records) + 1,
                        "vehicle_id": vehicle_id,
                        "date": date.isoformat(),
                        "mileage": mileage,
                        "gallons": gallons,
                        "cost": cost,
                        "price_per_gallon": price_per_gallon,
                        "fuel_type": fuel_type,
                        "station_name": station_name,
                        "created_at": datetime.now().isoformat()
                    }
                    
                    fuel_records.append(new_record)
                    save_all()
                    st.success("Fuel record added successfully!")
                    st.rerun()

# Expenses Page
elif page == "Expenses":
    st.header("💰 Expense Tracking")
    
    tab1, tab2 = st.tabs(["View Expenses", "Add Expense"])
    
    with tab1:
        if expenses:
            df = pd.DataFrame(expenses)
            # Format date for display
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No expense records yet. Use the 'Add Expense' tab to add your first expense.")
    
    with tab2:
        st.subheader("Add Expense")
        
        if not vehicles:
            st.warning("Please add a vehicle first before adding expenses.")
        else:
            vehicle_options = {f"{v['make']} {v['model']} ({v['year']})": v['id'] for v in vehicles}
            
            with st.form("expense_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    selected_vehicle = st.selectbox("Select Vehicle", options=list(vehicle_options.keys()))
                    vehicle_id = vehicle_options[selected_vehicle]
                    date = st.date_input("Date", value=datetime.now())
                    expense_type = st.selectbox("Expense Type", [
                        "Insurance", "Registration", "Parking", "Tolls", "Car Wash",
                        "Accessories", "Repairs (non-maintenance)", "Other"
                    ])
                    description = st.text_area("Description")
                
                with col2:
                    amount = st.number_input("Amount ($)", min_value=0.0, step=0.01, format="%.2f")
                    payment_method = st.selectbox("Payment Method", [
                        "Credit Card", "Debit Card", "Cash", "Check", "Other"
                    ])
                    receipt_number = st.text_input("Receipt Number (optional)")
                    warranty_info = st.text_input("Warranty Info (if applicable)")
                
                submitted = st.form_submit_button("Add Expense")
                
                if submitted:
                    new_expense = {
                        "id": len(expenses) + 1,
                        "vehicle_id": vehicle_id,
                        "date": date.isoformat(),
                        "expense_type": expense_type,
                        "description": description,
                        "amount": amount,
                        "payment_method": payment_method,
                        "receipt_number": receipt_number,
                        "warranty_info": warranty_info,
                        "created_at": datetime.now().isoformat()
                    }
                    
                    expenses.append(new_expense)
                    save_all()
                    st.success("Expense added successfully!")
                    st.rerun()

# Reports Page
elif page == "Reports":
    st.header("📈 Reports & Analytics")
    
    if not vehicles:
        st.warning("Please add a vehicle first to see reports.")
    else:
        vehicle_options = {f"{v['make']} {v['model']} ({v['year']})": v['id'] for v in vehicles}
        selected_vehicle_label = st.selectbox("Select Vehicle for Reports", options=list(vehicle_options.keys()))
        selected_vehicle_id = vehicle_options[selected_vehicle_label]
        
        # Filter data for selected vehicle
        vehicle_maintenance = [r for r in maintenance_records if r.get('vehicle_id') == selected_vehicle_id]
        vehicle_fuel = [r for r in fuel_records if r.get('vehicle_id') == selected_vehicle_id]
        vehicle_expenses = [e for e in expenses if e.get('vehicle_id') == selected_vehicle_id]
        
        tab1, tab2, tab3 = st.tabs(["Maintenance Analysis", "Fuel Efficiency", "Expense Summary"])
        
        with tab1:
            st.subheader("Maintenance Analysis")
            
            if vehicle_maintenance:
                # Maintenance cost over time
                df_maint = pd.DataFrame(vehicle_maintenance)
                df_maint['date'] = pd.to_datetime(df_maint['date'])
                df_maint = df_maint.sort_values('date')
                
                fig = px.line(df_maint, x='date', y='cost', title='Maintenance Cost Over Time',
                             labels={'date': 'Date', 'cost': 'Cost ($)'})
                fig.update_layout(xaxis_title="Date", yaxis_title="Cost ($)")
                st.plotly_chart(fig, use_container_width=True)
                
                # Service type distribution
                service_counts = df_maint['service_type'].value_counts()
                fig_pie = px.pie(values=service_counts.values, names=service_counts.index,
                                title='Maintenance Service Types')
                st.plotly_chart(fig_pie, use_container_width=True)
                
                # Statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Maintenance Cost", f"${df_maint['cost'].sum():.2f}")
                with col2:
                    st.metric("Average Service Cost", f"${df_maint['cost'].mean():.2f}")
                with col3:
                    st.metric("Number of Services", len(df_maint))
            else:
                st.info("No maintenance records for this vehicle yet.")
        
        with tab2:
            st.subheader("Fuel Efficiency Analysis")
            
            if vehicle_fuel:
                df_fuel = pd.DataFrame(vehicle_fuel)
                df_fuel['date'] = pd.to_datetime(df_fuel['date'])
                df_fuel = df_fuel.sort_values('date')
                
                # Calculate MPG if we have both mileage and gallons
                df_fuel['mpg'] = 0.0
                if len(df_fuel) > 1:
                    for i in range(1, len(df_fuel)):
                        miles_driven = df_fuel.iloc[i]['mileage'] - df_fuel.iloc[i-1]['mileage']
                        gallons_used = df_fuel.iloc[i]['gallons']
                        if gallons_used > 0:
                            df_fuel.iloc[i, df_fuel.columns.get_loc('mpg')] = miles_driven / gallons_used
                
                # MPG over time
                fig_mpg = px.line(df_fuel, x='date', y='mpg', title='Fuel Efficiency (MPG) Over Time',
                                 labels={'date': 'Date', 'mpg': 'Miles Per Gallon'})
                fig_mpg.update_layout(xaxis_title="Date", yaxis_title="MPG")
                st.plotly_chart(fig_mpg, use_container_width=True)
                
                # Fuel cost over time
                fig_cost = px.line(df_fuel, x='date', y='cost', title='Fuel Cost Over Time',
                                  labels={'date': 'Date', 'cost': 'Cost ($)'})
                fig_cost.update_layout(xaxis_title="Date", yaxis_title="Cost ($)")
                st.plotly_chart(fig_cost, use_container_width=True)
                
                # Statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    avg_mpg = df_fuel['mpg'].mean()
                    if not pd.isna(avg_mpg) and avg_mpg > 0:
                        st.metric("Average MPG", f"{avg_mpg:.1f}")
                    else:
                        st.metric("Average MPG", "N/A")
                with col2:
                    st.metric("Total Fuel Cost", f"${df_fuel['cost'].sum():.2f}")
                with col3:
                    st.metric("Total Gallons", f"{df_fuel['gallons'].sum():.1f}")
            else:
                st.info("No fuel records for this vehicle yet.")
        
        with tab3:
            st.subheader("Expense Summary")
            
            if vehicle_expenses:
                df_exp = pd.DataFrame(vehicle_expenses)
                df_exp['date'] = pd.to_datetime(df_exp['date'])
                df_exp = df_exp.sort_values('date')
                
                # Expense type breakdown
                expense_by_type = df_exp.groupby('expense_type')['amount'].sum().reset_index()
                fig_exp = px.pie(expense_by_type, values='amount', names='expense_type',
                                title='Expenses by Type')
                st.plotly_chart(fig_exp, use_container_width=True)
                
                # Expenses over time
                fig_exp_time = px.line(df_exp, x='date', y='amount', title='Expenses Over Time',
                                      labels={'date': 'Date', 'amount': 'Amount ($)'})
                fig_exp_time.update_layout(xaxis_title="Date", yaxis_title="Amount ($)")
                st.plotly_chart(fig_exp_time, use_container_width=True)
                
                # Statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Expenses", f"${df_exp['amount'].sum():.2f}")
                with col2:
                    st.metric("Average Expense", f"${df_exp['amount'].mean():.2f}")
                with col3:
                    st.metric("Number of Expenses", len(df_exp))
            else:
                st.info("No expense records for this vehicle yet.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Car Maintenance Tracker • Built with Streamlit • "
    f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    "</div>",
    unsafe_allow_html=True
)