<template>
  <v-autocomplete
    v-model="selected"
    v-model:search="searchText"
    :items="suggestions"
    :loading="loading"
    item-title="label"
    item-value="label"
    return-object
    clearable
    variant="outlined"
    bg-color="white"
    density="comfortable"
    rounded="lg"
    hide-no-data
    hide-details
    prepend-inner-icon="mdi-magnify"
    placeholder="Enter suburb or postcode (e.g., Toorak, 3142)"
    class="mx-auto mb-8"
    style="max-width: 1200px;"
    @update:model-value="onSelect"
    @update:search="onSearchUpdate"
  />
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { searchService, riskService } from '../services'

interface Suggestion {
  label: string
  suburb: string
  postcode: string
  lga: string
  risk_score: number
}

const props = defineProps<{
  modelValue?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
  'search': []
  'select': [suggestion: Suggestion]
  'clear': []
}>()


const searchText = ref('')
const selected = ref<Suggestion | null>(null)
const searchResults = ref<Suggestion[]>([])
const defaultSuggestions = ref<Suggestion[]>([])
const loading = ref(false)
let searchTimeout: ReturnType<typeof setTimeout> | undefined

const suggestions = computed(() => {
  if (searchText.value && searchText.value.length >= 2) {
    return searchResults.value
  }
  return defaultSuggestions.value
})

onMounted(async () => {
  try {
    const response = await riskService.getTopRisk({
      scope: 'postcode',
      sortOrder: 'desc',
      itemsPerPage: '20'
    })

    const items = response.items || []
    defaultSuggestions.value = items.map((r: any) => ({
      label: `${r.suburb}, ${r.postcode}`,
      suburb: String(r.suburb || ''),
      postcode: String(r.postcode || ''),
      lga: String(r.lga || ''),
      risk_score: Number(r.risk_score || 0)
    }))
  } catch (e) {
    console.warn('Failed to load default suggestions:', e)
    defaultSuggestions.value = []
  }
})

async function onSearchUpdate(value: string) {
  searchText.value = value

  if (searchTimeout) clearTimeout(searchTimeout)

  if (!value || value.length < 2) {
    searchResults.value = []
    return
  }

  searchTimeout = setTimeout(async () => {
    loading.value = true
    try {
      searchResults.value = await searchService.search(value)
    } catch (e) {
      console.error('Search failed:', e)
      searchResults.value = []
    } finally {
      loading.value = false
    }
  }, 300)
}

function onSelect(value: Suggestion | null) {
  selected.value = value

  if (value) {
    emit('update:modelValue', value.label)
    emit('select', value)
    emit('search')
  } else {
    emit('update:modelValue', '')
    emit('clear')
  }
}

function updateSelection(suburb: Suggestion | null) {
  selected.value = suburb
  if (suburb) {
    searchText.value = suburb.label
  }
}

defineExpose({ updateSelection })
</script>
