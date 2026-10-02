import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import '../../../styles-tailwind.css'
import Card from '../../../shared/components/Card'
import { Input } from '../../../shared/components/Input'
import { Button } from '../../../shared/components/Button'
import { Alert } from '../../../shared/components/Alert'
import logo from '../../../assets/logo.png'
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
		<main className="relative flex min-h-screen w-full flex-col items-center justify-center overflow-hidden bg-vitrine-black1 px-4 py-10 text-vitrine-white1">
			<div className="pointer-events-none absolute inset-0">
				<div className="absolute -top-28 left-1/2 h-80 w-80 -translate-x-1/2 rounded-full bg-dark-red1/25 blur-[120px]" />
				<div className="absolute bottom-0 right-8 h-64 w-64 rounded-full bg-vitrine-red1/20 blur-[120px]" />
			</div>

			<div className="relative z-10 mb-5 flex w-full max-w-[480px] items-center justify-between">
				<Link
					to="/"
					className="inline-flex items-center gap-1.5 text-sm text-vitrine-grey1 transition hover:text-vitrine-white1"
				>
					<span aria-hidden="true">←</span> Back to home
				</Link>
				<Link to="/" className="flex items-center gap-2">
					<img src={logo} alt="SidiWeb" className="h-7 w-auto object-contain" />
					<span className="text-sm font-bold">SidiWeb</span>
				</Link>
			</div>

			<div className="animate-rise relative z-10 w-full max-w-[480px]">
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
			</div>
		</main>
	)
}

export default Register
