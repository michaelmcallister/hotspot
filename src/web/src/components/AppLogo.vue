<template>
  <router-link to="/" class="app-logo-link">
    <div class="app-logo" :class="{ 'text-grey': grey }">
      <v-icon class="mr-1" :color="grey ? 'grey' : undefined">mdi-motorbike</v-icon>
      <span>Hotspot</span>
    </div>
  </router-link>
</template>

<script setup lang="ts">
defineProps<{
  grey?: boolean;
}>();
</script>

<style scoped>
.app-logo-link {
  text-decoration: none;
  color: inherit;
}

.app-logo {
  display: flex;
  align-items: center;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.app-logo:hover {
  opacity: 0.8;
}
</style>