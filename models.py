class Vehicle:
    def __init__(self, branch, category, colour, day_rate, fuel_economy, vehicle_index, make, model, number_seats, status, vin, vrm, year):
        self.branch = branch
        self.category = category
        self.colour = colour
        self.day_rate = day_rate
        self.fuel_economy = fuel_economy
        self.vehicle_index = vehicle_index
        self.make = make
        self.model = model
        self.number_seats = number_seats
        self.status = status
        self.vin = vin
        self.vrm = vrm
        self.year = year

    # Method to represent the object as a dictionary
    def to_dict(self):
        return {
            "branch": self.branch,
            "category": self.category,
            "colour": self.colour,
            "dayRate": self.day_rate,
            "fuelEconomy": self.fuel_economy,
            "index": self.vehicle_index,
            "make": self.make,
            "model": self.model,
            "numberSeats": self.number_seats,
            "status": self.status,
            "vin": self.vin,
            "vrm": self.vrm,
            "year": self.year
        }

    # Method to represent the object as a string (optional)
    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.status}) - VIN: {self.vin}"
