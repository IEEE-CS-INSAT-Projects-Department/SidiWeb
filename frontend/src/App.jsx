import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import './styles-tailwind.css'
import HomePage from './modules/home/pages/HomePage'
import Dashboard from './modules/home/pages/Dashboard'
import Login from './modules/auth/pages/Login'
import Register from './modules/auth/pages/Register'
import { isAuthenticated } from './modules/auth/services/authService'

function ProtectedRoute({ children }) {
  return isAuthenticated() ? children : <Navigate to="/login" replace />
}

function App() {
  return (
    <BrowserRouter>
      <div className="w-full min-w-0 overflow-x-hidden">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/dashboard/templates"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
