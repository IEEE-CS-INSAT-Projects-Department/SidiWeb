import '../../styles-tailwind.css'

const themeStyles = {
	dark: {
		container: 'bg-vitrine-black2 border-vitrine-grey3',
		title: 'text-vitrine-white1',
		text: 'text-vitrine-grey1',
		iconWrap: 'bg-vitrine-grey3/60',
		button: 'text-vitrine-grey1 hover:text-vitrine-white1',
	},
	light: {
		container: 'bg-light-white1 border-light-white3',
		title: 'text-light-black',
		text: 'text-light-white4',
		iconWrap: 'bg-light-white2',
		button: 'text-light-white4 hover:text-light-black',
	},
}

const statusStyles = {
	info: {
		accent: 'border-l-vitrine-grey1',
		icon: 'text-vitrine-grey1',
	},
	success: {
		accent: 'border-l-dark-red3',
		icon: 'text-dark-red3',
	},
	warning: {
		accent: 'border-l-light-red3',
		icon: 'text-light-red3',
	},
	error: {
		accent: 'border-l-light-red1',
		icon: 'text-light-red1',
	},
}

const statusIcons = {
	info: 'ℹ',
	success: '✓',
	warning: '⚠',
	error: '✕',
}

const statusTitles = {
	info: 'Information',
	success: 'Success',
	warning: 'Warning',
	error: 'Error',
}

export const Toast = ({
	theme = 'dark',
	status = 'info',
	title,
	message = '',
	description,
	icon,
	showClose = true,
	onClose,
	children,
	className = '',
	...rest
}) => {
	const selectedTheme = themeStyles[theme] || themeStyles.dark
	const normalizedStatus = typeof status === 'string' ? status.toLowerCase() : 'info'
	const selectedStatus = statusStyles[normalizedStatus] || statusStyles.info
	const selectedIcon = icon || statusIcons[normalizedStatus] || statusIcons.info
	const resolvedTitle = title || statusTitles[normalizedStatus] || statusTitles.info
	const resolvedMessage = message || description
	const semanticRole = normalizedStatus === 'error' ? 'alert' : 'status'
	const canClose = showClose && typeof onClose === 'function'

	return (
		<article
			className={`w-full max-w-md border border-l-4 rounded-[12px] px-4 py-3 shadow-sm ${selectedTheme.container} ${selectedStatus.accent} ${className}`}
			role={semanticRole}
			aria-live={semanticRole === 'alert' ? 'assertive' : 'polite'}
			{...rest}
		>
			<div className="flex items-start gap-3">
				<span
					className={`w-8 h-8 rounded-md flex items-center justify-center text-sm font-semibold ${selectedTheme.iconWrap} ${selectedStatus.icon}`}
					aria-hidden="true"
				>
					{selectedIcon}
				</span>

				<div className="min-w-0 flex-1">
					<h4 className={`text-sm font-semibold ${selectedTheme.title}`}>{resolvedTitle}</h4>
					{resolvedMessage ? <p className={`mt-1 text-sm ${selectedTheme.text}`}>{resolvedMessage}</p> : null}
					{children ? <div className="mt-2">{children}</div> : null}
				</div>

				{canClose ? (
					<button
						type="button"
						onClick={onClose}
						className={`text-base leading-none transition duration-200 cursor-pointer ${selectedTheme.button}`}
						aria-label="Close notification"
					>
						×
					</button>
				) : null}
			</div>
		</article>
	)
}

export default Toast
