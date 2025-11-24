<template>
  <div class="min-h-screen flex flex-col justify-center items-center bg-white px-6 py-10">

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-24 w-full max-w-6xl items-start">
      
      <!-- Left Section -->
      <div class="flex flex-col justify-start">
        <h1 class="font-bold text-5xl leading-tight mb-8">
          Scan student ID<br />
          with the<br />
          connected<br/>
          phone
        </h1>
        
        <RouterLink to="/scannewid">
          <Button
            variant="default"
            class="bg-[var(--dblue)] cursor-pointer hover:bg-[var(--mblue)] text-white"
          >
            <span class="mr-2">+</span> Register a new student
          </Button>
        </RouterLink>
      </div>

      <!-- Right Section -->
        <div class="flex flex-col items-end justify-start mt-2 w-full max-w-md ml-auto">
            <ScannedStudentsList 
                :scanned-students="scannedStudents"
                @delete-latest="handleDeleteLatest" 
            />

            <StudentRegistrationForm
                v-if="showBlueBox"
                :name="name"
                :student-id="studentId" 
                :nfc-id="nfcId"
                :api-post="apiPost"
                @update:name="name = $event"
                @update:studentId="studentId = $event"
                @update:nfc-id="nfcId = $event"
                @cancel="resetFields"
                @save="handleSaveStudent"
                @student-created="handleStudentCreated"
            />

            <!-- Bottom Buttons -->
            <div class="flex justify-between w-full mt-10">
                <router-link to="/meetings">
                <Button class="bg-[var(--orange)] hover:bg-orange-500 text-white font-medium px-6 py-2 rounded cursor-pointer">
                    Cancel Meeting
                </Button>
                </router-link>

                <Button 
                class="bg-[var(--dblue)] cursor-pointer hover:bg-[var(--mblue)] text-white"
                @click="goToCreateNewMeeting" 
                >
                Next
                </Button>
            </div>
        </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Button from '@/components/ui/button/Button.vue'
import ScannedStudentsList from '@/components/ScannedStudentsList.vue'
import StudentRegistrationForm from '@/components/StudentRegistrationForm.vue'

const router = useRouter()

const name = ref('')
const studentId = ref('')
const nfcId = ref('')
const showBlueBox = ref(false)
const scannedStudents = ref([])

function handleDeleteLatest() {
  scannedStudents.value.pop()
}

function goToCreateNewMeeting() {
  router.push('/createnewmeeting')
}
</script>
