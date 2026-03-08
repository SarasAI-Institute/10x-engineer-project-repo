import { useState, useEffect } from 'react';
import { Modal } from '../shared/Modal';
import { Button } from '../shared/Button';
import { createPrompt, updatePrompt } from '../../api/prompts';

function FieldError({ msg }) {
  if (!msg) return null;
  return <p role="alert" className="mt-1 text-xs text-red-600">{msg}</p>;
}

export function PromptForm({ isOpen, onClose, onSaved, collections, initialData }) {
  const isEdit = Boolean(initialData);

  const [form, setForm] = useState({ title: '', content: '', description: '', collection_id: '' });
  const [touched, setTouched] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isOpen) {
      setForm({
        title: initialData?.title || '',
        content: initialData?.content || '',
        description: initialData?.description || '',
        collection_id: initialData?.collection_id || '',
      });
      setTouched({});
      setError('');
    }
  }, [isOpen, initialData]);

  const set = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }));
  const touch = (field) => () => setTouched((t) => ({ ...t, [field]: true }));

  const errors = {
    title: !form.title.trim() ? 'Title is required' : form.title.trim().length > 200 ? 'Max 200 characters' : '',
    content: !form.content.trim() ? 'Content is required' : '',
  };
  const isValid = !errors.title && !errors.content;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setTouched({ title: true, content: true });
    if (!isValid) return;
    setLoading(true);
    setError('');
    try {
      const payload = {
        title: form.title.trim(),
        content: form.content.trim(),
        description: form.description.trim() || null,
        collection_id: form.collection_id || null,
      };
      const saved = isEdit
        ? await updatePrompt(initialData.id, payload)
        : await createPrompt(payload);
      onSaved(saved);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const inputClass = (field) =>
    `w-full px-3 py-2 text-sm border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent
    ${touched[field] && errors[field] ? 'border-red-400 bg-red-50' : 'border-gray-300'}`;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={isEdit ? 'Edit Prompt' : 'New Prompt'}>
      <form onSubmit={handleSubmit} noValidate className="space-y-4">
        {error && (
          <p role="alert" className="text-sm text-red-600 bg-red-50 px-3 py-2 rounded-lg">{error}</p>
        )}

        <div>
          <label htmlFor="prompt-title" className="block text-sm font-medium text-gray-700 mb-1">
            Title <span aria-hidden="true" className="text-red-500">*</span>
          </label>
          <input
            id="prompt-title"
            type="text"
            value={form.title}
            onChange={set('title')}
            onBlur={touch('title')}
            aria-required="true"
            aria-describedby={touched.title && errors.title ? 'title-error' : undefined}
            aria-invalid={Boolean(touched.title && errors.title)}
            className={inputClass('title')}
            placeholder="e.g. Code Review Assistant"
          />
          <FieldError msg={touched.title && errors.title} />
        </div>

        <div>
          <label htmlFor="prompt-content" className="block text-sm font-medium text-gray-700 mb-1">
            Content <span aria-hidden="true" className="text-red-500">*</span>
          </label>
          <textarea
            id="prompt-content"
            value={form.content}
            onChange={set('content')}
            onBlur={touch('content')}
            rows={6}
            aria-required="true"
            aria-describedby={touched.content && errors.content ? 'content-error' : undefined}
            aria-invalid={Boolean(touched.content && errors.content)}
            className={`${inputClass('content')} resize-none`}
            placeholder="You are a helpful assistant that..."
          />
          <FieldError msg={touched.content && errors.content} />
        </div>

        <div>
          <label htmlFor="prompt-description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <input
            id="prompt-description"
            type="text"
            value={form.description}
            onChange={set('description')}
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            placeholder="Optional short description"
          />
        </div>

        <div>
          <label htmlFor="prompt-collection" className="block text-sm font-medium text-gray-700 mb-1">
            Collection
          </label>
          <select
            id="prompt-collection"
            value={form.collection_id}
            onChange={set('collection_id')}
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          >
            <option value="">No collection</option>
            {collections.map((c) => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
        </div>

        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose} disabled={loading}>Cancel</Button>
          <Button type="submit" disabled={loading}>
            {loading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Saving…
              </span>
            ) : isEdit ? 'Save Changes' : 'Create Prompt'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
