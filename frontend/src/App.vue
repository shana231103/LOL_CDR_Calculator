<!-- File: frontend/src/App.vue -->
<script setup>
import { onMounted, ref } from 'vue'
import { useCalculatorStore } from './stores/calculatorStore'
import ChampionSelector from './components/ChampionSelector.vue'
import AbilityPanel from './components/AbilityPanel.vue'
import ItemInventory from './components/ItemInventory.vue'
import RuneSection from './components/RuneSection.vue'
import SummonerSpellSelector from './components/SummonerSpellSelector.vue'
import CooldownSummary from './components/CooldownSummary.vue'
import { RotateCcw, RefreshCw, Activity } from 'lucide-vue-next'
import api from './services/api'

const store = useCalculatorStore()
const isSyncing = ref(false)
const syncMessage = ref('')

onMounted(async () => {
  await store.init()
})

async function handleManualSync() {
  isSyncing.value = true
  syncMessage.value = ''
  try {
    const res = await api.syncPatch(true)
    syncMessage.value = `Synced ${res.patch || 'patch'}`
    await store.init()
  } catch (err) {
    syncMessage.value = 'Sync failed'
  } finally {
    isSyncing.value = false
    setTimeout(() => {
      syncMessage.value = ''
    }, 3000)
  }
}
</script>

<template>
  <div class="min-h-screen bg-app flex flex-col">
    <!-- Header Cockpit Bar -->
    <header class="border-b border-border-default bg-[#14161B] px-6 py-3 shrink-0">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <!-- Brand -->
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded bg-[#181A1F] border border-border-active flex items-center justify-center text-accent-ah font-bold">
            <Activity class="w-4 h-4" />
          </div>
          <div class="flex flex-col">
            <span class="text-sm font-bold tracking-wider uppercase text-white font-mono">
              LoL CDR Engine
            </span>
            <span class="text-3xs text-text-secondary">
              Tactical Cooldown Calculator Core
            </span>
          </div>
        </div>

        <!-- Controls & Patch Tag -->
        <div class="flex items-center gap-3">
          <div class="flex items-center gap-1.5 px-2.5 py-1 rounded bg-surface-inset border border-border-default text-xs font-mono">
            <span class="w-2 h-2 rounded-full bg-accent-success animate-pulse"></span>
            <span class="text-text-secondary">Patch:</span>
            <span class="text-white font-bold">{{ store.activePatch }}</span>
          </div>

          <button
            @click="handleManualSync"
            :disabled="isSyncing"
            class="px-2.5 py-1 rounded bg-[#21242C] border border-border-default hover:border-border-active text-xs font-medium text-text-primary hover:text-white flex items-center gap-1.5 transition-colors disabled:opacity-50"
            title="Force re-sync data from Riot Data Dragon"
          >
            <RefreshCw class="w-3 h-3" :class="{ 'animate-spin': isSyncing }" />
            <span>{{ isSyncing ? 'Syncing...' : 'Sync CDN' }}</span>
          </button>

          <span v-if="syncMessage" class="text-xs text-accent-ah font-mono">
            {{ syncMessage }}
          </span>

          <button
            @click="store.resetBuild"
            class="px-2.5 py-1 rounded bg-[#21242C] border border-border-default hover:border-border-active text-xs font-medium text-text-primary hover:text-white flex items-center gap-1.5 transition-colors"
            title="Reset active build ranks, items and runes"
          >
            <RotateCcw class="w-3 h-3" />
            <span>Reset Build</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Main 3-Column Cockpit Layout -->
    <main class="flex-1 max-w-7xl mx-auto w-full p-4 lg:p-6">
      <div v-if="store.isLoading" class="h-96 flex flex-col items-center justify-center gap-3">
        <div class="w-8 h-8 border-2 border-accent-ah border-t-transparent rounded-full animate-spin"></div>
        <span class="text-xs font-mono text-text-secondary tracking-wider uppercase">Loading Tactical Data...</span>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-12 gap-5">
        <!-- COLUMN 1: Champion & Ability Ranks (30% -> col-span-4) -->
        <div class="lg:col-span-4 flex flex-col gap-4">
          <ChampionSelector />
          <AbilityPanel />
        </div>

        <!-- COLUMN 2: Loadout Configuration (40% -> col-span-5) -->
        <div class="lg:col-span-5 flex flex-col gap-4">
          <ItemInventory />
          <RuneSection />
          <SummonerSpellSelector />
        </div>

        <!-- COLUMN 3: Telemetry & Results (30% -> col-span-3) -->
        <div class="lg:col-span-3">
          <CooldownSummary />
        </div>
      </div>
    </main>

    <!-- Footer Status -->
    <footer class="border-t border-border-subtle bg-[#111215] px-6 py-2.5 text-center text-3xs text-text-secondary font-mono">
      League of Legends CDR Engine • Authoritative Sub-50ms Calculation • DDD & Clean Architecture
    </footer>
  </div>
</template>

<style scoped>
.text-3xs {
  font-size: 9px;
  line-height: 12px;
}
</style>
