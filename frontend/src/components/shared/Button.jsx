function Button({ children, variant = 'solid', className = '', type = 'button', ...rest }) {
  const baseClass = 'rounded-2xl px-4 py-2 text-sm font-semibold transition focus:outline-none disabled:cursor-not-allowed disabled:opacity-60';
  const variants = {
    solid: 'bg-emerald-400/90 text-slate-950 hover:bg-emerald-400',
    ghost: 'border border-white/10 text-white hover:border-emerald-400/60',
  };

  return (
    <button type={type} className={`${baseClass} ${variants[variant] ?? variants.solid} ${className}`} {...rest}>
      {children}
    </button>
  );
}

export default Button;
