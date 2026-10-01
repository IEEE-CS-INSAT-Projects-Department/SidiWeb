import { getToken, clearToken } from '../../modules/auth/services/authService'

const API_BASE_URL = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '')

function buildUrl(path) {
	return `${API_BASE_URL}${path}`
}

function authHeaders(extra = {}) {
	const token = getToken()
	return { ...(token ? { Authorization: `Bearer ${token}` } : {}), ...extra }
}

function messageFrom(payload, status) {
	if (payload && typeof payload === 'object') {
		const d = payload.detail
		if (typeof d === 'string') return d
		if (Array.isArray(d) && d[0]?.msg) return d[0].msg
		if (payload.message) return payload.message
	}
	return `Request failed (${status})`
}

async function handle(response) {
	if (response.status === 401) {
		clearToken()
		if (typeof window !== 'undefined') window.location.assign('/login')
		throw new Error('Session expired. Please log in again.')
	}
	let payload = null
	if ((response.headers.get('content-type') || '').includes('application/json')) {
		payload = await response.json()
	}
	if (!response.ok) throw new Error(messageFrom(payload, response.status))
	return payload
}

export async function apiGet(path) {
	return handle(await fetch(buildUrl(path), { headers: authHeaders() }))
}

export async function apiPost(path, body) {
	return handle(
		await fetch(buildUrl(path), {
			method: 'POST',
			headers: authHeaders({ 'Content-Type': 'application/json' }),
			body: JSON.stringify(body),
		})
	)
}

export async function apiPut(path, body) {
	return handle(
		await fetch(buildUrl(path), {
			method: 'PUT',
			headers: authHeaders({ 'Content-Type': 'application/json' }),
			body: JSON.stringify(body),
		})
	)
}

export async function apiDelete(path) {
	return handle(await fetch(buildUrl(path), { method: 'DELETE', headers: authHeaders() }))
}

export async function apiUpload(path, formData) {
	return handle(await fetch(buildUrl(path), { method: 'POST', headers: authHeaders(), body: formData }))
}

export async function apiGetBlob(path) {
	const response = await fetch(buildUrl(path), { headers: authHeaders() })
	if (response.status === 401) {
		clearToken()
		if (typeof window !== 'undefined') window.location.assign('/login')
		throw new Error('Session expired')
	}
	if (!response.ok) throw new Error(`Failed to load (${response.status})`)
	return response.blob()
}

export { API_BASE_URL }
