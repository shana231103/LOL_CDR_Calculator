// File: frontend/src/services/api.js

import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const api = {
  async getChampions() {
    const res = await apiClient.get('/champions')
    return res.data
  },

  async getChampion(id) {
    const res = await apiClient.get(`/champions/${id}`)
    return res.data
  },

  async getItems(search = '') {
    const params = search ? { search } : {}
    const res = await apiClient.get('/items', { params })
    return res.data
  },

  async getRunes() {
    const res = await apiClient.get('/runes')
    return res.data
  },

  async getSpells() {
    const res = await apiClient.get('/summoner-spells')
    return res.data
  },

  async calculateCooldowns(payload) {
    const res = await apiClient.post('/calculate', payload)
    return res.data
  },

  async syncPatch(force = false) {
    const res = await apiClient.post('/sync', null, { params: { force } })
    return res.data
  },

  async getHealth() {
    const res = await apiClient.get('/health')
    return res.data
  },
}

export default api
