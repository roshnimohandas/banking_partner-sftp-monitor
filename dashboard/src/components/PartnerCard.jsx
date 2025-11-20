import React from 'react'

const PartnerCard = ({ partner }) => {
  const getStatusIcon = (status) => {
    switch (status) {
      case 'received':
        return '✅'
      case 'delayed':
        return '⚠️'
      case 'missing':
        return '❌'
      default:
        return '⏳'
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'received':
        return 'bg-green-100 text-green-800'
      case 'delayed':
        return 'bg-yellow-100 text-yellow-800'
      case 'missing':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusText = (status) => {
    switch (status) {
      case 'received':
        return 'Received'
      case 'delayed':
        return 'Delayed'
      case 'missing':
        return 'Missing'
      default:
        return 'Unknown'
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="border-b pb-4 mb-4">
        <h2 className="text-2xl font-bold text-gray-800">
          {partner.name}
          <span className="ml-2 text-sm font-normal text-gray-500">({partner.id})</span>
        </h2>
      </div>

      <div className="space-y-3">
        {partner.files.map((file, index) => (
          <div
            key={index}
            className="flex items-center justify-between p-4 rounded-lg border-l-4 hover:bg-gray-50 transition"
            style={{
              borderLeftColor: file.status === 'received' ? '#10b981' :
                              file.status === 'delayed' ? '#f59e0b' : '#ef4444'
            }}
          >
            <div className="flex items-center gap-4 flex-1">
              <span className="text-3xl">{getStatusIcon(file.status)}</span>
              <div className="flex-1">
                <div className="font-semibold text-gray-800">{file.name}</div>
                <div className="text-sm text-gray-500">
                  Expected: {file.expectedTime}
                </div>
              </div>
            </div>

            <div className="flex items-center gap-6">
              <div className="text-center">
                <div className="text-xs text-gray-500">Status</div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(file.status)}`}>
                  {getStatusText(file.status)}
                </span>
              </div>

              <div className="text-center">
                <div className="text-xs text-gray-500">Time</div>
                <div className="font-medium text-gray-800">{file.time}</div>
              </div>

              <div className="text-center">
                <div className="text-xs text-gray-500">Size</div>
                <div className="font-medium text-gray-800">{file.size}</div>
              </div>

              <div className="text-center">
                <div className="text-xs text-gray-500">Age</div>
                <div className="font-medium text-gray-800">{file.age}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default PartnerCard
