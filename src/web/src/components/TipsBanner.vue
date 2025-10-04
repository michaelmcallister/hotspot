<template>
  <v-alert 
    v-if="currentTip" 
    :text="currentTip.text" 
    color="primary"
    variant="tonal"
    class="mb-4 text-center"
    border="start"
    icon="mdi-lightbulb-on-outline"
  />
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

const tips = ref([
  "🔒 The more locks the merrier - make your bike look like effort.",
  "📍 Always lock to something that won't move.",
  "⚡ Use your ignition and steering locks - even for quick stops.",
  "🎯 A simple bike cover hides temptation.",
  "🚨 An anti-theft alarm can scare off thieves fast.",
  "🪖 Don't leave your helmet or gear unsecured - it attracts attention.",
  "💡 Well-lit spots = low-risk spots. Are you in the spotlight?",
  "📡 GPS trackers won't prevent theft, but they'll help get your bike back.",
  "👥 Thieves avoid groups. Park near fellow riders.",
  "🤝 Share safe parking spots with other riders - community helps.",
  "⏱️ How long would it take you to steal your own bike?",
  "🤔 Would you park there if it was a friend's bike?",
  "🔍 When did you last check your alarm or lock for faults?",
  "👀 If someone touched your bike right now, would anyone notice?",
  "🎯 Don't park by chance - park with purpose."
]);

const currentTipIndex = ref(0);
const currentTip = ref({ text: tips.value[0] });
let rotationInterval: number | null = null;

const nextTip = () => {
  currentTipIndex.value = (currentTipIndex.value + 1) % tips.value.length;
  currentTip.value = { text: tips.value[currentTipIndex.value] };
};

onMounted(() => {
  rotationInterval = window.setInterval(() => {
    nextTip();
  }, 10000);
});

onUnmounted(() => {
  if (rotationInterval) {
    clearInterval(rotationInterval);
  }
});
</script>