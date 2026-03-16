function LoadingSpinner({ label = 'Loading...' }) {
  return (
    <div className="flex items-center gap-2 text-sm text-slate-400">
      <div className="h-4 w-4 animate-spin rounded-full border-2 border-transparent border-t-emerald-400"></div>
      {label}
    </div>
  );
}

export default LoadingSpinner;
