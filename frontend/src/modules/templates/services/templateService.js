import { apiGet } from '../../../shared/services/apiClient'

export async function getTemplates() {
	const data = await apiGet('/templates')
	return Array.isArray(data) ? data : []
}

export async function getTemplate(id) {
	return apiGet(`/templates/${id}`)
}

export default { getTemplates, getTemplate }
