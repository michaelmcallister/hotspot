<template>
  <router-link to="/" class="app-logo-link text-decoration-none" aria-label="Home">
    <div class="app-logo d-flex align-center" :class="{ 'text-grey': grey, 'app-logo--compact': compact }">
      <v-icon class="mr-1" :color="grey ? 'grey' : undefined">mdi-motorbike</v-icon>
      <span>Hotspot</span>
    </div>
  </router-link>
</template>

<script setup lang="ts">
defineProps<{
  grey?: boolean;
  compact?: boolean;
}>();
</script>

<style scoped>
.app-logo-link {
  color: inherit;
}

.app-logo {
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.app-logo:hover {
  opacity: 0.8;
}

@media (max-width: 600px) {
  .app-logo--compact {
    line-height: 1;
  }
  .app-logo--compact .v-icon {
    font-size: 28px;
    margin-right: 0;
  }
  .app-logo--compact span {
    display: none;
  }
}
</style>
