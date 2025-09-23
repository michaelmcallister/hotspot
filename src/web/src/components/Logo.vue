<template>
  <div class="logo">
    <v-icon class="mr-1" :size="size" :class="iconClass">mdi-motorbike</v-icon>
    <span :class="textClass">Hotspot</span>
  </div>
</template>

<script setup lang="ts">
interface Props {
  size?: string | number
  textClass?: string
  iconClass?: string
}

const props = withDefaults(defineProps<Props>(), {
  size: 'default',
  textClass: '',
  iconClass: ''
})
</script>

<style scoped>
.logo {
  display: inline-flex;
  align-items: center;
}
</style>