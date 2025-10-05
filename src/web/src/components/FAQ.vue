<template>
  <v-container class="pt-1 pt-md-3" style="padding-bottom: 200px;">
    <PageHero
      title="Frequently Asked Questions"
      subtitle="Learn more about how Hotspot works and how to use it effectively"
      icon="mdi-help-circle-outline"
    />

    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <v-card elevation="1">
          <v-card-text class="pa-6">
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

          <v-expansion-panels v-model="expandedPanel" multiple>
            <v-expansion-panel
              v-for="(faq, index) in filteredFAQs"
              :key="faq.id"
              :value="index"
            >
              <v-expansion-panel-title>
                <span class="text-subtitle-1 font-weight-bold">{{ faq.question }}</span>
              </v-expansion-panel-title>
              <v-expansion-panel-text>
                <div v-html="faq.answer" class="faq-answer text-body-1"></div>
                <!-- Resources Section -->
                <div v-if="faq.resources && faq.resources.length > 0" class="mt-4 pt-3 border-t">
                  <h4 class="text-subtitle-2 font-weight-bold mb-2">Data Sources:</h4>
                  <v-list density="compact" class="bg-transparent">
                    <v-list-item
                      v-for="(resource, idx) in faq.resources"
                      :key="idx"
                      :href="resource.link"
                      target="_blank"
                      rel="noopener noreferrer"
                      class="pa-0 mb-1"
                    >
                      <template v-slot:prepend>
                        <v-icon size="small" color="primary">mdi-open-in-new</v-icon>
                      </template>
                      <v-list-item-title class="text-caption text-primary">
                        {{ resource.text }}
                      </v-list-item-title>
                    </v-list-item>
                  </v-list>
                </div>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>

          <v-empty-state v-if="filteredFAQs.length === 0">
            <template v-slot:media>
              <v-icon size="64" color="grey-lighten-1">mdi-help-circle-outline</v-icon>
            </template>
            <template v-slot:title>
              <h3 class="text-grey">No matching FAQs found</h3>
            </template>
            <template v-slot:text>
              <p class="text-grey">Try different keywords or browse the questions above.</p>
            </template>
          </v-empty-state>
          </v-card-text>
        </v-card>

        <!-- Contact Support Section -->
        <v-card class="mt-6" color="grey-lighten-5" elevation="1">
          <v-card-text class="text-center pa-6">
            <v-icon size="48" color="primary" class="mb-3">mdi-message-question</v-icon>
            <h3 class="text-h5 font-weight-bold text-high-emphasis mb-2">Still have questions?</h3>
            <p class="text-body-1 text-medium-emphasis mb-4">Can't find what you're looking for? Our support team is here to help.</p>
            <v-btn
              color="primary"
              variant="flat"
              size="large"
              prepend-icon="mdi-email-outline"
              @click="goToContact"
            >
              Contact Support
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import PageHero from './PageHero.vue'

const router = useRouter()
const searchQuery = ref('')
const expandedPanel = ref<number[]>([])

interface FAQItem {
  id: number
  question: string
  answer: string
  category: string
  resources?: {
    text: string
    link: string
  }[]
}

const faqItems = ref<FAQItem[]>([
  {
    id: 1,
    question: "What is the Safety Score and how is it calculated?",
    answer: "The Safety Score is a numerical rating from 0-100 that represents the relative safety of a suburb. Our safety score is based on an estimated risk of motorbike theft for each suburb. We start with official motor vehicle theft statistics for each Council area in Victoria. Using data on the proportion of motorbike riders in each Council, we estimate the number of motorbike thefts. This creates a relative risk score that we then normalize to a simple 0-100 scale for easy comparison, where higher scores indicate safer areas.",
    category: "safety",
    resources: [
      {
        text: "Crime Statistics Victoria - LGA Criminal Incidents",
        link: "https://files.crimestatistics.vic.gov.au/2025-06/Data_Tables_LGA_Criminal_Incidents_Year_Ending_March_2025.xlsx"
      },
      {
        text: "Transport Victoria - Travel and Activity Survey",
        link: "https://opendata.transport.vic.gov.au/dataset/victorian-integrated-survey-of-travel-and-activity-vista"
      }
    ]
  },
  {
    id: 2,
    question: "Can I contribute parking information to Hotspot?",
    answer: "Yes! We encourage users to contribute parking information. You can add new parking locations, rate existing ones, and provide details about lighting, CCTV, and nearby facilities.",
    category: "contribution"
  },
  {
    id: 3,
    question: "How accurate is the parking availability information?",
    answer: "Parking information is sourced from both official datasets and community contributions. While we strive for accuracy, availability can change rapidly. We recommend using this as a guide and verifying on-site when possible.",
    category: "parking"
  },
  {
    id: 4,
    question: "What do the different risk levels mean?",
    answer: "Risk levels are categorized as: <strong>Low Risk</strong> (80-100 safety score), <strong>Medium Risk</strong> (50-79 safety score), and <strong>High Risk</strong> (0-49 safety score). Suburbs within the same Council area often have similar scores because the initial risk calculation is done at the Council level using Victoria-wide crime and road user data. This Council-level score is then applied to all postcodes and suburbs within that Council. The score represents the overall risk level for the broader Council area rather than individual street-level risk.",
    category: "safety"
  },
  {
    id: 5,
    question: "How can I report incorrect information?",
    answer: "You can report incorrect information by contacting our support team through the Contact Us page. We review all reports promptly.",
    category: "support"
  },
  {
    id: 6,
    question: "Does Hotspot work in all Australian suburbs?",
    answer: "Currently, we focus on metropolitan areas in Melbourne and Victorian suburbs with available data. We're continuously expanding our coverage. If your suburb isn't listed, please contact us.",
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

onMounted(() => {
  expandedPanel.value = [0, 1, 2]
})
</script>
