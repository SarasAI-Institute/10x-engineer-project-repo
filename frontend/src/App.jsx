import { useState, useEffect, useCallback } from 'react';
import { Layout } from './components/layout/Layout';
import { PromptList } from './components/prompts/PromptList';
import { PromptForm } from './components/prompts/PromptForm';
import { PromptDetail } from './components/prompts/PromptDetail';
import { SearchBar } from './components/shared/SearchBar';
import { Button } from './components/shared/Button';
import { Toast } from './components/shared/Toast';
import { ConfirmDialog } from './components/shared/ConfirmDialog';
import { useToast } from './hooks/useToast';
import { useConfirm } from './hooks/useConfirm';
import { getPrompts, deletePrompt } from './api/prompts';
import { getCollections, deleteCollection } from './api/collections';

export default function App() {
  const [prompts, setPrompts] = useState([]);
  const [collections, setCollections] = useState([]);
  const [loadingPrompts, setLoadingPrompts] = useState(true);
  const [promptsError, setPromptsError] = useState('');
  const [search, setSearch] = useState('');
  const [selectedCollection, setSelectedCollection] = useState(null);

  const [showForm, setShowForm] = useState(false);
  const [editingPrompt, setEditingPrompt] = useState(null);
  const [viewingPrompt, setViewingPrompt] = useState(null);

  const { toasts, toast, dismiss } = useToast();
  const { confirm, confirmState, handleResponse } = useConfirm();

  const fetchCollections = useCallback(async () => {
    try {
      const data = await getCollections();
      setCollections(data.collections || []);
    } catch {
      // non-blocking
    }
  }, []);

  const fetchPrompts = useCallback(async () => {
    setLoadingPrompts(true);
    setPromptsError('');
    try {
      const params = {};
      if (selectedCollection) params.collection_id = selectedCollection;
      if (search) params.search = search;
      const data = await getPrompts(params);
      setPrompts(data.prompts || []);
    } catch (err) {
      setPromptsError(err.message);
    } finally {
      setLoadingPrompts(false);
    }
  }, [selectedCollection, search]);

  useEffect(() => { fetchCollections(); }, [fetchCollections]);
  useEffect(() => { fetchPrompts(); }, [fetchPrompts]);

  const handlePromptSaved = (saved) => {
    setShowForm(false);
    setEditingPrompt(null);
    fetchPrompts();
    toast(editingPrompt ? `"${saved.title}" updated` : `"${saved.title}" created`);
  };

  const handleDeletePrompt = async (prompt) => {
    const ok = await confirm(`Delete "${prompt.title}"? This cannot be undone.`);
    if (!ok) return;
    try {
      await deletePrompt(prompt.id);
      if (viewingPrompt?.id === prompt.id) setViewingPrompt(null);
      fetchPrompts();
      toast(`"${prompt.title}" deleted`);
    } catch (err) {
      toast(err.message, 'error');
    }
  };

  const handleDeleteCollection = async (id) => {
    const col = collections.find((c) => c.id === id);
    const ok = await confirm(`Delete collection "${col?.name}"? Prompts will not be deleted.`);
    if (!ok) return;
    try {
      await deleteCollection(id);
      if (selectedCollection === id) setSelectedCollection(null);
      fetchCollections();
      fetchPrompts();
      toast(`Collection "${col?.name}" deleted`);
    } catch (err) {
      toast(err.message, 'error');
    }
  };

  const openEdit = (prompt) => {
    setViewingPrompt(null);
    setEditingPrompt(prompt);
    setShowForm(true);
  };

  const isFiltered = Boolean(search || selectedCollection);
  const currentCollectionName = collections.find((c) => c.id === selectedCollection)?.name;

  return (
    <>
      <Layout
        collections={collections}
        selectedCollection={selectedCollection}
        onSelectCollection={setSelectedCollection}
        onCollectionCreated={() => fetchCollections()}
        onDeleteCollection={handleDeleteCollection}
      >
        <div className="p-4 sm:p-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
            <div>
              <h2 className="text-lg font-bold text-gray-900">
                {currentCollectionName || 'All Prompts'}
              </h2>
              <p className="text-sm text-gray-500">
                {loadingPrompts ? 'Loading…' : `${prompts.length} prompt${prompts.length !== 1 ? 's' : ''}`}
              </p>
            </div>
            <div className="flex items-center gap-2 sm:gap-3">
              <div className="flex-1 sm:w-64">
                <SearchBar
                  value={search}
                  onChange={setSearch}
                  placeholder="Search prompts…"
                />
              </div>
              <Button onClick={() => { setEditingPrompt(null); setShowForm(true); }}>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                <span className="hidden sm:inline">New Prompt</span>
                <span className="sm:hidden">New</span>
              </Button>
            </div>
          </div>

          <PromptList
            prompts={prompts}
            collections={collections}
            loading={loadingPrompts}
            error={promptsError}
            onRetry={fetchPrompts}
            onView={setViewingPrompt}
            onEdit={openEdit}
            onDelete={handleDeletePrompt}
            isFiltered={isFiltered}
          />
        </div>

        <PromptForm
          isOpen={showForm}
          onClose={() => { setShowForm(false); setEditingPrompt(null); }}
          onSaved={handlePromptSaved}
          collections={collections}
          initialData={editingPrompt}
        />

        <PromptDetail
          prompt={viewingPrompt}
          collectionName={collections.find((c) => c.id === viewingPrompt?.collection_id)?.name}
          isOpen={Boolean(viewingPrompt)}
          onClose={() => setViewingPrompt(null)}
          onEdit={() => openEdit(viewingPrompt)}
          onDelete={() => handleDeletePrompt(viewingPrompt)}
        />
      </Layout>

      <Toast toasts={toasts} onDismiss={dismiss} />
      <ConfirmDialog confirmState={confirmState} onResponse={handleResponse} />
    </>
  );
}
