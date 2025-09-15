<template>
  <v-autocomplete
    :items="suggestions"
    item-title="label"
    return-object
    :loading="loading"
    :search="search"
    @update:search="onSearchUpdate"
    @keyup.enter="emitSearch"
    v-model="selected"
    variant="outlined"
    bg-color="white"
    density="comfortable"
    rounded="lg"
    hide-details
    hide-no-data
    prepend-inner-icon="mdi-magnify"
    placeholder="Enter suburb or postcode (e.g., Toorak, 3142)"
    class="mx-auto mb-8"
    style="max-width: 1200px;"
  />
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';

interface Suggestion {
  label: string;
  suburb: string;
  postcode: string;
  lga: string;
  risk_score: number;
}

const props = defineProps<{
  modelValue: string
}>();

const emit = defineEmits<{
  'update:modelValue': [value: string]
  'search': []
  'select': [suggestion: Suggestion]
}>();

const search = ref(props.modelValue || '');
const suggestions = ref<Suggestion[]>([]);
const defaultSuggestions = ref<Suggestion[]>([]);
const loading = ref(false);
const selected = ref<Suggestion | null>(null);
let debounceId: ReturnType<typeof setTimeout> | undefined;

watch(() => props.modelValue, val => {
  if (val !== search.value) search.value = val || '';
});

const fetchSuggestions = async (q: string) => {
  if (!q || q.trim().length < 2) {
    // When query is empty/short, show default list so the dropdown isn't empty
    suggestions.value = defaultSuggestions.value;
    return;
  }
  loading.value = true;
  try {
    const response = await fetch(`/api/v1/search?q=${encodeURIComponent(q)}`);
    if (response.ok) {
      suggestions.value = await response.json();
    } else {
      suggestions.value = [];
    }
  } catch (e) {
    console.error('Search error:', e);
    suggestions.value = [];
  } finally {
    loading.value = false;
  }
};

// Prefetch a sensible default list so clicking the dropdown shows items
const fetchDefaultSuggestions = async () => {
  try {
    const params = new URLSearchParams({ scope: 'postcode', order: 'desc', limit: '50' });
    const res = await fetch(`/api/v1/risk/top?${params.toString()}`);
    if (!res.ok) throw new Error(`Failed to load defaults (${res.status})`);
    const rows = await res.json();
    const mapped: Suggestion[] = Array.isArray(rows)
      ? rows.map((r: any) => ({
          label: `${r.suburb} ${r.postcode}`.trim(),
          suburb: String(r.suburb ?? ''),
          postcode: String(r.postcode ?? ''),
          lga: String(r.lga ?? ''),
          risk_score: Number(r.risk_score ?? 0),
        }))
      : [];
    defaultSuggestions.value = mapped;
    // If user hasn't typed anything yet we can offer some defaults
    if (!search.value || search.value.trim().length < 2) {
      suggestions.value = defaultSuggestions.value;
    }
  } catch (e) {
    // Keep silent failure for defaults so search still works
    console.error('Default suggestions error:', e);
    defaultSuggestions.value = [];
  }
};

onMounted(() => {
  fetchDefaultSuggestions();
});

const onSearchUpdate = (val: string) => {
  search.value = val;
  emit('update:modelValue', val);
  if (debounceId) clearTimeout(debounceId);
  debounceId = setTimeout(() => fetchSuggestions(val), 300);
};

const emitSearch = () => {
  emit('search');
};

watch(selected, (val) => {
  if (val) {
    // When a suggestion is selected
    emit('update:modelValue', val.label);
    emit('select', val);
    emit('search');
  }
});
</script>
