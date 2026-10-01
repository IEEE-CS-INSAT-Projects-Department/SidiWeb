import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import '../../../styles-tailwind.css'
import Card from '../../../shared/components/Card'
import { Input } from '../../../shared/components/Input'
import { Button } from '../../../shared/components/Button'
import { Alert } from '../../../shared/components/Alert'
import { validateSignup } from '../validate'
import { register } from '../services/authService'

function Register() {
	const navigate = useNavigate()
	const [email, setEmail] = useState('')
	const [password, setPassword] = useState('')
	const [confirmPassword, setConfirmPassword] = useState('')
	const [errors, setErrors] = useState({})
	const [submitError, setSubmitError] = useState('')
	const [isLoading, setIsLoading] = useState(false)

	const handleSubmit = async (event) => {
		event.preventDefault()
		setSubmitError('')
		const validationErrors = validateSignup(email, password, confirmPassword)
		setErrors(validationErrors)
		if (Object.keys(validationErrors).length > 0) return

		setIsLoading(true)
		try {
			await register(email, password)
			navigate('/dashboard')
		} catch (err) {
			setSubmitError(err.message || 'Registration failed')
		} finally {
			setIsLoading(false)
		}
	}

	return (
		<main className="flex min-h-screen w-full items-center justify-center bg-vitrine-black1 px-4 py-10">
			<Card variant="auth" title="Create your account" description="Start building sites with SidiWeb">
				<form className="flex flex-col gap-4" onSubmit={handleSubmit} noValidate>
					{submitError ? <Alert theme="dark" status="error" message={submitError} /> : null}

					<Input
						variant="auth"
						type="email"
						id="register-email"
						label="Email"
						placeholder="you@example.com"
						value={email}
						onChange={(e) => setEmail(e.target.value)}
						error={errors.email}
						autoComplete="email"
					/>

					<Input
						variant="auth"
						type="password"
						id="register-password"
						label="Password"
						placeholder="At least 8 characters"
						value={password}
						onChange={(e) => setPassword(e.target.value)}
						error={errors.password}
						autoComplete="new-password"
					/>

					<Input
						variant="auth"
						type="password"
						id="register-confirm"
						label="Confirm password"
						placeholder="Re-enter your password"
						value={confirmPassword}
						onChange={(e) => setConfirmPassword(e.target.value)}
						error={errors.confirmPassword}
						autoComplete="new-password"
					/>

					<Button type="submit" variant="authPrimary" fullWidth isLoading={isLoading}>
						Sign up
					</Button>
				</form>

				<p className="mt-6 text-center text-sm text-dark-grey1">
					Already have an account?{' '}
					<Link to="/login" className="font-semibold text-light-red3 hover:underline">
						Log in
					</Link>
				</p>
			</Card>
		</main>
	)
}

export default Register
