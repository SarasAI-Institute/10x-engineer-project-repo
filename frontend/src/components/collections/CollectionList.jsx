import EmptyState from '../shared/EmptyState';

function CollectionList({ collections, counts = {}, actionProps }) {
  if (!collections.length) {
    return (
      <EmptyState
        title="No collections"
        description="Collections help organize prompts. Create one to get started."
        actionText="New collection"
        actionProps={{ type: 'button', ...actionProps }}
      />
    );
  }

  return (
    <div className="space-y-3">
      {collections.map((collection) => (
        <div
          key={collection.id}
          className="flex items-center justify-between rounded-2xl border border-white/10 bg-slate-900/60 px-4 py-3 text-sm text-slate-200"
        >
          <div>
            <p className="font-semibold text-white">{collection.name}</p>
            <p className="text-xs text-slate-400">{collection.description ?? 'No description'}</p>
          </div>
          <span className="text-xs uppercase tracking-[0.3em] text-slate-400">{counts[collection.id] ?? 0} prompts</span>
        </div>
      ))}
    </div>
  );
}

export default CollectionList;
