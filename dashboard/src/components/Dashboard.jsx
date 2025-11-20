import React, { useState } from 'react'
import PartnerCard from './PartnerCard'
import HistoryChart from './HistoryChart'
import StatsOverview from './StatsOverview'
import SearchFilter from './SearchFilter'

const Dashboard = ({ data }) => {
  const [searchTerm, setSearchTerm] = useState('')
  const [filterPartner, setFilterPartner] = useState('all')
  const [filterStatus, setFilterStatus] = useState('all')

  // Mock data structure (this would come from your API/Google Sheets)
  const partners = data?.partners || [
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

  // Filter partners
  const filteredPartners = partners.filter(partner => {
    const matchesSearch = partner.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         partner.id.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesPartner = filterPartner === 'all' || partner.id === filterPartner

    if (filterStatus === 'all') {
      return matchesSearch && matchesPartner
    }

    return matchesSearch && matchesPartner &&
           partner.files.some(file => file.status === filterStatus)
  })

  return (
    <div className="space-y-6">
      <StatsOverview partners={partners} />

      <SearchFilter
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        filterPartner={filterPartner}
        setFilterPartner={setFilterPartner}
        filterStatus={filterStatus}
        setFilterStatus={setFilterStatus}
        partners={partners}
      />

      <div className="grid gap-6">
        {filteredPartners.map(partner => (
          <PartnerCard key={partner.id} partner={partner} />
        ))}
      </div>

      <HistoryChart />

      <div className="flex gap-4 justify-center">
        <button className="px-6 py-3 bg-white text-brand-primary rounded-lg shadow hover:shadow-lg transition">
          📊 View 24h History
        </button>
        <button className="px-6 py-3 bg-white text-brand-primary rounded-lg shadow hover:shadow-lg transition">
          📥 Download Logs
        </button>
        <button className="px-6 py-3 bg-brand-primary text-white rounded-lg shadow hover:shadow-lg transition">
          🔍 Manual Check
        </button>
      </div>
    </div>
  )
}

export default Dashboard
