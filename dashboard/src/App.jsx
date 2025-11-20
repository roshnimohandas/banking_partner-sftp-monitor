import React, { useState, useEffect } from 'react'
import Dashboard from './components/Dashboard'
import Header from './components/Header'
import { fetchMonitoringData } from './utils/api'

function App() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [lastUpdate, setLastUpdate] = useState(null)
  const [error, setError] = useState(null)

  const loadData = async () => {
    try {
      setLoading(true)
      const result = await fetchMonitoringData()
      setData(result)
      setLastUpdate(new Date())
      setError(null)
    } catch (err) {
      console.error('Error loading data:', err)
      setError('Failed to load monitoring data')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    // Initial load
    loadData()

    // Auto-refresh every 30 seconds
    const interval = setInterval(loadData, 30000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen p-4">
      <div className="max-w-7xl mx-auto">
        <Header lastUpdate={lastUpdate} onRefresh={loadData} />

        {loading && !data && (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
          </div>
        )}

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mt-4">
            {error}
          </div>
        )}

        {data && <Dashboard data={data} />}
      </div>
    </div>
  )
}

export default App
