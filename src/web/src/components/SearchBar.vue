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
      @input="$emit('update:modelValue', $event.target.value)"
      @keyup.enter="$emit('search')"
      class="search-input"
      type="text"
      placeholder="Enter suburb (e.g., Toorak)"
      aria-label="Search suburb"
    />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: string
}>();

defineEmits<{
  'update:modelValue': [value: string]
  'search': []
}>();
</script>

<style scoped>
.search-container {
  position: relative;
  margin: 0 auto 2rem;
  max-width: 720px;
}
.search-input {
  width: 80%;
  padding: 1rem 1rem 1rem 3rem;
  border: 2px solid #e5e7eb;
  border-radius: 14px;
  font-size: 1.05rem;
  background: #67686b;
  transition: border-color .2s, box-shadow .2s;
}
.search-input:focus {
  outline: none;
  border-color: #0b1541;
  box-shadow: 0 0 0 4px rgba(37,99,235,.12);
}
.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
}
</style>