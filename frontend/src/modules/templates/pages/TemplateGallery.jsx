import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../../../styles-tailwind.css'
import AppShell from '../../../shared/layout/AppShell'
import { Button } from '../../../shared/components/Button'
import { Alert } from '../../../shared/components/Alert'
import LoadingSpinner from '../../../shared/components/LoadingSpinner'
import { getTemplates } from '../services/templateService'
import { createSite } from '../../home/services/siteService'

export default function TemplateGallery() {
	const navigate = useNavigate()
	const [templates, setTemplates] = useState([])
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState('')
	const [category, setCategory] = useState('all')
	const [creatingId, setCreatingId] = useState(null)

	useEffect(() => {
		let active = true
		;(async () => {
			try {
				const data = await getTemplates()
				if (active) setTemplates(data)
			} catch (e) {
				if (active) setError(e.message)
			} finally {
				if (active) setLoading(false)
			}
		})()
		return () => {
			active = false
		}
	}, [])

	const categories = useMemo(
		() => ['all', ...Array.from(new Set(templates.map((t) => t.category).filter(Boolean)))],
		[templates]
	)
	const filtered = category === 'all' ? templates : templates.filter((t) => t.category === category)

	const useTemplate = async (t) => {
		setCreatingId(t.id)
		setError('')
		try {
			const site = await createSite({ name: t.name, template_id: t.id })
			navigate(`/editor/${site.id || site._id}`)
		} catch (e) {
			setError(e.message)
			setCreatingId(null)
		}
	}

	return (
		<AppShell title="Templates" subtitle="Choisissez un modèle pour démarrer votre site">
			{error ? (
				<div className="mb-4">
					<Alert theme="light" status="error" message={error} />
				</div>
			) : null}

			{loading ? (
				<LoadingSpinner theme="light" label="Chargement des templates..." />
			) : (
				<>
					<div className="mb-5 flex flex-wrap gap-2">
						{categories.map((c) => (
							<button
								key={c}
								type="button"
								onClick={() => setCategory(c)}
								className={`rounded-full border px-3 py-1.5 text-sm capitalize transition ${
									category === c
										? 'border-light-red1 bg-light-red1/10 text-light-red1'
										: 'border-light-white3 text-light-white4 hover:text-light-black'
								}`}
							>
								{c === 'all' ? 'Tous' : c}
							</button>
						))}
					</div>

					<div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
						{filtered.map((t) => (
							<article
								key={t.id}
								className="flex flex-col rounded-2xl border border-light-white3 bg-light-white1 p-5"
							>
								<span className="w-fit rounded-full bg-light-red1/10 px-2.5 py-1 text-xs font-medium capitalize text-light-red1">
									{t.category}
								</span>
								<h3 className="mt-3 text-lg font-semibold">{t.name}</h3>
								<p className="mt-1 flex-1 text-sm text-light-white4">{t.description}</p>
								{t.structure?.pages ? (
									<p className="mt-3 text-xs text-light-white4">
										Pages : {t.structure.pages.join(', ')}
									</p>
								) : null}
								<Button
									className="mt-4"
									variant="primary"
									fullWidth
									isLoading={creatingId === t.id}
									onClick={() => useTemplate(t)}
								>
									Utiliser ce template
								</Button>
							</article>
						))}
					</div>

					{filtered.length === 0 ? (
						<p className="text-sm text-light-white4">Aucun template dans cette catégorie.</p>
					) : null}
				</>
			)}
		</AppShell>
	)
}
