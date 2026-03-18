import '../../styles-tailwind.css'

const themeStyles = {
	dark: {
		container: 'bg-dark-grey3 border-dark-grey2',
		title: 'text-dark-white1',
		text: 'text-dark-grey1',
		iconWrap: 'bg-dark-grey2',
	},
	light: {
		container: 'bg-light-white1 border-light-white3',
		title: 'text-light-black',
		text: 'text-light-white4',
		iconWrap: 'bg-light-white2',
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

export const Alert = ({
	theme = 'light',
	status = 'info',
	title,
	message = '',
	description,
	icon,
	actions,
	children,
	className = '',
	...rest
}) => {
	const selectedTheme = themeStyles[theme] || themeStyles.light
	const normalizedStatus = typeof status === 'string' ? status.toLowerCase() : 'info'
	const selectedStatus = statusStyles[normalizedStatus] || statusStyles.info
	const selectedIcon = icon || statusIcons[normalizedStatus] || statusIcons.info
	const resolvedTitle = title || statusTitles[normalizedStatus] || statusTitles.info
	const resolvedMessage = message || description
	const semanticRole = normalizedStatus === 'error' || normalizedStatus === 'warning' ? 'alert' : 'status'

	return (
		<article
			className={`w-full border rounded-[12px] border-l-4 p-4 ${selectedTheme.container} ${selectedStatus.accent} ${className}`}
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
					{actions ? <div className="mt-3 flex flex-wrap gap-2">{actions}</div> : null}
				</div>
			</div>
		</article>
	)
}

export default Alert
