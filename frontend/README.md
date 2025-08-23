# Streamlink Frontend

A modern, responsive web application for building your entertainment knowledge graph. Built with Next.js 14, TypeScript, and TailwindCSS.

## 🚀 Features

- **Modern UI/UX**: Clean, responsive design with dark/light theme support
- **Data Ingestion**: Upload Netflix CSV and connect YouTube accounts
- **AI Recommendations**: Personalized content suggestions powered by machine learning
- **Library Management**: Browse and search your entertainment collection
- **Real-time Updates**: Background processing with job status monitoring
- **Error Handling**: Comprehensive error boundaries and user feedback
- **Accessibility**: WCAG compliant with keyboard navigation support

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS + shadcn/ui components
- **Icons**: Lucide React
- **State Management**: React hooks + Context API
- **Form Handling**: React Hook Form + Zod validation
- **HTTP Client**: Fetch API with error handling
- **Testing**: Jest + React Testing Library (planned)

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── dashboard/          # Dashboard page
│   │   ├── ingest/            # Data ingestion page
│   │   ├── library/           # Media library page
│   │   ├── recommendations/   # AI recommendations page
│   │   ├── settings/          # User settings page
│   │   ├── globals.css        # Global styles
│   │   ├── layout.tsx         # Root layout
│   │   └── page.tsx           # Landing page
│   ├── components/            # Reusable UI components
│   │   ├── Navigation.tsx     # Main navigation
│   │   ├── ErrorBoundary.tsx  # Error handling
│   │   ├── Loading.tsx        # Loading states
│   │   ├── Toast.tsx          # Notifications
│   │   └── index.ts           # Component exports
│   └── utils/                 # Utility functions
│       └── errorHandler.ts    # Error handling utilities
├── public/                    # Static assets
├── package.json               # Dependencies and scripts
├── tailwind.config.ts         # TailwindCSS configuration
├── tsconfig.json              # TypeScript configuration
└── Dockerfile                 # Container configuration
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ 
- npm, yarn, or pnpm
- Docker (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd streamlink/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your configuration
   ```

4. **Start development server**
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

5. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

### Environment Variables

Create a `.env.local` file with the following variables:

```env
# Next.js
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Streamlink

# Authentication (if using NextAuth)
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key

# External APIs
NEXT_PUBLIC_TMDB_API_KEY=your-tmdb-api-key
NEXT_PUBLIC_YOUTUBE_API_KEY=your-youtube-api-key
```

## 🏗️ Development

### Available Scripts

```bash
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server

# Code Quality
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript compiler
npm run format       # Format code with Prettier
npm run format:check # Check code formatting

# Testing (planned)
npm run test         # Run tests
npm run test:watch   # Run tests in watch mode
npm run test:coverage # Run tests with coverage
```

### Code Style

- **TypeScript**: Strict mode enabled
- **ESLint**: Airbnb configuration with custom rules
- **Prettier**: Consistent code formatting
- **Husky**: Pre-commit hooks for code quality

### Component Development

Components follow these principles:

- **Composition over inheritance**
- **Props interface definition**
- **Error boundary integration**
- **Accessibility first**
- **Responsive design**
- **TypeScript strict typing**

Example component structure:

```tsx
'use client'

import { useState, useEffect } from 'react'
import { ComponentProps } from './types'
import { useToast } from '@/components/Toast'
import { Loading } from '@/components/Loading'

export default function ExampleComponent({ prop1, prop2 }: ComponentProps) {
  const [loading, setLoading] = useState(true)
  const { success, error } = useToast()

  // Component logic here

  if (loading) {
    return <Loading text="Loading..." />
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      {/* Component content */}
    </div>
  )
}
```

## 🎨 UI Components

### Design System

The application uses a consistent design system built with TailwindCSS:

- **Colors**: Semantic color palette with dark/light variants
- **Typography**: Consistent font hierarchy and spacing
- **Spacing**: 4px grid system (4, 8, 12, 16, 20, 24, 32, 48, 64)
- **Shadows**: Elevation system for depth
- **Borders**: Consistent border radius and colors

### Component Library

- **Navigation**: Responsive sidebar with mobile support
- **Cards**: Flexible content containers
- **Forms**: Accessible form components with validation
- **Buttons**: Primary, secondary, and tertiary variants
- **Loading States**: Skeleton screens and spinners
- **Error States**: User-friendly error messages
- **Toast Notifications**: Non-intrusive feedback system

## 🔧 Configuration

### TailwindCSS

Custom configuration in `tailwind.config.ts`:

```ts
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // Custom color palette
      },
      animation: {
        // Custom animations
      }
    }
  },
  plugins: [require('tailwindcss-animate')]
}
```

### TypeScript

Strict configuration in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true
  }
}
```

## 🧪 Testing

### Testing Strategy

- **Unit Tests**: Component logic and utilities
- **Integration Tests**: API interactions and state management
- **E2E Tests**: Critical user journeys (planned)
- **Accessibility Tests**: Screen reader and keyboard navigation

### Test Setup

```bash
# Install testing dependencies
npm install --save-dev jest @testing-library/react @testing-library/jest-dom

# Run tests
npm run test
```

## 🚀 Deployment

### Production Build

```bash
# Build the application
npm run build

# Start production server
npm run start
```

### Docker Deployment

```bash
# Build Docker image
docker build -t streamlink-frontend .

# Run container
docker run -p 3000:3000 streamlink-frontend
```

### Environment Configuration

Set production environment variables:

```env
NODE_ENV=production
NEXT_PUBLIC_API_BASE_URL=https://api.yourdomain.com
NEXT_PUBLIC_APP_NAME=Streamlink
```

## 📱 Responsive Design

The application is fully responsive with breakpoints:

- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

### Mobile-First Approach

- Touch-friendly interactions
- Optimized navigation for small screens
- Responsive data tables
- Adaptive layouts

## ♿ Accessibility

### WCAG 2.1 AA Compliance

- **Semantic HTML**: Proper heading hierarchy
- **ARIA Labels**: Screen reader support
- **Keyboard Navigation**: Full keyboard accessibility
- **Color Contrast**: Sufficient contrast ratios
- **Focus Management**: Visible focus indicators

### Testing Accessibility

```bash
# Install accessibility testing tools
npm install --save-dev axe-core @axe-core/react

# Run accessibility tests
npm run test:a11y
```

## 🔒 Security

### Best Practices

- **Input Validation**: Client and server-side validation
- **XSS Prevention**: Sanitized user input
- **CSRF Protection**: Token-based protection
- **Content Security Policy**: Restricted resource loading
- **HTTPS Only**: Secure communication

### Security Headers

Configure security headers in `next.config.js`:

```js
const securityHeaders = [
  {
    key: 'X-Frame-Options',
    value: 'DENY'
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  }
]
```

## 📊 Performance

### Optimization Strategies

- **Code Splitting**: Route-based code splitting
- **Image Optimization**: Next.js Image component
- **Bundle Analysis**: Webpack bundle analyzer
- **Lazy Loading**: Component and route lazy loading
- **Caching**: Static generation and ISR

### Performance Monitoring

```bash
# Analyze bundle size
npm run analyze

# Lighthouse CI
npm run lighthouse
```

## 🐛 Troubleshooting

### Common Issues

1. **Build Errors**
   - Clear `.next` folder
   - Reinstall dependencies
   - Check TypeScript errors

2. **Runtime Errors**
   - Check browser console
   - Verify environment variables
   - Check API connectivity

3. **Performance Issues**
   - Analyze bundle size
   - Check image optimization
   - Monitor API response times

### Debug Mode

Enable debug logging:

```env
DEBUG=streamlink:*
NODE_ENV=development
```

## 🤝 Contributing

### Development Workflow

1. **Fork the repository**
2. **Create feature branch**
3. **Make changes**
4. **Add tests**
5. **Update documentation**
6. **Submit pull request**

### Code Review Checklist

- [ ] TypeScript types defined
- [ ] Error handling implemented
- [ ] Accessibility considerations
- [ ] Responsive design tested
- [ ] Tests added/updated
- [ ] Documentation updated

## 📚 Resources

### Documentation

- [Next.js Documentation](https://nextjs.org/docs)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)
- [React Documentation](https://react.dev)

### Tools

- [VS Code Extensions](./docs/vscode-extensions.md)
- [Development Tools](./docs/dev-tools.md)
- [Performance Tools](./docs/performance-tools.md)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/your-org/streamlink/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/streamlink/discussions)
- **Documentation**: [Project Wiki](https://github.com/your-org/streamlink/wiki)
# Docker build test
