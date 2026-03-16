import { useEffect, useMemo, useState } from 'react';
import Layout from './components/layout/Layout';
import PromptList from './components/prompts/PromptList';
import PromptDetail from './components/prompts/PromptDetail';
import PromptForm from './components/prompts/PromptForm';
import CollectionList from './components/collections/CollectionList';
import CollectionForm from './components/collections/CollectionForm';
import SearchBar from './components/shared/SearchBar';
import Button from './components/shared/Button';
import Modal from './components/shared/Modal';
import LoadingSpinner from './components/shared/LoadingSpinner';
import ErrorMessage from './components/shared/ErrorMessage';
import { createCollection, getCollections } from './api/collections';
import { createPrompt, deletePrompt, getPrompts, updatePrompt } from './api/prompts';
import request from './api/client';

const promptSeed = [
  {
    id: 'prompt-1',
    title: 'Weekly meeting recap',
    content: 'Summarize the last standup with highlights, blockers, and next steps for the team.',
    description: 'Send an update with what happened in the meeting.',
    collection_id: 'collection-1',
  },
  {
    id: 'prompt-2',
    title: 'Product research assistant',
    content: 'Condense customer interviews into themes, pain points, and ideas.',
    description: 'Capture insights from research notes into action items.',
    collection_id: 'collection-2',
  },
  {
    id: 'prompt-3',
    title: 'Executive summary',
    content: 'Translate weekly metrics into a short memo with risk/opportunity.',
    description: 'Deliver a concise memo for leadership.',
    collection_id: 'collection-3',
  },
];

const collectionSeed = [
  { id: 'collection-1', name: 'Team Rituals', description: 'Templates used during recurring rituals and standups.' },
  { id: 'collection-2', name: 'Research', description: 'Customer discovery and research prompt bank.' },
  { id: 'collection-3', name: 'Reports', description: 'Summaries, memos, and executive-ready templates.' },
];

function App() {
  const [statusText, setStatusText] = useState('Checking API connectivity...');
  const [statusState, setStatusState] = useState('pending');
  const [prompts, setPrompts] = useState([]);
  const [collections, setCollections] = useState([]);
  const [activePrompt, setActivePrompt] = useState(null);
  const [query, setQuery] = useState('');
  const [isModalOpen, setModalOpen] = useState(false);
  const [isLoadingPrompts, setLoadingPrompts] = useState(true);
  const [isLoadingCollections, setLoadingCollections] = useState(true);
  const [errorText, setErrorText] = useState('');
  const [promptFormError, setPromptFormError] = useState('');
  const [collectionFormError, setCollectionFormError] = useState('');
  const [isSubmittingPrompt, setSubmittingPrompt] = useState(false);
  const [isSubmittingCollection, setSubmittingCollection] = useState(false);
  const [editingPrompt, setEditingPrompt] = useState(null);
  const [isDeletingPrompt, setDeletingPrompt] = useState(false);

  const focusPromptForm = () => {
    document.getElementById('prompt-title')?.focus();
  };

  const focusCollectionForm = () => {
    document.getElementById('collection-name')?.focus();
  };

  const handleStartEditing = () => {
    if (activePrompt) {
      setEditingPrompt(activePrompt);
      focusPromptForm();
    }
  };

  const handleCancelEditing = () => {
    setEditingPrompt(null);
    setPromptFormError('');
  };

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await request('/health');
        const versionLabel = response?.version ? `v${response.version}` : 'v1';
        setStatusText(response?.status ? `API ${response.status} (${versionLabel})` : 'API connection healthy');
        setStatusState('success');
      } catch (error) {
        setStatusText('Unable to reach the API. Configure VITE_API_URL in .env');
        setStatusState('error');
      }
    };

    checkStatus();
  }, []);

  useEffect(() => {
    const loadPrompts = async () => {
      setLoadingPrompts(true);
      try {
        const data = await getPrompts();
        const results = Array.isArray(data?.prompts) ? data.prompts : [];
        setPrompts(results.length ? results : promptSeed);
      } catch (error) {
        setErrorText('Unable to load prompts from the API. Showing cached data.');
        setPrompts(promptSeed);
      } finally {
        setLoadingPrompts(false);
      }
    };

    const loadCollections = async () => {
      setLoadingCollections(true);
      try {
        const data = await getCollections();
        const results = Array.isArray(data?.collections) ? data.collections : [];
        setCollections(results.length ? results : collectionSeed);
      } catch (error) {
        setErrorText((prev) => prev || 'Unable to load collections. Displaying examples only.');
        setCollections(collectionSeed);
      } finally {
        setLoadingCollections(false);
      }
    };

    loadPrompts();
    loadCollections();
  }, []);

  useEffect(() => {
    if (!activePrompt && prompts.length) {
      setActivePrompt(prompts[0]);
    }
  }, [prompts, activePrompt]);

  const collectionLookup = useMemo(() => {
    const map = {};
    collections.forEach((collection) => {
      map[collection.id] = collection.name;
    });
    return map;
  }, [collections]);

  const collectionCounts = useMemo(() => {
    return prompts.reduce((acc, prompt) => {
      const key = prompt.collection_id ?? 'unassigned';
      acc[key] = (acc[key] ?? 0) + 1;
      return acc;
    }, {});
  }, [prompts]);

  const statusBadge = useMemo(() => {
    if (statusState === 'success') return 'bg-emerald-500/90';
    if (statusState === 'error') return 'bg-rose-500/90';
    return 'bg-amber-400/90';
  }, [statusState]);

  const filteredPrompts = useMemo(() => {
    if (!query) return prompts;
    return prompts.filter((prompt) => prompt.title.toLowerCase().includes(query.toLowerCase()));
  }, [prompts, query]);

  const handlePromptSubmit = async (form) => {
    const payload = {
      title: form.title,
      content: form.content,
      description: form.description || undefined,
      collection_id: form.collectionId || undefined,
    };

    setSubmittingPrompt(true);
    setPromptFormError('');

    if (editingPrompt) {
      try {
        const response = await updatePrompt(editingPrompt.id, payload);
        const saved = response ?? { ...editingPrompt, ...payload };
        setPrompts((prev) => prev.map((prompt) => (prompt.id === saved.id ? saved : prompt)));
        setActivePrompt(saved);
        setEditingPrompt(null);
        setErrorText('');
      } catch (error) {
        setPromptFormError(error.message ?? 'Failed to update prompt.');
      } finally {
        setSubmittingPrompt(false);
      }
      return;
    }

    const fallbackPrompt = {
      id: `prompt-${Date.now()}`,
      ...payload,
    };

    try {
      const response = await createPrompt(payload);
      const saved = response ?? fallbackPrompt;
      setPrompts((prev) => [saved, ...prev]);
      setActivePrompt(saved);
      setErrorText('');
    } catch (error) {
      setPrompts((prev) => [fallbackPrompt, ...prev]);
      setActivePrompt(fallbackPrompt);
      setPromptFormError(error.message ?? 'Failed to save prompt. Local copy created.');
    } finally {
      setSubmittingPrompt(false);
    }
  };

  const handleCollectionSubmit = async (form) => {
    const fallbackCollection = {
      id: `collection-${Date.now()}`,
      name: form.name,
      description: form.description || 'Fresh collection',
    };

    setSubmittingCollection(true);
    setCollectionFormError('');

    try {
      const response = await createCollection({
        name: form.name,
        description: form.description || undefined,
      });
      const saved = response ?? fallbackCollection;
      setCollections((prev) => [saved, ...prev]);
      setErrorText('');
    } catch (error) {
      setCollections((prev) => [fallbackCollection, ...prev]);
      setCollectionFormError(error.message ?? 'Failed to create collection. Added locally.');
    } finally {
      setSubmittingCollection(false);
    }
  };

  const handleDeletePrompt = async (promptId) => {
    if (!promptId) return;
    setDeletingPrompt(true);
    try {
      await deletePrompt(promptId);
      const nextActive = prompts.find((prompt) => prompt.id !== promptId) ?? null;
      setPrompts((prev) => prev.filter((prompt) => prompt.id !== promptId));
      setActivePrompt(nextActive);
      if (editingPrompt?.id === promptId) {
        setEditingPrompt(null);
      }
      setErrorText('');
    } catch (error) {
      setErrorText(error.message ?? 'Failed to delete prompt.');
    } finally {
      setDeletingPrompt(false);
    }
  };

  return (
    <Layout>
      <div className="space-y-10">
        <section className="space-y-6">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-center">
            <div className="flex-1">
              <SearchBar value={query} onChange={setQuery} />
            </div>
            <Button onClick={() => setModalOpen(true)} variant="ghost">
              Browse collections
            </Button>
          </div>

          {errorText && <ErrorMessage message={errorText} />}

          <div className="rounded-3xl border border-white/10 bg-slate-900/80 p-6">
            <div className="flex flex-wrap items-center gap-3">
              <span className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wider text-slate-900 ${statusBadge}`}>
                {statusState === 'success' ? 'Connected' : statusState === 'error' ? 'Offline' : 'Checking'}
              </span>
              <p className="text-sm text-slate-300">{statusText}</p>
            </div>
            <div className="mt-4">
              {statusState === 'pending' ? (
                <LoadingSpinner label="Checking your API" />
              ) : statusState === 'error' ? (
                <ErrorMessage message={statusText} />
              ) : null}
            </div>
          </div>

          {isLoadingPrompts ? (
            <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-6">
              <LoadingSpinner label="Loading prompts" />
            </div>
          ) : (
            <PromptList
              prompts={filteredPrompts}
              onSelect={setActivePrompt}
              selectedId={activePrompt?.id}
              collectionLookup={collectionLookup}
              emptyActionProps={{ onClick: focusPromptForm }}
            />
          )}
        </section>

        <section className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_minmax(0,0.85fr)]">
          <div className="space-y-5">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-white">Prompt detail</h2>
              <p className="text-sm text-slate-400">Live preview</p>
            </div>
            <PromptDetail
              prompt={activePrompt}
              collectionName={collectionLookup[activePrompt?.collection_id]}
              onEdit={handleStartEditing}
              onDelete={() => handleDeletePrompt(activePrompt?.id)}
              isDeleting={isDeletingPrompt}
            />
          </div>

          <div className="space-y-8">
            <div className="space-y-3 rounded-3xl border border-white/5 bg-slate-900/80 p-6">
              <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Create prompt</p>
              <PromptForm
                onSubmit={handlePromptSubmit}
                collections={collections}
                isSubmitting={isSubmittingPrompt}
                error={promptFormError}
                initialData={editingPrompt}
                mode={editingPrompt ? 'edit' : 'create'}
                onCancel={handleCancelEditing}
              />
            </div>

            <div className="space-y-3 rounded-3xl border border-white/5 bg-slate-900/80 p-6">
              <div className="flex items-center justify-between">
                <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Collections</p>
                <span className="text-sm text-emerald-400">{collections.length} total</span>
              </div>
              <CollectionForm
                onSubmit={handleCollectionSubmit}
                isSubmitting={isSubmittingCollection}
                error={collectionFormError}
              />
              {isLoadingCollections ? (
                <LoadingSpinner label="Fetching collections" />
              ) : (
                <CollectionList
                  collections={collections.slice(0, 3)}
                  counts={collectionCounts}
                  actionProps={{ onClick: focusCollectionForm }}
                />
              )}
            </div>
          </div>
        </section>
      </div>

      <Modal isOpen={isModalOpen} title="Collections" onClose={() => setModalOpen(false)}>
        {isLoadingCollections ? (
          <LoadingSpinner label="Loading collections" />
        ) : (
          <CollectionList
            collections={collections}
            counts={collectionCounts}
            actionProps={{ onClick: focusCollectionForm }}
          />
        )}
        <Button onClick={() => setModalOpen(false)} className="w-full">
          Close
        </Button>
      </Modal>
    </Layout>
  );
}

export default App;
