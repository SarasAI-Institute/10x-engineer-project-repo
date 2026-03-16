function EmptyState({ title, description, actionText, actionProps }) {
  return (
    <div className="rounded-3xl border border-dashed border-white/10 bg-slate-900/60 p-6 text-center text-sm text-slate-300">
      <p className="text-xs uppercase tracking-[0.3em] text-slate-400">{title}</p>
      <p className="mt-3 text-base text-white">{description}</p>
      {actionText ? (
        <button
          type="button"
          className="mt-4 inline-flex items-center justify-center rounded-2xl border border-white/20 px-4 py-2 text-xs font-semibold uppercase tracking-[0.4em] text-emerald-300 transition hover:border-emerald-400 hover:text-white"
          {...actionProps}
        >
          {actionText}
        </button>
      ) : null}
    </div>
  );
}

export default EmptyState;
