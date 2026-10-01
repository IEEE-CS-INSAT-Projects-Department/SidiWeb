import '../../styles-tailwind.css'

const toneStyles = {
  light:
    'bg-light-white1 text-light-black placeholder-light-white4 border border-light-white3 focus:outline-none focus:ring-2 focus:ring-light-red1/20 focus:border-light-red1',
  dark:
    'bg-dark-grey2 text-dark-white1 placeholder-dark-grey1 border border-dark-grey3 focus:outline-none focus:ring-2 focus:ring-dark-red1/30 focus:border-dark-red1',
}

const sizeStyles = {
  compact: 'h-8 px-3 text-sm rounded-[6px]',
  sm: 'h-11 px-4 text-sm rounded-[8px]',
  md: 'h-12 px-4 text-base rounded-[12px]',
  lg: 'h-14 px-4 text-base rounded-[12px]',
  chat: 'h-14 px-4 text-sm rounded-[12px]',
  multiline: 'min-h-36 px-4 py-3 text-base rounded-[12px]',
}

const variantConfig = {
  search: { tone: 'light', size: 'compact', fullWidth: false, control: 'bg-light-white2' },
  auth: { tone: 'dark', size: 'md', fullWidth: true },
  auth_password: { tone: 'dark', size: 'md', fullWidth: true },
  chat: { tone: 'dark', size: 'chat', fullWidth: true, control: 'bg-dark-grey3 border-dark-grey2' },
  multiline: { tone: 'dark', size: 'multiline', fullWidth: true, as: 'textarea' },
  input_auth_small: { tone: 'dark', size: 'sm', fullWidth: true },
  input_auth_medium: { tone: 'dark', size: 'md', fullWidth: true },
  input_auth_large: { tone: 'dark', size: 'multiline', fullWidth: true, as: 'textarea' },
}

export const Input = ({
  variant = 'search',
  size,
  label,
  helperText,
  error,
  className = '',
  inputClassName = '',
  fullWidth,
  startAdornment,
  endAdornment,
  as,
  type = 'text',
  id,
  placeholder,
  ...rest
}) => {
  const normalizedVariant = typeof variant === 'string' ? variant.toLowerCase() : 'search'
  const selectedVariant = variantConfig[normalizedVariant] || variantConfig.search
  const selectedTone = toneStyles[selectedVariant.tone] || toneStyles.light
  const resolvedSize = size || selectedVariant.size || 'md'
  const selectedSize = sizeStyles[resolvedSize] || sizeStyles.md
  const resolvedFullWidth = typeof fullWidth === 'boolean' ? fullWidth : selectedVariant.fullWidth
  const widthClass = resolvedFullWidth ? 'w-full' : 'w-fit'
  const stateClass = error
    ? 'border-light-red1 ring-2 ring-light-red1/20 focus:ring-light-red1/30 focus:border-light-red1'
    : ''
  const variantControlClass = selectedVariant.control || ''
  const withStartAdornment = startAdornment ? 'pl-11' : ''
  const withEndAdornment = endAdornment ? 'pr-11' : ''
  const elementType = as || selectedVariant.as || 'input'
  const labelColor = selectedVariant.tone === 'dark' ? 'text-dark-white1' : 'text-light-black'
  const helperColor = selectedVariant.tone === 'dark' ? 'text-dark-grey1' : 'text-light-white4'

  const controlClass = `${selectedTone} ${selectedSize} ${variantControlClass} ${widthClass} ${stateClass} ${withStartAdornment} ${withEndAdornment} transition duration-300 ease-in-out ${inputClassName}`

  const renderControl = () => {
    if (elementType === 'textarea') {
      const rows = typeof rest.rows === 'number' ? rest.rows : 4
      return (
        <textarea
          id={id}
          placeholder={placeholder}
          className={`${controlClass} resize-none align-top`}
          rows={rows}
          {...rest}
        />
      )
    }

    return (
      <input
        id={id}
        type={type}
        placeholder={placeholder}
        className={controlClass}
        {...rest}
      />
    )
  }

  return (
    <div className={`flex flex-col gap-1.5 ${widthClass} ${className}`}>
      {label ? (
        <label htmlFor={id} className={`text-sm font-medium ${labelColor}`}>
          {label}
        </label>
      ) : null}

      <div className="relative">
        {startAdornment ? (
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-dark-grey1" aria-hidden="true">
            {startAdornment}
          </span>
        ) : null}

        {renderControl()}

        {endAdornment ? (
          <span className="absolute right-3 top-1/2 -translate-y-1/2 text-dark-grey1" aria-hidden="true">
            {endAdornment}
          </span>
        ) : null}
      </div>

      {error ? <p className="text-xs text-light-red3">{error}</p> : null}
      {!error && helperText ? <p className={`text-xs ${helperColor}`}>{helperText}</p> : null}
    </div>
  )
}

export default Input
