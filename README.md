# Car Maintenance Tracker

A comprehensive car maintenance tracking application built with Streamlit to help you track vehicle maintenance, fuel consumption, expenses, and service history.

## Features

- 🚗 Vehicle management (multiple vehicles support)
- 🔧 Maintenance tracking and scheduling
- ⛽ Fuel consumption tracking
- 💰 Expense tracking
- 📊 Statistics and reports
- 📅 Service reminders
- 📱 Responsive design

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aiuserchao/car_maintenance.git
   cd car_maintenance
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Project Structure

```
car_maintenance/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── data/                  # Data storage directory
│   ├── vehicles.json      # Vehicle information
│   ├── maintenance.json   # Maintenance records
│   ├── fuel.json          # Fuel records
│   └── expenses.json      # Expense records
├── docs/                  # Documentation
└── src/                   # Source code modules
    ├── database.py        # Data handling
    ├── utils.py           # Utility functions
    └── components.py      # UI components
```

## Usage

1. Launch the application with `streamlit run app.py`
2. Add your vehicle(s) in the Vehicles section
3. Log maintenance activities, fuel fill-ups, and expenses
4. View statistics and reports in the Dashboard
5. Set up service reminders for upcoming maintenance

## Data Storage

All data is stored locally in JSON format in the `data/` directory:
- `vehicles.json`: Vehicle information (make, model, year, VIN, etc.)
- `maintenance.json`: Maintenance records (date, mileage, service type, cost)
- `fuel.json`: Fuel records (date, mileage, gallons, cost, price per gallon)
- `expenses.json`: Other vehicle-related expenses

## Contributing

Feel free to submit issues and pull requests!

## License

MIT License