import { createContext, useCallback, useContext, useState } from 'react'
import '../../styles-tailwind.css'
import Toast from './Toast'

const ToastContext = createContext(null)

export function useToast() {
	return useContext(ToastContext) || { show: () => {}, success: () => {}, error: () => {}, info: () => {} }
}

export function ToastProvider({ children }) {
	const [toasts, setToasts] = useState([])

	const remove = useCallback((id) => {
		setToasts((list) => list.filter((t) => t.id !== id))
	}, [])

	const show = useCallback(
		(message, status = 'info', title) => {
			const id = `${Date.now()}-${Math.random()}`
			setToasts((list) => [...list, { id, message, status, title }])
			setTimeout(() => remove(id), 4000)
		},
		[remove]
	)

	const api = {
		show,
		success: (m, t) => show(m, 'success', t),
		error: (m, t) => show(m, 'error', t),
		info: (m, t) => show(m, 'info', t),
	}

	return (
		<ToastContext.Provider value={api}>
			{children}
			<div className="pointer-events-none fixed right-4 top-4 z-[100] flex w-[min(92vw,360px)] flex-col gap-2">
				{toasts.map((t) => (
					<div key={t.id} className="animate-rise pointer-events-auto">
						<Toast
							theme="light"
							status={t.status}
							title={t.title}
							message={t.message}
							onClose={() => remove(t.id)}
						/>
					</div>
				))}
			</div>
		</ToastContext.Provider>
	)
}

export default ToastProvider
