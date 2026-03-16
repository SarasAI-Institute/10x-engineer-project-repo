function Modal({ isOpen, title, children, onClose }) {
  if (!isOpen) return null;

  const titleId = 'modal-title';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4" role="dialog" aria-modal="true" aria-labelledby={titleId}>
      <div className="max-w-md rounded-3xl border border-white/10 bg-slate-900/80 p-6 text-white shadow-2xl" tabIndex={-1}>
        <div className="flex items-center justify-between">
          <h3 id={titleId} className="text-lg font-semibold">
            {title}
          </h3>
          <button
            type="button"
            className="text-xs uppercase tracking-[0.3em] text-slate-400"
            onClick={onClose}
            aria-label="Close modal"
          >
            Close
          </button>
        </div>
        <div className="mt-4 space-y-4">{children}</div>
      </div>
    </div>
  );
}

export default Modal;
