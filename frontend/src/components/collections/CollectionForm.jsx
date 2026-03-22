import { useState } from "react";
import { createCollection } from "../../api/collections";

function CollectionForm({ onSuccess }) {
  const [name, setName] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    createCollection({ name })
      .then(() => {
        setName("");
        onSuccess();
      })
      .catch((err) => console.error(err));
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4">
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="New collection"
        className="border p-2 rounded mr-2"
      />

      <button className="bg-black text-white px-3 py-2 rounded">
        Add
      </button>
    </form>
  );
}

export default CollectionForm;