const navItems = ['Prompts', 'Collections', 'Settings'];

function Header() {
  return (
    <header className="border-b border-white/10 bg-slate-950/80 px-4 py-3 backdrop-blur lg:px-10">
      <div className="mx-auto flex max-w-6xl items-center justify-between">
        <div className="flex items-center gap-3 text-lg font-semibold tracking-tight text-white">
          <span className="h-10 w-10 rounded-2xl bg-emerald-400/80 text-center text-2xl leading-[40px] text-slate-950">AI</span>
          <div>
            <p>Prompt Studio</p>
            <p className="text-xs text-slate-400">Week 4 Workspace</p>
          </div>
        </div>
        <nav className="hidden gap-6 text-sm uppercase tracking-[0.3em] text-slate-400 lg:flex">
          {navItems.map((item) => (
            <button key={item} className="transition hover:text-white">
              {item}
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
}

export default Header;
