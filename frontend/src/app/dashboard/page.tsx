'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { 
  TrendingUp, 
  Film, 
  Youtube, 
  Target, 
  Upload, 
  Library, 
  Settings,
  ArrowRight,
  Play,
  Clock,
  Star
} from 'lucide-react'
import { useToastHelpers } from '@/components/Toast'
import { Loading } from '@/components/Loading'

interface DashboardStats {
  totalItems: number
  totalEvents: number
  recommendations: number
  recentActivity: number
}

interface RecentActivity {
  id: string
  type: string
  title: string
  timestamp: string
  source: string
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([])
  const [loading, setLoading] = useState(true)
  const { success, error } = useToastHelpers()

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      // Simulate API calls
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      setStats({
        totalItems: 127,
        totalEvents: 342,
        recommendations: 23,
        recentActivity: 8
      })
      
      setRecentActivity([
        {
          id: '1',
          type: 'watch',
          title: 'The Queen\'s Gambit',
          timestamp: '2 hours ago',
          source: 'NETFLIX'
        },
        {
          id: '2',
          type: 'watch',
          title: 'Mindhunter Season 2',
          timestamp: '1 day ago',
          source: 'NETFLIX'
        },
        {
          id: '3',
          type: 'watch',
          title: 'How to Build a Computer',
          timestamp: '2 days ago',
          source: 'YOUTUBE'
        }
      ])
    } catch (err) {
      error('Failed to load dashboard', 'Please try refreshing the page')
    } finally {
      setLoading(false)
    }
  }

  const quickActions = [
    {
      title: 'Upload Netflix Data',
      description: 'Import your viewing history',
      icon: Upload,
      href: '/ingest',
      color: 'bg-blue-500 hover:bg-blue-600'
    },
    {
      title: 'Browse Library',
      description: 'View your collected content',
      icon: Library,
      href: '/library',
      color: 'bg-green-500 hover:bg-green-600'
    },
    {
      title: 'Get Recommendations',
      description: 'Discover new content',
      icon: Target,
      href: '/recommendations',
      color: 'bg-purple-500 hover:bg-purple-600'
    },
    {
      title: 'Settings',
      description: 'Manage your preferences',
      icon: Settings,
      href: '/settings',
      color: 'bg-gray-500 hover:bg-gray-600'
    }
  ]

  if (loading) {
    return <Loading size="xl" text="Loading your dashboard..." />
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Welcome Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome back!</h1>
          <p className="text-gray-600">
            Here's what's happening with your entertainment knowledge graph
          </p>
        </div>

        {/* Stats Overview */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Film className="w-6 h-6 text-blue-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Items</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalItems}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <Play className="w-6 h-6 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Watch Events</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalEvents}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                  <Target className="w-6 h-6 text-purple-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Recommendations</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.recommendations}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                  <Clock className="w-6 h-6 text-orange-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Recent Activity</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.recentActivity}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {quickActions.map((action) => (
              <Link
                key={action.title}
                href={action.href}
                className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow group"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className={`w-12 h-12 ${action.color} rounded-lg flex items-center justify-center mb-3 group-hover:scale-110 transition-transform`}>
                      <action.icon className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-1">{action.title}</h3>
                    <p className="text-sm text-gray-600">{action.description}</p>
                  </div>
                  <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-gray-600 transition-colors" />
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">Recent Activity</h2>
            <Link 
              href="/library" 
              className="text-blue-600 hover:text-blue-800 text-sm font-medium flex items-center"
            >
              View All
              <ArrowRight className="w-4 h-4 ml-1" />
            </Link>
          </div>
          
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            {recentActivity.length === 0 ? (
              <div className="p-8 text-center text-gray-500">
                <Clock className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                <p>No recent activity</p>
                <p className="text-sm">Start watching content to see your activity here</p>
              </div>
            ) : (
              <div className="divide-y divide-gray-200">
                {recentActivity.map((activity) => (
                  <div key={activity.id} className="p-4 hover:bg-gray-50 transition-colors">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                          <Play className="w-4 h-4 text-blue-600" />
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">{activity.title}</p>
                          <div className="flex items-center space-x-2 text-sm text-gray-500">
                            <span>{activity.timestamp}</span>
                            <span>•</span>
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                              activity.source === 'NETFLIX' 
                                ? 'bg-red-100 text-red-800' 
                                : 'bg-red-100 text-red-800'
                            }`}>
                              {activity.source}
                            </span>
                          </div>
                        </div>
                      </div>
                      <Star className="w-4 h-4 text-gray-300 hover:text-yellow-400 cursor-pointer transition-colors" />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Getting Started */}
        <div className="bg-blue-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">Getting Started</h3>
          <div className="grid md:grid-cols-3 gap-4 text-sm text-blue-800">
            <div>
              <h4 className="font-medium mb-2">1. Upload Your Data</h4>
              <p>Start by uploading your Netflix viewing history or connecting your YouTube account.</p>
            </div>
            <div>
              <h4 className="font-medium mb-2">2. Build Your Library</h4>
              <p>We'll automatically enrich your data with metadata, posters, and genres.</p>
            </div>
            <div>
              <h4 className="font-medium mb-2">3. Get Recommendations</h4>
              <p>Discover new content based on your viewing patterns and preferences.</p>
            </div>
          </div>
          <div className="mt-4">
            <Link
              href="/ingest"
              className="inline-flex items-center bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
            >
              Start Building Your Knowledge Graph
              <ArrowRight className="w-4 h-4 ml-2" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
