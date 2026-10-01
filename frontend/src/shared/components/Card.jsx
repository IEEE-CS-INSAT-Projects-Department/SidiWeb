import '../../styles-tailwind.css'

const variantStyles = {
  dark_step: 'bg-vitrine-black2 text-vitrine-white1 border border-vitrine-grey3',
  dark_image: 'bg-vitrine-black2 text-vitrine-white1 border border-vitrine-grey3',
  light_image: 'bg-light-white1 text-light-black border border-light-white3',
  auth_form: 'bg-dark-grey3 text-dark-white1 border border-dark-grey2 shadow-lg',
}

const layoutStyles = {
  dark_step: 'p-5 rounded-[16px] min-h-[120px]',
  dark_image: 'p-4 rounded-[18px]',
  light_image: 'p-4 rounded-[16px]',
  auth_form: 'p-6 md:p-8 rounded-[20px] w-full max-w-[480px]',
}

const normalizedVariantName = (variant) => {
  if (typeof variant !== 'string') {
    return 'dark_step'
  }

  const normalized = variant.toLowerCase().replace('-', '_')

  if (normalized === 'auth' || normalized === 'authform') {
    return 'auth_form'
  }

  return normalized
}

export const Card = ({
  variant = 'dark_step',
  title,
  description,
  imageSrc,
  icon,
  number,
  children,
  footer,
  className = '',
  ...rest
}) => {
  const normalizedVariant = normalizedVariantName(variant)
  const variantClass = variantStyles[normalizedVariant] || variantStyles.dark_step
  const layoutClass = layoutStyles[normalizedVariant] || layoutStyles.dark_step

  if (normalizedVariant === 'auth_form') {
    return (
      <article className={`${variantClass} ${layoutClass} ${className}`} {...rest}>
        {title ? <h3 className="text-2xl font-bold text-center">{title}</h3> : null}
        {description ? <p className="mt-2 text-sm text-dark-grey1 text-center">{description}</p> : null}
        {children ? <div className="mt-6">{children}</div> : null}
        {footer ? <div className="mt-6">{footer}</div> : null}
      </article>
    )
  }

  if (normalizedVariant === 'dark_step') {
    return (
      <article className={`${variantClass} ${layoutClass} ${className}`} {...rest}>
        <div className="flex items-start justify-between">
          <div className="w-10 h-10 rounded-[10px] bg-vitrine-grey3/60 flex items-center justify-center">
            {icon}
          </div>
          <span className="text-vitrine-grey1 text-sm font-semibold">{number}</span>
        </div>
        <h3 className="mt-4 font-semibold text-base">{title}</h3>
        <p className="mt-2 text-sm text-vitrine-grey1">{description}</p>
      </article>
    )
  }

  if (normalizedVariant === 'dark_image') {
    return (
      <article className={`${variantClass} ${layoutClass} ${className}`} {...rest}>
        <div className="w-full h-35 rounded-[12px] overflow-hidden bg-vitrine-black1">
          {imageSrc ? (
            <img src={imageSrc} alt={title || 'card image'} className="w-full h-full object-cover" />
          ) : null}
        </div>
        <h3 className="mt-4 font-semibold text-base">{title}</h3>
        <p className="mt-2 text-sm text-vitrine-grey1">{description}</p>
      </article>
    )
  }

  return (
    <article className={`${variantClass} ${layoutClass} ${className}`} {...rest}>
      <div className="w-full h-30 rounded-[12px] bg-light-red1/15 flex items-center justify-center">
        {imageSrc ? (
          <img src={imageSrc} alt={title || 'card image'} className="w-full h-full object-cover rounded-[12px]" />
        ) : null}
      </div>
      <h3 className="mt-4 font-semibold text-base">{title}</h3>
      <p className="mt-2 text-sm text-light-white4">{description}</p>
    </article>
  )
}

export default Card
