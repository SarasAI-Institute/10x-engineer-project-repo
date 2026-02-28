import React, { useState, useEffect } from 'react'

export default function PromptForm({ onSubmit, initial = null, onCancel }){
  const [title, setTitle] = useState(initial?.title || '')
  const [content, setContent] = useState(initial?.content || '')
  const [description, setDescription] = useState(initial?.description || '')

  useEffect(()=>{
    setTitle(initial?.title || '')
    setContent(initial?.content || '')
    setDescription(initial?.description || '')
  }, [initial])

  function handleSubmit(e){
    e.preventDefault()
    const payload = { title, content, description }
    onSubmit(payload)
    if(!initial){
      setTitle(''); setContent(''); setDescription('')
    }
  }

  return (
    <form className="form" onSubmit={handleSubmit} aria-label={initial ? 'Edit prompt form' : 'Create prompt form'}>
      <label className="sr-only">Title</label>
      <input required aria-label="Title" placeholder="Title" value={title} onChange={e=>setTitle(e.target.value)} />

      <label className="sr-only">Short description</label>
      <input aria-label="Short description" placeholder="Short description" value={description} onChange={e=>setDescription(e.target.value)} />

      <label className="sr-only">Prompt content</label>
      <textarea required aria-label="Prompt content" placeholder="Prompt content" value={content} onChange={e=>setContent(e.target.value)} />

      <div className="form-actions">
        <button type="submit" className="primary">{initial ? 'Save' : 'Create'}</button>
        {initial && <button type="button" className="muted" onClick={onCancel}>Cancel</button>}
      </div>
    </form>
  )
}
