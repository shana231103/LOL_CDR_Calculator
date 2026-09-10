// File: frontend/src/services/api.js

import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const api = {
  async getChampions(locale = 'vi_VN') {
    const res = await apiClient.get('/champions', { params: { locale } })
    return res.data
  },

  async getChampion(id, locale = 'vi_VN') {
    const res = await apiClient.get(`/champions/${id}`, { params: { locale } })
    return res.data
  },

  async getItems(search = '', locale = 'vi_VN') {
    const params = { locale }
    if (search) {
      params.search = search
    }
    const res = await apiClient.get('/items', { params })
    return res.data
  },

  async getRunes(locale = 'vi_VN') {
    const res = await apiClient.get('/runes', { params: { locale } })
    return res.data
  },

  async getSpells(locale = 'vi_VN') {
    const res = await apiClient.get('/summoner-spells', { params: { locale } })
    return res.data
  },

  async calculateCooldowns(payload) {
    const res = await apiClient.post('/calculate', payload)
    return res.data
  },

  async syncPatch(force = false, locales = 'vi_VN,en_US') {
    const params = { force }
    if (locales) {
      params.locales = locales
    }
    const res = await apiClient.post('/sync', null, { params })
    return res.data
  },

  async getHealth() {
    const res = await apiClient.get('/health')
    return res.data
  },
}

export default api
