import { useEffect, useState } from "react";
import api from "../../api/client";

function PromptForm({ onSuccess, selectedPrompt, setSelectedPrompt }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (selectedPrompt) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setTitle(selectedPrompt.title || "");
      setDescription(selectedPrompt.content || "");
    }
  }, [selectedPrompt]);

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);

    const payload = {
      title,
      content: description,
      tags: [],
      collection_id: null,
    };

    const request = selectedPrompt
      ? api.put(`/prompts/${selectedPrompt.id}`, payload)
      : api.post("/prompts/", payload);

    request
      .then((res) => {
        console.log("SUCCESS:", res.data);

        setTitle("");
        setDescription("");
        setSelectedPrompt(null);

        onSuccess();
      })
      .catch((err) => {
        console.error("FORM ERROR:", err.response?.data);
      })
      .finally(() => setLoading(false));
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
      <h2>{selectedPrompt ? "Edit Prompt" : "Create Prompt"}</h2>

      <input
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />

      <br />

      <textarea
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        required
      />

      <br />

      <button type="submit" disabled={loading}>
        {loading
          ? "Saving..."
          : selectedPrompt
          ? "Update"
          : "Create"}
      </button>

      {selectedPrompt && (
        <button
          type="button"
          onClick={() => {
            setSelectedPrompt(null);
            setTitle("");
            setDescription("");
          }}
        >
          Cancel
        </button>
      )}
    </form>
  );
}

export default PromptForm;