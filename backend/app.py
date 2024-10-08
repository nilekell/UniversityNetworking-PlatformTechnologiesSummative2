from flask import Flask, request, jsonify, Response
import pandas as pd
import models
import uuid
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

VEHICLE_CSV = "/Users/nile/Documents/NCH/Coursework/Networks & Platform Technologies/project/backend/test-data/vehicle.csv"
CUSTOMER_CSV = "/Users/nile/Documents/NCH/Coursework/Networks & Platform Technologies/project/backend/backend/test-data/customer.csv"

# Initialize the Flask app
app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "test-secret"

jwt = JWTManager(app)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(token=access_token)

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
# @app.route("/protected", methods=["GET"])
# @jwt_required()
# def protected():
#     # Access the identity of the current user with get_jwt_identity
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200

def startup():
    df = pd.read_csv(VEHICLE_CSV)
    if 'index' not in df.columns:
        df = df.rename(columns={'id': 'index'})
        df['index'] = [str(uuid.uuid4()) for _ in range(len(df))]
        df.to_csv(VEHICLE_CSV, index=False)

# Define a route for the default URL
@app.route('/', methods=['GET'])
def hello_world():
    return jsonify(message="Hello, World!")

@app.route('/vehicle', methods=['GET'])
@jwt_required()
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
        return jsonify({"error": "Vehicle not found."}), 404

@app.route('/rent', methods=['POST'])
@jwt_required()
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
            return jsonify({"message": "Vehicle rented successfully.", "vehicle": vehicle.to_dict()}), 201
        else:
            # Return a 409 Conflict if the vehicle is not available for rent
            return jsonify({"error": "Vehicle not available to rent."}), 409

    else:
        # Return a 404 if the vehicle is not found
        return jsonify({"error": "Vehicle not found"}), 404

@app.route('/return', methods=['POST'])
@jwt_required()
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
            return jsonify({"message": "Vehicle returned successfully.", "vehicle": vehicle.to_dict()}), 201
        elif vehicle.status == "AVAILABLE":
            return jsonify({"error": "Vehicle is not currently rented."}), 409
        elif vehicle.status == "SERVICEREQ" or vehicle.status == "DAMAGED":
            # Return a 409 Conflict if the vehicle is not available for return
            return jsonify({"error": "Vehicle not available to return."}), 409

    else:
        # Return a 404 if the vehicle is not found
        return jsonify({"error": "Vehicle not found"}), 404

@app.route('/vehicle', methods=['POST'])
@jwt_required()
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
        return jsonify({"error": "Failed to serialize vehicle from request."}), 422

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

    return jsonify({"message": "Vehicle added successfully.", "vehicle": vehicle.to_dict()}), 201

@app.route('/vehicle', methods=['DELETE'])
@jwt_required()
def remove_vehicle():
    data = request.get_json()
    vin = data.get('vin')

    df = pd.read_csv(VEHICLE_CSV)

    if not df[df['vin'] == vin].empty:
        df = df[df['vin'] != vin]
        df.to_csv(VEHICLE_CSV, index=False)
        return jsonify({"message": "Vehicle deleted successfully."}), 201
    else:
        return jsonify({"error": "Vehicle not found"}), 404

@app.route('/vehicles', methods=['GET'])
@jwt_required()
def show_all_vehicles():
    status = request.args.get('status')
    df = pd.read_csv(VEHICLE_CSV)
    if status == '':
        pass
    elif status == 'AVAILABLE':
        df = df[df.status == 'AVAILABLE']
    elif status == 'RENTED':
        df = df[df.status == 'RENTED']
    elif status == 'DAMAGED':
        df = df[df.status == 'DAMAGED']
    elif status == 'SERVICEREQ':
        df = df[df.status == 'SERVICEREQ']

    return Response(df.to_json(orient="records"), mimetype='application/json')

# Run the app
if __name__ == '__main__':
    startup()
    app.run(debug=True)