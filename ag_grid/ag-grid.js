const cellClassRules = {
    // Apply the 'cell-red' class if the string contains the word 'days' (if data is older than 1 day)
    // or apply the 'cell-green' class if the string doesn't contain 'days
    'cell-red': params => typeof params.value === 'string' && params.value.includes('days'),
    'cell-green': (params) => typeof params.value === 'string' && !params.value.includes('days')
};

const gridOptions = {
    // defines the columns to be displayed.
    columnDefs: [
        { field: "stationName", headerName: "Station Name" },
        { 
            field: "timeDelta", 
            headerName: "Time Since Last Updated",
            cellClassRules: cellClassRules // Apply cell class rules (red vs green colors)
        }
        ],
    defaultColDef: {
        flex: 1,
        sortable: true,
        filter: true,
    },
    rowData: []  // initial empty rowData
};

// function to fetch and parse CSV data
function fetchAndParseCSV() {
    fetch('../../../data/ops_aggrid/stations_timedelta.csv') // modify path as needed. This is the path being used on the CeNCOOS webserver
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok. Status: ' + response.status);
            }
            return response.text();
        })
        .then(csvData => {
            // Parse the CSV data using PapaParse (https://www.papaparse.com/)
            Papa.parse(csvData, {
                header: true,  // using the first row as header
                skipEmptyLines: true,
                dynamicTyping: true,  // convert numeric strings to numbers - not really needed in this case since everything is a string but keeping it here for now. 
                complete: function(results) {
                    console.log('Parsed CSV data:', results.data);  // Debugging log
                    gridOptions.api.setRowData(results.data);  // Set the parsed data to the grid, et voila!
                }
            });
        })
        .catch(error => {
            console.error('Error fetching or parsing CSV data:', error);
        });
}

// Initialize the grid when the DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    const eDiv = document.querySelector('#myGrid');
    new agGrid.Grid(eDiv, gridOptions);
    fetchAndParseCSV();  // Call the fetch&parse csv function from above
});
