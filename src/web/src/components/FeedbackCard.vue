<template>
  <section class="card accuracy-card" aria-labelledby="accuracy-title">
    <p id="accuracy-title" class="feedback-question">
      <strong>Is this score accurate?</strong> Help improve our data:
    </p>

    <div class="feedback-buttons">
      <button
        type="button"
        @click="submitFeedback('safer')"
        :class="['feedback-btn','feels-safer', { active: userFeedback === 'safer' }]"
        :aria-pressed="userFeedback === 'safer' ? 'true' : 'false'"
      >
        👍 Feels Safer
      </button>

      <button
        type="button"
        @click="submitFeedback('less-safe')"
        :class="['feedback-btn','feels-less-safe', { active: userFeedback === 'less-safe' }]"
        :aria-pressed="userFeedback === 'less-safe' ? 'true' : 'false'"
      >
        👎 Less Safe
      </button>
    </div>

    <p v-if="feedbackSubmitted" class="feedback-thankyou" aria-live="polite">
      Thank you for your feedback! ✓
    </p>
  </section>
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
.card {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 25px -10px rgba(2, 8, 23, 0.15);
  padding: 1.6rem;
  margin: 1.25rem auto 0;
  max-width: 720px;
}

.accuracy-card { padding: 1.25rem; }
.accuracy-card .feedback-question {
  color: #111827;
  margin-bottom: .9rem;
  font-size: 1rem;
}
.feedback-buttons {
  display: flex;
  gap: .75rem;
  justify-content: center;
  flex-wrap: wrap;
}
.feedback-btn {
  min-width: 190px;
  padding: .65rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  background: #fff;
  cursor: pointer;
  transition: all .2s;
  font-weight: 700;
  color: #111827;
}
.feedback-btn:hover { transform: translateY(-1px); }
.feedback-btn.active { border-color: #111827; }

.feels-safer.active { border-color:#10b981; background:#ecfdf5; color:#047857; }
.feels-less-safe.active { border-color:#ef4444; background:#fef2f2; color:#dc2626; }

.feedback-thankyou {
  margin-top: .6rem; color: #10b981; font-weight: 700; font-size: .95rem;
}
</style>