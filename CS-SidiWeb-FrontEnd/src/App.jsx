import './App.css'
import { Button } from './shared/components/Button'
import { Input } from './shared/components/Input'
import Card from './shared/components/Card'

function App() {
  return (
    <div className="flex flex-col items-center justify-center gap-6 min-h-screen">
      <Button variant="submit" dimension="submit" radius="submit">Click me</Button>
      <Input variant="input_auth_large" placeholder="Enter your email"></Input>
      <Card variant="dark_step" title="Step 1: Sign Up" description="Create your account to get started" number="1" icon={<span>🚀</span>} />
      <Card variant="dark_image" title="Beautiful Scenery" description="Experience the beauty of nature with us" imageSrc="https://source.unsplash.com/random/400x300" />
      <Card variant="light_image" title="Light Card" description="This is a light themed card with an image." imageSrc="https://source.unsplash.com/random/400x300?light" />
    </div>
  )
} 

export default App
