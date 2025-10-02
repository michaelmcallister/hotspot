<template>
  <v-main>
    <v-container class="pa-6" max-width="800">
      <v-row justify="center">
        <v-col cols="12">
          <div class="text-center mb-8">
            <h1 class="text-h3 font-weight-bold text-primary mb-2">Frequently Asked Questions</h1>
            <p class="text-body-1 text-grey">Learn more about how Hotspot works and how to use it effectively</p>
          </div>

          <v-card class="pa-6" elevation="1">
            <!-- Search Section -->
            <div class="mb-6">
              <v-text-field
                v-model="searchQuery"
                label="Search FAQs..."
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                clearable
                @update:model-value="filterFAQs"
              ></v-text-field>
            </div>

            <!-- FAQ List -->
            <v-expansion-panels v-model="expandedPanel" multiple>
              <v-expansion-panel
                v-for="(faq, index) in filteredFAQs"
                :key="faq.id"
                :value="index"
              >
                <v-expansion-panel-title>
                  <span class="font-weight-medium">{{ faq.question }}</span>
                </v-expansion-panel-title>
                <v-expansion-panel-text>
                  <div v-html="faq.answer" class="faq-answer"></div>
                  
                  <!-- Additional resources for specific FAQs -->
                  <div v-if="faq.resources" class="mt-3">
                    <v-divider class="my-3"></v-divider>
                    <h4 class="text-body-2 font-weight-medium mb-2">Related Resources:</h4>
                    <v-list density="compact" class="bg-transparent">
                      <v-list-item
                        v-for="resource in faq.resources"
                        :key="resource.text"
                        :href="resource.link"
                        target="_blank"
                        class="px-0"
                      >
                        <template v-slot:prepend>
                          <v-icon size="small" color="primary">mdi-open-in-new</v-icon>
                        </template>
                        <v-list-item-title class="text-body-2">{{ resource.text }}</v-list-item-title>
                      </v-list-item>
                    </v-list>
                  </div>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>

            <!-- No results message -->
            <div v-if="filteredFAQs.length === 0" class="text-center py-8">
              <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-magnify-remove</v-icon>
              <h3 class="text-h6 mb-2">No matching FAQs found</h3>
              <p class="text-body-2 text-grey">Try searching with different keywords</p>
            </div>
          </v-card>

          <!-- Contact Support Section -->
          <v-card class="mt-6 pa-6 text-center" color="primary-lighten-5">
            <v-icon size="48" color="primary" class="mb-4">mdi-help-circle</v-icon>
            <h3 class="text-h5 mb-2">Still have questions?</h3>
            <p class="text-body-1 mb-4">Can't find what you're looking for? Our support team is here to help.</p>
            <v-btn
              color="primary"
              variant="flat"
              rounded="lg"
              @click="goToContact"
              class="mr-2"
            >
              Contact Support
            </v-btn>
            <v-btn
              variant="outlined"
              rounded="lg"
              @click="goToHome"
            >
              Back to Home
            </v-btn>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchQuery = ref('')
const expandedPanel = ref<number[]>([])

interface FAQItem {
  id: number
  question: string
  answer: string
  category: string
  resources?: { text: string; link: string }[]
}

const faqItems = ref<FAQItem[]>([
  {
    id: 1,
    question: "What is the Safety Score and how is it calculated?",
    answer: "The Safety Score is a numerical rating from 0-100 that represents the relative safety of a suburb based on various factors including crime statistics, lighting coverage, CCTV availability, and community-reported data. Higher scores indicate safer areas.",
    category: "safety"
  },
  {
    id: 2,
    question: "How often is the safety data updated?",
    answer: "Our safety data is updated monthly from official sources. User-contributed data (parking locations, lighting reports) is updated in real-time as users submit new information.",
    category: "data"
  },
  {
    id: 3,
    question: "Can I contribute parking information to Hotspot?",
    answer: "We encourage users to contribute parking information. You can add new parking locations, rate existing ones, and provide details about lighting, CCTV, and nearby facilities. All contributions are reviewed by our community.",
    category: "contribution"
  },
  {
    id: 4,
    question: "How accurate is the parking availability information?",
    answer: "Parking information is sourced from both official datasets and community contributions. While we strive for accuracy, availability can change rapidly. We recommend using this as a guide and verifying on-site when possible.",
    category: "parking"
  },
  {
    id: 5,
    question: "What do the different risk levels mean?",
    answer: "Risk levels are categorized as: <strong>Low Risk</strong> (80-100), <strong>Moderate Risk</strong> (60-79), <strong>Elevated Risk</strong> (40-59), and <strong>High Risk</strong> (0-39). These are relative measures based on comparative analysis of suburbs.",
    category: "safety"
  },
  {
    id: 6,
    question: "Is my personal information safe when using Hotspot?",
    answer: "We take privacy seriously. We only collect essential information and never share personal data without consent. Anonymous contributions help improve the platform for everyone while protecting your privacy.",
    category: "privacy",
  },
  {
    id: 7,
    question: "How can I report incorrect information?",
    answer: "You can report incorrect information by contacting our support team through the Contact Us page.",
    category: "support"
  },
  {
    id: 8,
    question: "Does Hotspot work in all Australian suburbs?",
    answer: "Currently, we focus on metropolitan areas within Melbourne with available data. We're continuously expanding our coverage. If your suburb isn't listed, please contact us and we'll prioritize adding it.",
    category: "coverage"
  }
])

const filteredFAQs = computed(() => {
  if (!searchQuery.value) return faqItems.value
  
  const query = searchQuery.value.toLowerCase()
  return faqItems.value.filter(faq => 
    faq.question.toLowerCase().includes(query) || 
    faq.answer.toLowerCase().includes(query) ||
    faq.category.toLowerCase().includes(query)
  )
})

const filterFAQs = () => {
  
  if (searchQuery.value) {
    expandedPanel.value = filteredFAQs.value.map((_, index) => index)
  }
}

const goToContact = () => {
  router.push('/contact') 
}

const goToHome = () => {
  router.push('/')
}


onMounted(() => {
  expandedPanel.value = [0, 1, 2] 
})
</script>

<style scoped>
.faq-answer {
  line-height: 1.6;
}

.faq-answer :deep(strong) {
  color: rgb(var(--v-theme-primary));
}

.v-expansion-panel-title {
  min-height: 64px;
}
</style>