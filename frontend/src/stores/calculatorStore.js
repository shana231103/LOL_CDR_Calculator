// File: frontend/src/stores/calculatorStore.js

import { defineStore } from 'pinia'
import api from '../services/api'
import { messages } from '../locales/messages'

export const useCalculatorStore = defineStore('calculator', {
  state: () => ({
    currentLocale: localStorage.getItem('lol_cdr_locale') || 'vi_VN',
    champions: [],
    selectedChampion: null,
    skillRanks: { Q: 1, W: 1, E: 1, R: 1 },
    items: [null, null, null, null, null, null],
    availableItems: [],
    runes: [],
    selectedRunes: {},
    spells: [],
    selectedSpells: [null, null],
    calculationResult: null,
    activePatch: 'Active',
    isLoading: false,
    isCalculating: false,
    error: null,
    _debounceTimer: null,
  }),

  getters: {
    totalItemHaste: (state) => {
      return state.items.reduce((acc, item) => acc + (item ? item.ability_haste : 0), 0)
    },
    totalItemUltHaste: (state) => {
      return state.items.reduce((acc, item) => acc + (item ? (item.ultimate_haste || 0) : 0), 0)
    },
    totalItemBasicHaste: (state) => {
      return state.items.reduce((acc, item) => acc + (item ? (item.basic_haste || 0) : 0), 0)
    },
    totalItemSummHaste: (state) => {
      return state.items.reduce((acc, item) => acc + (item ? (item.summoner_haste || 0) : 0), 0)
    },
    activeRunesCount: (state) => {
      return Object.keys(state.selectedRunes).length
    },
  },

  actions: {
    t(key) {
      return messages[this.currentLocale]?.[key] || messages['vi_VN']?.[key] || key
    },

    async setLocale(newLocale) {
      if (this.currentLocale === newLocale) return
      this.currentLocale = newLocale
      localStorage.setItem('lol_cdr_locale', newLocale)

      this.isLoading = true
      try {
        const prevChampId = this.selectedChampion?.id
        const prevItemIds = this.items.map((it) => (it ? it.id : null))
        const prevSpellIds = this.selectedSpells.map((s) => (s ? s.id : null))

        const [champions, items, runes, spells] = await Promise.all([
          api.getChampions(newLocale),
          api.getItems('', newLocale),
          api.getRunes(newLocale),
          api.getSpells(newLocale),
        ])

        this.champions = champions
        this.availableItems = items
        this.runes = runes
        this.spells = spells

        if (prevChampId) {
          const found = champions.find((c) => c.id === prevChampId)
          if (found) {
            this.selectedChampion = found
          }
        }

        this.items = prevItemIds.map((id) => (id != null ? items.find((i) => String(i.id) === String(id)) || null : null))
        this.selectedSpells = prevSpellIds.map((id) => (id != null ? spells.find((s) => String(s.id) === String(id)) || null : null))

        this.triggerCalculate()
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Failed to switch language'
      } finally {
        this.isLoading = false
      }
    },

    async init() {
      this.isLoading = true
      this.error = null
      try {
        const [champions, items, runes, spells] = await Promise.all([
          api.getChampions(this.currentLocale),
          api.getItems('', this.currentLocale),
          api.getRunes(this.currentLocale),
          api.getSpells(this.currentLocale),
        ])

        this.champions = champions
        this.availableItems = items
        this.runes = runes
        this.spells = spells

        // Select default champion if available (e.g. Ahri or first one)
        if (champions.length > 0) {
          const defaultChamp = champions.find((c) => c.id === 'Ahri') || champions[0]
          this.selectChampion(defaultChamp)
        }

        // Set default summoner spells if available (Flash + Teleport / Ignite)
        if (spells.length >= 2) {
          const flash = spells.find((s) => s.id === 'SummonerFlash') || spells[0]
          const second = spells.find((s) => s.id === 'SummonerDot' || s.id === 'SummonerTeleport') || spells[1]
          this.selectedSpells = [flash, second]
        }
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Failed to initialize calculator data'
      } finally {
        this.isLoading = false
      }
    },

    selectChampion(champ) {
      if (!champ) return
      this.selectedChampion = champ
      this.skillRanks = { Q: 1, W: 1, E: 1, R: 1 }

      if (champ.abilities) {
        champ.abilities.forEach((ab) => {
          this.skillRanks[ab.slot] = 1
        })
      }
      this.triggerCalculate()
    },

    setSkillRank(slot, rank) {
      if (!this.selectedChampion) return
      const ab = this.selectedChampion.abilities?.find((a) => a.slot === slot)
      const maxRank = ab ? ab.max_rank : 5
      const newRank = Math.max(1, Math.min(rank, maxRank))
      this.skillRanks[slot] = newRank
      this.triggerCalculate()
    },

    setItem(index, item) {
      if (index < 0 || index >= 6) return
      this.items[index] = item
      this.triggerCalculate()
    },

    removeItem(index) {
      if (index < 0 || index >= 6) return
      this.items[index] = null
      this.triggerCalculate()
    },

    toggleRune(rune) {
      if (this.selectedRunes[rune.id] !== undefined) {
        delete this.selectedRunes[rune.id]
      } else {
        this.selectedRunes[rune.id] = rune.max_stacks > 0 ? rune.max_stacks : 0
      }
      this.triggerCalculate()
    },

    setRuneStacks(runeId, stacks) {
      const rune = this.runes.find((r) => r.id === runeId)
      if (!rune) return
      const bounded = Math.max(0, Math.min(stacks, rune.max_stacks))
      this.selectedRunes[runeId] = bounded
      this.triggerCalculate()
    },

    setSpell(index, spell) {
      if (index < 0 || index >= 2) return
      this.selectedSpells[index] = spell
      this.triggerCalculate()
    },

    removeSpell(index) {
      if (index < 0 || index >= 2) return
      this.selectedSpells[index] = null
      this.triggerCalculate()
    },

    resetBuild() {
      this.skillRanks = { Q: 1, W: 1, E: 1, R: 1 }
      this.items = [null, null, null, null, null, null]
      this.selectedRunes = {}
      this.triggerCalculate()
    },

    triggerCalculate() {
      if (this._debounceTimer) {
        clearTimeout(this._debounceTimer)
      }
      this._debounceTimer = setTimeout(() => {
        this.executeCalculation()
      }, 150)
    },

    async executeCalculation() {
      if (!this.selectedChampion) return
      this.isCalculating = true
      try {
        const itemIds = this.items.filter(Boolean).map((i) => i.id)
        const runesPayload = Object.entries(this.selectedRunes).map(([id, stacks]) => ({
          rune_id: parseInt(id, 10),
          stacks: Number(stacks),
        }))
        const spellIds = this.selectedSpells.filter(Boolean).map((s) => s.id)

        const payload = {
          champion_id: this.selectedChampion.id,
          abilities: this.skillRanks,
          items: itemIds,
          runes: runesPayload,
          summoner_spells: spellIds,
          locale: this.currentLocale,
        }

        const res = await api.calculateCooldowns(payload)
        this.calculationResult = res
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Calculation failed'
      } finally {
        this.isCalculating = false
      }
    },
  },
})
