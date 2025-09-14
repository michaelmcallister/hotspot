<template>
  <div
    v-if="show"
    class="modal-overlay"
    @click="$emit('close')"
    aria-modal="true"
    role="dialog"
    aria-labelledby="resources-modal-title"
  >
    <div class="modal-content" @click.stop>
      <button class="modal-close" @click="$emit('close')" aria-label="Close resources">×</button>

      <h1 id="resources-modal-title">Safety Resources</h1>

      <div class="resources-section">
        <h2>Emergency Contacts</h2>

        <div class="contact-card">
          <div class="contact-info">
            <h3>Police Emergency</h3>
            <p>For immediate emergencies</p>
          </div>
          <div class="contact-number">000</div>
        </div>

        <div class="contact-card">
          <div class="contact-info">
            <h3>Crime Stoppers</h3>
            <p>Report crimes anonymously</p>
          </div>
          <div class="contact-number">1800 333 000</div>
        </div>

        <div class="contact-card">
          <div class="contact-info">
            <h3>Victoria Police Non-Emergency</h3>
            <p>Non-urgent police matters</p>
          </div>
          <div class="contact-number">03 9247 6666</div>
        </div>
      </div>

      <div class="divider"></div>

      <div class="resources-section">
        <h2>Helpful Resources</h2>
        <div class="resource-links">
          <a href="#" @click.prevent class="resource-link">
            <span class="link-title">Melbourne Bike Theft Prevention Guide</span>
            <span class="link-desc">Learn how to protect your motorbike from theft</span>
          </a>
          <a href="#" @click.prevent class="resource-link">
            <span class="link-title">VicRoads Motorcycle Security Tips</span>
            <span class="link-desc">Official government advice on motorcycle security</span>
          </a>
          <a href="#" @click.prevent class="resource-link">
            <span class="link-title">Recent Theft Reports — {{ suburb }}</span>
            <span class="link-desc">Latest reports in your area</span>
          </a>
          <a href="#" @click.prevent class="resource-link">
            <span class="link-title">Insurance Claims for Stolen Bikes</span>
            <span class="link-desc">What to do if your motorcycle is stolen</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  show: boolean
  suburb: string
}>();

defineEmits<{
  close: []
}>();
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}
.modal-content {
  background: #fff;
  padding: 2.2rem;
  border-radius: 12px;
  max-width: 560px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 20px 25px -5px rgba(0,0,0,.15);
  text-align: left;
}
.modal-close {
  position: absolute;
  top: .75rem;
  right: .75rem;
  background: none;
  border: none;
  font-size: 1.6rem;
  cursor: pointer;
  color: #6b7280;
  padding: .25rem .5rem;
}
.modal-content h1 {
  color: #111827;
  font-size: 1.8rem;
  margin-bottom: 1.2rem;
  text-align: center;
}
.modal-content h2 {
  color: #374151;
  font-size: 1.2rem;
  margin: 1.2rem 0 .75rem;
  padding-bottom: .5rem;
  border-bottom: 2px solid #e5e7eb;
}

.contact-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
  margin-bottom: .75rem;
  border-left: 4px solid #ef4444;
}
.contact-info { flex: 1; }
.contact-info h3 {
  color: #111827;
  font-size: 1rem;
  margin: 0 0 .25rem;
  font-weight: 700;
}
.contact-info p { color:#6b7280; font-size:.9rem; margin:0; }
.contact-number {
  background: #ef4444; color:#fff; padding:.5rem 1rem; border-radius: 20px;
  font-weight: 700; font-size: .95rem; min-width: 80px; text-align: center;
}

.resource-links { display: flex; flex-direction: column; gap: .75rem; }
.resource-link {
  display: block; padding: 1rem; background:#f8fafc; border-radius: 8px;
  text-decoration: none; color: inherit; transition: background-color .2s;
  border-left: 4px solid #3b82f6;
}
.resource-link:hover { background:#eef2ff; }
.link-title { display:block; color:#111827; font-weight:700; font-size:.98rem; margin-bottom:.25rem; }
.link-desc { display:block; color:#6b7280; font-size:.9rem; }

.divider { height: 1px; background:#e5e7eb; margin: 1.25rem 0; }
</style>