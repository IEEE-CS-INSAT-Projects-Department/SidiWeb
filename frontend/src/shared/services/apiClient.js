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
	if (status >= 500) return 'Le serveur a rencontré une erreur, veuillez réessayer plus tard'
	return `La requête a échoué (${status})`
}

async function safeFetch(url, options) {
	try {
		return await fetch(url, options)
	} catch {
		// Network error / server unreachable / CORS failure
		throw new Error('Impossible de contacter le serveur. Vérifiez votre connexion et réessayez.')
	}
}

async function handle(response) {
	if (response.status === 401) {
		clearToken()
		if (typeof window !== 'undefined') window.location.assign('/login')
		throw new Error('Votre session a expiré, veuillez vous reconnecter')
	}
	let payload = null
	if ((response.headers.get('content-type') || '').includes('application/json')) {
		payload = await response.json()
	}
	if (!response.ok) throw new Error(messageFrom(payload, response.status))
	return payload
}

export async function apiGet(path) {
	return handle(await safeFetch(buildUrl(path), { headers: authHeaders() }))
}

export async function apiPost(path, body) {
	return handle(
		await safeFetch(buildUrl(path), {
			method: 'POST',
			headers: authHeaders({ 'Content-Type': 'application/json' }),
			body: JSON.stringify(body),
		})
	)
}

export async function apiPut(path, body) {
	return handle(
		await safeFetch(buildUrl(path), {
			method: 'PUT',
			headers: authHeaders({ 'Content-Type': 'application/json' }),
			body: JSON.stringify(body),
		})
	)
}

export async function apiDelete(path) {
	return handle(await safeFetch(buildUrl(path), { method: 'DELETE', headers: authHeaders() }))
}

export async function apiUpload(path, formData) {
	return handle(await safeFetch(buildUrl(path), { method: 'POST', headers: authHeaders(), body: formData }))
}

export async function apiGetBlob(path) {
	const response = await safeFetch(buildUrl(path), { headers: authHeaders() })
	if (response.status === 401) {
		clearToken()
		if (typeof window !== 'undefined') window.location.assign('/login')
		throw new Error('Votre session a expiré, veuillez vous reconnecter')
	}
	if (!response.ok) throw new Error("Impossible de charger l'image")
	return response.blob()
}

export { API_BASE_URL }
