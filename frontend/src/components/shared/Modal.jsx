import { useEffect, useRef } from 'react';

const FOCUSABLE = 'button:not([disabled]):not([tabindex="-1"]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled])';

/**
 * Accessible modal dialog component with focus management and keyboard support.
 *
 * When opened, the modal:
 * - Focuses the first focusable element inside the panel.
 * - Traps keyboard focus within the panel (Tab / Shift+Tab cycle).
 * - Closes when the user presses Escape or clicks the backdrop.
 *
 * Renders nothing when `isOpen` is false.
 *
 * @param {Object} props - Component props.
 * @param {boolean} props.isOpen - Controls visibility of the modal.
 * @param {function(): void} props.onClose - Callback invoked when the modal should close.
 * @param {string} props.title - Title displayed in the modal header (also used for aria-labelledby).
 * @param {React.ReactNode} props.children - Content rendered inside the modal body.
 * @returns {JSX.Element|null} The modal overlay and panel, or null when closed.
 *
 * @example
 * <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Edit Prompt">
 *   <p>Modal content goes here.</p>
 * </Modal>
 */
export function Modal({ isOpen, onClose, title, children }) {
  const panelRef = useRef(null);

  // Focus first field only when modal opens — NOT when onClose reference changes
  useEffect(() => {
    if (!isOpen) return;
    const first = panelRef.current?.querySelector(FOCUSABLE);
    first?.focus();
  }, [isOpen]);

  // Keyboard handler — use a ref for onClose to avoid re-running on every render
  const onCloseRef = useRef(onClose);
  useEffect(() => { onCloseRef.current = onClose; });

  /**
   * Handles keydown events for Escape (close) and Tab (focus trap) while the
   * modal is open. Attached to `document` so it intercepts events regardless
   * of which element currently has focus.
   *
   * @param {KeyboardEvent} e - The native keyboard event.
   * @returns {void}
   */
  useEffect(() => {
    if (!isOpen) return;
    const onKey = (e) => {
      if (e.key === 'Escape') { onCloseRef.current(); return; }
      if (e.key !== 'Tab') return;
      const focusable = [...(panelRef.current?.querySelectorAll(FOCUSABLE) || [])];
      if (!focusable.length) return;
      const last = focusable[focusable.length - 1];
      if (e.shiftKey) {
        if (document.activeElement === focusable[0]) { e.preventDefault(); last.focus(); }
      } else {
        if (document.activeElement === last) { e.preventDefault(); focusable[0].focus(); }
      }
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/50" onClick={onClose} aria-hidden="true" />
      <div
        ref={panelRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        className="relative bg-white rounded-xl shadow-xl w-full max-w-lg max-h-[90vh] flex flex-col"
      >
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
          <h2 id="modal-title" className="text-lg font-semibold text-gray-900">{title}</h2>
          <button
            type="button"
            onClick={onClose}
            tabIndex={-1}
            className="text-gray-400 hover:text-gray-600 transition-colors p-1 rounded cursor-pointer focus:outline-none focus:ring-2 focus:ring-indigo-500"
            aria-label="Close dialog"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div className="overflow-y-auto flex-1 px-6 py-4">{children}</div>
      </div>
    </div>
  );
}
