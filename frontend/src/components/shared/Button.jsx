const variants = {
  primary: 'bg-indigo-600 text-white hover:bg-indigo-700 focus:ring-indigo-500',
  secondary: 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50 focus:ring-indigo-500',
  danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
  ghost: 'bg-transparent text-gray-600 hover:bg-gray-100 focus:ring-gray-400',
};

const sizes = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-sm',
  lg: 'px-5 py-2.5 text-base',
};

/**
 * Reusable button component with built-in variant and size styling.
 *
 * Renders a `<button>` element with Tailwind utility classes derived from the
 * `variant` and `size` props. Additional class names and native button props
 * (e.g. `onClick`, `type`, `aria-*`) are forwarded via the rest spread.
 *
 * @param {Object} props - Component props.
 * @param {'primary'|'secondary'|'danger'|'ghost'} [props.variant='primary'] - Visual style variant.
 * @param {'sm'|'md'|'lg'} [props.size='md'] - Size of the button.
 * @param {boolean} [props.disabled] - Whether the button is disabled.
 * @param {React.ReactNode} props.children - Button label or content.
 * @param {string} [props.className=''] - Additional Tailwind classes to merge.
 * @param {...*} props - Any other native `<button>` attributes.
 * @returns {JSX.Element} A styled `<button>` element.
 *
 * @example
 * // Primary button
 * <Button onClick={handleSave}>Save</Button>
 *
 * @example
 * // Danger button, small size, disabled
 * <Button variant="danger" size="sm" disabled={loading}>Delete</Button>
 *
 * @example
 * // Ghost button with custom class
 * <Button variant="ghost" className="ml-2">Cancel</Button>
 */
export function Button({ variant = 'primary', size = 'md', disabled, children, className = '', ...props }) {
  return (
    <button
      disabled={disabled}
      className={`inline-flex items-center justify-center gap-1.5 font-medium rounded-lg
        focus:outline-none focus:ring-2 focus:ring-offset-1
        disabled:opacity-50 disabled:cursor-not-allowed
        transition-colors cursor-pointer
        ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
