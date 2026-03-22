import { useEffect, useState, useCallback } from "react";
import api from "../api/client";
import { getCollections } from "../api/collections";

import PromptForm from "../components/prompts/PromptForm";
import PromptList from "../components/prompts/PromptList";
import SearchBar from "../components/shared/SearchBar";

import CollectionList from "../components/collections/CollectionList";
import CollectionForm from "../components/collections/CollectionForm";

function Dashboard() {
  const [prompts, setPrompts] = useState([]);
  const [collections, setCollections] = useState([]);
  const [selectedCollection, setSelectedCollection] = useState(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedPrompt, setSelectedPrompt] = useState(null);
  const [search, setSearch] = useState("");

  // 🔥 Fetch prompts with search + collection filter
  const fetchPrompts = useCallback((searchValue = "", collectionId = null) => {
    setLoading(true);
    setError(null);

    const query = `/prompts/?search=${searchValue}&collection_id=${collectionId || ""}`;

    api.get(query)
      .then((res) => {
        setPrompts(res.data.prompts);
      })
      .catch(() => {
        setError("Failed to load prompts");
      })
      .finally(() => setLoading(false));
  }, []);

  // 🔥 Fetch collections
  const fetchCollections = () => {
    getCollections()
      .then((res) => {
        setCollections(res.data.collections);
      })
      .catch((err) => console.error(err));
  };

  const handleDelete = (id) => {
    api.delete(`/prompts/${id}`)
      .then(() => fetchPrompts(search, selectedCollection))
      .catch((err) => console.error(err));
  };

  const handleEdit = (prompt) => {
    setSelectedPrompt(prompt);
  };

  // 🔥 Load prompts when search or collection changes
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchPrompts(search, selectedCollection);
  }, [search, selectedCollection, fetchPrompts]);

  // 🔥 Load collections once
  useEffect(() => {
    fetchCollections();
  }, []);

  return (
    <div className="max-w-6xl mx-auto">

      {/* Collections */}
      <CollectionForm onSuccess={fetchCollections} />

      <CollectionList
        collections={collections}
        selected={selectedCollection}
        onSelect={setSelectedCollection}
      />

      {/* Search */}
      <SearchBar onSearch={setSearch} />

      {/* Form */}
      <div className="bg-white p-4 rounded-xl shadow mb-6">
        <PromptForm
          onSuccess={() => fetchPrompts(search, selectedCollection)}
          selectedPrompt={selectedPrompt}
          setSelectedPrompt={setSelectedPrompt}
        />
      </div>

      {/* Loading */}
      {loading && (
        <div className="text-center text-gray-500 py-10">
          Loading prompts...
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="text-center text-red-500 py-4">
          {error}
        </div>
      )}

      {/* List */}
      {!loading && !error && (
        <PromptList
          prompts={prompts}
          onDelete={handleDelete}
          onEdit={handleEdit}
        />
      )}
    </div>
  );
}

export default Dashboard;