import { useState } from 'react'
import '../../../styles-tailwind.css'
import { Input } from '../../../shared/components/Input'
import { Button } from '../../../shared/components/Button'
import { Alert } from '../../../shared/components/Alert'
import LoadingSpinner from '../../../shared/components/LoadingSpinner'
import ResponsiveGrid from '../../../shared/layout/ResponsiveGrid'

export const SiteList = ({
  sites = [],
  isLoading = false,
  error = '',
  onCreateSite,
  onDeleteSite,
  className = '',
}) => {
  const [newSiteName, setNewSiteName] = useState('')
  const [isCreating, setIsCreating] = useState(false)
  const [deletingId, setDeletingId] = useState(null)

  const handleCreate = async (event) => {
    event.preventDefault()

    const trimmedName = newSiteName.trim()
    if (!trimmedName || typeof onCreateSite !== 'function') {
      return
    }

    try {
      setIsCreating(true)
      await onCreateSite({ name: trimmedName })
      setNewSiteName('')
    } finally {
      setIsCreating(false)
    }
  }

  const handleDelete = async (siteId) => {
    if ((siteId === null || siteId === undefined) || typeof onDeleteSite !== 'function') {
      return
    }

    try {
      setDeletingId(siteId)
      await onDeleteSite(siteId)
    } finally {
      setDeletingId(null)
    }
  }

  const isCreateDisabled = isCreating || isLoading || !newSiteName.trim()

  return (
    <section className={`w-full ${className}`}>
      <div className="rounded-2xl border border-light-white3 bg-light-white1 p-4 sm:p-5">
        <div className="flex flex-col gap-4">
          <div className="flex flex-col gap-1">
            <h2 className="text-2xl font-semibold text-light-black">Mes Sites</h2>
            <p className="text-sm text-light-white4">
              Cree, affiche et supprime tes sites depuis le dashboard.
            </p>
          </div>

          <form onSubmit={handleCreate} className="flex flex-col gap-3 sm:flex-row sm:items-end">
            <Input
              id="new-site-name"
              label="Nom du site"
              placeholder="Ex: Portfolio Agence"
              variant="search"
              fullWidth
              value={newSiteName}
              onChange={(event) => setNewSiteName(event.target.value)}
            />
            <Button
              type="submit"
              variant="board"
              size="md"
              className="w-full sm:w-auto"
              isLoading={isCreating}
              disabled={isCreateDisabled}
            >
              Creer
            </Button>
          </form>

          {error ? (
            <Alert
              status="error"
              theme="light"
              title="Erreur de chargement"
              message={error}
            />
          ) : null}

          {isLoading ? (
            <div className="rounded-xl border border-light-white3 bg-light-white2 p-4">
              <LoadingSpinner theme="light" size="M" label="Chargement des sites..." />
            </div>
          ) : null}

          {!isLoading && sites.length === 0 ? (
            <Alert
              status="info"
              theme="light"
              title="Aucun site pour le moment"
              message="Ajoute ton premier site avec le formulaire ci-dessus."
            />
          ) : null}

          {!isLoading && sites.length > 0 ? (
            <ResponsiveGrid size="L" theme="transparent" width="full">
              {sites.map((site, index) => {
                const siteId = site.id ?? site._id ?? site.siteId ?? index
                const isDeleting = deletingId === siteId
                const siteName = site.name || site.title || 'Site sans nom'
                const siteDescription =
                  site.description ||
                  (site.createdAt
                    ? `Cree le ${new Date(site.createdAt).toLocaleDateString('fr-FR')}`
                    : 'Aucune description disponible.')

                return (
                  <article
                    key={siteId}
                    className="rounded-[18px] border border-light-white3 bg-light-white1 p-4 shadow-sm"
                  >
                    <div className="mb-3 inline-flex items-center rounded-full bg-light-white2 px-2.5 py-1 text-xs font-medium text-light-red1">
                      {siteId}
                    </div>
                    <h3 className="text-lg font-semibold text-light-black">{siteName}</h3>
                    <p className="mt-2 text-sm text-light-white4">{siteDescription}</p>
                    <div className="mt-4 flex items-center justify-end gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        className="h-9"
                        onClick={() => handleDelete(siteId)}
                        isLoading={isDeleting}
                        disabled={isDeleting}
                      >
                        Supprimer
                      </Button>
                    </div>
                  </article>
                )
              })}
            </ResponsiveGrid>
          ) : null}
        </div>
      </div>
    </section>
  )
}

export default SiteList