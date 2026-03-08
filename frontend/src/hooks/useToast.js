import { useState, useCallback } from 'react';

let nextId = 0;

/**
 * Custom React hook that manages a list of toast notifications.
 *
 * Provides functions to add and dismiss toasts. Each toast is assigned a
 * unique auto-incrementing ID. Toasts are typically auto-dismissed by the
 * `ToastItem` component after a timeout.
 *
 * @returns {{
 *   toasts: Array<{id: number, message: string, type: string}>,
 *   toast: function(message: string, type?: string): void,
 *   dismiss: function(id: number): void
 * }} Hook state and control functions.
 *
 * @example
 * function MyComponent() {
 *   const { toasts, toast, dismiss } = useToast();
 *
 *   return (
 *     <>
 *       <button onClick={() => toast('Saved!', 'success')}>Save</button>
 *       <button onClick={() => toast('Something broke', 'error')}>Fail</button>
 *       <Toast toasts={toasts} onDismiss={dismiss} />
 *     </>
 *   );
 * }
 */
export function useToast() {
  const [toasts, setToasts] = useState([]);

  /**
   * Adds a new toast notification to the list.
   *
   * @param {string} message - The text content to display in the toast.
   * @param {'success'|'error'} [type='success'] - Visual style of the toast.
   * @returns {void}
   *
   * @example
   * toast('Prompt deleted', 'success');
   * toast('Network error', 'error');
   */
  const addToast = useCallback((message, type = 'success') => {
    const id = ++nextId;
    setToasts((prev) => [...prev, { id, message, type }]);
  }, []);

  /**
   * Removes a toast from the list by its ID.
   *
   * @param {number} id - The unique ID of the toast to remove.
   * @returns {void}
   *
   * @example
   * dismiss(3); // removes the toast with id === 3
   */
  const dismiss = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  return { toasts, toast: addToast, dismiss };
}
