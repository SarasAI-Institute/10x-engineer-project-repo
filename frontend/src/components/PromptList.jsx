import React, { useEffect, useState } from 'react'
import { fetchPrompts, createPrompt, deletePrompt, patchPrompt } from '../api'
import PromptForm from './PromptForm'

export default function PromptList(){
  const [prompts, setPrompts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [editing, setEditing] = useState(null)
  const [query, setQuery] = useState('')

  useEffect(()=>{
    load()
  }, [])

  async function load(){
    setLoading(true)
    setError(null)
    try{
      const data = await fetchPrompts()
      setPrompts(data.prompts || data)
    }catch(err){
      setError(err.message)
    }finally{
      setLoading(false)
    }
  }

  async function handleCreate(payload){
    try{
      const created = await createPrompt(payload)
      setPrompts(prev => [created, ...prev])
    }catch(err){
      alert('Create failed: ' + err.message)
    }
  }

  async function handleDelete(id){
    if(!confirm('Delete this prompt?')) return
    try{
      await deletePrompt(id)
      setPrompts(prev => prev.filter(p => p.id !== id))
    }catch(err){
      alert('Delete failed: ' + err.message)
    }
  }

  async function handlePatch(id, patch){
    try{
      const updated = await patchPrompt(id, patch)
      setPrompts(prev => prev.map(p => p.id === id ? updated : p))
      setEditing(null)
    }catch(err){
      alert('Update failed: ' + err.message)
    }
  }

  if (loading) return <div className="panel">Loading prompts...</div>
  if (error) return <div className="panel error">Error: {error}</div>

  return (
    <div>
      <div className="panel">
        <div className="panel-header">
          <h2>Prompts</h2>
          <div className="controls">
            <input aria-label="Search prompts" placeholder="Search prompts..." value={query} onChange={e=>setQuery(e.target.value)} />
            <button className="secondary" onClick={async ()=>{
              setLoading(true); try{ const d = await fetchPrompts(query); setPrompts(d.prompts || d) }catch(e){ setError(e.message) }finally{ setLoading(false) }
            }}>Search</button>
          </div>
        </div>

        <PromptForm onSubmit={handleCreate} />
      </div>

      <div className="grid">
        {prompts.length === 0 && <div className="empty">No prompts yet — create one using the form above</div>}
        {prompts.map(p => (
          <div className="card" key={p.id}>
            <h3>{p.title}</h3>
            {p.description && <p className="muted">{p.description}</p>}
            <pre className="content" aria-label={`Prompt content for ${p.title}`}>{p.content}</pre>
            <div className="actions">
              <button onClick={()=>setEditing(p)}>Edit</button>
              <button className="danger" onClick={()=>handleDelete(p.id)}>Delete</button>
            </div>
            {editing && editing.id === p.id && (
              <PromptForm
                initial={editing}
                onSubmit={(payload)=>handlePatch(editing.id, payload)}
                onCancel={()=>setEditing(null)}
              />
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
