<template>
  <section>
    <p>{{ msg }}</p>
    <button @click="count++">You clicked {{ count }} times</button>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  msg: string
}>()

const count = ref<number>(0)
</script>

<style scoped>
p {
  margin: 0 0 1rem;
  font-size: 1.1rem;
}
button {
  padding: 0.6rem 1rem;
  border: 1px solid currentColor;
  background: transparent;
  cursor: pointer;
  border-radius: 8px;
}
button:hover {
  opacity: 0.85;
}
</style>
