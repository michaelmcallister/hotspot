<template>
  <v-container class="pt-1 pt-md-3 pb-20 pb-md-24" style="padding-bottom: 200px;">
    <PageHero
      title="Privacy Policy"
      subtitle="How we collect, use and protect information in Hotspot"
      icon="mdi-shield-account"
    />

    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <v-card elevation="1" rounded="lg">
          <v-card-text class="pa-6">
            <p class="text-caption text-medium-emphasis mb-4">Last updated: 03/10/2025</p>

            <p class="mb-4">
              Your privacy is important to us. This Privacy Policy explains how Monash University, ITO5002, TP5 2025 Group 2 ("we", "our", "us")
              collects, uses, and protects your information when you use Motorbike Theft Hotspot ("the App").
            </p>

            <h2 class="text-subtitle-1 font-weight-medium mb-2">1. Information We Collect</h2>
            <ul class="mb-4 pl-6">
              <li>Device and usage data (e.g. browser type, IP address, access times) to support performance, security and analytics.</li>
              <li>We do not collect personally identifiable information (such as name or email) unless you voluntarily provide it via forms (e.g., Contact).</li>
            </ul>

            <h2 class="text-subtitle-1 font-weight-medium mb-2">2. How We Use Information</h2>
            <ul class="mb-4 pl-6">
              <li>Provide and improve the App’s services and features.</li>
              <li>Display relevant hotspot and safety information.</li>
              <li>Monitor performance, usage, and security.</li>
              <li>Comply with legal obligations.</li>
            </ul>

            <h2 class="text-subtitle-1 font-weight-medium mb-2">3. Data Sharing</h2>
            <ul class="mb-4 pl-6">
              <li>We do not sell or rent your data to third parties.</li>
              <li>We may share data with trusted providers (e.g., hosting, analytics) under confidentiality and data‑processing agreements.</li>
              <li>We may disclose information if required by law or to protect rights, safety, or integrity of the App.</li>
            </ul>

            <h2 class="text-subtitle-1 font-weight-medium mb-2">4. Cookies & Tracking</h2>
            <ul class="mb-4 pl-6">
              <li>The App may use cookies or similar technologies for essential functionality and usage insights.</li>
              <li>You can disable cookies in your browser settings; some features may not work properly if disabled.</li>
            </ul>

            <h2 class="text-subtitle-1 font-weight-medium mb-2">5. Data Security</h2>
            <ul class="mb-4 pl-6">
              <li>We take reasonable technical and organisational measures to protect your data.</li>
              <li>No method of transmission or storage is 100% secure; we cannot guarantee absolute security.</li>
            </ul>

            <h2 class="text-subtitle-1 font-weight-medium mb-2">6. Your Rights</h2>
            <ul class="mb-4 pl-6">
              <li>Depending on your location, you may have rights to access, correct, delete, restrict, or object to processing.</li>
              <li>You may withdraw consent where applicable.</li>
              <li>To exercise rights, please contact us using the in‑app contact form.</li>
            </ul>

            <h2 class="text-subtitle-1 font-weight-medium mb-2">7. Changes to This Policy</h2>
            <p class="mb-4">We may update this Policy from time to time. Changes will be posted here with a new "Last updated" date.</p>

            <h2 class="text-subtitle-1 font-weight-medium mb-2">8. Contact Us</h2>
            <p>If you have questions about this Policy or our practices, please contact us via the <router-link to="/contact">contact form</router-link>.</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import PageHero from './components/PageHero.vue'
</script>

<style scoped>
ul { list-style: disc; }
</style>

