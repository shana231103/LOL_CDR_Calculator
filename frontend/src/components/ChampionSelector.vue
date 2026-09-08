<!-- File: frontend/src/components/ChampionSelector.vue -->
<script setup>
import { ref, computed } from 'vue'
import { useCalculatorStore } from '../stores/calculatorStore'
import { Search, UserCheck, X } from 'lucide-vue-next'

const store = useCalculatorStore()
const isOpen = ref(false)
const searchQuery = ref('')

const filteredChampions = computed(() => {
  if (!searchQuery.value.trim()) {
    return store.champions
  }
  const q = searchQuery.value.toLowerCase()
  return store.champions.filter(
    (c) => c.name.toLowerCase().includes(q) || c.id.toLowerCase().includes(q)
  )
})

function selectChampion(champ) {
  store.selectChampion(champ)
  isOpen.value = false
  searchQuery.value = ''
}
</script>

<template>
  <div class="bg-surface border border-border-default rounded-md p-4 flex flex-col gap-3">
    <div class="flex items-center justify-between">
      <span class="text-xs uppercase tracking-wider text-text-secondary font-semibold">Champion</span>
      <button
        @click="isOpen = true"
        class="text-xs text-accent-ah hover:text-white transition-colors flex items-center gap-1 font-medium"
      >
        <UserCheck class="w-3.5 h-3.5" />
        {{ store.selectedChampion ? 'Switch Champion' : 'Select Champion' }}
      </button>
    </div>

    <!-- Active Champion Card -->
    <div
      v-if="store.selectedChampion"
      @click="isOpen = true"
      class="flex items-center gap-3.5 p-2.5 rounded bg-surface-inset border border-border-subtle hover:border-border-active cursor-pointer transition-colors"
    >
      <img
        :src="store.selectedChampion.image_url"
        :alt="store.selectedChampion.name"
        class="w-14 h-14 rounded-md object-cover border border-border-default"
      />
      <div class="flex flex-col min-w-0">
        <span class="text-base font-bold tracking-tight text-white truncate">
          {{ store.selectedChampion.name }}
        </span>
        <span class="text-xs text-text-secondary truncate">
          {{ store.selectedChampion.title }}
        </span>
      </div>
    </div>

    <div
      v-else
      @click="isOpen = true"
      class="h-16 border-2 border-dashed border-border-default hover:border-border-active rounded-md flex items-center justify-center cursor-pointer text-text-secondary hover:text-white transition-colors"
    >
      <span class="text-sm font-medium">+ Choose Champion</span>
    </div>

    <!-- Modal Popover -->
    <div
      v-if="isOpen"
      class="fixed inset-0 z-50 bg-black/75 backdrop-blur-xs flex items-center justify-center p-4"
    >
      <div
        class="bg-[#181A1F] border border-[#2A2D35] rounded-lg w-full max-w-2xl max-h-[80vh] flex flex-col shadow-2xl"
      >
        <!-- Modal Header -->
        <div class="flex items-center justify-between p-4 border-b border-border-default">
          <h2 class="text-base font-bold text-white tracking-wide">Select Champion</h2>
          <button
            @click="isOpen = false"
            class="p-1 rounded text-text-secondary hover:text-white hover:bg-surface-hover transition-colors"
          >
            <X class="w-5 h-5" />
          </button>
        </div>

        <!-- Search Bar -->
        <div class="p-3 border-b border-border-subtle bg-surface-inset">
          <div class="relative">
            <Search class="absolute left-3 top-2.5 w-4 h-4 text-text-secondary" />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search champion by name..."
              class="w-full bg-[#111215] border border-border-default rounded-md pl-9 pr-3 py-2 text-sm text-white placeholder-text-secondary focus:outline-none focus:border-accent-ah"
              autofocus
            />
          </div>
        </div>

        <!-- Champion Grid -->
        <div class="p-4 overflow-y-auto grid grid-cols-4 sm:grid-cols-6 md:grid-cols-7 gap-2.5">
          <button
            v-for="c in filteredChampions"
            :key="c.id"
            @click="selectChampion(c)"
            class="flex flex-col items-center p-2 rounded-md hover:bg-[#21242C] border border-transparent hover:border-border-active transition-all group"
          >
            <img
              :src="c.image_url"
              :alt="c.name"
              class="w-12 h-12 rounded object-cover border border-border-default group-hover:border-accent-ah transition-colors"
              loading="lazy"
            />
            <span class="text-2xs text-text-secondary group-hover:text-white mt-1.5 text-center truncate w-full font-medium">
              {{ c.name }}
            </span>
          </button>
          <div
            v-if="filteredChampions.length === 0"
            class="col-span-full py-12 text-center text-text-secondary text-sm"
          >
            No champions found matching "{{ searchQuery }}"
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
