'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Target, RefreshCw, Star, TrendingUp, Clock, Heart, Eye, Loader2 } from 'lucide-react'

interface Recommendation {
  id: string
  score: number
  reason: string
  algorithm: string
  created_at: string
  item: {
    id: string
    title: string
    source: string
    type: string
    year?: number
    overview?: string
    poster_url?: string
    genres?: string[]
    runtime?: number
  }
}

export default function RecommendationsPage() {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([])
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [stats, setStats] = useState<any>(null)

  useEffect(() => {
    fetchRecommendations()
    fetchStats()
  }, [])

  const fetchRecommendations = async () => {
    try {
      setLoading(true)
      const response = await fetch('/api/recommendations?user_id=demo-user-id&limit=20')
      if (response.ok) {
        const data = await response.json()
        setRecommendations(data)
      } else {
        setError('Failed to fetch recommendations')
      }
    } catch (error) {
      setError('Network error occurred')
    } finally {
      setLoading(false)
    }
  }

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/recommendations/stats/demo-user-id')
      if (response.ok) {
        const data = await response.json()
        setStats(data)
      }
    } catch (error) {
      console.error('Failed to fetch stats:', error)
    }
  }

  const handleRefresh = async () => {
    try {
      setRefreshing(true)
      const response = await fetch('/api/recommendations/refresh?user_id=demo-user-id', {
        method: 'POST'
      })
      
      if (response.ok) {
        const result = await response.json()
        // In real app, poll for completion
        setTimeout(() => {
          fetchRecommendations()
          fetchStats()
        }, 2000)
      } else {
        setError('Failed to refresh recommendations')
      }
    } catch (error) {
      setError('Network error occurred')
    } finally {
      setRefreshing(false)
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600'
    if (score >= 0.6) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreLabel = (score: number) => {
    if (score >= 0.8) return 'Excellent Match'
    if (score >= 0.6) return 'Good Match'
    return 'Fair Match'
  }

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

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your recommendations...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 text-6xl mb-4">⚠️</div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Recommendations</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button 
            onClick={fetchRecommendations}
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
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Your Recommendations</h1>
              <p className="text-gray-600">
                Personalized content suggestions based on your viewing patterns
              </p>
            </div>
            
            <button
              onClick={handleRefresh}
              disabled={refreshing}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-lg transition-colors disabled:cursor-not-allowed flex items-center"
            >
              {refreshing ? (
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              ) : (
                <RefreshCw className="w-4 h-4 mr-2" />
              )}
              {refreshing ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>
        </div>

        {/* Stats Overview */}
        {stats && (
          <div className="grid md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center">
                <Target className="w-8 h-8 text-blue-600 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Recommendations</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.total_recommendations}</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center">
                <TrendingUp className="w-8 h-8 text-green-600 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600">Recent</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.recent_recommendations}</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center">
                <Star className="w-8 h-8 text-yellow-600 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600">Algorithm</p>
                  <p className="text-2xl font-bold text-gray-900">Content</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center">
                <Clock className="w-8 h-8 text-purple-600 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600">Last Updated</p>
                  <p className="text-lg font-bold text-gray-900">Today</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Recommendations */}
        {recommendations.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <div className="text-gray-400 text-6xl mb-4">🎯</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No recommendations yet</h3>
            <p className="text-gray-600 mb-6">
              Start by uploading some data and we'll generate personalized recommendations for you.
            </p>
            <div className="space-x-4">
              <Link
                href="/ingest"
                className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
              >
                Upload Data
              </Link>
              <button
                onClick={handleRefresh}
                className="bg-gray-600 hover:bg-gray-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
              >
                Generate Recommendations
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {recommendations.map((rec, index) => (
              <div key={rec.id} className="bg-white rounded-lg shadow-md overflow-hidden">
                <div className="p-6">
                  <div className="flex items-start space-x-4">
                    {/* Rank */}
                    <div className="flex-shrink-0">
                      <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                        <span className="text-blue-600 font-bold text-lg">#{index + 1}</span>
                      </div>
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between mb-2">
                        <h3 className="text-xl font-semibold text-gray-900">{rec.item.title}</h3>
                        <div className="flex items-center space-x-2">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSourceColor(rec.item.source)}`}>
                            {rec.item.source}
                          </span>
                          <span className="px-2 py-1 bg-purple-100 text-purple-800 rounded-full text-xs font-medium">
                            {rec.algorithm}
                          </span>
                        </div>
                      </div>

                      {rec.item.overview && (
                        <p className="text-gray-600 mb-3">{rec.item.overview}</p>
                      )}

                      {/* Metadata */}
                      <div className="flex items-center space-x-6 text-sm text-gray-500 mb-3">
                        {rec.item.year && (
                          <span>{rec.item.year}</span>
                        )}
                        {rec.item.runtime && (
                          <span>{rec.item.runtime} min</span>
                        )}
                        {rec.item.genres && rec.item.genres.length > 0 && (
                          <span>{rec.item.genres.join(', ')}</span>
                        )}
                      </div>

                      {/* Reason */}
                      <div className="bg-blue-50 rounded-lg p-3 mb-4">
                        <p className="text-blue-800 text-sm">
                          <strong>Why recommended:</strong> {rec.reason}
                        </p>
                      </div>

                      {/* Score */}
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <span className="text-sm text-gray-600">Match Score:</span>
                          <span className={`font-semibold ${getScoreColor(rec.score)}`}>
                            {Math.round(rec.score * 100)}%
                          </span>
                          <span className="text-xs text-gray-500">
                            ({getScoreLabel(rec.score)})
                          </span>
                        </div>

                        <div className="flex items-center space-x-2">
                          <button className="text-gray-400 hover:text-red-500 transition-colors">
                            <Heart className="w-5 h-5" />
                          </button>
                          <button className="text-gray-400 hover:text-blue-500 transition-colors">
                            <Eye className="w-5 h-5" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* How it works */}
        <div className="mt-12 bg-blue-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">How Recommendations Work</h3>
          <div className="grid md:grid-cols-3 gap-4 text-sm text-blue-800">
            <div>
              <h4 className="font-medium mb-2">1. Data Analysis</h4>
              <p>We analyze your viewing patterns, genres, and preferences from your uploaded data.</p>
            </div>
            <div>
              <h4 className="font-medium mb-2">2. AI Processing</h4>
              <p>Our AI creates embeddings of content to understand similarities and relationships.</p>
            </div>
            <div>
              <h4 className="font-medium mb-2">3. Smart Matching</h4>
              <p>We find content that matches your preferences using advanced algorithms.</p>
            </div>
          </div>
        </div>

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
