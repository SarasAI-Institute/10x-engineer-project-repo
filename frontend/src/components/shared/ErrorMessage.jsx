/**
 * Inline error state component with an optional retry action.
 *
 * Displays a centred error icon, a human-readable message, and — when an
 * `onRetry` callback is provided — a "Try again" link button. Suitable for
 * replacing content areas when a data fetch fails.
 *
 * @param {Object} props - Component props.
 * @param {string} [props.message] - Error text to display. Defaults to
 *   'Something went wrong' when falsy.
 * @param {function(): void} [props.onRetry] - Optional callback invoked when
 *   the user clicks "Try again". If omitted, the retry button is not rendered.
 * @returns {JSX.Element} A centred error display with icon, message, and optional retry button.
 *
 * @example
 * // Basic error with no retry
 * <ErrorMessage message="Failed to load collections." />
 *
 * @example
 * // Error with retry callback
 * <ErrorMessage message={error} onRetry={fetchPrompts} />
 */
export function ErrorMessage({ message, onRetry }) {
  return (
    <div className="flex flex-col items-center justify-center py-12 gap-3 text-center">
      <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
        <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <p className="text-sm text-gray-600">{message || 'Something went wrong'}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="text-sm text-indigo-600 hover:underline cursor-pointer"
        >
          Try again
        </button>
      )}
    </div>
  );
}
