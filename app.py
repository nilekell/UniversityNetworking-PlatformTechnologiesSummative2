from flask import Flask, request, jsonify
import pandas as pd
import models

VEHICLE_CSV = "/Users/nile/Documents/NCH/Coursework/Networks & Platform Technologies/vehicles-api/pythonProject/test-data/vehicle.csv"
CUSTOMER_CSV = "/Users/nile/Documents/NCH/Coursework/Networks & Platform Technologies/vehicles-api/pythonProject/test-data/customer.csv"

# Initialize the Flask app
app = Flask(__name__)

# Define a route for the default URL
@app.route('/')
def hello_world():
    return jsonify(message="Hello, World!")

@app.route('/find', methods=['GET'])
def find_vehicle():
    # vehicle identification number
    vin = request.args.get('vin')
    df = pd.read_csv(VEHICLE_CSV)

    vehicle_df = df[df["vin"] == vin]

    # Convert to dictionary and return the first result (if exists)
    if not vehicle_df.empty:
        vehicle_data = vehicle_df.iloc[0].to_dict()  # Get the first matching row as a dictionary

        vehicle = models.Vehicle(
            branch=vehicle_data['branch'],
            category=vehicle_data['category'],
            colour=vehicle_data['colour'],
            day_rate=vehicle_data['dayRate'],
            fuel_economy=vehicle_data['fuelEconomy'],
            vehicle_id=vehicle_data['id'],
            make=vehicle_data['make'],
            model=vehicle_data['model'],
            number_seats=vehicle_data['numberSeats'],
            status=vehicle_data['status'],
            vin=vehicle_data['vin'],
            vrm=vehicle_data['vrm'],
            year=vehicle_data['year']
        )
        return jsonify(vehicle.to_dict())
    else:
        return jsonify({"error": "Vehicle not found"}), 404

@app.route('/rent', methods=['POST'])
def rent_vehicle():
    # Extract VIN from the JSON body of the POST request
    data = request.get_json()
    vin = data.get('vin')

    # Load the vehicle data from CSV
    df = pd.read_csv(VEHICLE_CSV)

    # Filter the DataFrame for the vehicle by VIN
    vehicle_df = df[df["vin"] == vin]

    if not vehicle_df.empty:
        # Get the index of the vehicle in the DataFrame
        vehicle_index = vehicle_df.index[0]

        # Convert the first row of the filtered DataFrame to a dictionary
        vehicle_data = vehicle_df.iloc[0].to_dict()

        # Create the Vehicle object (assuming you have a Vehicle class)
        vehicle = models.Vehicle(
            branch=vehicle_data['branch'],
            category=vehicle_data['category'],
            colour=vehicle_data['colour'],
            day_rate=vehicle_data['dayRate'],
            fuel_economy=vehicle_data['fuelEconomy'],
            vehicle_id=vehicle_data['id'],
            make=vehicle_data['make'],
            model=vehicle_data['model'],
            number_seats=vehicle_data['numberSeats'],
            status=vehicle_data['status'],
            vin=vehicle_data['vin'],
            vrm=vehicle_data['vrm'],
            year=vehicle_data['year']
        )

        # Check if the vehicle is available for rent
        if vehicle.status == "AVAILABLE":
            # Update the vehicle's status to "RENTED"
            vehicle.status = "RENTED"
            df.at[vehicle_index, 'status'] = "RENTED"
            
            # Save the updated DataFrame back to the CSV file
            df.to_csv(VEHICLE_CSV, index=False)

            # Return the updated vehicle information
            return jsonify(vehicle.to_dict())
        else:
            # Return a 409 Conflict if the vehicle is not available for rent
            return jsonify({"error": "Vehicle not available to rent."}), 409

    else:
        # Return a 404 if the vehicle is not found
        return jsonify({"error": "Vehicle not found"}), 404


@app.route('/return', methods=['POST'])
def return_vehicle():
    # Extract VIN from the JSON body of the POST request
    data = request.get_json()
    vin = data.get('vin')

    # Load the vehicle data from CSV
    df = pd.read_csv(VEHICLE_CSV)

    # Filter the DataFrame for the vehicle by VIN
    vehicle_df = df[df["vin"] == vin]

    if not vehicle_df.empty:
        # Get the index of the vehicle in the DataFrame
        vehicle_index = vehicle_df.index[0]

        # Convert the first row of the filtered DataFrame to a dictionary
        vehicle_data = vehicle_df.iloc[0].to_dict()

        # Create the Vehicle object (assuming you have a Vehicle class)
        vehicle = models.Vehicle(
            branch=vehicle_data['branch'],
            category=vehicle_data['category'],
            colour=vehicle_data['colour'],
            day_rate=vehicle_data['dayRate'],
            fuel_economy=vehicle_data['fuelEconomy'],
            vehicle_id=vehicle_data['id'],
            make=vehicle_data['make'],
            model=vehicle_data['model'],
            number_seats=vehicle_data['numberSeats'],
            status=vehicle_data['status'],
            vin=vehicle_data['vin'],
            vrm=vehicle_data['vrm'],
            year=vehicle_data['year']
        )

        # Check if the vehicle is available for rent
        if vehicle.status == "RENTED":
            # Update the vehicle's status to "RENTED"
            vehicle.status = "AVAILABLE"
            df.at[vehicle_index, 'status'] = "AVAILABLE"
            
            # Save the updated DataFrame back to the CSV file
            df.to_csv(VEHICLE_CSV, index=False)

            # Return the updated vehicle information
            return jsonify(vehicle.to_dict())
        elif vehicle.status == "AVAILABLE":
            return jsonify({"error": "Vehicle is not currently rented."}), 409
        elif vehicle.status == "SERVICEREQ" or vehicle.status == "DAMAGED":
            # Return a 409 Conflict if the vehicle is not available for return
            return jsonify({"error": "Vehicle not available to return."}), 409

    else:
        # Return a 404 if the vehicle is not found
        return jsonify({"error": "Vehicle not found"}), 404

@app.route('/add', methods=['POST'])
def add_vehicle():
    return jsonify(message="Hello, World!")

@app.route('/remove')
def remove_vehicle():
    return jsonify(message="Hello, World!")

@app.route('/show-all')
def show_all_vehicles():
    return jsonify(message="Hello, World!")

@app.route('/show-rented')
def show_rented_vehicles():
    return jsonify(message="Hello, World!")

@app.route('/show-available')
def show_available_vehicles():
    return jsonify(message="Hello, World!")


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
