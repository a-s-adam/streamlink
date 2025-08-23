'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Search, Filter, Grid, List, Eye, Calendar, Clock, Tag } from 'lucide-react'

interface MediaItem {
  id: string
  title: string
  source: string
  type: string
  year?: number
  overview?: string
  poster_url?: string
  genres?: string[]
  runtime?: number
  created_at: string
}

export default function LibraryPage() {
  const [items, setItems] = useState<MediaItem[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedSource, setSelectedSource] = useState<string>('all')
  const [selectedType, setSelectedType] = useState<string>('all')
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchItems()
  }, [])

  const fetchItems = async () => {
    try {
      setLoading(true)
      const response = await fetch('/api/items')
      if (response.ok) {
        const data = await response.json()
        setItems(data)
      } else {
        setError('Failed to fetch items')
      }
    } catch (error) {
      setError('Network error occurred')
    } finally {
      setLoading(false)
    }
  }

  const filteredItems = items.filter(item => {
    const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (item.overview && item.overview.toLowerCase().includes(searchTerm.toLowerCase()))
    const matchesSource = selectedSource === 'all' || item.source === selectedSource
    const matchesType = selectedType === 'all' || item.type === selectedType
    
    return matchesSearch && matchesSource && matchesType
  })

  const getSourceColor = (source: string) => {
    switch (source) {
      case 'NETFLIX':
        return 'bg-red-100 text-red-800'
      case 'YOUTUBE':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'movie':
        return '🎬'
      case 'tv_show':
        return '📺'
      case 'video':
        return '🎥'
      default:
        return '📄'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your library...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 text-6xl mb-4">⚠️</div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Library</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button 
            onClick={fetchItems}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Your Library</h1>
          <p className="text-gray-600">
            Browse your collected entertainment data and viewing history
          </p>
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Search */}
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Search titles, descriptions..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Source Filter */}
            <div className="flex-shrink-0">
              <select
                value={selectedSource}
                onChange={(e) => setSelectedSource(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All Sources</option>
                <option value="NETFLIX">Netflix</option>
                <option value="YOUTUBE">YouTube</option>
              </select>
            </div>

            {/* Type Filter */}
            <div className="flex-shrink-0">
              <select
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All Types</option>
                <option value="movie">Movies</option>
                <option value="tv_show">TV Shows</option>
                <option value="video">Videos</option>
              </select>
            </div>

            {/* View Mode Toggle */}
            <div className="flex-shrink-0">
              <div className="flex border border-gray-300 rounded-lg">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`px-3 py-2 rounded-l-lg ${
                    viewMode === 'grid' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-white text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  <Grid className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`px-3 py-2 rounded-r-lg ${
                    viewMode === 'list' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-white text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  <List className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Results Count */}
        <div className="mb-6">
          <p className="text-gray-600">
            Showing {filteredItems.length} of {items.length} items
          </p>
        </div>

        {/* Items Display */}
        {filteredItems.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <div className="text-gray-400 text-6xl mb-4">📚</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No items found</h3>
            <p className="text-gray-600 mb-6">
              {searchTerm || selectedSource !== 'all' || selectedType !== 'all'
                ? 'Try adjusting your search or filters'
                : 'Start by uploading some data from the Ingest page'
              }
            </p>
            {!searchTerm && selectedSource === 'all' && selectedType === 'all' && (
              <Link
                href="/ingest"
                className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
              >
                Go to Ingest
              </Link>
            )}
          </div>
        ) : (
          <div className={viewMode === 'grid' ? 'grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6' : 'space-y-4'}>
            {filteredItems.map((item) => (
              <div key={item.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                {/* Poster/Image */}
                <div className="aspect-video bg-gray-200 flex items-center justify-center">
                  {item.poster_url ? (
                    <img 
                      src={item.poster_url} 
                      alt={item.title}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="text-4xl">{getTypeIcon(item.type)}</div>
                  )}
                </div>

                {/* Content */}
                <div className="p-4">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-gray-900 line-clamp-2">{item.title}</h3>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSourceColor(item.source)}`}>
                      {item.source}
                    </span>
                  </div>

                  {item.overview && (
                    <p className="text-gray-600 text-sm mb-3 line-clamp-2">{item.overview}</p>
                  )}

                  {/* Metadata */}
                  <div className="space-y-2 text-sm text-gray-500">
                    {item.year && (
                      <div className="flex items-center">
                        <Calendar className="w-4 h-4 mr-2" />
                        {item.year}
                      </div>
                    )}
                    
                    {item.runtime && (
                      <div className="flex items-center">
                        <Clock className="w-4 h-4 mr-2" />
                        {item.runtime} min
                      </div>
                    )}

                    {item.genres && item.genres.length > 0 && (
                      <div className="flex items-center">
                        <Tag className="w-4 h-4 mr-2" />
                        <span className="line-clamp-1">{item.genres.join(', ')}</span>
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="mt-4 pt-3 border-t border-gray-100">
                    <button className="text-blue-600 hover:text-blue-800 text-sm font-medium flex items-center">
                      <Eye className="w-4 h-4 mr-1" />
                      View Details
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        <div className="mt-8 text-center">
          <Link 
            href="/dashboard"
            className="text-blue-600 hover:text-blue-800 font-medium"
          >
            ← Back to Dashboard
          </Link>
        </div>
      </div>
    </div>
  )
}
