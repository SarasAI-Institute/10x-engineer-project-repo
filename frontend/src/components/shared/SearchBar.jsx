function SearchBar({ value, onChange, placeholder = 'Search prompts' }) {
  return (
    <label className="relative block w-full">
      <span className="sr-only">{placeholder}</span>
      <input
        value={value}
        onChange={(event) => onChange?.(event.target.value)}
        placeholder={placeholder}
        className="w-full rounded-2xl border border-transparent bg-white/5 px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-emerald-400/80 focus:outline-none"
      />
    </label>
  );
}

export default SearchBar;
