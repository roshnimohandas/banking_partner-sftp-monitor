# Google Sheets Setup Guide

This guide explains how to set up Google Sheets for automated file monitoring data logging.

## Sheet Structure

Create a new Google Sheet with the following sheets:

### Sheet 1: Real-Time Status

| Column | Description | Example |
|--------|-------------|---------|
| Partner | Banking partner code | CUB |
| File | File/Report type | CIC Report |
| Status | Current status | ✅ Received |
| Time | Actual received time | 14:02 |
| Size | File size | 2.1MB |
| Age | Time since file received | 2h |
| Expected Time | When file was expected | 14:00 |
| Last Updated | Last check timestamp | 2024-11-20 16:30:00 |

**Example Data:**

```
Partner | File        | Status       | Time  | Size  | Age | Expected | Last Updated
--------|-------------|--------------|-------|-------|-----|----------|---------------
CUB     | CIC         | ✅ Received  | 14:02 | 2.1MB | 2h  | 14:00    | 2024-11-20 16:30
CUB     | AccMstr     | ✅ Received  | 09:15 | 1.8MB | 7h  | 09:00    | 2024-11-20 16:30
SSFB    | CIC         | ⚠️ Delayed   | 15:45 | 3.2MB | 1h  | 15:00    | 2024-11-20 16:30
SSFB    | AccMstr     | ❌ Missing   | -     | -     | -   | 16:00    | 2024-11-20 16:30
```

### Sheet 2: Historical Log

| Column | Description |
|--------|-------------|
| Timestamp | When the check occurred |
| Date | Date of the file |
| Partner | Banking partner |
| Report Type | Type of report |
| Expected Time | Expected delivery time |
| Actual Time | Actual delivery time |
| Status | File status |
| Size | File size |
| Validation Result | Validation details |
| Alerts Sent | Number of alerts sent |
| Error Details | Any errors encountered |

### Sheet 3: Daily Summary

| Column | Description |
|--------|-------------|
| Date | Date |
| Partner | Banking partner |
| Total Files Expected | Total expected |
| Files Received | Successfully received |
| Files Delayed | Delayed files |
| Files Missing | Missing files |
| Success Rate % | Success percentage |
| Total Alerts | Alerts sent |

### Sheet 4: Charts & Metrics

Create charts using the data:

1. **Timeline Chart**: File delivery times over 24 hours
2. **Success Rate Pie Chart**: Received vs Delayed vs Missing
3. **Partner Comparison**: Bar chart comparing partners
4. **Trend Line**: Success rate over last 30 days

## Setting Up Google Sheets API

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project: "42cards-sftp-monitor"
3. Enable Google Sheets API
4. Enable Google Drive API (for file access)

### 2. Create Service Account

1. Go to IAM & Admin → Service Accounts
2. Create service account: "n8n-sftp-monitor"
3. Download JSON key file
4. Copy email address (e.g., `n8n-sftp-monitor@project.iam.gserviceaccount.com`)

### 3. Share Google Sheet

1. Create your monitoring Google Sheet
2. Click "Share"
3. Add the service account email
4. Give "Editor" permissions
5. Copy the Sheet ID from URL:
   ```
   https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
   ```

### 4. Configure n8n

1. In n8n, go to Credentials
2. Add "Google Sheets API" credential
3. Upload the service account JSON key
4. Test the connection

## n8n Workflow for Sheets Updates

### Update Real-Time Status Workflow

```javascript
// Node: Update Real-Time Status
const partner = $json.partner;
const reportType = $json.report_type;
const status = $json.status;
const time = $json.actual_time;
const size = $json.size_mb;
const age = calculateAge($json.modified_time);
const expectedTime = $json.expected_time;
const lastUpdated = new Date().toISOString();

return {
  json: {
    Partner: partner,
    File: reportType,
    Status: status,
    Time: time,
    Size: size,
    Age: age,
    'Expected Time': expectedTime,
    'Last Updated': lastUpdated
  }
};
```

### Clear and Update Pattern

To keep the Real-Time Status sheet current:

1. **Clear Old Data**: Use Google Sheets node with "Clear" operation
2. **Write New Data**: Use Google Sheets node with "Append" operation
3. **Run on Schedule**: Every time the monitor runs

## Formulas for Sheets

### Auto-Calculate Age

In the "Age" column (assuming modified time in column H):

```excel
=IF(H2="", "-", TEXT(NOW()-H2, "h""h"" m""m"""))
```

### Status with Conditional Formatting

Apply conditional formatting to Status column:

- **Green**: Contains "Received" or ✅
- **Yellow**: Contains "Delayed" or ⚠️
- **Red**: Contains "Missing" or ❌

### Success Rate Formula

```excel
=COUNTIF(C:C,"✅")/COUNTA(C:C)*100
```

### Daily Summary (Sheet 3)

```excel
// Total Files Expected
=COUNTIFS('Historical Log'!B:B, A2, 'Historical Log'!C:C, B2)

// Files Received
=COUNTIFS('Historical Log'!B:B, A2, 'Historical Log'!C:C, B2, 'Historical Log'!G:G, "✅*")

// Success Rate
=C2/D2*100
```

## Publishing for Dashboard

### Option 1: Publish as JSON (Recommended for React Dashboard)

1. File → Share → Publish to web
2. Select "Entire Document" or specific sheet
3. Choose "Comma-separated values (.csv)"
4. Click "Publish"
5. Use the URL in your React dashboard

**Or use Google Sheets API:**

```javascript
const SHEET_ID = 'your-sheet-id';
const API_KEY = 'your-api-key';
const RANGE = 'Real-Time Status!A:H';

const url = `https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values/${RANGE}?key=${API_KEY}`;

fetch(url)
  .then(response => response.json())
  .then(data => {
    // Process data
  });
```

### Option 2: Apps Script for JSON Endpoint

Create a Google Apps Script:

```javascript
function doGet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Real-Time Status');
  const data = sheet.getDataRange().getValues();

  const headers = data[0];
  const rows = data.slice(1);

  const json = rows.map(row => {
    const obj = {};
    headers.forEach((header, i) => {
      obj[header] = row[i];
    });
    return obj;
  });

  return ContentService
    .createTextOutput(JSON.stringify({ data: json }))
    .setMimeType(ContentService.MimeType.JSON);
}
```

Deploy as web app and use the URL in your dashboard.

## Sample Sheet Template

Copy this Google Sheet template:

**[42Cards SFTP Monitor Template](#)** (Create and share publicly)

## Automation Schedule

1. **Every 15 minutes (Business Hours)**: Update Real-Time Status
2. **Every check**: Append to Historical Log
3. **Daily at midnight**: Generate Daily Summary
4. **Weekly**: Generate weekly report

## Troubleshooting

### Issue: "Insufficient permissions"

- Verify service account has Editor access to sheet
- Check that Sheets API is enabled in Google Cloud

### Issue: "Quota exceeded"

- Google Sheets API has quotas (100 requests per 100 seconds per user)
- Implement caching in n8n workflows
- Use batch operations where possible

### Issue: Data not updating

- Check n8n workflow execution logs
- Verify Sheet ID is correct
- Ensure service account credentials are valid

## Best Practices

1. **Archive Old Data**: Move historical data older than 90 days to archive sheet
2. **Use Named Ranges**: Reference data by named ranges, not cell addresses
3. **Backup Regularly**: Set up automated backups using Google Takeout
4. **Monitor Quota Usage**: Track API usage in Google Cloud Console
5. **Version Control**: Keep track of sheet structure changes

## Example n8n Node Configuration

```json
{
  "parameters": {
    "authentication": "serviceAccount",
    "resource": "sheet",
    "operation": "appendOrUpdate",
    "documentId": {
      "__rl": true,
      "value": "YOUR_SHEET_ID",
      "mode": "id"
    },
    "sheetName": {
      "__rl": true,
      "value": "Real-Time Status",
      "mode": "name"
    },
    "dataMode": "autoMapInputData",
    "options": {
      "dataLocationOnSheet": "append"
    }
  }
}
```
