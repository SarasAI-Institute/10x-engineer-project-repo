import { useState } from 'react';
import Button from '../shared/Button';

const emptyForm = {
  name: '',
  description: '',
};

function CollectionForm({ onSubmit, isSubmitting = false, error = '' }) {
  const [form, setForm] = useState(emptyForm);
  const [validationError, setValidationError] = useState('');

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    if (validationError) {
      setValidationError('');
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!form.name.trim()) {
      setValidationError('Collection name is required.');
      return;
    }
    onSubmit?.(form);
    setForm({ ...emptyForm });
  };

  const errorId = 'collection-form-error';

  return (
    <form onSubmit={handleSubmit} className="space-y-3" aria-live="polite">
      <div>
        <label htmlFor="collection-name" className="text-xs uppercase tracking-[0.3em] text-slate-400">
          Collection name
        </label>
        <input
          id="collection-name"
          name="name"
          value={form.name}
          onChange={handleChange}
          placeholder="Weekly Ops"
          aria-invalid={Boolean(validationError && !form.name.trim())}
          aria-describedby={errorId}
          className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-900/70 px-4 py-3 text-sm text-white focus:border-emerald-400/70 focus:outline-none"
        />
      </div>
      <div>
        <label htmlFor="collection-description" className="text-xs uppercase tracking-[0.3em] text-slate-400">
          Description
        </label>
        <textarea
          id="collection-description"
          name="description"
          value={form.description}
          onChange={handleChange}
          placeholder="Guides for the leadership team"
          className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-900/70 px-4 py-3 text-sm text-white focus:border-emerald-400/70 focus:outline-none"
          rows={2}
        />
      </div>
      <div className="space-y-2">
        <Button type="submit" variant="ghost" className="w-full" disabled={isSubmitting}>
          {isSubmitting ? 'Saving…' : 'Create collection'}
        </Button>
        <p id={errorId} className="text-xs text-rose-300" aria-live="polite">
          {validationError || error}
        </p>
      </div>
    </form>
  );
}

export default CollectionForm;
