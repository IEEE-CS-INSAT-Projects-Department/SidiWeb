import { getToken, clearToken } from '../../auth/services/authService'

const API_BASE_URL = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '')
const SITES_ENDPOINT = API_BASE_URL ? `${API_BASE_URL}/sites` : '/sites'

function errorMessage(payload, status) {
	if (payload && typeof payload === 'object') {
		const d = payload.detail
		if (typeof d === 'string') return d
		if (Array.isArray(d) && d[0]?.msg) return d[0].msg
		if (payload.message) return payload.message
	}
	if (status >= 500) return 'The server encountered an error, please try again later'
	return `Request failed (${status})`
}

async function request(url, options = {}) {
	const token = getToken()
	let response
	try {
		response = await fetch(url, {
			headers: {
				'Content-Type': 'application/json',
				...(token ? { Authorization: `Bearer ${token}` } : {}),
				...(options.headers || {})
			},
			...options
		})
	} catch {
		throw new Error('Cannot reach the server. Check your connection and try again.')
	}

	if (response.status === 401) {
		clearToken()
		if (typeof window !== 'undefined') window.location.assign('/login')
		throw new Error('Your session has expired, please log in again')
	}

	let payload = null
	const contentType = response.headers.get('content-type') || ''
	if (contentType.includes('application/json')) {
		payload = await response.json()
	} else {
		const text = await response.text()
		payload = text || null
	}

	if (!response.ok) {
		throw new Error(errorMessage(payload, response.status))
	}

	return payload
}

function normalizeSites(payload) {
	if (Array.isArray(payload)) return payload
	if (Array.isArray(payload?.sites)) return payload.sites
	if (Array.isArray(payload?.data)) return payload.data
	return []
}

export async function getSites() {
	const payload = await request(SITES_ENDPOINT, { method: 'GET' })
	return normalizeSites(payload)
}

export async function getAllSites() {
	return getSites()
}

export async function getSite(siteId) {
	return request(`${SITES_ENDPOINT}/${siteId}`, { method: 'GET' })
}

export async function createSite(siteData) {
	return request(SITES_ENDPOINT, {
		method: 'POST',
		body: JSON.stringify(siteData)
	})
}

export async function updateSite(siteId, siteData) {
	return request(`${SITES_ENDPOINT}/${siteId}`, {
		method: 'PUT',
		body: JSON.stringify(siteData)
	})
}

export async function deleteSite(siteId) {
	await request(`${SITES_ENDPOINT}/${siteId}`, { method: 'DELETE' })
	return true
}

const siteService = {
	getAllSites,
	getSites,
	getSite,
	createSite,
	updateSite,
	deleteSite
}

export default siteService