<template>
  <div class="min-h-screen flex flex-col justify-center items-center bg-white px-6 py-10">

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-24 w-full max-w-6xl items-start">
      
      <!-- Left Section -->
      <div class="flex flex-col justify-start">
        <h1 class="font-bold text-5xl leading-tight mb-8">
          To register,<br />
          scan student ID<br />
          with the<br/>
          connected<br/>
          phone
        </h1>
      </div>

      <!-- Right Section -->
        <div class="flex flex-col items-end justify-start mt-2 w-full max-w-md ml-auto">

             <!-- Waiting for NFC -->
            <div v-if="!nfcId"class="flex items-center gap-2 ">
              <span class="h-3 w-3 rounded-full bg-green-500"></span>
              <p class="text-gray-700 font-medium">Waiting for NFC scan...</p>
            </div>

            <StudentRegistrationForm
              v-if="nfcId"
              :name="name"
              :student-id="studentId"
              :nfc-id="nfcId"
              @update:name="name = $event"
              @update:studentId="studentId = $event"
              @cancel="resetFields"
              @save="handleSaveStudent"
              @student-created="(s) => scannedStudents.push(s)"
            />



            <!-- Bottom Buttons -->
            <div class="flex justify-end w-full mt-10">
                <router-link to="/scanmeeting">
                <Button class="bg-[var(--orange)] hover:bg-orange-500 text-white font-medium px-6 py-2 rounded cursor-pointer">
                    Go Back
                </Button>
                </router-link>
            </div>
        </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from "vue"
import { useRouter } from "vue-router"
import Button from '@/components/ui/button/Button.vue'
import StudentRegistrationForm from '@/components/StudentRegistrationForm.vue'
import { useNfcSocket } from '@/composables/useNfcSocket'
import axios from 'axios'

const router = useRouter()

const name = ref('')
const studentId = ref('')
const nfcId = ref(null) // hidden stored NFC ID
const scannedStudents = ref([])

// WS URL: replace IP with your Django host IP
const WS_URL = import.meta.env.VITE_WS_URL || "ws://192.168.1.6:8000/ws/nfc/"
const { lastScan, connected } = useNfcSocket(WS_URL)

// update stored nfcId when new scan arrives
watch(lastScan, (val) => {
  if (val && val.nfc_id) {
    nfcId.value = val.nfc_id
    // optional: short-lived UI state or toast
  }
})

const canSave = computed(() => {
  return !!nfcId.value && name.value.trim() !== '' && studentId.value.trim() !== ''
})

async function handleSaveStudent(payload) {
  try {
    await axios.post("http://192.168.1.6:8000/api/student-create/", {
      name: payload.name,
      school_ID: payload.school_id,
      nfc_ID: payload.nfc_id
    })

    resetFields()
  } catch (err) {
    console.error(err)
  }
}




function resetFields() {
  name.value = ''
  studentId.value = ''
  nfcId.value = null
}

function handleDeleteLatest() {
  scannedStudents.value.pop()
}

function goToCreateNewMeeting() {
  router.push('/createnewmeeting')
}
</script>

