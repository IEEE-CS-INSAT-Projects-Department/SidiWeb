import '../../index.css'

const variantStyles = {
  dark_step: 'bg-vitrine-black2 text-vitrine-white1 border border-vitrine-grey3',
  dark_image: 'bg-vitrine-black2 text-vitrine-white1 border border-vitrine-grey3',
  light_image: 'bg-light-white1 text-light-black border border-light-white3',
}

const layoutStyles = {
  dark_step: 'p-5 rounded-[16px] min-h-[120px]',
  dark_image: 'p-4 rounded-[18px]',
  light_image: 'p-4 rounded-[16px]',
}

export const Card = ({ variant = 'dark_step', title, description, imageSrc, icon, number, ...rest }) => {
  const variantClass = variantStyles[variant] || variantStyles.dark_step
  const layoutClass = layoutStyles[variant] || layoutStyles.dark_step

  if (variant === 'dark_step') {
    return (
      <article className={`${variantClass} ${layoutClass}`} {...rest}>
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

  if (variant === 'dark_image') {
    return (
      <article className={`${variantClass} ${layoutClass}`} {...rest}>
        <div className="w-full h-[140px] rounded-[12px] overflow-hidden bg-vitrine-black1">
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
    <article className={`${variantClass} ${layoutClass}`} {...rest}>
      <div className="w-full h-[120px] rounded-[12px] bg-light-red1/15 flex items-center justify-center">
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
