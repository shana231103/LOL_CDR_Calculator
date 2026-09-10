<!-- File: frontend/src/components/ItemInventory.vue -->
<script setup>
import { ref, computed } from 'vue'
import { useCalculatorStore } from '../stores/calculatorStore'
import { normalizeText } from '../utils/text'
import { Plus, X, Search } from 'lucide-vue-next'

const store = useCalculatorStore()
const activeSlot = ref(null)
const isPickerOpen = ref(false)
const searchQuery = ref('')

const filteredItems = computed(() => {
  const items = store.availableItems || []
  if (!searchQuery.value.trim()) {
    return items
  }
  const qNorm = normalizeText(searchQuery.value)
  return items.filter((i) => {
    const nameNorm = normalizeText(i.name)
    const descNorm = normalizeText(i.description || '')
    return nameNorm.includes(qNorm) || descNorm.includes(qNorm)
  })
})

function openPicker(index) {
  activeSlot.value = index
  isPickerOpen.value = true
}

function selectItem(item) {
  if (activeSlot.value !== null) {
    store.setItem(activeSlot.value, item)
  }
  closePicker()
}

function removeItem(index, event) {
  event.stopPropagation()
  store.removeItem(index)
}

function closePicker() {
  isPickerOpen.value = false
  activeSlot.value = null
  searchQuery.value = ''
}
</script>

<template>
  <div class="bg-surface border border-border-default rounded-md p-4 flex flex-col gap-3">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <span class="text-xs uppercase tracking-wider text-text-secondary font-semibold">
          {{ store.t('itemTitle') }}
        </span>
        <span class="text-2xs text-text-secondary">(Max 6)</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="flex items-center gap-1.5 px-2 py-0.5 rounded bg-surface-inset border border-border-subtle">
          <span class="text-2xs text-text-secondary">AH:</span>
          <span class="text-xs font-mono font-bold text-accent-ah tabular-nums">
            +{{ store.totalItemHaste }}
          </span>
        </div>
        <div
          v-if="store.totalItemUltHaste > 0"
          class="flex items-center gap-1.5 px-2 py-0.5 rounded bg-surface-inset border border-border-subtle"
        >
          <span class="text-2xs text-text-secondary">Ult:</span>
          <span class="text-xs font-mono font-bold text-accent-ult tabular-nums">
            +{{ store.totalItemUltHaste }}
          </span>
        </div>
      </div>
    </div>

    <!-- 2x3 Grid of Item Slots -->
    <div class="grid grid-cols-3 gap-2.5">
      <div
        v-for="(item, idx) in store.items"
        :key="idx"
        @click="openPicker(idx)"
        class="h-16 rounded-md bg-surface-inset border border-border-default hover:border-border-active transition-all cursor-pointer relative group flex items-center justify-center overflow-hidden"
      >
        <template v-if="item">
          <img
            :src="item.image_url"
            :alt="item.name"
            class="w-full h-full object-cover"
          />
          <!-- Remove button on hover -->
          <button
            @click="removeItem(idx, $event)"
            class="absolute top-1 right-1 w-5 h-5 rounded bg-black/80 text-text-secondary hover:text-white flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
            :title="store.t('remove')"
          >
            <X class="w-3.5 h-3.5" />
          </button>
          <!-- Haste Badges -->
          <div class="absolute bottom-1 left-1 flex flex-col gap-0.5 pointer-events-none">
            <span
              v-if="item.ability_haste > 0"
              class="px-1 py-0.5 rounded text-3xs font-mono font-bold bg-[#111215]/90 text-accent-ah border border-border-subtle leading-none"
            >
              +{{ item.ability_haste }}
            </span>
            <span
              v-if="item.ultimate_haste > 0"
              class="px-1 py-0.5 rounded text-3xs font-mono font-bold bg-[#111215]/90 text-accent-ult border border-border-subtle leading-none"
            >
              +{{ item.ultimate_haste }} R
            </span>
            <span
              v-if="item.basic_haste > 0"
              class="px-1 py-0.5 rounded text-3xs font-mono font-bold bg-[#111215]/90 text-cyan-400 border border-border-subtle leading-none"
            >
              +{{ item.basic_haste }} QWE
            </span>
            <span
              v-if="item.summoner_haste > 0"
              class="px-1 py-0.5 rounded text-3xs font-mono font-bold bg-[#111215]/90 text-accent-summoner border border-border-subtle leading-none"
            >
              +{{ item.summoner_haste }} Summ
            </span>
          </div>
        </template>

        <template v-else>
          <div class="flex flex-col items-center gap-1 text-border-active group-hover:text-text-secondary">
            <Plus class="w-4 h-4" />
            <span class="text-3xs uppercase font-mono tracking-wider">{{ store.t('emptySlot') }} {{ idx + 1 }}</span>
          </div>
        </template>
      </div>
    </div>

    <!-- Item Search Modal -->
    <div
      v-if="isPickerOpen"
      class="fixed inset-0 z-50 bg-black/75 backdrop-blur-xs flex items-center justify-center p-4"
    >
      <div
        class="bg-[#181A1F] border border-[#2A2D35] rounded-lg w-full max-w-xl max-h-[80vh] flex flex-col shadow-2xl"
      >
        <div class="flex items-center justify-between p-4 border-b border-border-default">
          <h2 class="text-base font-bold text-white tracking-wide">
            {{ store.t('itemTitle') }} — {{ store.t('emptySlot') }} {{ (activeSlot ?? 0) + 1 }}
          </h2>
          <button
            @click="closePicker"
            class="p-1 rounded text-text-secondary hover:text-white hover:bg-surface-hover transition-colors"
          >
            <X class="w-5 h-5" />
          </button>
        </div>

        <div class="p-3 border-b border-border-subtle bg-surface-inset">
          <div class="relative">
            <Search class="absolute left-3 top-2.5 w-4 h-4 text-text-secondary" />
            <input
              v-model="searchQuery"
              type="text"
              :placeholder="store.t('itemSearchPlaceholder')"
              class="w-full bg-[#111215] border border-border-default rounded-md pl-9 pr-3 py-2 text-sm text-white placeholder-text-secondary focus:outline-none focus:border-accent-ah"
              autofocus
            />
          </div>
        </div>

        <div class="p-4 overflow-y-auto max-h-[50vh] flex flex-col gap-2">
          <div
            v-for="i in filteredItems"
            :key="i.id"
            @click="selectItem(i)"
            class="flex items-center justify-between p-2.5 rounded-md hover:bg-surface-hover border border-border-subtle hover:border-border-active cursor-pointer transition-colors"
          >
            <div class="flex items-center gap-3 min-w-0">
              <img
                :src="i.image_url"
                :alt="i.name"
                class="w-10 h-10 rounded object-cover border border-border-default shrink-0"
                loading="lazy"
              />
              <div class="flex flex-col min-w-0">
                <span class="text-sm font-semibold text-white truncate">{{ i.name }}</span>
                <span class="text-2xs text-text-secondary truncate">{{ i.gold_total }} {{ store.t('goldCost') }}</span>
              </div>
            </div>

            <div class="shrink-0 flex items-center gap-1.5 flex-wrap justify-end">
              <span
                v-if="i.ability_haste > 0"
                class="px-2 py-0.5 rounded text-xs font-mono font-bold bg-surface-inset border border-border-default text-accent-ah"
              >
                +{{ i.ability_haste }} AH
              </span>
              <span
                v-if="i.ultimate_haste > 0"
                class="px-2 py-0.5 rounded text-xs font-mono font-bold bg-surface-inset border border-border-default text-accent-ult"
              >
                +{{ i.ultimate_haste }} Ult
              </span>
              <span
                v-if="i.basic_haste > 0"
                class="px-2 py-0.5 rounded text-xs font-mono font-bold bg-surface-inset border border-border-default text-cyan-400"
              >
                +{{ i.basic_haste }} QWE
              </span>
              <span
                v-if="i.summoner_haste > 0"
                class="px-2 py-0.5 rounded text-xs font-mono font-bold bg-surface-inset border border-border-default text-accent-summoner"
              >
                +{{ i.summoner_haste }} Summ
              </span>
              <span
                v-if="!i.ability_haste && !i.ultimate_haste && !i.basic_haste && !i.summoner_haste"
                class="text-2xs text-text-secondary"
              >
                0 AH
              </span>
            </div>
          </div>

          <div
            v-if="filteredItems.length === 0"
            class="py-12 text-center text-text-secondary text-sm"
          >
            {{ store.t('noItemsFound') }} "{{ searchQuery }}"
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.text-3xs {
  font-size: 9px;
  line-height: 12px;
}
</style>
