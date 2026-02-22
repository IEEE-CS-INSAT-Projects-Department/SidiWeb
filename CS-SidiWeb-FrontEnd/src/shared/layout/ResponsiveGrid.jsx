import '../../styles-tailwind.css'

const themeStyles = {
	dark: 'bg-vitrine-black2',
	light: 'bg-light-white2',
	transparent: 'bg-transparent',
}

const sizeStyles = {
	M: 'grid-cols-1 md:grid-cols-2 gap-4',
	L: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5',
	XL: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6',
}

const widthStyles = {
	compact: 'max-w-5xl',
	full: 'max-w-7xl',
}

export const ResponsiveGrid = ({
	children,
	theme = 'transparent',
	size = 'L',
	width = 'full',
	as = 'section',
	className = '',
	...rest
}) => {
	const Component = as
	const selectedTheme = themeStyles[theme] || themeStyles.transparent
	const normalizedSize = typeof size === 'string' ? size.toUpperCase() : 'L'
	const selectedSize = sizeStyles[normalizedSize] || sizeStyles.L
	const selectedWidth = widthStyles[width] || widthStyles.full

	return (
		<Component className={`w-full ${selectedTheme} ${className}`} {...rest}>
			<div className={`mx-auto w-full ${selectedWidth}`}>
				<div className={`grid ${selectedSize}`}>{children}</div>
			</div>
		</Component>
	)
}

export default ResponsiveGrid
