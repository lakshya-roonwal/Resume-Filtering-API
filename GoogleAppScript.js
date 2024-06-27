// This code will be written in the app script of the google sheet

function main() {
    // Define the target column
    var targetColumn = 'C'; // Change this to the desired target column letter or number
    var startFrom=2; // Change this to desried row from where you want to start the filtering 
    // Note : This sholud be the exact row no. from the google sheet
  
    // Get the active sheet
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // Get the range of column B
    var columnRange = sheet.getRange('B:B');
    
    // Get the values in column B
    var columnValues = columnRange.getValues();
      
    // Filter out empty rows
    columnValues = columnValues.filter(function(row) {
      return row[0] != '';
    });
    
    // Extract values starting from the second row
    columnValues = columnValues.slice(startFrom-1).flat();
  
   
    // Iterate through each link in column 
    columnValues.forEach(function(row, index) {
      console.log(row)
      // Run your function on the link here (replace the placeholder with your actual function)
      var result = has_live_links(getLink(row));
      
      // Set the result in the target column on the same row
      var targetCell = sheet.getRange(index + 1 +startFrom-1, getColumnNumber(targetColumn));
      targetCell.setValue(result);
    });
  
  
  }
  
  
  
  
  
  function has_live_links(id){
    // console.log(id)
    // return true;
    // Getting the File
    var pdfBlob = DriveApp.getFileById(id).getBlob();
  
    // Uploading the file to API
    // Construct the URL of the external API endpoint
    var apiUrl = "https://resume-filtering-api.onrender.com/check_live_links"; 
  
    // Construct the payload
    // Construct the payload
    var payload = {
      file: pdfBlob // Ensure that the field name matches what the API expects
    };
  
    // Configure the options for the API request
    var options = {
      method: "post",
      payload: payload
    };
  
      // Make the API request
    var response = UrlFetchApp.fetch(apiUrl, options);
  
  
    // Make the API request
    var jsonResponse = JSON.parse(response.getContentText());
  
    // Access the "has_live_links" field from the response
    var hasLiveLinks = jsonResponse.has_live_links;
  
    // Log the value of "has_live_links"
    Logger.log("Has Live Links: " + hasLiveLinks);
  
    return hasLiveLinks;
  }
  
  // Define a function to convert column letter to column number
  function getColumnNumber(columnLetter) {
    var base = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    var columnNumber = 0;
    for (var i = 0; i < columnLetter.length; i++) {
      columnNumber += (base.indexOf(columnLetter.charAt(i)) + 1) * Math.pow(26, columnLetter.length - i - 1);
    }
    return columnNumber;
  }
  
  // Function for getting the id of the drive file
  function getLink(URL){
    var parts = URL.split('=');
    return parts[1];
  }