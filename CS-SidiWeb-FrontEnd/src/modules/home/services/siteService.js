const API_BASE_URL = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '')
const SITES_ENDPOINT = API_BASE_URL ? `${API_BASE_URL}/sites` : '/sites'

async function request(url, options = {}) {
	const response = await fetch(url, {
		headers: {
			'Content-Type': 'application/json',
			...(options.headers || {})
		},
		...options
	})

	let payload = null
	const contentType = response.headers.get('content-type') || ''

	if (contentType.includes('application/json')) {
		payload = await response.json()
	} else {
		const text = await response.text()
		payload = text || null
	}

	if (!response.ok) {
		const message =
			(typeof payload === 'object' && payload && payload.message) ||
			`Request failed (${response.status})`
		throw new Error(message)
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

export async function createSite(siteData) {
	return request(SITES_ENDPOINT, {
		method: 'POST',
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
	createSite,
	deleteSite
}

export default siteService