import { useEffect, useRef, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import '../../../styles-tailwind.css'
import AppShell from '../../../shared/layout/AppShell'
import { Button } from '../../../shared/components/Button'
import { Alert } from '../../../shared/components/Alert'
import LoadingSpinner from '../../../shared/components/LoadingSpinner'
import { getSite, updateSite } from '../../home/services/siteService'

const BLOCK_TYPES = [
	{ type: 'heading', label: 'Heading', defaults: { text: 'Main heading' } },
	{ type: 'paragraph', label: 'Text', defaults: { text: 'Your text here…' } },
	{ type: 'image', label: 'Image', defaults: { url: '', alt: 'Image' } },
	{ type: 'button', label: 'Button', defaults: { label: 'Click here', href: '#' } },
	{ type: 'divider', label: 'Divider', defaults: {} },
	{ type: 'contact', label: 'Contact', defaults: { title: 'Contact us' } },
]

const DEVICE_WIDTH = { desktop: '100%', tablet: '768px', mobile: '375px' }

const newId = () =>
	typeof crypto !== 'undefined' && crypto.randomUUID ? crypto.randomUUID() : String(Date.now() + Math.random())

function BlockPreview({ block }) {
	const { type, data } = block
	if (type === 'heading') return <h2 className="text-2xl font-bold text-gray-900">{data.text}</h2>
	if (type === 'paragraph') return <p className="text-gray-700">{data.text}</p>
	if (type === 'image')
		return data.url ? (
			<img src={data.url} alt={data.alt} className="max-h-60 w-full rounded-lg object-cover" />
		) : (
			<div className="flex h-32 items-center justify-center rounded-lg bg-gray-100 text-sm text-gray-400">
				Image (add a URL)
			</div>
		)
	if (type === 'button')
		return (
			<a
				href={data.href}
				onClick={(e) => e.preventDefault()}
				className="inline-block rounded-lg bg-red-600 px-4 py-2 font-medium text-white"
			>
				{data.label}
			</a>
		)
	if (type === 'divider') return <hr className="border-gray-200" />
	if (type === 'contact')
		return (
			<div className="rounded-lg border border-gray-200 p-4">
				<h3 className="mb-3 font-semibold text-gray-900">{data.title}</h3>
				<div className="flex flex-col gap-2">
					<input className="h-9 rounded border border-gray-300 px-3 text-sm" placeholder="Name" disabled />
					<input className="h-9 rounded border border-gray-300 px-3 text-sm" placeholder="Email" disabled />
					<button className="h-9 rounded bg-red-600 text-sm text-white" disabled>
						Send
					</button>
				</div>
			</div>
		)
	return null
}

function BlockEditor({ block, onChange }) {
	const set = (key, value) => onChange({ ...block, data: { ...block.data, [key]: value } })
	const inputClass =
		'w-full rounded-md border border-light-white3 bg-light-white1 px-3 py-2 text-sm focus:border-light-red1 focus:outline-none focus:ring-2 focus:ring-light-red1/20'
	if (block.type === 'heading' || block.type === 'paragraph' || block.type === 'contact') {
		const key = block.type === 'contact' ? 'title' : 'text'
		return (
			<textarea
				rows={block.type === 'paragraph' ? 3 : 1}
				className={inputClass}
				value={block.data[key] || ''}
				onChange={(e) => set(key, e.target.value)}
			/>
		)
	}
	if (block.type === 'image') {
		return (
			<div className="flex flex-col gap-2">
				<input className={inputClass} placeholder="Image URL" value={block.data.url || ''} onChange={(e) => set('url', e.target.value)} />
				<input className={inputClass} placeholder="Alt text" value={block.data.alt || ''} onChange={(e) => set('alt', e.target.value)} />
			</div>
		)
	}
	if (block.type === 'button') {
		return (
			<div className="flex flex-col gap-2">
				<input className={inputClass} placeholder="Label" value={block.data.label || ''} onChange={(e) => set('label', e.target.value)} />
				<input className={inputClass} placeholder="Link (href)" value={block.data.href || ''} onChange={(e) => set('href', e.target.value)} />
			</div>
		)
	}
	return <p className="text-xs text-light-white4">No options</p>
}

export default function Editor() {
	const { id } = useParams()
	const navigate = useNavigate()
	const [site, setSite] = useState(null)
	const [blocks, setBlocks] = useState([])
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState('')
	const [status, setStatus] = useState('')
	const [saving, setSaving] = useState(false)
	const [device, setDevice] = useState('desktop')
	const dragIndex = useRef(null)

	useEffect(() => {
		let active = true
		;(async () => {
			try {
				const data = await getSite(id)
				if (!active) return
				setSite(data)
				setBlocks(Array.isArray(data?.content?.blocks) ? data.content.blocks : [])
			} catch (e) {
				if (active) setError(e.message)
			} finally {
				if (active) setLoading(false)
			}
		})()
		return () => {
			active = false
		}
	}, [id])

	const addBlock = (type) => {
		const def = BLOCK_TYPES.find((b) => b.type === type)
		setBlocks((prev) => [...prev, { id: newId(), type, data: { ...def.defaults } }])
		setStatus('')
	}
	const updateBlock = (index, next) => setBlocks((prev) => prev.map((b, i) => (i === index ? next : b)))
	const removeBlock = (index) => setBlocks((prev) => prev.filter((_, i) => i !== index))
	const move = (index, delta) => {
		setBlocks((prev) => {
			const next = [...prev]
			const target = index + delta
			if (target < 0 || target >= next.length) return prev
			;[next[index], next[target]] = [next[target], next[index]]
			return next
		})
	}
	const onDrop = (index) => {
		const from = dragIndex.current
		dragIndex.current = null
		if (from === null || from === index) return
		setBlocks((prev) => {
			const next = [...prev]
			const [moved] = next.splice(from, 1)
			next.splice(index, 0, moved)
			return next
		})
	}

	const save = async () => {
		setSaving(true)
		setError('')
		setStatus('')
		try {
			const updated = await updateSite(id, { content: { blocks } })
			setSite(updated)
			setStatus('Saved ✓')
		} catch (e) {
			setError(e.message)
		} finally {
			setSaving(false)
		}
	}

	const publish = async () => {
		setSaving(true)
		setError('')
		try {
			const updated = await updateSite(id, { content: { blocks }, published: true })
			setSite(updated)
			setStatus(updated.public_url ? `Published: ${updated.public_url}` : 'Published ✓')
		} catch (e) {
			setError(e.message)
		} finally {
			setSaving(false)
		}
	}

	if (loading) {
		return (
			<AppShell title="Editor">
				<LoadingSpinner theme="light" label="Loading site..." />
			</AppShell>
		)
	}

	if (error && !site) {
		return (
			<AppShell title="Editor">
				<Alert theme="light" status="error" message={error} />
				<Link to="/dashboard" className="mt-4 inline-block text-sm text-light-red1 hover:underline">
					← Back to dashboard
				</Link>
			</AppShell>
		)
	}

	return (
		<AppShell
			title={`Editor — ${site?.name || ''}`}
			subtitle={site?.published ? 'Published' : 'Draft'}
			actions={
				<div className="flex items-center gap-2">
					<Button variant="outline" size="sm" isLoading={saving} onClick={save}>
						Save
					</Button>
					<Button variant="primary" size="sm" isLoading={saving} onClick={publish}>
						Publish
					</Button>
				</div>
			}
		>
			{error ? (
				<div className="mb-4">
					<Alert theme="light" status="error" message={error} />
				</div>
			) : null}
			{status ? (
				<div className="mb-4">
					<Alert theme="light" status="success" message={status} />
				</div>
			) : null}

			<div className="grid grid-cols-1 gap-6 lg:grid-cols-[380px_1fr]">
				{/* Editing panel */}
				<div className="flex flex-col gap-4">
					<div className="rounded-2xl border border-light-white3 bg-light-white1 p-4">
						<p className="mb-2 text-sm font-semibold">Add a block</p>
						<div className="flex flex-wrap gap-2">
							{BLOCK_TYPES.map((b) => (
								<button
									key={b.type}
									type="button"
									onClick={() => addBlock(b.type)}
									className="rounded-lg border border-light-white3 px-3 py-1.5 text-sm text-light-black hover:border-light-red1 hover:text-light-red1"
								>
									+ {b.label}
								</button>
							))}
						</div>
					</div>

					{blocks.length === 0 ? (
						<p className="text-sm text-light-white4">No blocks yet. Add one to get started.</p>
					) : (
						blocks.map((block, index) => (
							<div
								key={block.id}
								draggable
								onDragStart={() => (dragIndex.current = index)}
								onDragOver={(e) => e.preventDefault()}
								onDrop={() => onDrop(index)}
								className="rounded-2xl border border-light-white3 bg-light-white1 p-4"
							>
								<div className="mb-2 flex items-center justify-between">
									<span className="cursor-grab text-xs font-semibold uppercase text-light-white4">
										⠿ {block.type}
									</span>
									<div className="flex items-center gap-1">
										<button type="button" onClick={() => move(index, -1)} className="px-1.5 text-light-white4 hover:text-light-black" aria-label="Move up">↑</button>
										<button type="button" onClick={() => move(index, 1)} className="px-1.5 text-light-white4 hover:text-light-black" aria-label="Move down">↓</button>
										<button type="button" onClick={() => removeBlock(index)} className="px-1.5 text-light-red1 hover:underline" aria-label="Delete">✕</button>
									</div>
								</div>
								<BlockEditor block={block} onChange={(next) => updateBlock(index, next)} />
							</div>
						))
					)}
				</div>

				{/* Live preview */}
				<div>
					<div className="mb-3 flex items-center gap-2">
						<span className="text-sm text-light-white4">Preview:</span>
						{['desktop', 'tablet', 'mobile'].map((d) => (
							<button
								key={d}
								type="button"
								onClick={() => setDevice(d)}
								className={`rounded-lg border px-3 py-1 text-sm capitalize ${
									device === d
										? 'border-light-red1 bg-light-red1/10 text-light-red1'
										: 'border-light-white3 text-light-white4 hover:text-light-black'
								}`}
							>
								{d}
							</button>
						))}
					</div>
					<div className="rounded-2xl border border-light-white3 bg-light-white2 p-4">
						<div
							className="mx-auto rounded-xl bg-white p-6 shadow-sm transition-all"
							style={{ maxWidth: DEVICE_WIDTH[device] }}
						>
							{blocks.length === 0 ? (
								<p className="py-16 text-center text-sm text-gray-400">
									Your site preview will appear here.
								</p>
							) : (
								<div className="flex flex-col gap-4">
									{blocks.map((block) => (
										<BlockPreview key={block.id} block={block} />
									))}
								</div>
							)}
						</div>
					</div>
				</div>
			</div>
		</AppShell>
	)
}
