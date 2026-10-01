import { useEffect, useRef, useState } from 'react'
import '../../../styles-tailwind.css'
import AppShell from '../../../shared/layout/AppShell'
import { Button } from '../../../shared/components/Button'
import { Alert } from '../../../shared/components/Alert'
import LoadingSpinner from '../../../shared/components/LoadingSpinner'
import { listMedia, uploadMedia, deleteMedia, getMediaBlobUrl } from '../services/mediaService'

function MediaThumb({ item, onDelete }) {
	const [src, setSrc] = useState(null)
	const id = item.id || item._id

	useEffect(() => {
		let active = true
		let url
		;(async () => {
			try {
				url = await getMediaBlobUrl(id)
				if (active) setSrc(url)
			} catch {
				/* leave placeholder */
			}
		})()
		return () => {
			active = false
			if (url) URL.revokeObjectURL(url)
		}
	}, [id])

	return (
		<article className="overflow-hidden rounded-2xl border border-light-white3 bg-light-white1">
			<div className="flex h-40 items-center justify-center bg-light-white2">
				{src ? (
					<img src={src} alt={item.filename} className="h-full w-full object-cover" />
				) : (
					<span className="text-xs text-light-white4">Aperçu…</span>
				)}
			</div>
			<div className="flex items-center justify-between gap-2 p-3">
				<span className="truncate text-sm" title={item.filename}>
					{item.filename}
				</span>
				<button
					type="button"
					onClick={() => onDelete(id)}
					className="shrink-0 text-sm font-medium text-light-red1 hover:underline"
				>
					Supprimer
				</button>
			</div>
		</article>
	)
}

export default function MediaLibrary() {
	const inputRef = useRef(null)
	const [items, setItems] = useState([])
	const [loading, setLoading] = useState(true)
	const [uploading, setUploading] = useState(false)
	const [error, setError] = useState('')

	const refresh = async () => {
		try {
			setItems(await listMedia())
		} catch (e) {
			setError(e.message)
		} finally {
			setLoading(false)
		}
	}

	useEffect(() => {
		refresh()
	}, [])

	const onPick = async (e) => {
		const file = e.target.files?.[0]
		if (!file) return
		setError('')
		if (!file.type.startsWith('image/')) {
			setError('Seules les images (JPG/PNG) sont acceptées.')
			e.target.value = ''
			return
		}
		if (file.size > 5 * 1024 * 1024) {
			setError('La taille maximale est de 5 Mo.')
			e.target.value = ''
			return
		}
		setUploading(true)
		try {
			await uploadMedia(file)
			await refresh()
		} catch (err) {
			setError(err.message)
		} finally {
			setUploading(false)
			if (inputRef.current) inputRef.current.value = ''
		}
	}

	const onDelete = async (id) => {
		if (!window.confirm('Supprimer cette image ?')) return
		setError('')
		try {
			await deleteMedia(id)
			setItems((prev) => prev.filter((m) => (m.id || m._id) !== id))
		} catch (err) {
			setError(err.message)
		}
	}

	return (
		<AppShell
			title="Bibliothèque média"
			subtitle="Téléchargez et gérez vos images (JPG/PNG, max 5 Mo)"
			actions={
				<>
					<input
						ref={inputRef}
						type="file"
						accept="image/png,image/jpeg"
						className="hidden"
						onChange={onPick}
					/>
					<Button variant="primary" isLoading={uploading} onClick={() => inputRef.current?.click()}>
						Téléverser une image
					</Button>
				</>
			}
		>
			{error ? (
				<div className="mb-4">
					<Alert theme="light" status="error" message={error} />
				</div>
			) : null}

			{loading ? (
				<LoadingSpinner theme="light" label="Chargement de la bibliothèque..." />
			) : items.length === 0 ? (
				<div className="rounded-2xl border border-dashed border-light-white3 p-10 text-center text-sm text-light-white4">
					Aucune image. Téléversez votre première image.
				</div>
			) : (
				<div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
					{items.map((item) => (
						<MediaThumb key={item.id || item._id} item={item} onDelete={onDelete} />
					))}
				</div>
			)}
		</AppShell>
	)
}
