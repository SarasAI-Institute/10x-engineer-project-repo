import { Modal } from '../shared/Modal';
import { Button } from '../shared/Button';

/**
 * Modal component displaying the full details of a single prompt.
 *
 * Shows the prompt title as the modal heading, with optional description,
 * full content in a monospace pre block, collection badge, and formatted
 * created/updated timestamps. Action buttons for editing and deleting are
 * rendered in a footer row.
 *
 * Returns null when `prompt` is falsy so callers can safely pass `null`
 * when no prompt is selected without needing conditional rendering.
 *
 * @param {Object} props - Component props.
 * @param {{
 *   title: string,
 *   content: string,
 *   description?: string,
 *   collection_id?: string,
 *   created_at: string,
 *   updated_at: string
 * }|null} props.prompt - The prompt to display, or null to render nothing.
 * @param {string} [props.collectionName] - Human-readable collection name for the badge.
 * @param {boolean} props.isOpen - Controls modal visibility.
 * @param {function(): void} props.onClose - Callback to close the modal.
 * @param {function(): void} props.onEdit - Callback invoked when the Edit button is clicked.
 * @param {function(): void} props.onDelete - Callback invoked when the Delete button is clicked.
 * @returns {JSX.Element|null} The detail modal, or null when prompt is falsy.
 *
 * @example
 * <PromptDetail
 *   prompt={viewingPrompt}
 *   collectionName="Marketing"
 *   isOpen={Boolean(viewingPrompt)}
 *   onClose={() => setViewingPrompt(null)}
 *   onEdit={() => openEdit(viewingPrompt)}
 *   onDelete={() => handleDeletePrompt(viewingPrompt)}
 * />
 */
export function PromptDetail({ prompt, collectionName, isOpen, onClose, onEdit, onDelete }) {
  if (!prompt) return null;

  /**
   * Formats an ISO date string into a long human-readable date and time.
   *
   * @param {string} iso - An ISO 8601 date string (e.g. '2024-03-08T14:30:00Z').
   * @returns {string} Formatted string such as 'March 8, 2024 at 02:30 PM'.
   *
   * @example
   * formatDate('2024-03-08T14:30:00Z'); // 'March 8, 2024 at 02:30 PM'
   */
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
