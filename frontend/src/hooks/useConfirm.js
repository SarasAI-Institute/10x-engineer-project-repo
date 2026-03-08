import { useState, useCallback } from 'react';

export function useConfirm() {
  const [state, setState] = useState(null); // { message, resolve }

  const confirm = useCallback((message) => {
    return new Promise((resolve) => {
      setState({ message, resolve });
    });
  }, []);

  const handleResponse = (result) => {
    state?.resolve(result);
    setState(null);
  };

  return { confirm, confirmState: state, handleResponse };
}
