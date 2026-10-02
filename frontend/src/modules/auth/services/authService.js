const API_BASE_URL = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '')
const AUTH_BASE = API_BASE_URL ? `${API_BASE_URL}/auth` : '/auth'

const TOKEN_KEY = 'authToken'

export function getToken() {
	try {
		return localStorage.getItem(TOKEN_KEY)
	} catch {
		return null
	}
}

export function setToken(token) {
	try {
		if (token) localStorage.setItem(TOKEN_KEY, token)
	} catch {
		/* storage unavailable */
	}
}

export function clearToken() {
	try {
		localStorage.removeItem(TOKEN_KEY)
	} catch {
		/* storage unavailable */
	}
}

export function isAuthenticated() {
	return Boolean(getToken())
}

function extractError(payload, status) {
	if (payload && typeof payload === 'object') {
		if (typeof payload.detail === 'string') return payload.detail
		if (Array.isArray(payload.detail) && payload.detail[0]?.msg) return payload.detail[0].msg
		if (payload.message) return payload.message
	}
	if (status >= 500) return 'The server encountered an error, please try again later'
	return `Request failed (${status})`
}

async function postJson(url, body) {
	let response
	try {
		response = await fetch(url, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(body),
		})
	} catch {
		throw new Error('Cannot reach the server. Check your connection and try again.')
	}

	let payload = null
	if ((response.headers.get('content-type') || '').includes('application/json')) {
		payload = await response.json()
	}

	if (!response.ok) {
		throw new Error(extractError(payload, response.status))
	}
	return payload
}

export async function login(email, password) {
	const data = await postJson(`${AUTH_BASE}/login`, { email, password })
	if (data?.access_token) setToken(data.access_token)
	return data
}

export async function register(email, password) {
	// Backend register returns the user (no token); log in right after for a smooth flow
	await postJson(`${AUTH_BASE}/register`, { email, password })
	return login(email, password)
}

export async function getCurrentUser() {
	const token = getToken()
	if (!token) return null
	const response = await fetch(`${AUTH_BASE}/me`, {
		headers: { Authorization: `Bearer ${token}` },
	})
	if (!response.ok) {
		if (response.status === 401) clearToken()
		return null
	}
	return response.json()
}

export function logout() {
	clearToken()
}

const authService = { login, register, logout, getCurrentUser, getToken, isAuthenticated }
export default authService
