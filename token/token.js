fetch('http://localhost:8000/api/auth/google/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ token: googleIdToken }),
})
.then(response => response.json())
.then(data => {
    console.log('User Token:', data.token);
})
.catch(error => console.error('Error:', error));
