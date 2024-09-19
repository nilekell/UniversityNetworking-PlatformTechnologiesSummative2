from flask import Flask, request, jsonify, Response
import pandas as pd
import models
import uuid

VEHICLE_CSV = "/Users/nile/Documents/NCH/Coursework/Networks & Platform Technologies/vehicles-api/pythonProject/test-data/vehicle.csv"
CUSTOMER_CSV = "/Users/nile/Documents/NCH/Coursework/Networks & Platform Technologies/vehicles-api/pythonProject/test-data/customer.csv"

# Initialize the Flask app
app = Flask(__name__)

def startup():
    df = pd.read_csv(VEHICLE_CSV)
    if 'index' not in df.columns:
        df = df.rename(columns={'id': 'index'})
        df['index'] = [str(uuid.uuid4()) for _ in range(len(df))]
        df.to_csv(VEHICLE_CSV, index=False)

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
            vehicle_index=vehicle_data['index'],
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
            vehicle_index=vehicle_data['index'],
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
            vehicle_index=vehicle_data['index'],
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
    try:
        data = request.get_json()

        vehicle = models.Vehicle(
            branch=data['branch'],
            category=data['category'],
            colour=data['colour'],
            day_rate=data['dayRate'],
            fuel_economy=data['fuelEconomy'],
            vehicle_index=data['index'],
            make=data['make'],
            model=data['model'],
            number_seats=data['numberSeats'],
            status=data['status'],
            vin=data['vin'],
            vrm=data['vrm'],
            year=data['year']
        )
    except:
        return jsonify({"error": "Failed to serialize vehicle from request"}), 422

    vehicle_dict = vehicle.to_dict()

    # Load the vehicle data from CSV
    df = pd.read_csv(VEHICLE_CSV)

    # Update id of inserted vehicle with new uuid
    vehicle_dict['index'] = str(uuid.uuid4())

    # Append the new vehicle data to the DataFrame
    vehicle_df = pd.DataFrame([vehicle_dict])
    df = pd.concat([df, vehicle_df], ignore_index=False)

    # save dataframe changes back to the csv file
    df.to_csv(VEHICLE_CSV, index=False)

    return jsonify({"message": "Vehicle added successfully", "vehicle": vehicle.to_dict()}), 201

@app.route('/remove', methods=['POST'])
def remove_vehicle():
    data = request.get_json()
    vin = data.get('vin')

    df = pd.read_csv(VEHICLE_CSV)

    if not df[df['vin'] == vin].empty:
        df = df[df['vin'] != vin]
        df.to_csv(VEHICLE_CSV, index=False)
        return jsonify({"message": "Vehicle deleted successfully"}), 201
    else:
        return jsonify({"error": "Vehicle not found"}), 404

@app.route('/all', methods=['GET'])
def show_all_vehicles():
    df = pd.read_csv(VEHICLE_CSV)
    return Response(df.to_json(orient="records"), mimetype='application/json')

@app.route('/rented')
def show_rented_vehicles():
    df = pd.read_csv(VEHICLE_CSV)
    df = df[df.status == 'RENTED']
    df = df.head(n=5)
    return Response(df.to_json(orient="records"), mimetype='application/json')

@app.route('/available')
def show_available_vehicles():
    return jsonify(message="Hello, World!")


# Run the app
if __name__ == '__main__':
    startup()
    app.run(debug=True)