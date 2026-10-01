import '../../styles-tailwind.css'

const themeStyles = {
	dark: {
		track: 'border-dark-grey2',
		head: 'border-t-dark-red1',
		text: 'text-dark-white1',
	},
	light: {
		track: 'border-light-white3',
		head: 'border-t-light-red1',
		text: 'text-light-black',
	},
}

const sizeStyles = {
	M: 'w-10 h-10 border-4',
	L: 'w-14 h-14 border-4',
	XL: 'w-20 h-20 border-[5px]',
}

export const LoadingSpinner = ({ theme = 'dark', size = 'L', label = 'Chargement...', className = '' }) => {
	const selectedTheme = themeStyles[theme] || themeStyles.dark
	const normalizedSize = typeof size === 'string' ? size.toUpperCase() : 'L'
	const selectedSize = sizeStyles[normalizedSize] || sizeStyles.L

	return (
		<div className={`inline-flex items-center gap-3 ${className}`} role="status" aria-live="polite">
			<span
				className={`animate-spin rounded-full border-solid ${selectedTheme.track} ${selectedTheme.head} ${selectedSize}`}
				aria-hidden="true"
			/>
			{label ? <span className={`text-sm font-medium ${selectedTheme.text}`}>{label}</span> : null}
		</div>
	)
}

export default LoadingSpinner
