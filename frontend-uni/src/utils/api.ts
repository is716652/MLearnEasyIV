export type ContentItem = {
  id: number
  module: string
  subcategory: string
  title: string
  content_body: string
  python_code: string
  formulas?: Record<string, string | any>
  charts_data?: Record<string, any>
  tags?: string[] | string
  created_at?: string
  updated_at?: string
}

type TokenPair = { access_token: string; refresh_token: string; token_type: string }

type Favorite = { id: number; content_id: number; note?: string | null; created_at: string }

type ContentSummary = { id: number; title: string; module?: string; subcategory?: string; tags?: string[] | string; created_at: string }

type FavoriteWithContent = { id: number; content_id: number; note?: string | null; created_at: string; content?: ContentSummary | null }

const API_BASE = (import.meta as any).env?.VITE_API_BASE || 'http://localhost:8000/api/v1'

const tokenStore = {
  get access() { try { return localStorage.getItem('access_token') || '' } catch { return '' } },
  set access(v: string) { try { localStorage.setItem('access_token', v) } catch {} },
  get refresh() { try { return localStorage.getItem('refresh_token') || '' } catch { return '' } },
  set refresh(v: string) { try { localStorage.setItem('refresh_token', v) } catch {} },
  clear() { try { localStorage.removeItem('access_token'); localStorage.removeItem('refresh_token') } catch {} },
}

async function rawRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(init?.headers || {}) },
    ...init,
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(text || `HTTP ${res.status}`)
  }
  return res.json() as Promise<T>
}

async function authRequest<T>(path: string, init?: RequestInit): Promise<T> {
  // attach access token
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  const at = tokenStore.access
  if (at) headers['Authorization'] = `Bearer ${at}`
  try {
    return await rawRequest<T>(path, { ...init, headers })
  } catch (e: any) {
    // 如果失败，尝试用 refresh 刷新一次
    if (String(e?.message || '').includes('401') || String(e?.message || '').includes('无效或过期')) {
      const rt = tokenStore.refresh
      if (rt) {
        try {
          const pair = await rawRequest<TokenPair>('/auth/refresh', { method: 'POST', body: JSON.stringify({ refresh_token: rt }) })
          tokenStore.access = pair.access_token
          tokenStore.refresh = pair.refresh_token
          headers['Authorization'] = `Bearer ${pair.access_token}`
          return await rawRequest<T>(path, { ...init, headers })
        } catch {
          tokenStore.clear()
          throw e
        }
      }
    }
    throw e
  }
}

export const api = {
  base: API_BASE,
  // content
  listContents(params?: { module?: string; subcategory?: string; skip?: number; limit?: number }) {
    const q: string[] = []
    if (params?.module) q.push(`module=${encodeURIComponent(params.module)}`)
    if (params?.subcategory) q.push(`subcategory=${encodeURIComponent(params.subcategory)}`)
    if (typeof params?.skip === 'number') q.push(`skip=${params.skip}`)
    if (typeof params?.limit === 'number') q.push(`limit=${params.limit}`)
    const qs = q.length ? `?${q.join('&')}` : ''
    return rawRequest<ContentItem[]>(`/content/${qs}`)
  },
  getContentById(id: number) {
    return rawRequest<ContentItem>(`/content/${id}`)
  },
  search(params: { query: string; module?: string; skip?: number; limit?: number }) {
    const q: string[] = [`query=${encodeURIComponent(params.query)}`]
    if (params.module) q.push(`module=${encodeURIComponent(params.module)}`)
    if (typeof params.skip === 'number') q.push(`skip=${params.skip}`)
    if (typeof params.limit === 'number') q.push(`limit=${params.limit}`)
    return rawRequest<{ results: ContentItem[]; total_count: number }>(`/search/?${q.join('&')}`)
  },
  // auth
  async register(username: string, email: string, password: string) {
    return rawRequest<{ id: number; username: string; email: string }>(`/auth/register`, { method: 'POST', body: JSON.stringify({ username, email, password }) })
  },
  async login(username: string, password: string) {
    const form = new URLSearchParams()
    form.set('username', username)
    form.set('password', password)
    // OAuth2PasswordRequestForm requires grant_type omitted
    const pair = await fetch(`${API_BASE}/auth/login`, { method: 'POST', headers: {}, body: form as any }).then(async res => {
      if (!res.ok) throw new Error(await res.text().catch(() => `HTTP ${res.status}`))
      return res.json() as Promise<TokenPair>
    })
    tokenStore.access = pair.access_token
    tokenStore.refresh = pair.refresh_token
    return pair
  },
  async refresh() {
    const rt = tokenStore.refresh
    if (!rt) throw new Error('No refresh token')
    const pair = await rawRequest<TokenPair>(`/auth/refresh`, { method: 'POST', body: JSON.stringify({ refresh_token: rt }) })
    tokenStore.access = pair.access_token
    tokenStore.refresh = pair.refresh_token
    return pair
  },
  logout() { tokenStore.clear() },
  // me/profile
  me() { return authRequest<{ id: number; username: string; email: string }>(`/auth/me`) },
  getProfile() { return authRequest<any>(`/auth/profile`) },
  updateProfile(data: { nickname?: string; avatar_url?: string; bio?: string }) { return authRequest<any>(`/auth/profile`, { method: 'PUT', body: JSON.stringify(data) }) },
  // favorites
  addFavorite(content_id: number, note?: string) { return authRequest<Favorite>(`/auth/favorites`, { method: 'POST', body: JSON.stringify({ content_id, note }) }) },
  listFavorites() { return authRequest<Favorite[]>(`/auth/favorites`) },
  listFavoritesWithContent() { return authRequest<FavoriteWithContent[]>(`/auth/favorites/with-content`) },
  removeFavorite(content_id: number) { return authRequest<{ deleted: number }>(`/auth/favorites/${content_id}`, { method: 'DELETE' }) },
}