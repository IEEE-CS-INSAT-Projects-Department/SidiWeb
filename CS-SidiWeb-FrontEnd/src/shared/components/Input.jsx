import '../../styles-tailwind.css'

const variantStyles = {
  search: 'bg-light-white2 text-light-black placeholder-light-white4 border border-light-white3 focus:outline-none focus:ring-2 focus:ring-light-red1',
  input_auth_small: 'bg-dark-grey2 text-dark-white1 placeholder-dark-grey1 border border-dark-grey3 focus:outline-none focus:ring-2 focus:ring-dark-red1',
  input_auth_medium: 'bg-dark-grey2 text-dark-white1 placeholder-dark-grey1 border border-dark-grey3 focus:outline-none focus:ring-2 focus:ring-dark-red1',
  input_auth_large: 'bg-dark-grey2 text-dark-white1 placeholder-dark-grey1 border border-dark-grey3 focus:outline-none focus:ring-2 focus:ring-dark-red1',
  chat: 'bg-dark-grey3 text-dark-white1 placeholder-dark-grey1 border border-dark-grey2 focus:outline-none focus:ring-2 focus:ring-dark-red1',
}

const dimensionStyles = {
  search: 'w-[186px] h-[31.5px] px-3 py-2 rounded-[4px] text-sm',
  input_auth_small: 'w-[381px] h-[55px] px-4 py-3 rounded-[8px] text-base font-normal',
  input_auth_medium: 'w-[560px] h-[65px] px-4 py-3 rounded-[8px] text-base font-normal',
  input_auth_large: 'w-[836px] h-[436px] px-4 py-3 rounded-[8px] text-base font-normal',
  chat: 'w-[987px] h-[62px] px-4 py-3 rounded-[12px] text-sm font-normal',
}

export const Input = ({ variant = 'search', placeholder, ...rest }) => {
  const variantClass = variantStyles[variant] || variantStyles.search;
  const dimensionClass = dimensionStyles[variant] || dimensionStyles.search;

  // Les inputs auth_large sont des textareas pour multiligne
  if (variant === 'input_auth_large') {
    return (
      <textarea
        placeholder={placeholder}
        className={`${variantClass} ${dimensionClass} resize-none align-top transition duration-300 ease-in-out`}
        {...rest}
      />
    );
  }

  return (
    <input
      type="text"
      placeholder={placeholder}
      className={`${variantClass} ${dimensionClass} transition duration-300 ease-in-out`}
      {...rest}
    />
  );
}

export default Input
