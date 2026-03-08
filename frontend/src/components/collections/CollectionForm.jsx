import { useState } from 'react';
import { Modal } from '../shared/Modal';
import { Button } from '../shared/Button';
import { createCollection } from '../../api/collections';

export function CollectionForm({ isOpen, onClose, onCreated }) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [touched, setTouched] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const nameError = touched && !name.trim() ? 'Name is required' : '';

  const handleClose = () => {
    setName(''); setDescription(''); setTouched(false); setError('');
    onClose();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setTouched(true);
    if (!name.trim()) return;
    setLoading(true);
    setError('');
    try {
      const col = await createCollection({ name: name.trim(), description: description.trim() || null });
      setName(''); setDescription(''); setTouched(false);
      onCreated(col);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title="New Collection">
      <form onSubmit={handleSubmit} noValidate className="space-y-4">
        {error && (
          <p role="alert" className="text-sm text-red-600 bg-red-50 px-3 py-2 rounded-lg">{error}</p>
        )}
        <div>
          <label htmlFor="col-name" className="block text-sm font-medium text-gray-700 mb-1">
            Name <span aria-hidden="true" className="text-red-500">*</span>
          </label>
          <input
            id="col-name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            onBlur={() => setTouched(true)}
            aria-required="true"
            aria-invalid={Boolean(nameError)}
            className={`w-full px-3 py-2 text-sm border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent
              ${nameError ? 'border-red-400 bg-red-50' : 'border-gray-300'}`}
            placeholder="e.g. Marketing Prompts"
          />
          {nameError && <p role="alert" className="mt-1 text-xs text-red-600">{nameError}</p>}
        </div>
        <div>
          <label htmlFor="col-desc" className="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea
            id="col-desc"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
            placeholder="Optional description..."
          />
        </div>
        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={handleClose} disabled={loading}>Cancel</Button>
          <Button type="submit" disabled={loading}>
            {loading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Creating…
              </span>
            ) : 'Create'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
