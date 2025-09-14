<template>
  <div class="search-container">
    <svg
      class="search-icon"
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      aria-hidden="true"
    >
      <circle cx="11" cy="11" r="8"></circle>
      <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
    </svg>
    <input
      :value="modelValue"
      @input="handleInput"
      @keyup.enter="handleSelect"
      @keydown.down="moveSelection(1)"
      @keydown.up="moveSelection(-1)"
      @keydown.escape="clearSuggestions"
      @focus="handleFocus"
      @blur="handleBlur"
      class="search-input"
      type="text"
      placeholder="Enter suburb or postcode (e.g., Toorak, 3142)"
      aria-label="Search suburb"
      aria-autocomplete="list"
      :aria-expanded="showSuggestions"
      aria-controls="search-suggestions"
    />
    <ul
      v-if="showSuggestions && suggestions.length > 0"
      id="search-suggestions"
      class="suggestions-list"
      role="listbox"
    >
      <li
        v-for="(suggestion, index) in suggestions"
        :key="index"
        @mousedown="selectSuggestion(suggestion)"
        :class="{ selected: index === selectedIndex }"
        class="suggestion-item"
        role="option"
        :aria-selected="index === selectedIndex"
      >
        {{ suggestion.label }}
      </li>
    </ul>
  </div>
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

const suggestions = ref<Suggestion[]>([]);
const showSuggestions = ref(false);
const selectedIndex = ref(-1);
const searchTimeout = ref<NodeJS.Timeout>();

const handleInput = async (event: Event) => {
  const value = (event.target as HTMLInputElement).value;
  emit('update:modelValue', value);

  clearTimeout(searchTimeout.value);

  if (value.trim().length < 2) {
    clearSuggestions();
    return;
  }

  searchTimeout.value = setTimeout(async () => {
    try {
      const response = await fetch(`/api/v1/search?q=${encodeURIComponent(value)}`);
      if (response.ok) {
        suggestions.value = await response.json();
        showSuggestions.value = suggestions.value.length > 0;
        selectedIndex.value = -1;
      }
    } catch (error) {
      console.error('Search error:', error);
      clearSuggestions();
    }
  }, 300);
};

const handleFocus = () => {
  if (suggestions.value.length > 0) {
    showSuggestions.value = true;
  }
};

const handleBlur = () => {
  setTimeout(() => {
    showSuggestions.value = false;
  }, 200);
};

const selectSuggestion = (suggestion: Suggestion) => {
  emit('update:modelValue', suggestion.label);
  emit('select', suggestion);
  clearSuggestions();
  emit('search');
};

const handleSelect = () => {
  if (selectedIndex.value >= 0 && selectedIndex.value < suggestions.value.length) {
    selectSuggestion(suggestions.value[selectedIndex.value]);
  } else {
    emit('search');
  }
};

const moveSelection = (direction: number) => {
  if (!showSuggestions.value || suggestions.value.length === 0) return;

  selectedIndex.value = selectedIndex.value + direction;

  if (selectedIndex.value < 0) {
    selectedIndex.value = suggestions.value.length - 1;
  } else if (selectedIndex.value >= suggestions.value.length) {
    selectedIndex.value = 0;
  }
};

const clearSuggestions = () => {
  suggestions.value = [];
  showSuggestions.value = false;
  selectedIndex.value = -1;
};

watch(() => props.modelValue, (newValue) => {
  if (!newValue) {
    clearSuggestions();
  }
});
</script>

<style scoped>
.search-container {
  position: relative;
  margin: 0 auto 2rem;
  max-width: 720px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.search-input {
  width: 80%;
  padding: 1rem 1rem 1rem 3rem;
  border: 2px solid #e5e7eb;
  border-radius: 14px;
  font-size: 1.05rem;
  background: #ffffff;
  transition: border-color .2s, box-shadow .2s;
}
.search-input:focus {
  outline: none;
  border-color: #0b1541;
  box-shadow: 0 0 0 4px rgba(37,99,235,.12);
}
.search-icon {
  position: absolute;
  left: 10%;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  z-index: 2;
  margin-left: 1rem;
}
.suggestions-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 0.25rem;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 10px 25px -10px rgba(2, 8, 23, 0.15);
  list-style: none;
  padding: 0.5rem 0;
  max-height: 300px;
  overflow-y: auto;
  z-index: 1000;
  width: 80%;
  margin-left: auto;
  margin-right: auto;
  left: 50%;
  transform: translateX(-50%);
}
.suggestion-item {
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: background-color 0.15s;
  color: #111827;
  font-size: 0.95rem;
}
.suggestion-item:hover,
.suggestion-item.selected {
  background-color: #f3f4f6;
}
.suggestion-item.selected {
  background-color: #e5e7eb;
}
</style>