console.log("Reading shorestations.js file...");
console.log("Current document ready state:", document.readyState);
console.log(agGrid);


const cellClassRulesStations = {
    // Apply the 'cell-orange' class if the number of days is between 1 and 7
    'cell-orange': params => {
        if (typeof params.value === 'string') {
            // Extract the number of days from the string using a more flexible regex
            const daysMatch = params.value.match(/(\d+)\s*days?/i);
            if (daysMatch) {
                const days = parseInt(daysMatch[1], 10);
                return days >= 1 && days <= 7;
            }
        }
        return false;
    },

    // Apply the 'cell-red' class if the number of days is greater than 7
    'cell-red': params => {
        if (typeof params.value === 'string') {
            const daysMatch = params.value.match(/(\d+)\s*days?/i);
            if (daysMatch) {
                const days = parseInt(daysMatch[1], 10);
                return days > 7;
            }
        }
        return false;
    },

    // Apply the 'cell-green' class if the string doesn't contain 'days'
    'cell-green': params => typeof params.value === 'string' && !/days?/i.test(params.value),

    // Apply the 'cell-grey' class if the string includes "ERDDAP", aka if there is an error 
    'cell-grey': params => typeof params.value === 'string' && params.value.includes('ERDDAP')
};

const gridOptionsStations = {
    columnDefs: [
        {
            field: "stationName",
            headerName: "Station Name",
            // Custom cell renderer to make the station name a hyperlink
            cellRenderer: (params) => {
                // get the URL from the `caloos_link` field
                const url = params.data.caloosLink;
                if (url) {
                    // return the station name as a clickable link
                    return `<a href="${url}" target="_blank">${params.value}</a>`;
                } else {
                    // return the station name without a link if the URL is not available
                    return params.value;
                }
            }
        },
        {
            field: "timeDelta",
            headerName: "Time Since Last Updated",
            // Apply cell class rules (red vs green colors)
            cellClassRules: cellClassRulesStations
        },
        {
            field: "gsheetsStatus",
            headerName: "Comment from Technician"
        }
    ],

    defaultColDef: {
        flex: 1,
        sortable: true,
        filter: true,
    },
    rowData: [] // Initial empty rowData
};

// function to fetch and parse CSV data
function fetchAndParseCSVStations() {
    console.log("Starting to fetch CSV...");

    fetch('https://www.cencoos.org/data/system_state/stations_timedelta.csv')
        .then(response => {
            console.log("Fetch response status:", response.status);
            if (!response.ok) {
                throw new Error(`Network response was not ok. Status: ${response.status}`);
            }
            return response.text();
        })
        .then(csvData => {
            if (!csvData || csvData.trim().length === 0) {
                throw new Error("Fetched CSV data is empty.");
            }
            
            console.log("Raw CSV data preview:", csvData.substring(0, 500)); // Log first 500 chars for debugging
            
            Papa.parse(csvData, {
                header: true,
                skipEmptyLines: true,
                dynamicTyping: true,
                complete: function(results) {
                    console.log(`CSV parsed successfully. Total rows: ${results.data.length}`);

                    if (!results.data || results.data.length === 0) {
                        console.warn("Parsed CSV contains no rows.");
                        return;
                    }

                    if (gridOptionsStations.api) {
                        console.log("Updating AG Grid with new data...");
                        gridOptionsStations.api.setRowData(results.data);
                    } else {
                        console.error("AG Grid API is not available yet. Retrying in 1 second...");
                        setTimeout(() => {
                            if (gridOptionsStations.api) {
                                gridOptionsStations.api.setRowData(results.data);
                            } else {
                                console.error("AG Grid API still not available.");
                            }
                        }, 1000);
                    }
                }
            });
        })
        .catch(error => {
            console.error("Error fetching or parsing CSV data:", error);
        });
}


// Ensure DOM is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM fully loaded!");

    const eDiv = document.querySelector('#myGrid_new');
    if (!eDiv) {
        console.error("Element #myGrid_new not found.");
        return;
    }

    console.log("Initializing AG Grid...");
    new agGrid.Grid(eDiv, gridOptionsStations);
    eDiv.style.height = '300px'; 
    console.log("Calling fetchAndParseCSV()...");
    fetchAndParseCSVStations();
});
