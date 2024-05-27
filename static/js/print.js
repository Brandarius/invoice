// print.js

// Function to handle print functionality
function handlePrint() {
    document.getElementById('printButton').addEventListener('click', function() {
        window.print();
    });
}

// Call the function to set up the event listener when the DOM is ready
document.addEventListener('DOMContentLoaded', handlePrint);
