import './styles-tailwind.css'
import Card from './shared/components/Card'
import LoadingSpinner from './shared/components/LoadingSpinner'
import { Alert } from './shared/components/Alert'
import { Toast } from './shared/components/Toast'
import ResponsiveGrid from './shared/layout/ResponsiveGrid'
import HomePage from './modules/home/pages/HomePage'

function App() {
  return (
    <div className="App">
      <HomePage />
    </div>
    
  )
} 

export default App
