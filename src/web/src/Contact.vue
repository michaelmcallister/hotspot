<template>
  <v-main>
    <v-container class="pa-6">
      <v-row justify="center">
        <v-col cols="12" md="8" lg="6">
          <h1 class="text-h3 font-weight-bold text-primary mb-2 text-center">Contact Us</h1>

          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="email"
              label="Email"
              type="email"
              variant="outlined"
              :rules="emailRules"
              required
              class="mb-4"
            />

            <v-select
              v-model="category"
              :items="categoryItems"
              label="Category"
              variant="outlined"
              :rules="categoryRules"
              required
              class="mb-4"
            />

            <v-text-field
              v-model="subject"
              label="Subject"
              variant="outlined"
              :rules="subjectRules"
              required
              class="mb-4"
            />

            <v-text-field
              v-model="postcode"
              label="Postcode (optional)"
              variant="outlined"
              type="text"
              :rules="postcodeRules"
              class="mb-4"
            />

            <v-textarea
              v-model="details"
              label="Details"
              variant="outlined"
              rows="6"
              :rules="detailsRules"
              required
              class="mb-6"
            />

            <div class="recaptcha-send-container mb-6">
              <div id="recaptcha-widget" v-show="recaptchaReady"></div>
              <div v-show="!recaptchaReady">Loading reCAPTCHA...</div>
              <v-btn
                color="primary"
                variant="flat"
                size="large"
                rounded="lg"
                :disabled="!valid || !recaptchaToken || showLoadingDialog"
                :loading="showLoadingDialog"
                @click="handleSubmit"
                class="send-button"
              >
                Send
              </v-btn>
            </div>
          </v-form>
        </v-col>
      </v-row>
    </v-container>

    <v-dialog v-model="showLoadingDialog" max-width="400" persistent>
      <v-card>
        <v-card-text class="text-center pa-8">
          <v-progress-circular
            indeterminate
            size="64"
            width="6"
            color="primary"
            class="mb-4"
          ></v-progress-circular>
          <h3 class="text-h6 mb-2">Submitting your message...</h3>
          <p class="text-body-2 text-grey">Please wait while we process your request</p>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showSuccessDialog" max-width="500" persistent>
      <v-card>
        <v-card-text class="text-center pa-6">
          <v-icon
            color="success"
            size="80"
            class="mb-4"
          >
            mdi-check-circle
          </v-icon>
          <h3 class="text-h5 mb-2">Thank you!</h3>
          <p class="text-body-1">{{ successMessage }}</p>
        </v-card-text>
        <v-card-actions class="justify-center pb-4">
          <v-btn
            color="primary"
            variant="flat"
            rounded="lg"
            @click="showSuccessDialog = false"
          >
            Got it
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showErrorDialog" max-width="500" persistent>
      <v-card>
        <v-card-text class="text-center pa-6">
          <v-icon
            color="error"
            size="80"
            class="mb-4"
          >
            mdi-alert-circle
          </v-icon>
          <h3 class="text-h5 mb-2">Error</h3>
          <p class="text-body-1">{{ errorMessage }}</p>
        </v-card-text>
        <v-card-actions class="justify-center pb-4">
          <v-btn
            color="primary"
            variant="flat"
            rounded="lg"
            @click="showErrorDialog = false"
          >
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import validator from 'validator'

const recaptchaReady = ref(false)
let recaptchaWidgetId: number | null = null

onMounted(() => {
  // Yes there are libraries and you'd think they would be easy to use, but I couldn't get it to work (and I tried a few...)
  const checkRecaptcha = () => {
    if (window.grecaptcha && window.grecaptcha.ready) {
      window.grecaptcha.ready(() => {
        recaptchaWidgetId = window.grecaptcha.render('recaptcha-widget', {
          // This sitekey is not a secret, it's safe to commit to git.
          sitekey: '6LcA4dIrAAAAAJLNNCHqH4Xsmqz52_Kq5tgZecjs',
          callback: handleLoadCallback,
          'expired-callback': handleExpiredCallback,
          'error-callback': handleErrorCalback
        });

        recaptchaReady.value = true;
      });
    } else {
      setTimeout(checkRecaptcha, 500);
    }
  };

  checkRecaptcha();
})

const form = ref()
const valid = ref(false)
const email = ref('')
const category = ref('')
const subject = ref('')
const postcode = ref('')
const details = ref('')
const recaptchaToken = ref('')
const showSuccessDialog = ref(false)
const showErrorDialog = ref(false)
const showLoadingDialog = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const categoryItems = [
  'General Inquiry',
  'Technical Support',
  'Feature Request',
  'Bug Report',
  'Data Issue',
  'Other'
]

const emailRules = [
  (v: string) => !!v || 'Email is required',
  (v: string) => validator.isEmail(v) || 'Email must be valid',
]

const categoryRules = [
  (v: string) => !!v || 'Category is required',
]

const subjectRules = [
  (v: string) => !!v || 'Subject is required',
]

const detailsRules = [
  (v: string) => !!v || 'Details are required',
]

const postcodeRules = [
  (v: string) => {
    if (!v) return true
    return validator.isPostalCode(v, 'AU')
  }
]


const resetRecaptcha = () => {
  recaptchaToken.value = ''
}

const handleErrorCalback = resetRecaptcha
const handleExpiredCallback = resetRecaptcha

const handleLoadCallback = (response: string) => {
  recaptchaToken.value = response
};

const resetForm = () => {
  form.value?.reset()
  email.value = ''
  category.value = ''
  subject.value = ''
  postcode.value = ''
  details.value = ''
}

const resetRecaptchaWidget = () => {
  if (window.grecaptcha && recaptchaWidgetId !== null) {
    window.grecaptcha.reset(recaptchaWidgetId)
  }
  recaptchaToken.value = ''
}


const handleSubmit = async (event?: Event) => {
  if (event) {
    event.preventDefault()
  }
  if (!recaptchaToken.value) {
    errorMessage.value = 'Please complete the reCAPTCHA verification.'
    showErrorDialog.value = true
    return
  }

  showLoadingDialog.value = true

  // Form data ready for submission
  const formData = {
    email: email.value,
    category: category.value,
    subject: subject.value,
    postcode: postcode.value,
    details: details.value,
    recaptchaToken: recaptchaToken.value
  }

  try {
    const response = await fetch('/api/v1/contact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })

    if (response.ok) {
      const result = await response.json()
      showLoadingDialog.value = false
      successMessage.value = 'Your message has been sent successfully.'
      showSuccessDialog.value = true

      resetForm()
    } else {
      const errorData = await response.json()
      showLoadingDialog.value = false
      errorMessage.value = errorData.detail || 'Failed to submit form. Please try again.'
      showErrorDialog.value = true
    }

  } catch (error) {
    showLoadingDialog.value = false
    errorMessage.value = 'Failed to submit form. Please check your connection and try again.'
    showErrorDialog.value = true
  } finally {
    resetRecaptchaWidget()
  }
}



</script>

<style scoped>
.recaptcha-send-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.send-button {
  flex-shrink: 0;
}
</style>
