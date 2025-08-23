import { Loader2, RefreshCw } from 'lucide-react'

interface LoadingProps {
  size?: 'sm' | 'md' | 'lg' | 'xl'
  text?: string
  variant?: 'spinner' | 'dots' | 'pulse' | 'skeleton'
  className?: string
}

export function Loading({ 
  size = 'md', 
  text = 'Loading...', 
  variant = 'spinner',
  className = '' 
}: LoadingProps) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
    xl: 'w-12 h-12'
  }

  const textSizes = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
    xl: 'text-xl'
  }

  if (variant === 'dots') {
    return (
      <div className={`flex items-center justify-center space-x-1 ${className}`}>
        <div className="flex space-x-1">
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
        </div>
        {text && <span className={`ml-2 text-gray-600 ${textSizes[size]}`}>{text}</span>}
      </div>
    )
  }

  if (variant === 'pulse') {
    return (
      <div className={`flex items-center justify-center ${className}`}>
        <div className={`${sizeClasses[size]} bg-blue-600 rounded-full animate-pulse`}></div>
        {text && <span className={`ml-3 text-gray-600 ${textSizes[size]}`}>{text}</span>}
      </div>
    )
  }

  if (variant === 'skeleton') {
    return (
      <div className={`animate-pulse ${className}`}>
        <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-5/6"></div>
      </div>
    )
  }

  // Default spinner
  return (
    <div className={`flex items-center justify-center ${className}`}>
      <Loader2 className={`${sizeClasses[size]} text-blue-600 animate-spin`} />
      {text && <span className={`ml-3 text-gray-600 ${textSizes[size]}`}>{text}</span>}
    </div>
  )
}

// Full page loading component
export function PageLoading({ text = 'Loading page...' }: { text?: string }) {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600 text-lg">{text}</p>
      </div>
    </div>
  )
}

// Content skeleton loading
export function ContentSkeleton() {
  return (
    <div className="animate-pulse space-y-4">
      <div className="h-8 bg-gray-200 rounded w-1/3"></div>
      <div className="space-y-3">
        <div className="h-4 bg-gray-200 rounded w-full"></div>
        <div className="h-4 bg-gray-200 rounded w-5/6"></div>
        <div className="h-4 bg-gray-200 rounded w-4/6"></div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
        {[1, 2, 3].map((i) => (
          <div key={i} className="bg-white rounded-lg shadow-md p-4">
            <div className="h-32 bg-gray-200 rounded mb-3"></div>
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="h-3 bg-gray-200 rounded w-1/2"></div>
          </div>
        ))}
      </div>
    </div>
  )
}

// Table skeleton loading
export function TableSkeleton({ rows = 5, columns = 4 }: { rows?: number; columns?: number }) {
  return (
    <div className="animate-pulse">
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="grid grid-cols-4 gap-4">
            {Array.from({ length: columns }).map((_, i) => (
              <div key={i} className="h-4 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
        
        {/* Rows */}
        {Array.from({ length: rows }).map((_, rowIndex) => (
          <div key={rowIndex} className="px-6 py-4 border-b border-gray-100 last:border-b-0">
            <div className="grid grid-cols-4 gap-4">
              {Array.from({ length: columns }).map((_, colIndex) => (
                <div key={colIndex} className="h-4 bg-gray-100 rounded"></div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// Card skeleton loading
export function CardSkeleton({ count = 3 }: { count?: number }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="bg-white rounded-lg shadow-md overflow-hidden animate-pulse">
          <div className="h-48 bg-gray-200"></div>
          <div className="p-6">
            <div className="h-6 bg-gray-200 rounded w-3/4 mb-3"></div>
            <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-5/6 mb-4"></div>
            <div className="flex space-x-2">
              <div className="h-6 bg-gray-200 rounded w-16"></div>
              <div className="h-6 bg-gray-200 rounded w-20"></div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

// Inline loading with refresh capability
export function InlineLoading({ 
  text = 'Loading...', 
  onRefresh, 
  showRefresh = false 
}: { 
  text?: string
  onRefresh?: () => void
  showRefresh?: boolean
}) {
  return (
    <div className="flex items-center justify-center py-8">
      <div className="text-center">
        <div className="flex items-center justify-center mb-2">
          <RefreshCw className="w-6 h-6 text-blue-600 animate-spin mr-2" />
          <span className="text-gray-600">{text}</span>
        </div>
        {showRefresh && onRefresh && (
          <button
            onClick={onRefresh}
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            Refresh
          </button>
        )}
      </div>
    </div>
  )
}
