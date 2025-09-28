<template>
  <div class="app-logo" :class="{ 'text-grey': grey }">
    <v-icon class="mr-1" :color="grey ? 'grey' : undefined">mdi-motorbike</v-icon>
    <span>Hotspot</span>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  grey?: boolean;
}>();
</script>

<style scoped>
.app-logo {
  display: flex;
  align-items: center;
  font-weight: 600;
}
</style>