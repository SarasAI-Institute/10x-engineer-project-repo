const quickLinks = ['All Prompts', 'Favorites', 'Recently Updated', 'Templates'];

function Sidebar() {
  return (
    <aside className="w-full rounded-3xl border border-white/5 bg-slate-900/60 p-5 shadow-xl shadow-black/40 lg:w-72">
      <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Dashboard</p>
      <div className="mt-5 space-y-3">
        {quickLinks.map((link) => (
          <button
            key={link}
            className="w-full rounded-2xl border border-white/5 bg-white/5 px-4 py-3 text-left text-sm font-medium text-white transition hover:border-emerald-400/60"
          >
            {link}
          </button>
        ))}
      </div>
    </aside>
  );
}

export default Sidebar;
