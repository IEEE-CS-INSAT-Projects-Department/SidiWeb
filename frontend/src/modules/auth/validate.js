export function isValidEmail(email) {
	return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())
}

export function isValidPassword(password) {
	if (password.length < 8) return 'Password must be at least 8 characters'
	if (!/[A-Z]/.test(password)) return 'Password must contain at least one uppercase letter'
	if (!/[0-9]/.test(password)) return 'Password must contain at least one number'
	return null
}

export function validateLogin(email, password) {
	const errors = {}
	if (!email) errors.email = 'Email is required'
	else if (!isValidEmail(email)) errors.email = 'Enter a valid email address'
	if (!password) errors.password = 'Password is required'
	return errors
}

export function validateSignup(email, password, confirmPassword) {
	const errors = {}
	if (!email) errors.email = 'Email is required'
	else if (!isValidEmail(email)) errors.email = 'Enter a valid email address'
	if (!password) {
		errors.password = 'Password is required'
	} else {
		const pwErr = isValidPassword(password)
		if (pwErr) errors.password = pwErr
	}
	if (!confirmPassword) errors.confirmPassword = 'Please confirm your password'
	else if (password !== confirmPassword) errors.confirmPassword = 'Passwords do not match'
	return errors
}
