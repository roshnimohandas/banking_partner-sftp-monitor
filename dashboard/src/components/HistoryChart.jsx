import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const HistoryChart = () => {
  // Mock 24-hour history data
  const data = [
    { time: '00:00', received: 4, delayed: 0, missing: 0 },
    { time: '03:00', received: 4, delayed: 0, missing: 0 },
    { time: '06:00', received: 4, delayed: 0, missing: 0 },
    { time: '09:00', received: 5, delayed: 0, missing: 0 },
    { time: '12:00', received: 6, delayed: 1, missing: 0 },
    { time: '15:00', received: 5, delayed: 1, missing: 1 },
    { time: '18:00', received: 6, delayed: 0, missing: 0 },
    { time: '21:00', received: 6, delayed: 0, missing: 0 },
  ]

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">24-Hour File Status History</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="received" stroke="#10b981" strokeWidth={2} name="Received" />
          <Line type="monotone" dataKey="delayed" stroke="#f59e0b" strokeWidth={2} name="Delayed" />
          <Line type="monotone" dataKey="missing" stroke="#ef4444" strokeWidth={2} name="Missing" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default HistoryChart
