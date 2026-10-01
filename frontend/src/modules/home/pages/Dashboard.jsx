import { useEffect, useMemo, useState } from 'react'
import '../../../styles-tailwind.css'
import { Input } from '../../../shared/components/Input'
import { Button } from '../../../shared/components/Button'
import { Alert } from '../../../shared/components/Alert'
import siteService from '../services/siteService'

const Dashboard = () => {
  const [sites, setSites] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [errorMessage, setErrorMessage] = useState('')
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [newSiteName, setNewSiteName] = useState('')
  const [newSiteDescription, setNewSiteDescription] = useState('')
  const [isCreating, setIsCreating] = useState(false)

  const getSiteId = (site, fallback = undefined) => site.id ?? site._id ?? site.siteId ?? fallback
  const getSiteName = (site) => site.name || site.title || 'Site sans nom'
  const getSiteDescription = (site) => site.description || 'Aucune description disponible.'
  const skeletonItems = Array.from({ length: 6 }, (_, index) => index)
  const currentPath = window.location.pathname
  const isTemplateView = currentPath === '/dashboard/templates'

  useEffect(() => {
    const token = localStorage.getItem('authToken') || localStorage.getItem('token')
    setIsAuthenticated(Boolean(token))
  }, [])

  useEffect(() => {
    const loadSites = async () => {
      setIsLoading(true)
      setErrorMessage('')

      try {
        // Simule un appel reseau pour visualiser le skeleton screen
        await new Promise((resolve) => setTimeout(resolve, 900))
        const loadedSites = await siteService.getAllSites()
        setSites(Array.isArray(loadedSites) ? loadedSites : [])
      } catch (error) {
        setErrorMessage(error.message || 'Impossible de charger les sites.')
      } finally {
        setIsLoading(false)
      }
    }

    loadSites()
  }, [])

  const filteredSites = useMemo(() => {
    const normalizedQuery = searchQuery.trim().toLowerCase()
    if (!normalizedQuery) {
      return sites
    }

    return sites.filter((site) => {
      const name = getSiteName(site).toLowerCase()
      return name.includes(normalizedQuery)
    })
  }, [sites, searchQuery])

  const hasNoSites = !isLoading && filteredSites.length === 0
  const hasSites = !isLoading && filteredSites.length > 0

  const handleCreateSite = async (event) => {
    event.preventDefault()

    const trimmedName = newSiteName.trim()
    const trimmedDescription = newSiteDescription.trim()
    if (!trimmedName) {
      setErrorMessage('Le nom du site est requis.')
      return
    }

    try {
      setIsCreating(true)
      setErrorMessage('')
      const createdSite = await siteService.createSite({
        name: trimmedName,
        description: trimmedDescription,
      })

      const normalizedCreatedSite = createdSite && typeof createdSite === 'object'
        ? createdSite
        : { id: Date.now(), name: trimmedName, description: trimmedDescription }

      setSites((prevSites) => [normalizedCreatedSite, ...prevSites])
      setNewSiteName('')
      setNewSiteDescription('')
    } catch (error) {
      setErrorMessage(error.message || 'La creation du site a echoue.')
    } finally {
      setIsCreating(false)
    }
  }

  const handleDeleteSite = async (siteId, siteName) => {
    const shouldDelete = window.confirm(`Supprimer le site "${siteName}" ?`)
    if (!shouldDelete) {
      return
    }

    try {
      await siteService.deleteSite(siteId)
      setSites((prevSites) => prevSites.filter((site) => getSiteId(site) !== siteId))
    } catch (error) {
      setErrorMessage(error.message || 'La suppression a echoue.')
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('authToken')
    localStorage.removeItem('token')
    setIsAuthenticated(false)
    window.location.href = '/'
  }

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-4 sm:px-6 sm:py-6 lg:px-8 lg:py-8">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-4 lg:flex-row">
        <aside className="w-full rounded-2xl border border-slate-200 bg-white p-4 shadow-sm lg:w-72">
          <div className="mb-6 flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-600 text-white">
              <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M3 7l9-4 9 4-9 4-9-4z" />
                <path d="M3 12l9 4 9-4" />
                <path d="M3 17l9 4 9-4" />
              </svg>
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-900">Sidi Builder</p>
              <p className="text-xs text-slate-500">Tableau de bord</p>
            </div>
          </div>

          <nav className="space-y-2">
            <a
              href="/dashboard"
              className={`flex items-center gap-2 rounded-xl px-3 py-2 text-sm ${
                !isTemplateView
                  ? 'bg-indigo-50 font-medium text-indigo-700'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M3 12l9-9 9 9" />
                <path d="M9 21V9h6v12" />
              </svg>
              Dashboard
            </a>
            <a
              href="/templates"
              className="flex items-center gap-2 rounded-xl px-3 py-2 text-sm text-slate-600 hover:bg-slate-100"
            >
              <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="4" width="18" height="16" rx="2" />
                <path d="M7 8h10" />
              </svg>
              Templates
            </a>
            <a
              href="/assistant"
              className="flex items-center gap-2 rounded-xl px-3 py-2 text-sm text-slate-600 hover:bg-slate-100"
            >
              <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 3a7 7 0 0 1 7 7c0 2.5-1.5 4-3 5.5V18H8v-2.5C6.5 14 5 12.5 5 10a7 7 0 0 1 7-7z" />
                <path d="M9 21h6" />
              </svg>
              Assistant IA
            </a>
            <a
              href="/media"
              className="flex items-center gap-2 rounded-xl px-3 py-2 text-sm text-slate-600 hover:bg-slate-100"
            >
              <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="5" width="18" height="14" rx="2" />
                <path d="M3 15l5-5 4 4 3-3 6 6" />
              </svg>
              Média
            </a>
          </nav>

          <div className="mt-6 rounded-xl bg-slate-50 p-3">
            <p className="text-xs font-medium uppercase tracking-wide text-slate-500">Auth</p>
            <p className="mt-1 text-sm text-slate-700">
              {isAuthenticated ? 'Session active' : 'Aucune session'}
            </p>
            <Button
              variant="outline"
              size="sm"
              className="mt-3 w-full! border-slate-300! text-slate-700! hover:bg-slate-100!"
              onClick={handleLogout}
            >
              Deconnexion
            </Button>
          </div>
        </aside>

        <section className="min-w-0 flex-1 space-y-4">
          <header className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:p-5">
            <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
              <div>
                <h1 className="text-2xl font-semibold tracking-tight text-slate-900">
                  {isTemplateView ? 'Template Gallery' : 'Mes sites'}
                </h1>
                <p className="mt-1 text-sm text-slate-500">
                  {isTemplateView
                    ? 'Structure vide pour M2, prete pour integration.'
                    : `${filteredSites.length} site(s) affiche(s)`}
                </p>
              </div>

              <div className="w-full lg:max-w-sm">
                {!isTemplateView ? (
                  <Input
                    id="site-search"
                    variant="search"
                    fullWidth
                    placeholder="Rechercher un site par nom..."
                    value={searchQuery}
                    onChange={(event) => setSearchQuery(event.target.value)}
                    startAdornment={
                      <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="11" cy="11" r="8" />
                        <path d="m21 21-4.35-4.35" />
                      </svg>
                    }
                  />
                ) : null}
              </div>
            </div>
          </header>

          {!isTemplateView ? (
            <form
              onSubmit={handleCreateSite}
              className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:p-5"
            >
              <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
                <Input
                  id="new-site-name"
                  variant="search"
                  fullWidth
                  label="Nom du site"
                  placeholder="Ex: Portfolio agence"
                  value={newSiteName}
                  onChange={(event) => setNewSiteName(event.target.value)}
                />
                <Input
                  id="new-site-description"
                  variant="search"
                  fullWidth
                  label="Description"
                  placeholder="Ex: Site vitrine moderne"
                  value={newSiteDescription}
                  onChange={(event) => setNewSiteDescription(event.target.value)}
                />
              </div>
              <div className="mt-3 flex justify-end">
                <Button
                  type="submit"
                  variant="board"
                  size="md"
                  isLoading={isCreating}
                  disabled={isCreating || !newSiteName.trim()}
                >
                  Creer le site
                </Button>
              </div>
            </form>
          ) : null}

          {errorMessage ? (
            <Alert
              status="error"
              theme="light"
              title="Erreur"
              message={errorMessage}
            />
          ) : null}

          {!isTemplateView && isLoading ? (
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
              {skeletonItems.map((index) => (
                <article key={index} className="animate-pulse rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                  <div className="mb-4 h-5 w-20 rounded-full bg-slate-200" />
                  <div className="h-5 w-2/3 rounded bg-slate-200" />
                  <div className="mt-3 h-4 w-full rounded bg-slate-200" />
                  <div className="mt-2 h-4 w-4/5 rounded bg-slate-200" />
                </article>
              ))}
            </div>
          ) : null}

          {!isTemplateView && hasNoSites ? (
            <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-8 text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100 text-slate-500">
                <svg viewBox="0 0 24 24" className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M4 4h16v16H4z" />
                  <path d="M8 12h8" />
                </svg>
              </div>
              <h3 className="mt-4 text-lg font-semibold text-slate-900">Aucun site trouve</h3>
              <p className="mt-1 text-sm text-slate-500">Essaie une autre recherche ou cree un nouveau site.</p>
            </div>
          ) : null}

          {!isTemplateView && hasSites ? (
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
              {filteredSites.map((site, index) => (
                <article
                  key={getSiteId(site, index)}
                  className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md sm:p-5"
                >
                  <div className="mb-4 flex items-center justify-between gap-3">
                    <span className="inline-flex items-center rounded-full bg-indigo-50 px-2.5 py-1 text-xs font-semibold text-indigo-700">
                      {getSiteId(site, 'N/A')}
                    </span>
                    <button
                      type="button"
                      onClick={() => handleDeleteSite(getSiteId(site), getSiteName(site))}
                      className="inline-flex items-center gap-1 rounded-lg px-2 py-1 text-xs font-medium text-rose-600 transition hover:bg-rose-50"
                    >
                      <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M3 6h18" />
                        <path d="M8 6V4h8v2" />
                        <path d="M19 6l-1 14H6L5 6" />
                      </svg>
                      Supprimer
                    </button>
                  </div>

                  <h2 className="text-lg font-semibold text-slate-900">{getSiteName(site)}</h2>
                  <p className="mt-2 line-clamp-3 text-sm text-slate-600">{getSiteDescription(site)}</p>
                </article>
              ))}
            </div>
          ) : null}

          {isTemplateView ? (
            <section className="rounded-2xl border border-dashed border-slate-300 bg-white p-6 shadow-sm sm:p-8">
              <h2 className="text-lg font-semibold text-slate-900">Structure Template Gallery</h2>
              <p className="mt-2 text-sm text-slate-500">
                Cette vue est volontairement vide pour M2. Tu pourras y afficher les templates sous forme de cards.
              </p>
              <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
                {['Template A', 'Template B', 'Template C'].map((label) => (
                  <article
                    key={label}
                    className="rounded-xl border border-slate-200 bg-slate-50 p-4"
                  >
                    <div className="h-28 rounded-lg border border-slate-200 bg-white" />
                    <p className="mt-3 text-sm font-medium text-slate-700">{label}</p>
                    <p className="mt-1 text-xs text-slate-500">Placeholder</p>
                  </article>
                ))}
              </div>
            </section>
          ) : null}
        </section>
      </div>
    </main>
  )
}

export default Dashboard