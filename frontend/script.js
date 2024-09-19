// Function to make API request and get vehicle details by VIN
async function getVehicle() {
    const vin = document.getElementById('vin').value;

    if (!vin) {
        alert('Please enter a VIN');
        return;
    }

    try {
        // Make a GET request to the Flask API
        const response = await fetch(`http://127.0.0.1:5000/vehicle?vin=${vin}`);
        
        if (response.ok) {
            const data = await response.json();
            // Display the response in the frontend
            document.getElementById('vehicle-details').textContent = JSON.stringify(data, null, 2);
        } else {
            const data = await response.json();
            document.getElementById('vehicle-details').textContent = data.error;
        }
    } catch (error) {
        document.getElementById('vehicle-details').textContent = 'Error: ' + error.message;
    }
}

async function rentVehicle() {
    const vin = document.getElementById('vin').value;

    if (!vin) {
        alert('Please enter a VIN');
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/rent", {
            method: "POST",
            body: JSON.stringify({
                vin: `${vin}`,
            }),
            headers: {
                "Content-type": "application/json"
            }
            });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('vehicle-details').textContent = data.message;
        } else {
            const data = await response.json();
            document.getElementById('vehicle-details').textContent = data.error;
        }
    } catch (error) {
        console.log(`error: ${error}`)
        document.getElementById('vehicle-details').textContent = 'Error: ' + error.message;
    }
}

async function returnVehicle() {
    const vin = document.getElementById('vin').value;

    if (!vin) {
        alert('Please enter a VIN');
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/return", {
            method: "POST",
            body: JSON.stringify({
                vin: `${vin}`,
            }),
            headers: {
                "Content-type": "application/json"
            }
            });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('vehicle-details').textContent = data.message;
        } else {
            const data = await response.json();
            document.getElementById('vehicle-details').textContent = data.error;
        }
    } catch (error) {
        console.log(`error: ${error}`)
        document.getElementById('vehicle-details').textContent = 'Error: ' + error.message;
    }
}

async function deleteVehicle() {
    const vin = document.getElementById('vin').value;

    if (!vin) {
        alert('Please enter a VIN');
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/vehicle", {
            method: "DELETE",
            body: JSON.stringify({
                vin: `${vin}`,
            }),
            headers: {
                "Content-type": "application/json"
            }
            });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('vehicle-details').textContent = data.message;
        } else {
            const data = await response.json();
            document.getElementById('vehicle-details').textContent = data.error;
        }
    } catch (error) {
        console.log(`error: ${error}`)
        document.getElementById('vehicle-details').textContent = 'Error: ' + error.message;
    }
}