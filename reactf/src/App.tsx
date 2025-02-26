import { useState, useEffect } from 'react'

function App() {
  const [message, setMessage] = useState('')

  useEffect(() => {
    // Using environment variable would be better in production
    fetch('http://localhost:8000/api/hello')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok')
        }
        return response.json()
      })
      .then(data => setMessage(data.message))
      .catch(error => {
        console.error('Error:', error)
        setMessage('Failed to fetch message from server')
      })
  }, [])

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-4">Chess App Frontend</h1>
        <p className="text-gray-600">
          {message || 'Loading message from backend...'}
        </p>
      </div>
    </div>
  )
}

export default App