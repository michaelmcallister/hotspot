<template>
  <v-dialog :model-value="show" @update:model-value="onUpdate" :max-width="maxWidth">
    <v-card>
      <v-card-title class="text-h6 d-flex align-center justify-space-between">
        <span :id="titleId">{{ title }}</span>
        <v-btn icon="mdi-close" variant="text" @click="$emit('close')" :aria-label="closeAriaLabel" />
      </v-card-title>
      <v-card-text>
        <slot />
      </v-card-text>
      <v-card-actions v-if="$slots.actions" class="justify-end">
        <slot name="actions" />
      </v-card-actions>
      <v-card-actions v-else class="justify-end">
        <v-btn color="primary" @click="$emit('close')">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
const props = defineProps<{
  show: boolean
  title: string
  maxWidth?: string | number
  titleId?: string
  closeAriaLabel?: string
}>();

const emit = defineEmits<{
  close: []
}>();

const onUpdate = (val: boolean) => {
  if (!val) emit('close');
};
</script>