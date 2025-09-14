<template>
  <div class="accuracy-card" aria-labelledby="accuracy-title">
    <p id="accuracy-title" class="feedback-question">
      <strong>Is this score accurate?</strong> Help improve our data:
    </p>

    <div class="d-flex flex-wrap justify-center ga-3">
      <v-btn
        color="success"
        variant="outlined"
        :append-icon="userFeedback === 'safer' ? 'mdi-check' : undefined"
        :class="{ 'font-weight-bold': userFeedback === 'safer' }"
        @click="submitFeedback('safer')"
      >
        👍 Feels Safer
      </v-btn>

      <v-btn
        color="error"
        variant="outlined"
        :append-icon="userFeedback === 'less-safe' ? 'mdi-check' : undefined"
        :class="{ 'font-weight-bold': userFeedback === 'less-safe' }"
        @click="submitFeedback('less-safe')"
      >
        👎 Less Safe
      </v-btn>
    </div>

    <v-alert
      v-if="feedbackSubmitted"
      type="success"
      variant="tonal"
      class="mt-3 text-center"
      density="compact"
    >
      Thank you for your feedback! ✓
    </v-alert>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const props = defineProps<{
  suburb: string
}>();

const userFeedback = ref<null | 'safer' | 'less-safe'>(null);
const feedbackSubmitted = ref(false);

const submitFeedback = (feedbackType: 'safer' | 'less-safe') => {
  userFeedback.value = feedbackType;
  feedbackSubmitted.value = true;

  console.log(`User feedback: ${feedbackType} for ${props.suburb}`);

  setTimeout(() => {
    feedbackSubmitted.value = false;
    userFeedback.value = null;
  }, 3000);
};
</script>

<style scoped>
.accuracy-card { padding: 1.25rem; }
.accuracy-card .feedback-question {
  color: #111827;
  margin-bottom: .9rem;
  font-size: 1rem;
}
</style>
