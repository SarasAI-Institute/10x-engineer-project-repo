import { useState } from 'react';
import { CollectionList } from '../collections/CollectionList';
import { CollectionForm } from '../collections/CollectionForm';

export function Sidebar({ collections, selectedCollection, onSelectCollection, onCollectionCreated, onDeleteCollection }) {
  const [showForm, setShowForm] = useState(false);

  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
      <div className="p-4 border-b border-gray-100 flex items-center justify-between">
        <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Collections</span>
        <button
          onClick={() => setShowForm(true)}
          className="text-indigo-600 hover:text-indigo-800 p-1 rounded cursor-pointer"
          title="New collection"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
        </button>
      </div>

      <nav className="flex-1 overflow-y-auto p-2">
        <button
          onClick={() => onSelectCollection(null)}
          className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors mb-1 cursor-pointer
            ${!selectedCollection
              ? 'bg-indigo-50 text-indigo-700 font-medium'
              : 'text-gray-700 hover:bg-gray-100'}`}
        >
          All Prompts
        </button>

        <CollectionList
          collections={collections}
          selectedId={selectedCollection}
          onSelect={onSelectCollection}
          onDelete={onDeleteCollection}
        />
      </nav>

      <CollectionForm
        isOpen={showForm}
        onClose={() => setShowForm(false)}
        onCreated={(col) => { onCollectionCreated(col); setShowForm(false); }}
      />
    </aside>
  );
}
