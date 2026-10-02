import { useEffect } from 'react'
import '../../styles-tailwind.css'
import { Button } from './Button'

export default function ConfirmDialog({
	open,
	title = 'Are you sure?',
	message,
	confirmLabel = 'Confirm',
	cancelLabel = 'Cancel',
	onConfirm,
	onCancel,
	busy = false,
}) {
	useEffect(() => {
		if (!open) return
		const onKey = (e) => {
			if (e.key === 'Escape') onCancel?.()
		}
		window.addEventListener('keydown', onKey)
		return () => window.removeEventListener('keydown', onKey)
	}, [open, onCancel])

	if (!open) return null

	return (
		<div
			className="animate-fade fixed inset-0 z-[110] flex items-center justify-center bg-light-black/40 p-4 backdrop-blur-sm"
			role="dialog"
			aria-modal="true"
			onClick={onCancel}
		>
			<div
				className="animate-rise w-full max-w-sm rounded-2xl border border-light-white3 bg-light-white1 p-5 shadow-xl"
				onClick={(e) => e.stopPropagation()}
			>
				<h3 className="text-lg font-semibold text-light-black">{title}</h3>
				{message ? <p className="mt-1.5 text-sm text-light-white4">{message}</p> : null}
				<div className="mt-5 flex justify-end gap-2">
					<Button variant="outline" size="sm" onClick={onCancel} disabled={busy}>
						{cancelLabel}
					</Button>
					<Button variant="primary" size="sm" onClick={onConfirm} isLoading={busy}>
						{confirmLabel}
					</Button>
				</div>
			</div>
		</div>
	)
}
