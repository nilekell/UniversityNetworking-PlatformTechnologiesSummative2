// Function to make API request and get vehicle details by VIN
async function getVehicle() {
    const vin = document.getElementById('vin').value;

    if (!vin) {
        alert('Please enter a VIN');
        return;
    }

    try {
        const token = localStorage.getItem('jwt-token');
        const response = await fetch(`http://127.0.0.1:5000/vehicle?vin=${vin}`, {
            method: "GET",
            headers: {
                "Content-type": "application/json",
                "Authorization": 'Bearer ' + token
            }
            });

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
        const token = localStorage.getItem('jwt-token');
        const response = await fetch("http://127.0.0.1:5000/rent", {
            method: "POST",
            body: JSON.stringify({
                vin: `${vin}`,
            }),
            headers: {
                "Content-type": "application/json",
                "Authorization": 'Bearer ' + token
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
        const token = localStorage.getItem('jwt-token');
        const response = await fetch("http://127.0.0.1:5000/return", {
            method: "POST",
            body: JSON.stringify({
                vin: `${vin}`,
            }),
            headers: {
                "Content-type": "application/json",
                "Authorization": 'Bearer ' + token
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
        const token = localStorage.getItem('jwt-token');
        const response = await fetch("http://127.0.0.1:5000/vehicle", {
            method: "DELETE",
            body: JSON.stringify({
                vin: `${vin}`,
            }),
            headers: {
                "Content-type": "application/json",
                "Authorization": 'Bearer ' + token
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

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');

    const response = await fetch(`http://127.0.0.1:5000/login`, { 
         method: "POST",
         headers: {
            "Content-Type": "application/json",
        },
         body: JSON.stringify({ username, password }) 
    })

    if(!response.ok) {
        const data = await response.json()
        errorMessage.textContent =  data.error ?? 'Invalid username or password. Please try again.';
        return
    }

    const data = await response.json()

    // Save token in the localStorage
    // Also you should set your user into the store using the setItem function
    localStorage.setItem("jwt-token", data.token);

    console.log('saved token to local storage')

    window.location.href = 'portal.html';
}