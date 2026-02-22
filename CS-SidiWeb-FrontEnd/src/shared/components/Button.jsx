import '../../styles-tailwind.css'

const variantStyles = {
  login: 'border-2 border-light-red1 text-light-red1 font-semibold text-base hover:bg-light-red1/10',
  signup: 'bg-light-red1 text-light-white1 font-semibold text-base hover:bg-light-red2',
  demo: 'bg-vitrine-grey2 text-vitrine-white1 font-medium text-sm hover:bg-vitrine-grey3',
  submit: 'bg-dark-red1 text-dark-white1 font-semibold text-lg hover:bg-dark-red2',
  board: 'bg-light-red1 text-light-white1 font-medium text-sm hover:bg-light-red2',
}

const radiusStyles = {
  login: 'rounded-[20px]',
  signup: 'rounded-[20px]',
  submit: 'rounded-[15px]',
  demo: 'rounded-[25px]',
  board: 'rounded-[25px]',
}

const dimensionStyles = {
  login: 'w-24 h-12',
  signup: 'w-24 h-12',
  submit: 'w-[600px] h-[100px]',
  demo: 'w-[120px] h-[90px]',
  board: 'w-[120px] h-[90px]',
}

export const Button = ({ variant, size, children, ...rest }) => {
  const variantClass = variantStyles[variant] || '';
  const dimensionClass = dimensionStyles[variant] || '';
  const sizeClass = dimensionClass ? '' : (dimensionStyles[size] || '');
  const radiusClass = radiusStyles[variant] || 'border-radius-[15px]';
    return (
    <button
        className={`${variantClass} ${dimensionClass} ${sizeClass} ${radiusClass} cursor-pointer
        transition duration-300 ease-in-out`}
        {...rest}
    >
        {children}
    </button>  );
}   

