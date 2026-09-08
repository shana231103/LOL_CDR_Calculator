<!-- File: frontend/src/components/CooldownSummary.vue -->
<script setup>
import { computed } from 'vue'
import { useCalculatorStore } from '../stores/calculatorStore'
import { Zap, Flame, ShieldAlert } from 'lucide-vue-next'

const store = useCalculatorStore()

const res = computed(() => store.calculationResult)

const abilityOrder = ['Q', 'W', 'E', 'R']

const orderedAbilities = computed(() => {
  if (!res.value || !res.value.abilities) return []
  return abilityOrder
    .map((slot) => res.value.abilities[slot])
    .filter(Boolean)
})
</script>

<template>
  <div class="flex flex-col gap-3 sticky top-4">
    <!-- Haste Metric Cards -->
    <div class="grid grid-cols-3 gap-2.5">
      <!-- General AH -->
      <div class="bg-surface border border-border-default rounded-md p-3 flex flex-col gap-1">
        <div class="flex items-center gap-1.5 text-accent-ah">
          <Zap class="w-3.5 h-3.5" />
          <span class="text-2xs uppercase tracking-wider font-semibold">Ability Haste</span>
        </div>
        <span class="tabular-nums text-xl font-bold font-mono text-white">
          {{ res ? res.ability_haste : 0 }}
        </span>
      </div>

      <!-- Ultimate Haste -->
      <div class="bg-surface border border-border-default rounded-md p-3 flex flex-col gap-1">
        <div class="flex items-center gap-1.5 text-accent-ult">
          <Flame class="w-3.5 h-3.5" />
          <span class="text-2xs uppercase tracking-wider font-semibold">Ult Haste</span>
        </div>
        <span class="tabular-nums text-xl font-bold font-mono text-white">
          {{ res ? res.ultimate_haste : 0 }}
        </span>
      </div>

      <!-- Summoner Haste -->
      <div class="bg-surface border border-border-default rounded-md p-3 flex flex-col gap-1">
        <div class="flex items-center gap-1.5 text-accent-summoner">
          <ShieldAlert class="w-3.5 h-3.5" />
          <span class="text-2xs uppercase tracking-wider font-semibold">Summ. Haste</span>
        </div>
        <span class="tabular-nums text-xl font-bold font-mono text-white">
          {{ res ? res.summoner_haste : 0 }}
        </span>
      </div>
    </div>

    <!-- Cooldown Telemetry Table -->
    <div class="bg-surface border border-border-default rounded-md p-4 flex flex-col gap-3">
      <div class="flex items-center justify-between">
        <span class="text-xs uppercase tracking-wider text-text-secondary font-semibold">
          Cooldown Telemetry
        </span>
        <span
          v-if="store.isCalculating"
          class="text-2xs font-mono text-accent-ah animate-pulse"
        >
          Calculating...
        </span>
        <span v-else class="text-2xs font-mono text-text-secondary">
          Live Authoritative
        </span>
      </div>

      <div v-if="orderedAbilities.length > 0" class="flex flex-col gap-2.5">
        <div
          v-for="ab in orderedAbilities"
          :key="ab.slot"
          class="bg-surface-inset border border-border-subtle rounded-md p-3 flex flex-col gap-2"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span
                class="w-6 h-6 rounded bg-[#111215] border border-border-active flex items-center justify-center text-xs font-bold font-mono text-white"
              >
                {{ ab.slot }}
              </span>
              <div class="flex flex-col">
                <span class="text-xs font-semibold text-white">{{ ab.name }}</span>
                <span class="text-3xs text-text-secondary font-mono">Rank {{ ab.rank }}/{{ ab.max_rank }}</span>
              </div>
            </div>

            <!-- Stats Column -->
            <div class="flex items-baseline gap-2.5">
              <div class="flex flex-col items-end">
                <span class="text-2xs text-text-secondary font-mono">
                  Base: {{ ab.base_cooldown }}s
                </span>
                <span
                  class="text-3xs font-mono"
                  :class="ab.slot === 'R' && res?.ultimate_haste > 0 ? 'text-accent-ult font-bold' : 'text-accent-ah'"
                >
                  +{{ ab.applicable_haste }} Haste
                </span>
              </div>

              <!-- Final Cooldown Display (Primary Highlight) -->
              <div class="flex flex-col items-end min-w-[70px]">
                <span class="tabular-nums text-lg font-bold font-mono text-white">
                  {{ ab.final_cooldown }}s
                </span>
                <span class="text-3xs font-mono text-accent-success font-semibold">
                  -{{ ab.reduction_percentage }}%
                </span>
              </div>
            </div>
          </div>

          <!-- Gauge Progress Bar -->
          <div class="w-full h-1 bg-[#21242C] rounded-full overflow-hidden">
            <div
              class="h-full bg-accent-ah transition-all duration-300"
              :class="ab.slot === 'R' ? 'bg-accent-ult' : 'bg-accent-ah'"
              :style="{ width: `${Math.min(100, Math.max(0, ab.reduction_percentage))}%` }"
            ></div>
          </div>
        </div>
      </div>

      <div v-else class="py-12 text-center text-text-secondary text-xs">
        No active champion telemetry
      </div>
    </div>

    <!-- Summoner Spells Cooldowns -->
    <div
      v-if="res && res.summoner_spells && res.summoner_spells.length > 0"
      class="bg-surface border border-border-default rounded-md p-4 flex flex-col gap-2.5"
    >
      <span class="text-xs uppercase tracking-wider text-text-secondary font-semibold">
        Summoner Spells Telemetry
      </span>

      <div class="grid grid-cols-2 gap-2">
        <div
          v-for="s in res.summoner_spells"
          :key="s.id"
          class="bg-surface-inset border border-border-subtle rounded-md p-2.5 flex flex-col gap-1"
        >
          <div class="flex items-center justify-between">
            <span class="text-xs font-semibold text-white truncate">{{ s.name }}</span>
            <span class="text-3xs font-mono text-accent-success font-semibold">
              -{{ s.reduction_percentage }}%
            </span>
          </div>

          <div class="flex items-baseline justify-between mt-1">
            <span class="text-2xs text-text-secondary font-mono">{{ s.base_cooldown }}s</span>
            <span class="tabular-nums text-base font-bold font-mono text-white">
              {{ s.final_cooldown }}s
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
