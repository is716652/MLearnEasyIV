export type ContentItem = {
  id: number
  module: string
  subcategory: string
  title: string
  content_body: string
  python_code: string
  formulas?: Record<string, string>
  charts_data?: Record<string, any>
  tags?: string[]
  created_at?: string
  updated_at?: string
}

const API_BASE = (import.meta as any).env?.VITE_API_BASE || 'http://localhost:8000/api/v1'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(text || `HTTP ${res.status}`)
  }
  return res.json() as Promise<T>
}

export const api = {
  base: API_BASE,
  listContents(params?: { module?: string; subcategory?: string; skip?: number; limit?: number }) {
    const q: string[] = []
    if (params?.module) q.push(`module=${encodeURIComponent(params.module)}`)
    if (params?.subcategory) q.push(`subcategory=${encodeURIComponent(params.subcategory)}`)
    if (typeof params?.skip === 'number') q.push(`skip=${params.skip}`)
    if (typeof params?.limit === 'number') q.push(`limit=${params.limit}`)
    const qs = q.length ? `?${q.join('&')}` : ''
    return request<ContentItem[]>(`/content/${qs}`)
  },
  getContentById(id: number) {
    return request<ContentItem>(`/content/${id}`)
  },
  search(params: { query: string; module?: string; skip?: number; limit?: number }) {
    const q: string[] = [`query=${encodeURIComponent(params.query)}`]
    if (params.module) q.push(`module=${encodeURIComponent(params.module)}`)
    if (typeof params.skip === 'number') q.push(`skip=${params.skip}`)
    if (typeof params.limit === 'number') q.push(`limit=${params.limit}`)
    return request<{ results: ContentItem[]; total_count: number }>(`/search/?${q.join('&')}`)
  },
}