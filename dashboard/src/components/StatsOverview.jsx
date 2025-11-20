import React from 'react'

const StatsOverview = ({ partners }) => {
  // Calculate stats
  const totalFiles = partners.reduce((sum, p) => sum + p.files.length, 0)
  const receivedFiles = partners.reduce((sum, p) =>
    sum + p.files.filter(f => f.status === 'received').length, 0)
  const delayedFiles = partners.reduce((sum, p) =>
    sum + p.files.filter(f => f.status === 'delayed').length, 0)
  const missingFiles = partners.reduce((sum, p) =>
    sum + p.files.filter(f => f.status === 'missing').length, 0)

  const successRate = totalFiles > 0 ? ((receivedFiles / totalFiles) * 100).toFixed(1) : 0

  return (
    <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="text-sm text-gray-500 mb-1">Total Files</div>
        <div className="text-3xl font-bold text-brand-primary">{totalFiles}</div>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="text-sm text-gray-500 mb-1">Received</div>
        <div className="text-3xl font-bold text-green-600">{receivedFiles}</div>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="text-sm text-gray-500 mb-1">Delayed</div>
        <div className="text-3xl font-bold text-yellow-600">{delayedFiles}</div>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="text-sm text-gray-500 mb-1">Missing</div>
        <div className="text-3xl font-bold text-red-600">{missingFiles}</div>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="text-sm text-gray-500 mb-1">Success Rate</div>
        <div className="text-3xl font-bold text-brand-primary">{successRate}%</div>
      </div>
    </div>
  )
}

export default StatsOverview
