import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../../../styles-tailwind.css'
import AppShell from '../../../shared/layout/AppShell'
import { Input } from '../../../shared/components/Input'
import { Button } from '../../../shared/components/Button'
import { Alert } from '../../../shared/components/Alert'
import ConfirmDialog from '../../../shared/components/ConfirmDialog'
import { useToast } from '../../../shared/components/ToastProvider'
import siteService from '../services/siteService'

const getSiteId = (site, fallback) => site.id ?? site._id ?? site.siteId ?? fallback
const getSiteName = (site) => site.name || site.title || 'Untitled site'
const getSiteDescription = (site) => site.description || 'No description available.'

export default function Dashboard() {
	const navigate = useNavigate()
	const toast = useToast()
	const [sites, setSites] = useState([])
	const [isLoading, setIsLoading] = useState(true)
	const [searchQuery, setSearchQuery] = useState('')
	const [errorMessage, setErrorMessage] = useState('')
	const [showCreate, setShowCreate] = useState(false)
	const [newSiteName, setNewSiteName] = useState('')
	const [newSiteDescription, setNewSiteDescription] = useState('')
	const [isCreating, setIsCreating] = useState(false)
	const [pendingDelete, setPendingDelete] = useState(null)
	const [isDeleting, setIsDeleting] = useState(false)

	useEffect(() => {
		;(async () => {
			setIsLoading(true)
			setErrorMessage('')
			try {
				const loaded = await siteService.getAllSites()
				setSites(Array.isArray(loaded) ? loaded : [])
			} catch (error) {
				setErrorMessage(error.message || 'Failed to load sites.')
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
			setErrorMessage('Site name is required.')
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
			toast.success(`"${name}" created`)
		} catch (error) {
			toast.error(error.message || 'Failed to create site.')
		} finally {
			setIsCreating(false)
		}
	}

	const confirmDelete = async () => {
		if (!pendingDelete) return
		setIsDeleting(true)
		try {
			await siteService.deleteSite(pendingDelete.id)
			setSites((prev) => prev.filter((s) => getSiteId(s) !== pendingDelete.id))
			toast.success('Site deleted')
			setPendingDelete(null)
		} catch (error) {
			toast.error(error.message || 'Failed to delete the site.')
		} finally {
			setIsDeleting(false)
		}
	}

	const openSite = (site) => navigate(`/editor/${getSiteId(site)}`)

	return (
		<AppShell
			title="My sites"
			subtitle={isLoading ? 'Loading...' : `${filteredSites.length} site(s)`}
			actions={
				<div className="flex w-full flex-wrap items-center gap-2 sm:w-auto">
					<div className="min-w-[200px] flex-1 sm:flex-none">
						<Input
							id="site-search"
							variant="search"
							fullWidth
							placeholder="Search sites..."
							value={searchQuery}
							onChange={(e) => setSearchQuery(e.target.value)}
						/>
					</div>
					<Button variant="primary" size="sm" onClick={() => setShowCreate((v) => !v)}>
						{showCreate ? 'Close' : '+ New site'}
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
							label="Site name"
							placeholder="e.g. Agency portfolio"
							value={newSiteName}
							onChange={(e) => setNewSiteName(e.target.value)}
						/>
						<Input
							id="new-site-description"
							variant="search"
							fullWidth
							label="Description"
							placeholder="e.g. Modern showcase site"
							value={newSiteDescription}
							onChange={(e) => setNewSiteDescription(e.target.value)}
						/>
					</div>
					<div className="mt-4 flex items-center gap-2">
						<Button type="submit" variant="primary" size="sm" isLoading={isCreating} disabled={!newSiteName.trim()}>
							Create site
						</Button>
						<span className="text-xs text-light-white4">
							Tip: start from a template on the Templates page for pre-filled content.
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
					<h3 className="text-lg font-semibold">No sites</h3>
					<p className="mt-1 text-sm text-light-white4">
						{searchQuery ? 'No results for this search.' : 'Create your first site to get started.'}
					</p>
					{!searchQuery ? (
						<div className="mt-4 flex items-center justify-center gap-2">
							<Button variant="primary" size="sm" onClick={() => setShowCreate(true)}>
								+ New site
							</Button>
							<Button variant="outline" size="sm" onClick={() => navigate('/templates')}>
								Browse templates
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
										{published ? 'Published' : 'Draft'}
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
										Open
									</Button>
									<Button
										variant="outline"
										size="sm"
										onClick={() => setPendingDelete({ id: getSiteId(site), name: getSiteName(site) })}
									>
										Delete
									</Button>
								</div>
							</article>
						)
					})}
				</div>
			)}
			<ConfirmDialog
				open={!!pendingDelete}
				title="Delete site"
				message={pendingDelete ? `"${pendingDelete.name}" will be permanently deleted. This cannot be undone.` : ''}
				confirmLabel="Delete"
				busy={isDeleting}
				onConfirm={confirmDelete}
				onCancel={() => setPendingDelete(null)}
			/>
		</AppShell>
	)
}
