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
import { ref, watch } from 'vue';

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
const loading = ref(false);
const selected = ref<Suggestion | null>(null);
let debounceId: ReturnType<typeof setTimeout> | undefined;

watch(() => props.modelValue, val => {
  if (val !== search.value) search.value = val || '';
});

const fetchSuggestions = async (q: string) => {
  if (!q || q.trim().length < 2) {
    suggestions.value = [];
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
