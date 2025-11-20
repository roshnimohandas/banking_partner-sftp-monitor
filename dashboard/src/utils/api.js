import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

// For demo/trial, you can use a static JSON file or Google Sheets public URL
const DEMO_DATA_URL = '/data/monitoring-status.json'

export const fetchMonitoringData = async () => {
  try {
    // Option 1: Fetch from Flask API
    // const response = await axios.get(`${API_BASE_URL}/status`)

    // Option 2: Fetch from static JSON (for GitHub Pages deployment)
    const response = await axios.get(DEMO_DATA_URL)

    // Option 3: Fetch from Google Sheets (requires CORS proxy or published sheet)
    // const SHEET_URL = 'https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/gviz/tq?tqx=out:json'
    // const response = await axios.get(SHEET_URL)

    return response.data
  } catch (error) {
    console.error('Error fetching monitoring data:', error)
    // Return mock data for demo
    return getMockData()
  }
}

const getMockData = () => {
  return {
    lastUpdate: new Date().toISOString(),
    partners: [
      {
        id: 'PARTNER_A',
        name: 'Banking Partner A',
        files: [
          {
            name: 'CIC Report',
            status: 'received',
            time: '14:02',
            size: '2.1 MB',
            age: '2h',
            expectedTime: '14:00'
          },
          {
            name: 'Account Master',
            status: 'received',
            time: '09:15',
            size: '1.8 MB',
            age: '7h',
            expectedTime: '09:00'
          },
          {
            name: 'Transaction Master',
            status: 'delayed',
            time: '-',
            size: '-',
            age: '-',
            expectedTime: '10:00'
          }
        ]
      },
      {
        id: 'PARTNER_B',
        name: 'Banking Partner B',
        files: [
          {
            name: 'CIC Report',
            status: 'received',
            time: '15:30',
            size: '3.2 MB',
            age: '1h',
            expectedTime: '15:00'
          },
          {
            name: 'Account Master',
            status: 'missing',
            time: '-',
            size: '-',
            age: '-',
            expectedTime: '16:00'
          },
          {
            name: 'Transaction Master',
            status: 'received',
            time: '11:45',
            size: '2.5 MB',
            age: '5h',
            expectedTime: '11:00'
          }
        ]
      }
    ]
  }
}
