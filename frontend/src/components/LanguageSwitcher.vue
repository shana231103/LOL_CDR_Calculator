<!-- File: frontend/src/components/LanguageSwitcher.vue -->
<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useCalculatorStore } from '../stores/calculatorStore'
import { Globe, Check, ChevronDown } from 'lucide-vue-next'

const store = useCalculatorStore()
const isOpen = ref(false)
const dropdownRef = ref(null)

const languages = [
  { code: 'vi_VN', label: 'Tiếng Việt', flag: '🇻🇳' },
  { code: 'en_US', label: 'English', flag: '🇬🇧' },
]

function toggleDropdown() {
  isOpen.value = !isOpen.value
}

async function selectLocale(code) {
  if (store.currentLocale !== code) {
    await store.setLocale(code)
  }
  isOpen.value = false
}

function handleClickOutside(event) {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<template>
  <div class="relative" ref="dropdownRef">
    <!-- Trigger Button -->
    <button
      @click="toggleDropdown"
      class="px-2.5 py-1 rounded bg-[#21242C] border border-border-default hover:border-border-active text-xs font-medium text-text-primary hover:text-white flex items-center gap-2 transition-all shadow-sm focus:outline-none"
      :title="store.currentLocale === 'vi_VN' ? 'Đổi ngôn ngữ' : 'Change language'"
    >
      <Globe class="w-3.5 h-3.5 text-accent-ah" />
      <span class="flex items-center gap-1 font-mono">
        <span>{{ store.currentLocale === 'vi_VN' ? '🇻🇳' : '🇬🇧' }}</span>
        <span>{{ store.currentLocale === 'vi_VN' ? 'Tiếng Việt' : 'English' }}</span>
      </span>
      <ChevronDown class="w-3 h-3 text-text-secondary transition-transform duration-200" :class="{ 'rotate-180': isOpen }" />
    </button>

    <!-- Dropdown Menu -->
    <div
      v-if="isOpen"
      class="absolute right-0 mt-1.5 w-36 py-1 bg-[#1A1D24] border border-border-default rounded-md shadow-xl z-50 overflow-hidden backdrop-blur-md animate-in fade-in zoom-in-95 duration-100"
    >
      <button
        v-for="lang in languages"
        :key="lang.code"
        @click="selectLocale(lang.code)"
        class="w-full px-3 py-1.5 text-xs flex items-center justify-between hover:bg-[#262A34] transition-colors"
        :class="store.currentLocale === lang.code ? 'text-accent-ah font-bold bg-[#21252E]' : 'text-text-primary'"
      >
        <div class="flex items-center gap-2">
          <span>{{ lang.flag }}</span>
          <span>{{ lang.label }}</span>
        </div>
        <Check v-if="store.currentLocale === lang.code" class="w-3 h-3 text-accent-ah" />
      </button>
    </div>
  </div>
</template>
