<!-- File: frontend/src/components/SummonerSpellSelector.vue -->
<script setup>
import { ref } from 'vue'
import { useCalculatorStore } from '../stores/calculatorStore'
import { Plus, X } from 'lucide-vue-next'

const store = useCalculatorStore()
const activeSlot = ref(null)
const isModalOpen = ref(false)

function openModal(slotIndex) {
  activeSlot.value = slotIndex
  isModalOpen.value = true
}

function selectSpell(spell) {
  if (activeSlot.value !== null) {
    store.setSpell(activeSlot.value, spell)
  }
  closeModal()
}

function removeSpell(slotIndex, event) {
  event.stopPropagation()
  store.removeSpell(slotIndex)
}

function closeModal() {
  isModalOpen.value = false
  activeSlot.value = null
}
</script>

<template>
  <div class="bg-surface border border-border-default rounded-md p-4 flex flex-col gap-3">
    <div class="flex items-center justify-between">
      <span class="text-xs uppercase tracking-wider text-text-secondary font-semibold">
        {{ store.t('spellTitle') }}
      </span>
      <span class="text-2xs text-text-secondary">{{ store.t('twoSlots') }}</span>
    </div>

    <!-- 2 Spell Slots -->
    <div class="grid grid-cols-2 gap-3">
      <div
        v-for="(spell, idx) in store.selectedSpells"
        :key="idx"
        @click="openModal(idx)"
        class="h-16 rounded-md bg-surface-inset border border-border-default hover:border-border-active transition-all cursor-pointer relative group flex items-center p-2.5 gap-3"
      >
        <template v-if="spell">
          <div class="relative shrink-0">
            <img
              :src="spell.image_url"
              :alt="spell.name"
              class="w-11 h-11 rounded object-cover border border-border-default"
            />
            <span
              class="absolute -top-1.5 -left-1.5 px-1.5 py-0.5 rounded text-3xs font-bold font-mono uppercase bg-[#111215] border border-border-active text-white"
            >
              {{ idx === 0 ? 'D' : 'F' }}
            </span>
          </div>

          <div class="flex flex-col min-w-0">
            <span class="text-sm font-semibold text-white truncate">{{ spell.name }}</span>
            <span class="text-2xs text-text-secondary font-mono">{{ spell.cooldown }}s {{ store.t('base') }}</span>
          </div>

          <button
            @click="removeSpell(idx, $event)"
            class="absolute top-1.5 right-1.5 w-5 h-5 rounded bg-black/80 text-text-secondary hover:text-white flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <X class="w-3.5 h-3.5" />
          </button>
        </template>

        <template v-else>
          <div class="w-full flex items-center justify-center gap-2 text-border-active group-hover:text-text-secondary">
            <Plus class="w-4 h-4" />
            <span class="text-xs uppercase font-mono tracking-wider">{{ store.t('spellTitle') }} {{ idx === 0 ? 'D' : 'F' }}</span>
          </div>
        </template>
      </div>
    </div>

    <!-- Spell Selection Modal -->
    <div
      v-if="isModalOpen"
      class="fixed inset-0 z-50 bg-black/75 backdrop-blur-xs flex items-center justify-center p-4"
    >
      <div
        class="bg-[#181A1F] border border-[#2A2D35] rounded-lg w-full max-w-md max-h-[80vh] flex flex-col shadow-2xl"
      >
        <div class="flex items-center justify-between p-4 border-b border-border-default">
          <h2 class="text-base font-bold text-white tracking-wide">
            {{ store.t('selectSummonerSpell') }} (Slot {{ activeSlot === 0 ? 'D' : 'F' }})
          </h2>
          <button
            @click="closeModal"
            class="p-1 rounded text-text-secondary hover:text-white hover:bg-surface-hover transition-colors"
          >
            <X class="w-5 h-5" />
          </button>
        </div>

        <div class="p-4 overflow-y-auto max-h-[50vh] flex flex-col gap-2">
          <div
            v-for="s in store.spells"
            :key="s.id"
            @click="selectSpell(s)"
            class="flex items-center justify-between p-2.5 rounded-md hover:bg-surface-hover border border-border-subtle hover:border-border-active cursor-pointer transition-colors"
          >
            <div class="flex items-center gap-3 min-w-0">
              <img
                :src="s.image_url"
                :alt="s.name"
                class="w-10 h-10 rounded object-cover border border-border-default shrink-0"
              />
              <div class="flex flex-col min-w-0">
                <span class="text-sm font-semibold text-white truncate">{{ s.name }}</span>
                <span class="text-2xs text-text-secondary truncate">{{ s.description }}</span>
              </div>
            </div>

            <span class="text-xs font-mono font-bold text-text-secondary shrink-0">
              {{ s.cooldown }}s
            </span>
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
