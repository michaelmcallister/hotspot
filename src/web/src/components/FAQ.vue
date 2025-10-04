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
    answer: "The Safety Score is a numerical rating from 1-100 that represents the relative safety of a suburb. Our safety score is based on an estimated risk of motorbike theft for each suburb. We start with official motor vehicle theft statistics for each Local Government Area (LGA) in Victoria. Using data on the proportion of motorbike riders in each LGA, we estimate the number of motorbike thefts. This creates a relative risk score that we then normalize to a simple 0-1 scale for easy comparison, where lower scores indicate safer areas.",
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
    category: "contribution",

  },
  {
    id: 3,
    question: "How accurate is the parking availability information?",
    answer: "Parking information is sourced from official datasets and while we strive for accuracy, availability can change rapidly. We recommend using this as a guide and verifying on-site when possible.",
    category: "parking"
  },
  {
    id: 4,
    question: "What do the different risk levels mean?",
    answer: "Risk levels are categorized as: <strong>Low Risk</strong>(100-75), <strong>medium Risk</strong>(74-50) and <strong>High Risk</strong>(50-1). Suburbs within the same Local Government Area (LGA) often have similar scores because the initial risk calculation is done at the LGA level using Victoria-wide crime and road user data. This LGA-level score is then applied to all postcodes and suburbs within that LGA. The score represents the overall risk level for the broader local government area rather than individual street-level risk..",
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