import { useEffect, useState } from 'react';
import Button from '../shared/Button';

const emptyForm = {
  title: '',
  content: '',
  description: '',
  collectionId: '',
};

function PromptForm({
  onSubmit,
  collections = [],
  isSubmitting = false,
  error = '',
  initialData = null,
  mode = 'create',
  onCancel,
}) {
  const [form, setForm] = useState(emptyForm);
  const [validationError, setValidationError] = useState('');

  useEffect(() => {
    if (!initialData) {
      setForm(emptyForm);
      return;
    }

    setForm({
      title: initialData.title ?? '',
      content: initialData.content ?? '',
      description: initialData.description ?? '',
      collectionId: initialData.collection_id ?? '',
    });
    setValidationError('');
  }, [initialData]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    if (validationError) {
      setValidationError('');
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!form.title.trim()) {
      setValidationError('Title is required.');
      return;
    }
    if (!form.content.trim()) {
      setValidationError('Content is required.');
      return;
    }
    onSubmit?.(form);
  };

  const errorId = 'prompt-form-error';

  return (
    <form onSubmit={handleSubmit} className="space-y-4" aria-live="polite">
      <div>
        <label htmlFor="prompt-title" className="text-xs uppercase tracking-[0.3em] text-slate-400">
          Title
        </label>
        <input
          id="prompt-title"
          name="title"
          value={form.title}
          onChange={handleChange}
          placeholder="Summarize meeting notes"
          aria-invalid={Boolean(validationError && !form.title.trim())}
          aria-describedby={errorId}
          className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-900/70 px-4 py-3 text-sm text-white focus:border-emerald-400/70 focus:outline-none"
        />
      </div>
      <div>
        <label htmlFor="prompt-content" className="text-xs uppercase tracking-[0.3em] text-slate-400">
          Content
        </label>
        <textarea
          id="prompt-content"
          name="content"
          value={form.content}
          onChange={handleChange}
          placeholder="Hey AI, summarize the last standup..."
          aria-invalid={Boolean(validationError && !form.content.trim())}
          aria-describedby={errorId}
          className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-900/70 px-4 py-3 text-sm text-white focus:border-emerald-400/70 focus:outline-none"
          rows={4}
        />
      </div>
      <div>
        <label htmlFor="prompt-description" className="text-xs uppercase tracking-[0.3em] text-slate-400">
          Description
        </label>
        <textarea
          id="prompt-description"
          name="description"
          value={form.description}
          onChange={handleChange}
          placeholder="Add context and expected format"
          className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-900/70 px-4 py-3 text-sm text-white focus:border-emerald-400/70 focus:outline-none"
          rows={2}
        />
      </div>
      <div>
        <label htmlFor="prompt-collection" className="text-xs uppercase tracking-[0.3em] text-slate-400">
          Collection
        </label>
        <select
          id="prompt-collection"
          name="collectionId"
          value={form.collectionId}
          onChange={handleChange}
          className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-900/70 px-4 py-3 text-sm text-white focus:border-emerald-400/70 focus:outline-none"
        >
          <option value="">(None)</option>
          {collections.map((collection) => (
            <option key={collection.id} value={collection.id}>
              {collection.name}
            </option>
          ))}
        </select>
      </div>
      <div className="space-y-2">
        <div className="flex flex-wrap gap-3">
          <Button type="submit" className="flex-1" disabled={isSubmitting}>
            {isSubmitting ? (mode === 'edit' ? 'Saving…' : 'Saving…') : mode === 'edit' ? 'Update prompt' : 'Save prompt'}
          </Button>
          {mode === 'edit' && (
            <Button type="button" variant="ghost" className="flex-1" onClick={onCancel} disabled={isSubmitting}>
              Cancel
            </Button>
          )}
        </div>
        <p id={errorId} className="text-xs text-rose-300" aria-live="polite">
          {validationError || error}
        </p>
      </div>
    </form>
  );
}

export default PromptForm;
