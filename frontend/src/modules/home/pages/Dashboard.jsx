import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../../../styles-tailwind.css'
import AppShell from '../../../shared/layout/AppShell'
import { Input } from '../../../shared/components/Input'
import { Button } from '../../../shared/components/Button'
import { Alert } from '../../../shared/components/Alert'
import siteService from '../services/siteService'

const getSiteId = (site, fallback) => site.id ?? site._id ?? site.siteId ?? fallback
const getSiteName = (site) => site.name || site.title || 'Site sans nom'
const getSiteDescription = (site) => site.description || 'Aucune description disponible.'

export default function Dashboard() {
	const navigate = useNavigate()
	const [sites, setSites] = useState([])
	const [isLoading, setIsLoading] = useState(true)
	const [searchQuery, setSearchQuery] = useState('')
	const [errorMessage, setErrorMessage] = useState('')
	const [showCreate, setShowCreate] = useState(false)
	const [newSiteName, setNewSiteName] = useState('')
	const [newSiteDescription, setNewSiteDescription] = useState('')
	const [isCreating, setIsCreating] = useState(false)

	useEffect(() => {
		;(async () => {
			setIsLoading(true)
			setErrorMessage('')
			try {
				const loaded = await siteService.getAllSites()
				setSites(Array.isArray(loaded) ? loaded : [])
			} catch (error) {
				setErrorMessage(error.message || 'Impossible de charger les sites.')
			} finally {
				setIsLoading(false)
			}
		})()
	}, [])

	const filteredSites = useMemo(() => {
		const q = searchQuery.trim().toLowerCase()
		if (!q) return sites
		return sites.filter((s) => getSiteName(s).toLowerCase().includes(q))
	}, [sites, searchQuery])

	const handleCreateSite = async (event) => {
		event.preventDefault()
		const name = newSiteName.trim()
		if (!name) {
			setErrorMessage('Le nom du site est requis.')
			return
		}
		setIsCreating(true)
		setErrorMessage('')
		try {
			const created = await siteService.createSite({ name, description: newSiteDescription.trim() })
			setSites((prev) => [created, ...prev])
			setNewSiteName('')
			setNewSiteDescription('')
			setShowCreate(false)
		} catch (error) {
			setErrorMessage(error.message || 'La création du site a échoué.')
		} finally {
			setIsCreating(false)
		}
	}

	const handleDeleteSite = async (siteId, siteName) => {
		if (!window.confirm(`Supprimer le site « ${siteName} » ?`)) return
		try {
			await siteService.deleteSite(siteId)
			setSites((prev) => prev.filter((s) => getSiteId(s) !== siteId))
		} catch (error) {
			setErrorMessage(error.message || 'La suppression a échoué.')
		}
	}

	const openSite = (site) => navigate(`/editor/${getSiteId(site)}`)

	return (
		<AppShell
			title="Mes sites"
			subtitle={isLoading ? 'Chargement…' : `${filteredSites.length} site(s)`}
			actions={
				<div className="flex w-full flex-wrap items-center gap-2 sm:w-auto">
					<div className="min-w-[200px] flex-1 sm:flex-none">
						<Input
							id="site-search"
							variant="search"
							fullWidth
							placeholder="Rechercher un site…"
							value={searchQuery}
							onChange={(e) => setSearchQuery(e.target.value)}
						/>
					</div>
					<Button variant="primary" size="sm" onClick={() => setShowCreate((v) => !v)}>
						{showCreate ? 'Fermer' : '+ Nouveau site'}
					</Button>
				</div>
			}
		>
			{errorMessage ? (
				<div className="mb-4">
					<Alert theme="light" status="error" message={errorMessage} />
				</div>
			) : null}

			{showCreate ? (
				<form
					onSubmit={handleCreateSite}
					className="mb-6 rounded-2xl border border-light-white3 bg-light-white1 p-5"
				>
					<div className="grid grid-cols-1 gap-4 md:grid-cols-2">
						<Input
							id="new-site-name"
							variant="search"
							fullWidth
							label="Nom du site"
							placeholder="Ex : Portfolio agence"
							value={newSiteName}
							onChange={(e) => setNewSiteName(e.target.value)}
						/>
						<Input
							id="new-site-description"
							variant="search"
							fullWidth
							label="Description"
							placeholder="Ex : Site vitrine moderne"
							value={newSiteDescription}
							onChange={(e) => setNewSiteDescription(e.target.value)}
						/>
					</div>
					<div className="mt-4 flex items-center gap-2">
						<Button type="submit" variant="primary" size="sm" isLoading={isCreating} disabled={!newSiteName.trim()}>
							Créer le site
						</Button>
						<span className="text-xs text-light-white4">
							Astuce : partez d'un modèle depuis la page Templates pour un contenu prérempli.
						</span>
					</div>
				</form>
			) : null}

			{isLoading ? (
				<div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
					{Array.from({ length: 6 }).map((_, i) => (
						<div key={i} className="animate-pulse rounded-2xl border border-light-white3 bg-light-white1 p-5">
							<div className="h-5 w-20 rounded-full bg-light-white2" />
							<div className="mt-4 h-5 w-2/3 rounded bg-light-white2" />
							<div className="mt-3 h-4 w-full rounded bg-light-white2" />
							<div className="mt-2 h-4 w-4/5 rounded bg-light-white2" />
						</div>
					))}
				</div>
			) : filteredSites.length === 0 ? (
				<div className="rounded-2xl border border-dashed border-light-white3 bg-light-white1 p-10 text-center">
					<h3 className="text-lg font-semibold">Aucun site</h3>
					<p className="mt-1 text-sm text-light-white4">
						{searchQuery ? 'Aucun résultat pour cette recherche.' : 'Créez votre premier site pour commencer.'}
					</p>
					{!searchQuery ? (
						<div className="mt-4 flex items-center justify-center gap-2">
							<Button variant="primary" size="sm" onClick={() => setShowCreate(true)}>
								+ Nouveau site
							</Button>
							<Button variant="outline" size="sm" onClick={() => navigate('/templates')}>
								Parcourir les modèles
							</Button>
						</div>
					) : null}
				</div>
			) : (
				<div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
					{filteredSites.map((site, index) => {
						const published = Boolean(site.published)
						return (
							<article
								key={getSiteId(site, index)}
								className="flex flex-col rounded-2xl border border-light-white3 bg-light-white1 p-5 transition hover:-translate-y-0.5 hover:shadow-md"
							>
								<div className="mb-3 flex items-center justify-between">
									<span
										className={`rounded-full px-2.5 py-1 text-xs font-medium ${
											published ? 'bg-emerald-50 text-emerald-700' : 'bg-light-white2 text-light-white4'
										}`}
									>
										{published ? 'Publié' : 'Brouillon'}
									</span>
								</div>

								<h3 className="text-lg font-semibold">{getSiteName(site)}</h3>
								<p className="mt-1 line-clamp-2 flex-1 text-sm text-light-white4">
									{getSiteDescription(site)}
								</p>

								{published && site.public_url ? (
									<a
										href={site.public_url}
										target="_blank"
										rel="noreferrer"
										className="mt-2 truncate text-xs text-light-red1 hover:underline"
									>
										{site.public_url}
									</a>
								) : null}

								<div className="mt-4 flex items-center gap-2">
									<Button variant="primary" size="sm" onClick={() => openSite(site)}>
										Ouvrir
									</Button>
									<Button
										variant="outline"
										size="sm"
										onClick={() => handleDeleteSite(getSiteId(site), getSiteName(site))}
									>
										Supprimer
									</Button>
								</div>
							</article>
						)
					})}
				</div>
			)}
		</AppShell>
	)
}
