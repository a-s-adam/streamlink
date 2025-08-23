'use client'

import { useState, useEffect, createContext, useContext, ReactNode } from 'react'
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react'

export type ToastType = 'success' | 'error' | 'warning' | 'info'

export interface Toast {
  id: string
  type: ToastType
  title: string
  message?: string
  duration?: number
  action?: {
    label: string
    onClick: () => void
  }
}

interface ToastContextType {
  toasts: Toast[]
  addToast: (toast: Omit<Toast, 'id'>) => void
  removeToast: (id: string) => void
  clearToasts: () => void
}

const ToastContext = createContext<ToastContextType | undefined>(undefined)

export function useToast() {
  const context = useContext(ToastContext)
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider')
  }
  return context
}

interface ToastProviderProps {
  children: ReactNode
}

export function ToastProvider({ children }: ToastProviderProps) {
  const [toasts, setToasts] = useState<Toast[]>([])

  const addToast = (toast: Omit<Toast, 'id'>) => {
    const id = Math.random().toString(36).substr(2, 9)
    const newToast: Toast = {
      ...toast,
      id,
      duration: toast.duration ?? 5000
    }
    
    setToasts(prev => [...prev, newToast])

    // Auto-remove toast after duration
    if (newToast.duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, newToast.duration)
    }
  }

  const removeToast = (id: string) => {
    setToasts(prev => prev.filter(toast => toast.id !== id))
  }

  const clearToasts = () => {
    setToasts([])
  }

  return (
    <ToastContext.Provider value={{ toasts, addToast, removeToast, clearToasts }}>
      {children}
      <ToastContainer />
    </ToastContext.Provider>
  )
}

function ToastContainer() {
  const { toasts, removeToast } = useToast()

  if (toasts.length === 0) return null

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2 max-w-sm">
      {toasts.map((toast) => (
        <ToastItem key={toast.id} toast={toast} onRemove={removeToast} />
      ))}
    </div>
  )
}

interface ToastItemProps {
  toast: Toast
  onRemove: (id: string) => void
}

function ToastItem({ toast, onRemove }: ToastItemProps) {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    // Trigger entrance animation
    const timer = setTimeout(() => setIsVisible(true), 100)
    return () => clearTimeout(timer)
  }, [])

  const getIcon = () => {
    switch (toast.type) {
      case 'success':
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-500" />
      case 'warning':
        return <AlertTriangle className="w-5 h-5 text-yellow-500" />
      case 'info':
        return <Info className="w-5 h-5 text-blue-500" />
      default:
        return null
    }
  }

  const getToastStyles = () => {
    const baseStyles = 'bg-white rounded-lg shadow-lg border-l-4 p-4 max-w-sm transform transition-all duration-300 ease-in-out'
    
    switch (toast.type) {
      case 'success':
        return `${baseStyles} border-green-500`
      case 'error':
        return `${baseStyles} border-red-500`
      case 'warning':
        return `${baseStyles} border-yellow-500`
      case 'info':
        return `${baseStyles} border-blue-500`
      default:
        return `${baseStyles} border-gray-500`
    }
  }

  const handleRemove = () => {
    setIsVisible(false)
    setTimeout(() => onRemove(toast.id), 300)
  }

  return (
    <div
      className={`${getToastStyles()} ${
        isVisible 
          ? 'translate-x-0 opacity-100' 
          : 'translate-x-full opacity-0'
      }`}
    >
      <div className="flex items-start">
        <div className="flex-shrink-0 mr-3 mt-0.5">
          {getIcon()}
        </div>
        
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">
                {toast.title}
              </p>
              {toast.message && (
                <p className="mt-1 text-sm text-gray-600">
                  {toast.message}
                </p>
              )}
              {toast.action && (
                <button
                  onClick={toast.action.onClick}
                  className="mt-2 text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors"
                >
                  {toast.action.label}
                </button>
              )}
            </div>
            
            <button
              onClick={handleRemove}
              className="ml-4 flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

// Convenience functions for common toast types
export function useToastHelpers() {
  const { addToast } = useToast()

  const success = (title: string, message?: string, options?: Partial<Toast>) => {
    addToast({ type: 'success', title, message, ...options })
  }

  const error = (title: string, message?: string, options?: Partial<Toast>) => {
    addToast({ type: 'error', title, message, ...options })
  }

  const warning = (title: string, message?: string, options?: Partial<Toast>) => {
    addToast({ type: 'warning', title, message, ...options })
  }

  const info = (title: string, message?: string, options?: Partial<Toast>) => {
    addToast({ type: 'info', title, message, ...options })
  }

  return { success, error, warning, info }
}

// Standalone toast component for use outside of context
export function StandaloneToast({ toast, onRemove }: { toast: Toast; onRemove: () => void }) {
  return (
    <div className="fixed top-4 right-4 z-50">
      <ToastItem toast={toast} onRemove={() => onRemove()} />
    </div>
  )
}
