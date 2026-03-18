import '../../styles-tailwind.css'

const variantStyles = {
  primary: 'bg-light-red1 text-light-white1 font-semibold hover:bg-light-red2',
  outline: 'border border-light-red1 text-light-red1 font-semibold hover:bg-light-red1/10',
  social: 'border border-light-white3 bg-light-white1 text-light-black font-medium hover:bg-light-white2',
  ghost: 'text-light-black hover:bg-light-white2',
  login: 'border-2 border-light-red1 text-light-red1 font-semibold hover:bg-light-red1/10',
  signup: 'bg-light-red1 text-light-white1 font-semibold hover:bg-light-red2',
  demo: 'bg-vitrine-grey2 text-vitrine-white1 font-medium hover:bg-vitrine-grey3',
  submit: 'bg-dark-red1 text-dark-white1 font-semibold hover:bg-dark-red2',
  board: 'bg-light-red1 text-light-white1 font-medium hover:bg-light-red2',
  authPrimary: 'bg-light-red1 text-light-white1 font-semibold hover:bg-light-red2',
  authOutline: 'border border-light-red1 text-light-red1 font-semibold hover:bg-light-red1/10',
}

const sizeStyles = {
  xs: 'h-9 px-3 text-xs rounded-lg',
  sm: 'h-10 px-4 text-sm rounded-xl',
  md: 'h-11 px-5 text-sm rounded-xl',
  lg: 'h-12 px-6 text-base rounded-2xl',
  nav: 'h-12 px-6 text-base rounded-[20px]',
  auth: 'h-12 px-4 text-[0.95rem] rounded-[12px]',
}

const defaultSizeByVariant = {
  primary: 'md',
  outline: 'md',
  social: 'auth',
  ghost: 'md',
  login: 'nav',
  signup: 'nav',
  demo: 'md',
  submit: 'auth',
  board: 'md',
  authPrimary: 'auth',
  authOutline: 'auth',
}

export const Button = ({
  variant = 'primary',
  size,
  fullWidth = false,
  isLoading = false,
  leftIcon,
  rightIcon,
  className = '',
  type = 'button',
  disabled = false,
  children,
  ...rest
}) => {
  const variantClass = variantStyles[variant] || variantStyles.primary
  const resolvedSize = size || defaultSizeByVariant[variant] || 'md'
  const sizeClass = sizeStyles[resolvedSize] || sizeStyles.md
  const widthClass = fullWidth ? 'w-full' : 'w-fit'

  return (
    <button
      type={type}
      className={`${variantClass} ${sizeClass} ${widthClass} inline-flex items-center justify-center gap-2 whitespace-nowrap transition duration-300 ease-in-out disabled:cursor-not-allowed disabled:opacity-60 active:scale-[0.99] ${className}`}
      disabled={isLoading || disabled}
      {...rest}
    >
      {isLoading ? (
        <span
          className="w-4 h-4 rounded-full border-2 border-current border-r-transparent animate-spin"
          aria-hidden="true"
        />
      ) : null}
      {leftIcon && !isLoading ? <span aria-hidden="true">{leftIcon}</span> : null}
      <span>{children}</span>
      {rightIcon ? <span aria-hidden="true">{rightIcon}</span> : null}
    </button>
  )
}

export default Button

