import React from 'react'
import { formatDistanceToNow } from 'date-fns'

const Header = ({ lastUpdate, onRefresh }) => {
  return (
    <header className="bg-white rounded-lg shadow-lg p-6 mb-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-brand-primary">
            🏦 42Cards SFTP File Monitor
          </h1>
          <p className="text-gray-600 mt-1">
            Real-time banking partner file monitoring dashboard
          </p>
        </div>
        <div className="text-right">
          <div className="text-sm text-gray-500">
            Last Updated: {lastUpdate ? formatDistanceToNow(lastUpdate, { addSuffix: true }) : 'Never'}
          </div>
          <button
            onClick={onRefresh}
            className="mt-2 px-4 py-2 bg-brand-primary text-white rounded-lg hover:bg-opacity-90 transition"
          >
            🔄 Refresh Now
          </button>
        </div>
      </div>
    </header>
  )
}

export default Header
