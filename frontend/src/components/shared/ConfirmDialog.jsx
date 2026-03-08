import { Button } from './Button';

export function ConfirmDialog({ confirmState, onResponse }) {
  if (!confirmState) return null;

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/50" />
      <div
        role="alertdialog"
        aria-modal="true"
        aria-labelledby="confirm-title"
        aria-describedby="confirm-desc"
        className="relative bg-white rounded-xl shadow-xl w-full max-w-sm p-6"
      >
        <div className="flex items-start gap-4 mb-5">
          <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center shrink-0">
            <svg className="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div>
            <h3 id="confirm-title" className="font-semibold text-gray-900 mb-1">Are you sure?</h3>
            <p id="confirm-desc" className="text-sm text-gray-600">{confirmState.message}</p>
          </div>
        </div>
        <div className="flex justify-end gap-2">
          <Button type="button" variant="secondary" onClick={() => onResponse(false)}>Cancel</Button>
          <Button type="button" variant="danger" onClick={() => onResponse(true)}>Delete</Button>
        </div>
      </div>
    </div>
  );
}
