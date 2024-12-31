window.onload = () => {
    // Hide the results section
    //document.getElementById('dca-results').style.display = '';
    setTimeout(() => {
        document.body.classList.add('loaded');
    }, 2000); // Delay before revealing the content

    document.getElementById('dca-form').addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent the default form submission behavior
            document.getElementById('calculate-dca').click(); // Trigger the button's click event
        }
    });
};

// Wait for the DOM to be fully loaded before adding event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Attach the event listener to the 'Clear' button
    document.getElementById('clear-button').addEventListener('click', function() {
        // Reset the form fields
        document.getElementById('dca-form').reset();

        // Hide the results section
        document.getElementById('dca-results').style.display = 'none';
    });
});


document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('calculate-dca').addEventListener('click', function () {
        // Collect the form data
        // Attach keydown event for the "Enter" key

        document.getElementById('dca-results').style.display = ''
        const formData = new FormData(document.getElementById('dca-form'));
        const data = {
            investment_value: formData.get('investment_value'),
            repeat_purchase: formData.get('repeat_purchase'),
            start_date: formData.get('start_date'),
            end_date: formData.get('end_date')
        };

        // Send AJAX request
        fetch('/', {
            method: 'POST',  // POST method for sending data
            headers: {
                'Content-Type': 'application/json'  // Ensure that the server knows it's JSON
            },
            body: JSON.stringify(data)  // Convert the data to a JSON string
        })
            .then(response => response.json())  // Parse the JSON response
            .then(result => {
                const dcaResultsElement = document.getElementById('dca-results');
                
                // Reset the content and apply the fade class
                dcaResultsElement.className = 'fade';  // Apply the base fade class
                dcaResultsElement.innerHTML = ''; // Clear content initially
                
                if (data.investment_value === 'NULL' || !data.investment_value) {
                    dcaResultsElement.innerHTML = `
                        <h2>Error:</h2>
                        <p>Please provide a valid purchase amount.</p>
                    `;
                } else if (typeof result.current_price === 'undefined') {
                    dcaResultsElement.innerHTML = `
                        <h2>Error:</h2>
                        <p>Free limit of API reached - try again in 30 seconds.</p>
                    `;
                } else {
                    dcaResultsElement.classList.add('result-box')
                    dcaResultsElement.innerHTML = `
                        <h2>DCA Strategy Results:</h2>
                        <p>Total investment: <br>${result.total_investment}</p>
                        <p>Total Bitcoin amount: <br>${result.total_bitcoin}</p>
                        <p>Average cost per Bitcoin: <br>${result.avg_cost}</p>
                        <p>Current Value: <br>${result.current_value}</p>
                        <p>Current profit: <br>${result.profit}$</p>
                        <p>Value on end date: <br>${result.value_on_end_date}$</p>
                        <p>Profit on end date: <br>${result.end_date_profit}$</p>
                        <p>Current BTC price: <br>${result.current_price}</p>
                        <br>
                        <a href="/chart?investment_value=${data.investment_value}&repeat_purchase=${data.repeat_purchase}&start_date=${data.start_date}&end_date=${data.end_date}">View Chart</a>
                    `;
                }
                
                // Add the "show" class to trigger the fade-in effect
                setTimeout(() => {
                    dcaResultsElement.classList.add('show');
                }, 10);  // Delay ensures the transition is applied
            })
            .catch(error => {
                console.error('Error:', error);
                const dcaResultsElement = document.getElementById('dca-results');
                dcaResultsElement.className = 'fade';
                dcaResultsElement.innerHTML = `
                    <h2>Error:</h2>
                    <p>Something went wrong. Please try again later.</p>
                `;
                setTimeout(() => {
                    dcaResultsElement.classList.add('show');
                }, 10);
            });
    });

    document.getElementById('clear-button').addEventListener('click', function () {
        document.getElementById('dca-form').reset();
        document.getElementById('dca-results').style.display = 'none';
    });
});
