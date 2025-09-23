<template>
  <div>
    <v-container class="pa-6">
      <v-row justify="center">
        <v-col cols="12" md="8" lg="6">
          <h1 class="text-h3 font-weight-bold text-primary mb-8 text-center">Contact Us</h1>

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
                type="submit"
                color="primary"
                variant="flat"
                size="large"
                rounded="lg"
                :disabled="!valid || !recaptchaToken"
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
  </div>
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
const disabled = ref(true)

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


const handleErrorCalback = () => {
  console.log('reCAPTCHA error callback triggered');
  recaptchaToken.value = '';
  disabled.value = true;
};

const handleExpiredCallback = () => {
  console.log('reCAPTCHA expired callback triggered');
  recaptchaToken.value = '';
  disabled.value = true;
};

const handleLoadCallback = (response: string) => {
  console.log('reCAPTCHA load/verify callback triggered with response:', response);
  recaptchaToken.value = response;
  if (response) {
    disabled.value = false;
  } else {
    disabled.value = true;
  }
};


const handleSubmit = async () => {
  if (!recaptchaToken.value) {
    alert('Please complete the reCAPTCHA verification.')
    return
  }

  // Form data ready for submission
  const formData = {
    email: email.value,
    category: category.value,
    subject: subject.value,
    postcode: postcode.value,
    details: details.value,
    recaptchaToken: recaptchaToken.value
  }

  // TODO: Send form data including recaptchaToken to backend for verification
  console.log(formData);
  alert('Form submitted successfully!')

  // Reset reCAPTCHA and form
  if (window.grecaptcha && recaptchaWidgetId !== null) {
    window.grecaptcha.reset(recaptchaWidgetId);
  }
  recaptchaToken.value = ''
  disabled.value = true
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
