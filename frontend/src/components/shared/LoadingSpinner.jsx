/**
 * Animated SVG loading spinner with configurable size.
 *
 * Renders an indigo spinning circle using Tailwind's `animate-spin` utility.
 * The `size` prop maps to a preset width/height class; additional Tailwind
 * classes can be appended via `className`.
 *
 * @param {Object} props - Component props.
 * @param {'sm'|'md'|'lg'} [props.size='md'] - Preset size: sm=16px, md=32px, lg=48px.
 * @param {string} [props.className=''] - Additional Tailwind classes to apply to the SVG.
 * @returns {JSX.Element} An animated SVG spinner element.
 *
 * @example
 * // Default medium spinner
 * <LoadingSpinner />
 *
 * @example
 * // Large spinner centred in a flex container
 * <div className="flex justify-center py-20">
 *   <LoadingSpinner size="lg" />
 * </div>
 *
 * @example
 * // Small inline spinner with extra margin
 * <LoadingSpinner size="sm" className="ml-2" />
 */
export function LoadingSpinner({ size = 'md', className = '' }) {
  const sizes = { sm: 'w-4 h-4', md: 'w-8 h-8', lg: 'w-12 h-12' };
  return (
    <svg
      className={`animate-spin text-indigo-600 ${sizes[size]} ${className}`}
      fill="none" viewBox="0 0 24 24"
    >
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
      <path className="opacity-75" fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
    </svg>
  );
}
