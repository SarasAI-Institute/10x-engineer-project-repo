import Button from '../shared/Button';

function PromptDetail({ prompt, collectionName, onEdit, onDelete, isDeleting = false }) {
  if (!prompt) {
    return <p className="text-sm text-slate-400">Select a prompt to preview the full details.</p>;
  }

  return (
    <div className="space-y-4 rounded-3xl border border-white/10 bg-slate-900/70 p-5">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Active Prompt</p>
          <h3 className="text-xl font-semibold text-white">{prompt.title}</h3>
        </div>
        <span className="rounded-full bg-emerald-500/80 px-3 py-1 text-xs font-semibold text-slate-950">
          {collectionName ?? 'Unassigned'}
        </span>
      </div>
      <p className="text-sm text-slate-300">{prompt.description ?? 'No description provided.'}</p>
      <div className="rounded-2xl border border-dashed border-white/10 bg-slate-950/60 p-4 text-sm text-slate-300">
        {prompt.content}
      </div>
      <div className="flex gap-3">
        <Button type="button" className="flex-1" onClick={onEdit} variant="ghost">
          Edit
        </Button>
        <Button type="button" className="flex-1" onClick={onDelete} disabled={isDeleting}>
          {isDeleting ? 'Deleting…' : 'Delete'}
        </Button>
      </div>
    </div>
  );
}

export default PromptDetail;
