export interface AppError {
  code: string
  message: string
  details?: string
  timestamp: Date
  context?: Record<string, any>
}

export class ErrorHandler {
  private static instance: ErrorHandler
  private errorLog: AppError[] = []

  private constructor() {}

  static getInstance(): ErrorHandler {
    if (!ErrorHandler.instance) {
      ErrorHandler.instance = new ErrorHandler()
    }
    return ErrorHandler.instance
  }

  // Handle different types of errors
  handleError(error: unknown, context?: Record<string, any>): AppError {
    let appError: AppError

    if (error instanceof Error) {
      appError = {
        code: this.getErrorCode(error),
        message: error.message,
        details: error.stack,
        timestamp: new Date(),
        context
      }
    } else if (typeof error === 'string') {
      appError = {
        code: 'UNKNOWN_ERROR',
        message: error,
        timestamp: new Date(),
        context
      }
    } else {
      appError = {
        code: 'UNKNOWN_ERROR',
        message: 'An unexpected error occurred',
        timestamp: new Date(),
        context
      }
    }

    // Log the error
    this.logError(appError)

    // In production, you might want to send to an error reporting service
    if (process.env.NODE_ENV === 'production') {
      this.reportError(appError)
    }

    return appError
  }

  // Handle API errors specifically
  handleApiError(response: Response, context?: Record<string, any>): AppError {
    let message = 'API request failed'
    let code = 'API_ERROR'

    try {
      if (response.status === 401) {
        code = 'UNAUTHORIZED'
        message = 'You are not authorized to perform this action'
      } else if (response.status === 403) {
        code = 'FORBIDDEN'
        message = 'Access to this resource is forbidden'
      } else if (response.status === 404) {
        code = 'NOT_FOUND'
        message = 'The requested resource was not found'
      } else if (response.status === 429) {
        code = 'RATE_LIMITED'
        message = 'Too many requests. Please try again later.'
      } else if (response.status >= 500) {
        code = 'SERVER_ERROR'
        message = 'Server error occurred. Please try again later.'
      }
    } catch (e) {
      // If we can't parse the response, use default values
    }

    const appError: AppError = {
      code,
      message,
      details: `HTTP ${response.status}: ${response.statusText}`,
      timestamp: new Date(),
      context: {
        ...context,
        status: response.status,
        statusText: response.statusText,
        url: response.url
      }
    }

    this.logError(appError)
    return appError
  }

  // Handle network errors
  handleNetworkError(error: unknown, context?: Record<string, any>): AppError {
    const appError: AppError = {
      code: 'NETWORK_ERROR',
      message: 'Network error occurred. Please check your connection and try again.',
      details: error instanceof Error ? error.message : String(error),
      timestamp: new Date(),
      context: {
        ...context,
        type: 'network'
      }
    }

    this.logError(appError)
    return appError
  }

  // Handle validation errors
  handleValidationError(errors: Record<string, string[]>, context?: Record<string, any>): AppError {
    const appError: AppError = {
      code: 'VALIDATION_ERROR',
      message: 'Please check your input and try again.',
      details: JSON.stringify(errors),
      timestamp: new Date(),
      context: {
        ...context,
        validationErrors: errors
      }
    }

    this.logError(appError)
    return appError
  }

  // Get user-friendly error messages
  getUserFriendlyMessage(error: AppError): string {
    const messages: Record<string, string> = {
      'UNAUTHORIZED': 'Please log in to continue',
      'FORBIDDEN': 'You don\'t have permission to access this resource',
      'NOT_FOUND': 'The requested item was not found',
      'RATE_LIMITED': 'Too many requests. Please wait a moment and try again.',
      'SERVER_ERROR': 'Something went wrong on our end. Please try again later.',
      'NETWORK_ERROR': 'Connection problem. Please check your internet and try again.',
      'VALIDATION_ERROR': 'Please check your input and try again.',
      'UPLOAD_ERROR': 'Failed to upload file. Please try again.',
      'PROCESSING_ERROR': 'Failed to process your data. Please try again.',
      'RECOMMENDATION_ERROR': 'Unable to generate recommendations. Please try again.'
    }

    return messages[error.code] || error.message || 'An unexpected error occurred'
  }

  // Get error severity for UI display
  getErrorSeverity(error: AppError): 'low' | 'medium' | 'high' | 'critical' {
    const severityMap: Record<string, 'low' | 'medium' | 'high' | 'critical'> = {
      'UNAUTHORIZED': 'medium',
      'FORBIDDEN': 'medium',
      'NOT_FOUND': 'low',
      'RATE_LIMITED': 'medium',
      'SERVER_ERROR': 'high',
      'NETWORK_ERROR': 'medium',
      'VALIDATION_ERROR': 'low',
      'UPLOAD_ERROR': 'medium',
      'PROCESSING_ERROR': 'high',
      'RECOMMENDATION_ERROR': 'medium'
    }

    return severityMap[error.code] || 'medium'
  }

  // Check if error is retryable
  isRetryable(error: AppError): boolean {
    const retryableCodes = ['NETWORK_ERROR', 'SERVER_ERROR', 'RATE_LIMITED']
    return retryableCodes.includes(error.code)
  }

  // Get retry delay in milliseconds
  getRetryDelay(error: AppError, attempt: number): number {
    if (error.code === 'RATE_LIMITED') {
      return Math.min(1000 * Math.pow(2, attempt), 30000) // Exponential backoff, max 30s
    }
    return 1000 * attempt // Linear backoff
  }

  // Log error to console (in development) or error service
  private logError(error: AppError): void {
    this.errorLog.push(error)

    if (process.env.NODE_ENV === 'development') {
      console.error('Application Error:', {
        code: error.code,
        message: error.message,
        details: error.details,
        context: error.context,
        timestamp: error.timestamp
      })
    }

    // Keep only last 100 errors in memory
    if (this.errorLog.length > 100) {
      this.errorLog = this.errorLog.slice(-100)
    }
  }

  // Report error to external service (e.g., Sentry, LogRocket)
  private reportError(error: AppError): void {
    // Implementation would depend on your error reporting service
    // Example with Sentry:
    // Sentry.captureException(new Error(error.message), {
    //   tags: { code: error.code },
    //   extra: { context: error.context }
    // })
  }

  // Get error code from Error instance
  private getErrorCode(error: Error): string {
    if (error.name === 'TypeError') return 'TYPE_ERROR'
    if (error.name === 'ReferenceError') return 'REFERENCE_ERROR'
    if (error.name === 'SyntaxError') return 'SYNTAX_ERROR'
    if (error.name === 'RangeError') return 'RANGE_ERROR'
    return 'GENERAL_ERROR'
  }

  // Get recent errors
  getRecentErrors(limit: number = 10): AppError[] {
    return this.errorLog.slice(-limit).reverse()
  }

  // Clear error log
  clearErrorLog(): void {
    this.errorLog = []
  }

  // Get error statistics
  getErrorStats(): Record<string, number> {
    const stats: Record<string, number> = {}
    this.errorLog.forEach(error => {
      stats[error.code] = (stats[error.code] || 0) + 1
    })
    return stats
  }
}

// Export singleton instance
export const errorHandler = ErrorHandler.getInstance()

// Convenience functions
export const handleError = (error: unknown, context?: Record<string, any>) => 
  errorHandler.handleError(error, context)

export const handleApiError = (response: Response, context?: Record<string, any>) => 
  errorHandler.handleApiError(response, context)

export const handleNetworkError = (error: unknown, context?: Record<string, any>) => 
  errorHandler.handleNetworkError(error, context)

export const handleValidationError = (errors: Record<string, string[]>, context?: Record<string, any>) => 
  errorHandler.handleValidationError(errors, context)

export const getUserFriendlyMessage = (error: AppError) => 
  errorHandler.getUserFriendlyMessage(error)

export const getErrorSeverity = (error: AppError) => 
  errorHandler.getErrorSeverity(error)

export const isRetryable = (error: AppError) => 
  errorHandler.isRetryable(error)

export const getRetryDelay = (error: AppError, attempt: number) => 
  errorHandler.getRetryDelay(error, attempt)
