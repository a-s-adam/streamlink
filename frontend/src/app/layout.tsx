import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Navigation from '@/components/Navigation'
import ErrorBoundary from '@/components/ErrorBoundary'
import { ToastProvider } from '@/components/Toast'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Streamlink - Your Entertainment Knowledge Graph',
  description: 'Build your personal entertainment knowledge graph with Netflix and YouTube data, powered by AI recommendations.',
  keywords: 'entertainment, recommendations, netflix, youtube, ai, machine learning',
  authors: [{ name: 'Streamlink Team' }],
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.className} h-full bg-gray-50`}>
        <ErrorBoundary>
          <ToastProvider>
            <div className="min-h-full">
              <Navigation />
              <main className="lg:pl-64">
                {children}
              </main>
            </div>
          </ToastProvider>
        </ErrorBoundary>
      </body>
    </html>
  )
}
