import { useState, useCallback } from 'react';

/**
 * Custom React hook that provides an imperative confirmation dialog API.
 *
 * Returns a `confirm` function that opens a dialog and resolves a Promise with
 * the user's boolean choice (true = confirmed, false = cancelled). Intended to
 * be used alongside the `ConfirmDialog` component which consumes `confirmState`
 * and calls `handleResponse`.
 *
 * @returns {{
 *   confirm: function(message: string): Promise<boolean>,
 *   confirmState: {message: string, resolve: function(boolean): void}|null,
 *   handleResponse: function(result: boolean): void
 * }} Hook state and control functions.
 *
 * @example
 * function MyComponent() {
 *   const { confirm, confirmState, handleResponse } = useConfirm();
 *
 *   const handleDelete = async () => {
 *     const ok = await confirm('Are you sure you want to delete this item?');
 *     if (ok) deleteItem();
 *   };
 *
 *   return (
 *     <>
 *       <button onClick={handleDelete}>Delete</button>
 *       <ConfirmDialog confirmState={confirmState} onResponse={handleResponse} />
 *     </>
 *   );
 * }
 */
export function useConfirm() {
  const [state, setState] = useState(null); // { message, resolve }

  /**
   * Opens the confirmation dialog with the given message and returns a Promise
   * that resolves once the user responds.
   *
   * @param {string} message - The confirmation question to display to the user.
   * @returns {Promise<boolean>} Resolves to `true` if confirmed, `false` if cancelled.
   *
   * @example
   * const confirmed = await confirm('Delete this prompt? This cannot be undone.');
   * if (confirmed) await deletePrompt(id);
   */
  const confirm = useCallback((message) => {
    return new Promise((resolve) => {
      setState({ message, resolve });
    });
  }, []);

  /**
   * Resolves the pending confirmation Promise with the user's choice and
   * closes the dialog by resetting internal state to null.
   *
   * @param {boolean} result - `true` if the user confirmed, `false` if cancelled.
   * @returns {void}
   *
   * @example
   * // Called by ConfirmDialog when the user clicks "Confirm" or "Cancel"
   * handleResponse(true);  // user confirmed
   * handleResponse(false); // user cancelled
   */
  const handleResponse = (result) => {
    state?.resolve(result);
    setState(null);
  };

  return { confirm, confirmState: state, handleResponse };
}
