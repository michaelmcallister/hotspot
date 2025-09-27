<template>
  <v-dialog :model-value="show" max-width="500" persistent>
    <v-card>
      <v-card-text class="text-center pa-6">
        <v-icon
          :color="type === 'success' ? 'success' : 'error'"
          size="80"
          class="mb-4"
        >
          {{ type === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle' }}
        </v-icon>
        <h3 class="text-h5 mb-2">{{ title }}</h3>
        <p class="text-body-1 mb-0">{{ message }}</p>
      </v-card-text>
      <v-card-actions class="justify-center pb-4">
        <v-btn
          color="primary"
          variant="flat"
          rounded="lg"
          @click="$emit('close')"
        >
          {{ buttonText }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
  defineProps<{
    show: boolean;
    type: 'success' | 'error';
    title: string;
    message: string;
    buttonText?: string;
  }>();

  defineEmits<{
    close: [];
  }>();
</script>
