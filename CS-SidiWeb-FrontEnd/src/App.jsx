import './styles-tailwind.css'
import HomePage from './modules/home/pages/HomePage'
import Dashboard from './modules/home/pages/Dashboard'

function App() {
  const pathname = window.location.pathname

  if (pathname === '/dashboard' || pathname === '/dashboard/templates') {
    return (
      <div className="w-full min-w-0 overflow-x-hidden">
        <Dashboard />
      </div>
    )
  }

  return (
    <div className="w-full min-w-0 overflow-x-hidden">
      <HomePage />
    </div>

  )
}

export default App
