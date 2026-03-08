import { Modal } from '../shared/Modal';
import { Button } from '../shared/Button';

export function PromptDetail({ prompt, collectionName, isOpen, onClose, onEdit, onDelete }) {
  if (!prompt) return null;

  const formatDate = (iso) => new Date(iso).toLocaleString('en-US', {
    month: 'long', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit'
  });

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={prompt.title}>
      <div className="space-y-4">
        {prompt.description && (
          <p className="text-sm text-gray-600">{prompt.description}</p>
        )}

        <div>
          <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
            Prompt Content
          </label>
          <pre className="bg-gray-50 border border-gray-200 rounded-lg p-4 text-sm font-mono
            text-gray-800 whitespace-pre-wrap leading-relaxed">
            {prompt.content}
          </pre>
        </div>

        <div className="flex items-center gap-4 text-xs text-gray-500 pt-1">
          {collectionName && (
            <span className="bg-indigo-50 text-indigo-700 px-2 py-1 rounded-full font-medium">
              {collectionName}
            </span>
          )}
          <span>Created: {formatDate(prompt.created_at)}</span>
          <span>Updated: {formatDate(prompt.updated_at)}</span>
        </div>

        <div className="flex justify-end gap-2 pt-2 border-t border-gray-100">
          <Button variant="danger" size="sm" onClick={onDelete}>Delete</Button>
          <Button variant="primary" size="sm" onClick={onEdit}>Edit</Button>
        </div>
      </div>
    </Modal>
  );
}
