import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../../../styles-tailwind.css'
import AppShell from '../../../shared/layout/AppShell'
import { Button } from '../../../shared/components/Button'
import { Alert } from '../../../shared/components/Alert'
import LoadingSpinner from '../../../shared/components/LoadingSpinner'
import { getRecommendations } from '../services/recommendationService'
import { createSite } from '../../home/services/siteService'

const SECTORS = ['portfolio', 'entreprise', 'education', 'artisan', 'evenement', 'freelance', 'service', 'association', 'startup', 'landing', 'cv', 'vitrine']
const STYLES = ['moderne', 'classique', 'minimaliste']
const COLORS = ['bleu', 'rouge', 'vert', 'noir', 'pastel']

function Field({ label, children }) {
	return (
		<label className="flex flex-col gap-1.5">
			<span className="text-sm font-medium text-light-black">{label}</span>
			{children}
		</label>
	)
}

const selectClass =
	'h-11 rounded-[10px] border border-light-white3 bg-light-white1 px-3 text-sm text-light-black focus:border-light-red1 focus:outline-none focus:ring-2 focus:ring-light-red1/20'

export default function Assistant() {
	const navigate = useNavigate()
	const [sector, setSector] = useState('portfolio')
	const [style, setStyle] = useState('moderne')
	const [color, setColor] = useState('bleu')
	const [contact, setContact] = useState(true)
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState('')
	const [result, setResult] = useState(null)
	const [feedback, setFeedback] = useState({})

	const submit = async (e) => {
		e.preventDefault()
		setLoading(true)
		setError('')
		setResult(null)
		try {
			const preferences = [`couleur ${color}`, contact ? 'formulaire de contact' : '']
				.filter(Boolean)
				.join(', ')
			const r = await getRecommendations({ category: sector, style, preferences })
			setResult(r)
		} catch (err) {
			setError(err.message)
		} finally {
			setLoading(false)
		}
	}

	const useTemplate = async (templateId) => {
		setError('')
		try {
			const site = await createSite({ name: `Site ${sector}`, template_id: templateId })
			navigate(`/editor/${site.id || site._id}`)
		} catch (err) {
			setError(err.message)
		}
	}

	const templates = result?.recommended_templates || []
	const palette = result?.recommended_palette
	const fonts = result?.recommended_fonts

	return (
		<AppShell
			title="Assistant de démarrage"
			subtitle="Quelques questions pour des recommandations personnalisées"
		>
			<div className="grid grid-cols-1 gap-6 lg:grid-cols-[360px_1fr]">
				<form
					onSubmit={submit}
					className="flex flex-col gap-4 rounded-2xl border border-light-white3 bg-light-white1 p-5"
				>
					<Field label="Quel est le secteur de votre activité ?">
						<select className={selectClass} value={sector} onChange={(e) => setSector(e.target.value)}>
							{SECTORS.map((s) => (
								<option key={s} value={s} className="capitalize">
									{s}
								</option>
							))}
						</select>
					</Field>

					<Field label="Quel style préférez-vous ?">
						<select className={selectClass} value={style} onChange={(e) => setStyle(e.target.value)}>
							{STYLES.map((s) => (
								<option key={s} value={s}>
									{s}
								</option>
							))}
						</select>
					</Field>

					<Field label="Couleur dominante souhaitée ?">
						<select className={selectClass} value={color} onChange={(e) => setColor(e.target.value)}>
							{COLORS.map((c) => (
								<option key={c} value={c}>
									{c}
								</option>
							))}
						</select>
					</Field>

					<label className="flex items-center gap-2 text-sm text-light-black">
						<input
							type="checkbox"
							checked={contact}
							onChange={(e) => setContact(e.target.checked)}
							className="h-4 w-4 accent-[color:var(--color-light-red1,#c0392b)]"
						/>
						Besoin d'un formulaire de contact
					</label>

					<Button type="submit" variant="primary" fullWidth isLoading={loading}>
						Obtenir des recommandations
					</Button>
				</form>

				<div>
					{error ? (
						<div className="mb-4">
							<Alert theme="light" status="error" message={error} />
						</div>
					) : null}

					{loading ? <LoadingSpinner theme="light" label="Analyse de vos réponses..." /> : null}

					{!loading && !result ? (
						<div className="rounded-2xl border border-dashed border-light-white3 p-10 text-center text-sm text-light-white4">
							Remplissez le questionnaire pour voir vos recommandations.
						</div>
					) : null}

					{result ? (
						<div className="flex flex-col gap-6">
							<section>
								<h2 className="mb-3 text-lg font-semibold">Templates recommandés</h2>
								<div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
									{templates.map((t) => (
										<article
											key={t.id}
											className="rounded-2xl border border-light-white3 bg-light-white1 p-4"
										>
											<h3 className="font-semibold">{t.id}</h3>
											<p className="mt-1 text-sm text-light-white4">{t.reason}</p>
											<div className="mt-3 flex items-center gap-2">
												<Button variant="primary" size="sm" onClick={() => useTemplate(t.id)}>
													Utiliser
												</Button>
												<button
													type="button"
													aria-label="J'aime"
													onClick={() => setFeedback((f) => ({ ...f, [t.id]: 'up' }))}
													className={`rounded-lg border px-2 py-1 text-sm ${
														feedback[t.id] === 'up'
															? 'border-light-red1 text-light-red1'
															: 'border-light-white3 text-light-white4'
													}`}
												>
													👍
												</button>
												<button
													type="button"
													aria-label="Je n'aime pas"
													onClick={() => setFeedback((f) => ({ ...f, [t.id]: 'down' }))}
													className={`rounded-lg border px-2 py-1 text-sm ${
														feedback[t.id] === 'down'
															? 'border-light-red1 text-light-red1'
															: 'border-light-white3 text-light-white4'
													}`}
												>
													👎
												</button>
											</div>
										</article>
									))}
								</div>
							</section>

							{palette ? (
								<section>
									<h2 className="mb-2 text-lg font-semibold">Palette suggérée</h2>
									<div className="rounded-2xl border border-light-white3 bg-light-white1 p-4">
										<p className="text-sm font-medium">{palette.id}</p>
										<p className="mt-1 text-sm text-light-white4">{palette.reason}</p>
										{Array.isArray(palette.colors) ? (
											<div className="mt-3 flex gap-2">
												{palette.colors.map((hex) => (
													<span
														key={hex}
														title={hex}
														className="h-8 w-8 rounded-md border border-light-white3"
														style={{ backgroundColor: hex }}
													/>
												))}
											</div>
										) : null}
									</div>
								</section>
							) : null}

							{fonts ? (
								<section>
									<h2 className="mb-2 text-lg font-semibold">Polices suggérées</h2>
									<div className="rounded-2xl border border-light-white3 bg-light-white1 p-4 text-sm">
										<p>
											<span className="text-light-white4">Titres :</span> {fonts.heading}
										</p>
										<p className="mt-1">
											<span className="text-light-white4">Corps :</span> {fonts.body}
										</p>
										{fonts.reason ? (
											<p className="mt-2 text-light-white4">{fonts.reason}</p>
										) : null}
									</div>
								</section>
							) : null}
						</div>
					) : null}
				</div>
			</div>
		</AppShell>
	)
}
