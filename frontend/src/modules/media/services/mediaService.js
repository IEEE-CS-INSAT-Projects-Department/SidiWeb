import { apiGet, apiDelete, apiUpload, apiGetBlob } from '../../../shared/services/apiClient'

export async function listMedia() {
	const data = await apiGet('/media')
	return Array.isArray(data) ? data : []
}

export async function uploadMedia(file) {
	const form = new FormData()
	form.append('file', file)
	return apiUpload('/media/upload', form)
}

export async function deleteMedia(id) {
	return apiDelete(`/media/${id}`)
}

export async function getMediaBlobUrl(id) {
	const blob = await apiGetBlob(`/media/${id}`)
	return URL.createObjectURL(blob)
}

export default { listMedia, uploadMedia, deleteMedia, getMediaBlobUrl }
