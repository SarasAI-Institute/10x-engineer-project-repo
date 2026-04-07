import { useEffect } from 'react';

const icons = {
  success: (
    <svg className="w-5 h-5 text-green-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
    </svg>
  ),
  error: (
    <svg className="w-5 h-5 text-red-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
};

/**
 * Container component that renders a stack of toast notification items.
 *
 * Positioned fixed at the bottom-right of the viewport. Each toast in the
 * `toasts` array is rendered as a `ToastItem`. Passes `onDismiss` through to
 * each item so they can be dismissed manually or automatically.
 *
 * @param {Object} props - Component props.
 * @param {Array<{id: number, message: string, type: 'success'|'error'}>} props.toasts - Active toasts to display.
 * @param {function(id: number): void} props.onDismiss - Callback to remove a toast by ID.
 * @returns {JSX.Element} A fixed-position container with rendered toast items.
 *
 * @example
 * const { toasts, dismiss } = useToast();
 * return <Toast toasts={toasts} onDismiss={dismiss} />;
 */
export function Toast({ toasts, onDismiss }) {
  return (
    <div
      role="status"
      aria-live="polite"
      className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 pointer-events-none"
    >
      {toasts.map((t) => (
        <ToastItem key={t.id} toast={t} onDismiss={onDismiss} />
      ))}
    </div>
  );
}

/**
 * Individual toast notification item with auto-dismiss after 4 seconds.
 *
 * Displays the toast message alongside a type-specific icon and a manual
 * dismiss button. Automatically calls `onDismiss` with the toast ID after a
 * 4000 ms timeout, clearing the timer on unmount.
 *
 * @param {Object} props - Component props.
 * @param {{id: number, message: string, type: 'success'|'error'}} props.toast - Toast data to display.
 * @param {function(id: number): void} props.onDismiss - Callback to remove this toast from the list.
 * @returns {JSX.Element} A styled toast card with icon, message, and close button.
 *
 * @example
 * // Rendered internally by Toast; not usually used directly
 * <ToastItem toast={{ id: 1, message: 'Saved!', type: 'success' }} onDismiss={dismiss} />
 */
function ToastItem({ toast, onDismiss }) {
  useEffect(() => {
    const timer = setTimeout(() => onDismiss(toast.id), 4000);
    return () => clearTimeout(timer);
  }, [toast.id, onDismiss]);

  return (
    <div
      className="pointer-events-auto flex items-center gap-3 bg-white border border-gray-200
        rounded-xl shadow-lg px-4 py-3 text-sm text-gray-800 min-w-64 max-w-sm
        animate-[slideIn_0.2s_ease-out]"
    >
      {icons[toast.type]}
      <span className="flex-1">{toast.message}</span>
      <button
        type="button"
        onClick={() => onDismiss(toast.id)}
        className="text-gray-400 hover:text-gray-600 cursor-pointer"
        aria-label="Dismiss notification"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  );
}
