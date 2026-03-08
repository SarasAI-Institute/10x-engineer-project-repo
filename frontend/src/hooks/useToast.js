import { useState, useCallback } from 'react';

let nextId = 0;

export function useToast() {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((message, type = 'success') => {
    const id = ++nextId;
    setToasts((prev) => [...prev, { id, message, type }]);
  }, []);

  const dismiss = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  return { toasts, toast: addToast, dismiss };
}
