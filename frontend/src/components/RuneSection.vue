<!-- File: frontend/src/components/RuneSection.vue -->
<script setup>
import { useCalculatorStore } from '../stores/calculatorStore'
import { Minus, Plus, Check } from 'lucide-vue-next'

const store = useCalculatorStore()

function isSelected(runeId) {
  return store.selectedRunes[runeId] !== undefined
}

function getStacks(runeId) {
  return store.selectedRunes[runeId] || 0
}

function toggleRune(rune) {
  store.toggleRune(rune)
}

function changeStacks(rune, delta, event) {
  event.stopPropagation()
  if (!isSelected(rune.id)) {
    store.toggleRune(rune)
  }
  const current = getStacks(rune.id)
  store.setRuneStacks(rune.id, current + delta)
}
</script>

<template>
  <div class="bg-surface border border-border-default rounded-md p-4 flex flex-col gap-3">
    <div class="flex items-center justify-between">
      <span class="text-xs uppercase tracking-wider text-text-secondary font-semibold">
        Haste Runes & Shards
      </span>
      <span class="text-2xs text-text-secondary">
        {{ store.activeRunesCount }} Selected
      </span>
    </div>

    <div class="flex flex-col gap-2">
      <div
        v-for="rune in store.runes"
        :key="rune.id"
        @click="toggleRune(rune)"
        :class="[
          'p-2.5 rounded-md border transition-all cursor-pointer flex items-center justify-between gap-3',
          isSelected(rune.id)
            ? 'bg-surface-hover border-border-active'
            : 'bg-surface-inset border-border-subtle hover:border-border-default'
        ]"
      >
        <!-- Icon & Name -->
        <div class="flex items-center gap-3 min-w-0">
          <div
            :class="[
              'w-5 h-5 rounded border flex items-center justify-center shrink-0 transition-colors',
              isSelected(rune.id)
                ? 'bg-accent-ah border-accent-ah text-black'
                : 'border-border-default bg-[#111215]'
            ]"
          >
            <Check v-if="isSelected(rune.id)" class="w-3.5 h-3.5 stroke-[3]" />
          </div>

          <div class="flex flex-col min-w-0">
            <span
              :class="[
                'text-sm font-semibold truncate',
                isSelected(rune.id) ? 'text-white' : 'text-text-secondary'
              ]"
            >
              {{ rune.name }}
            </span>
            <span class="text-2xs text-text-secondary">
              <template v-if="rune.haste_type === 'ULTIMATE_HASTE'">
                <span class="text-accent-ult">Ultimate Haste</span>
                • {{ rune.base_haste }} + {{ rune.haste_per_stack }}/stack
              </template>
              <template v-else-if="rune.haste_type === 'SUMMONER_HASTE'">
                <span class="text-accent-summoner">Summoner Haste</span>
                • +{{ rune.base_haste }} SH
              </template>
              <template v-else>
                <span class="text-accent-ah">Ability Haste</span>
                <span v-if="rune.max_stacks > 0">
                  • +{{ rune.haste_per_stack }}/stack (Max {{ rune.max_stacks }})
                </span>
                <span v-else>
                  • +{{ rune.base_haste }} AH
                </span>
              </template>
            </span>
          </div>
        </div>

        <!-- Stacks Control if stackable -->
        <div
          v-if="rune.max_stacks > 0"
          class="flex items-center gap-1.5 shrink-0"
          @click.stop
        >
          <button
            @click="changeStacks(rune, -1, $event)"
            :disabled="!isSelected(rune.id) || getStacks(rune.id) <= 0"
            class="w-7 h-7 rounded bg-[#21242C] border border-border-default hover:border-border-active disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center text-white transition-colors"
          >
            <Minus class="w-3 h-3" />
          </button>

          <span class="tabular-nums text-xs font-mono font-bold w-12 text-center text-white">
            {{ getStacks(rune.id) }} / {{ rune.max_stacks }}
          </span>

          <button
            @click="changeStacks(rune, 1, $event)"
            :disabled="!isSelected(rune.id) || getStacks(rune.id) >= rune.max_stacks"
            class="w-7 h-7 rounded bg-[#21242C] border border-border-default hover:border-border-active disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center text-white transition-colors"
          >
            <Plus class="w-3 h-3" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
