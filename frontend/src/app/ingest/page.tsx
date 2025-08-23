'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Upload, Youtube, FileText, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'

interface UploadStatus {
  status: 'idle' | 'uploading' | 'success' | 'error'
  message: string
  taskId?: string
}

export default function IngestPage() {
  const [netflixFile, setNetflixFile] = useState<File | null>(null)
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>({ status: 'idle', message: '' })
  const [isProcessing, setIsProcessing] = useState(false)

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file && file.name.toLowerCase().endsWith('.csv')) {
      setNetflixFile(file)
      setUploadStatus({ status: 'idle', message: '' })
    } else {
      setUploadStatus({ status: 'error', message: 'Please select a valid CSV file' })
    }
  }

  const handleNetflixUpload = async () => {
    if (!netflixFile) return

    setIsProcessing(true)
    setUploadStatus({ status: 'uploading', message: 'Uploading Netflix CSV...' })

    try {
      const formData = new FormData()
      formData.append('file', netflixFile)
      formData.append('user_id', 'demo-user-id') // In real app, get from auth

      const response = await fetch('/api/ingest/netflix', {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        const result = await response.json()
        setUploadStatus({ 
          status: 'success', 
          message: 'Upload successful! Processing in background...',
          taskId: result.task_id
        })
      } else {
        const error = await response.json()
        setUploadStatus({ status: 'error', message: error.detail || 'Upload failed' })
      }
    } catch (error) {
      setUploadStatus({ status: 'error', message: 'Network error occurred' })
    } finally {
      setIsProcessing(false)
    }
  }

  const handleYouTubeConnect = async () => {
    setIsProcessing(true)
    setUploadStatus({ status: 'uploading', message: 'Connecting to YouTube...' })

    try {
      const response = await fetch('/api/ingest/youtube/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ user_id: 'demo-user-id' })
      })

      if (response.ok) {
        const result = await response.json()
        // In real app, redirect to OAuth URL
        setUploadStatus({ 
          status: 'success', 
          message: 'YouTube connection initiated! Check your email for next steps.' 
        })
      } else {
        const error = await response.json()
        setUploadStatus({ status: 'error', message: error.detail || 'Connection failed' })
      }
    } catch (error) {
      setUploadStatus({ status: 'error', message: 'Network error occurred' })
    } finally {
      setIsProcessing(false)
    }
  }

  const getStatusIcon = () => {
    switch (uploadStatus.status) {
      case 'success':
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-500" />
      case 'uploading':
        return <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />
      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Data Ingestion</h1>
          <p className="text-gray-600">Upload your entertainment data to start building your knowledge graph</p>
        </div>

        {/* Netflix CSV Upload */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="flex items-center mb-4">
            <FileText className="w-6 h-6 text-blue-600 mr-3" />
            <h2 className="text-xl font-semibold">Netflix Viewing History</h2>
          </div>
          
          <div className="mb-4">
            <p className="text-gray-600 mb-4">
              Export your Netflix viewing history as a CSV file and upload it here. 
              We'll process your data and enrich it with metadata from TMDB.
            </p>
            
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <input
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                className="hidden"
                id="netflix-csv"
              />
              <label htmlFor="netflix-csv" className="cursor-pointer">
                <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">
                  {netflixFile ? netflixFile.name : 'Click to select CSV file or drag and drop'}
                </p>
                <p className="text-sm text-gray-500 mt-2">
                  Supports Netflix viewing history CSV exports
                </p>
              </label>
            </div>
          </div>

          <button
            onClick={handleNetflixUpload}
            disabled={!netflixFile || isProcessing}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-2 px-6 rounded-lg transition-colors disabled:cursor-not-allowed"
          >
            {isProcessing ? 'Processing...' : 'Upload and Process'}
          </button>
        </div>

        {/* YouTube Integration */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="flex items-center mb-4">
            <Youtube className="w-6 h-6 text-red-600 mr-3" />
            <h2 className="text-xl font-semibold">YouTube Integration</h2>
          </div>
          
          <div className="mb-4">
            <p className="text-gray-600 mb-4">
              Connect your YouTube account to analyze your viewing patterns and get personalized recommendations.
            </p>
            
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="font-medium text-gray-900 mb-2">What we'll access:</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Your YouTube viewing history</li>
                <li>• Video metadata and statistics</li>
                <li>• Watch time patterns</li>
              </ul>
            </div>
          </div>

          <button
            onClick={handleYouTubeConnect}
            disabled={isProcessing}
            className="bg-red-600 hover:bg-red-700 disabled:bg-gray-400 text-white font-semibold py-2 px-6 rounded-lg transition-colors disabled:cursor-not-allowed"
          >
            {isProcessing ? 'Connecting...' : 'Connect YouTube Account'}
          </button>
        </div>

        {/* Status Display */}
        {uploadStatus.status !== 'idle' && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <div className="flex items-center">
              {getStatusIcon()}
              <div className="ml-3">
                <p className={`font-medium ${
                  uploadStatus.status === 'success' ? 'text-green-800' :
                  uploadStatus.status === 'error' ? 'text-red-800' :
                  'text-blue-800'
                }`}>
                  {uploadStatus.message}
                </p>
                {uploadStatus.taskId && (
                  <p className="text-sm text-gray-600 mt-1">
                    Task ID: {uploadStatus.taskId}
                  </p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Instructions */}
        <div className="bg-blue-50 rounded-lg p-6 mb-8">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">How to get your data:</h3>
          
          <div className="space-y-4">
            <div>
              <h4 className="font-medium text-blue-800 mb-2">Netflix CSV Export:</h4>
              <ol className="text-sm text-blue-700 space-y-1 ml-4">
                <li>1. Go to Netflix Account Settings</li>
                <li>2. Click "Privacy" → "Download your personal information"</li>
                <li>3. Request "Viewing Activity"</li>
                <li>4. Download the CSV file when ready</li>
              </ol>
            </div>
            
            <div>
              <h4 className="font-medium text-blue-800 mb-2">YouTube Data:</h4>
              <p className="text-sm text-blue-700">
                We'll guide you through the OAuth process to securely access your YouTube viewing history.
              </p>
            </div>
          </div>
        </div>

        <div className="text-center">
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
