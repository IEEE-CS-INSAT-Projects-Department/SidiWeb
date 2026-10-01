import { apiPost } from '../../../shared/services/apiClient'

export async function getRecommendations({ category, style, preferences = '' }) {
	return apiPost('/recommendations', { category, style, preferences })
}

export default { getRecommendations }
