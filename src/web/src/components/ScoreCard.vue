<template>
  <section class="card score-card" aria-labelledby="score-title">
    <div id="score-title" class="suburb-name">{{ suburb }}</div>
    <div class="safety-score">{{ score }}</div>
    <div class="score-label">Safety Score</div>

    <div class="risk-chip" :class="riskClass">{{ riskLabel }}</div>

    <p class="description">
      Premium suburb with top-tier security and surveillance. Minimal theft risk.
    </p>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  suburb: string
  score: number
}>();

const riskLabel = computed(() => {
  if (props.score >= 80) return 'Low Risk';
  if (props.score >= 50) return 'Medium Risk';
  return 'High Risk';
});

const riskClass = computed(() => {
  if (props.score >= 80) return 'low';
  if (props.score >= 50) return 'med';
  return 'high';
});
</script>

<style scoped>
.card {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 25px -10px rgba(2, 8, 23, 0.15);
  padding: 1.6rem;
  margin: 1.25rem auto 0;
  max-width: 100%;
}

.score-card .suburb-name {
  color: #111827;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: .25rem;
}
.safety-score {
  color: #059669;
  font-size: 3.25rem;
  font-weight: 800;
  margin: .25rem 0 0;
}
.score-label {
  color: #6b7280;
  margin-bottom: .6rem;
}
.risk-chip {
  display: inline-block;
  padding: .35rem .7rem;
  border-radius: 999px;
  font-size: .85rem;
  font-weight: 700;
  margin: .25rem 0 .9rem;
  border: 1px solid transparent;
}
.risk-chip.low { background:#ecfdf5; color:#047857; border-color:#a7f3d0; }
.risk-chip.med { background:#fff7ed; color:#9a3412; border-color:#fed7aa; }
.risk-chip.high { background:#fef2f2; color:#dc2626; border-color:#fecaca; }

.description {
  color: #4b5563;
  line-height: 1.6;
  margin: 0 auto;
  max-width: 560px;
  background: #f9fafb;
  border-radius: 10px;
  padding: 1rem 1.25rem;
  border-left: 4px solid #10b981;
}
</style>
