import React, { useEffect, useState } from 'react'
import { fetchCollections, createCollection, deleteCollection } from '../api'

export default function Collections(){
  const [collections, setCollections] = useState([])
  const [loading, setLoading] = useState(true)
  const [name, setName] = useState('')

  useEffect(()=>{ load() }, [])

  async function load(){
    setLoading(true)
    try{
      const d = await fetchCollections()
      setCollections(d.collections || d)
    }catch(err){
      console.error(err)
    }finally{ setLoading(false) }
  }

  async function handleCreate(e){
    e.preventDefault()
    if(!name.trim()) return
    try{
      const created = await createCollection({ name, description: '' })
      setCollections(prev => [created, ...prev])
      setName('')
    }catch(err){
      alert('Create failed: ' + err.message)
    }
  }

  async function handleDelete(id){
    if(!confirm('Delete this collection? This will keep prompts but remove the collection reference.')) return
    try{
      await deleteCollection(id)
      setCollections(prev => prev.filter(c => c.id !== id))
    }catch(err){
      alert('Delete failed: ' + err.message)
    }
  }

  if(loading) return <div className="panel">Loading collections...</div>

  return (
    <div className="panel">
      <h3>Collections</h3>
      <form onSubmit={handleCreate} className="inline-form" aria-label="Create collection form">
        <input aria-label="New collection name" placeholder="New collection" value={name} onChange={e=>setName(e.target.value)} />
        <button type="submit" className="primary">Add</button>
      </form>
      <ul className="collections">
        {collections.map(c => (
          <li key={c.id}>
            <span>{c.name}</span>
            <button className="danger" onClick={()=>handleDelete(c.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  )
}
