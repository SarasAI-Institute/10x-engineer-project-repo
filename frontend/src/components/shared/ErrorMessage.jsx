function ErrorMessage({ message }) {
  return (
    <div className="rounded-2xl border border-rose-500/60 bg-rose-500/10 px-4 py-3 text-sm text-rose-300">
      {message}
    </div>
  );
}

export default ErrorMessage;
