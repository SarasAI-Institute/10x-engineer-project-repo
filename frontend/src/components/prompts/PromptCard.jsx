function PromptCard({ prompt, isSelected, onSelect, collectionName }) {
  return (
    <button
      type="button"
      onClick={() => onSelect(prompt)}
      className={`flex h-full flex-col justify-between rounded-2xl border border-white/10 bg-gradient-to-br from-slate-900/80 to-slate-900/30 p-5 text-left transition hover:border-emerald-400/70 ${
        isSelected ? 'ring-2 ring-emerald-400/60' : ''
      }`}
    >
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Prompt</p>
        <h3 className="mt-3 text-lg font-semibold text-white">{prompt.title}</h3>
        <p className="mt-2 text-sm text-slate-300">{prompt.description}</p>
      </div>
      <div className="mt-4 text-xs text-slate-400">{collectionName ?? 'Unassigned'}</div>
    </button>
  );
}

export default PromptCard;
