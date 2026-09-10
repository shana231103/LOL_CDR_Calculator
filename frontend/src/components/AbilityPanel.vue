<!-- File: frontend/src/components/AbilityPanel.vue -->
<script setup>
import { computed } from 'vue'
import { useCalculatorStore } from '../stores/calculatorStore'
import { Minus, Plus } from 'lucide-vue-next'

const store = useCalculatorStore()

const abilities = computed(() => {
  if (!store.selectedChampion || !store.selectedChampion.abilities) {
    return []
  }
  const order = ['Q', 'W', 'E', 'R']
  return [...store.selectedChampion.abilities].sort(
    (a, b) => order.indexOf(a.slot) - order.indexOf(b.slot)
  )
})

function decreaseRank(slot) {
  const current = store.skillRanks[slot] || 1
  if (current > 1) {
    store.setSkillRank(slot, current - 1)
  }
}

function increaseRank(slot, maxRank) {
  const current = store.skillRanks[slot] || 1
  if (current < maxRank) {
    store.setSkillRank(slot, current + 1)
  }
}

function getBaseCooldown(ability, rank) {
  if (!ability.cooldowns || ability.cooldowns.length === 0) return '0.0s'
  const idx = rank - 1
  const val = ability.cooldowns[idx] !== undefined ? ability.cooldowns[idx] : ability.cooldowns[0]
  return `${val.toFixed(1)}s`
}
</script>

<template>
  <div class="bg-surface border border-border-default rounded-md p-4 flex flex-col gap-3">
    <div class="flex items-center justify-between">
      <span class="text-xs uppercase tracking-wider text-text-secondary font-semibold">
        {{ store.t('abilityTitle') }}
      </span>
      <span class="text-2xs text-text-secondary">{{ store.t('qwerStepper') }}</span>
    </div>

    <div v-if="abilities.length > 0" class="flex flex-col gap-2.5">
      <div
        v-for="ab in abilities"
        :key="ab.id"
        class="bg-surface-inset border border-border-subtle rounded-md p-3 flex items-center justify-between gap-3"
      >
        <!-- Icon & Info -->
        <div class="flex items-center gap-3 min-w-0">
          <div class="relative shrink-0">
            <img
              :src="ab.image_url"
              :alt="ab.name"
              class="w-11 h-11 rounded object-cover border border-border-default"
            />
            <span
              class="absolute -top-1.5 -left-1.5 px-1.5 py-0.5 rounded text-2xs font-bold font-mono uppercase bg-[#111215] border border-border-active text-white"
            >
              {{ ab.slot }}
            </span>
          </div>

          <div class="flex flex-col min-w-0">
            <span class="text-sm font-semibold text-white truncate">
              {{ ab.name }}
            </span>
            <span class="text-2xs text-text-secondary font-mono">
              {{ store.t('base') }}: {{ getBaseCooldown(ab, store.skillRanks[ab.slot] || 1) }}
            </span>
          </div>
        </div>

        <!-- Rank Stepper -->
        <div class="flex items-center gap-2 shrink-0">
          <button
            @click="decreaseRank(ab.slot)"
            :disabled="(store.skillRanks[ab.slot] || 1) <= 1"
            class="w-8 h-8 rounded bg-[#21242C] border border-border-default hover:border-border-active disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center text-white transition-colors"
          >
            <Minus class="w-3.5 h-3.5" />
          </button>

          <span class="tabular-nums text-sm font-semibold font-mono w-10 text-center text-white">
            {{ store.skillRanks[ab.slot] || 1 }} / {{ ab.max_rank }}
          </span>

          <button
            @click="increaseRank(ab.slot, ab.max_rank)"
            :disabled="(store.skillRanks[ab.slot] || 1) >= ab.max_rank"
            class="w-8 h-8 rounded bg-[#21242C] border border-border-default hover:border-border-active disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center text-white transition-colors"
          >
            <Plus class="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>

    <div v-else class="py-8 text-center text-text-secondary text-xs">
      {{ store.t('selectChampionAbilities') }}
    </div>
  </div>
</template>
