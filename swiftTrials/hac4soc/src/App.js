import React, { useState, useEffect } from 'react';

const App = () => {
    const [output, setOutput] = useState('');

    useEffect(() => {
        // Make a request to the Django server
        fetch('http://localhost:8000/api/run-python-program/')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                // Return the promise from response.json()
                return response.json();
            })
            .then(data => {
              console.log(JSON.stringify(data));
              setOutput(JSON.stringify(data))
              if (data && data.output !== undefined) {
                  console.log(data.output);
                  setOutput(data.output);
              } else {
                  console.error('Invalid data structure:', data);
              }
              
          })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }, []);

    return (
        <div>
            <h1>Python Output:</h1>
            <p>{output}</p>
        </div>
    );
}

export default App;
