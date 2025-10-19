<template>
  <div class="min-h-screen flex flex-col justify-center items-center bg-white px-6 py-10">
    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 w-full max-w-6xl items-start">
      <!-- Left Section -->
      <div>
        <h1 class="font-bold text-5xl leading-tight mb-8">
          Scan student ID<br />
          with the<br />
          connected phone
        </h1>

        <!-- Scanned Students Box -->
        <div class="bg-[var(--lblue)] p-6 rounded-2xl max-w-sm">
          <p class="font-medium mb-2">Successfully Scanned:</p>
          <ul class="space-y-1 text-gray-700 text-sm">
            <li v-for="(student, index) in scannedStudents" :key="index">
              {{ student.name }} : {{ student.id }}
            </li>
            <li v-if="scannedStudents.length === 0" class="text-gray-500 italic">
              No students scanned yet
            </li>
          </ul>
        </div>

        <!-- Delete Button -->
        <div class="flex justify-end mt-4 max-w-sm">
          <Button
            v-if="scannedStudents.length > 0"
            class="bg-[var(--orange)] hover:bg-orange-500 text-white text-sm font-medium"
            @click="deleteLatestStudent"
          >
            Delete Latest
          </Button>
        </div>
      </div>

      <!-- Right Section -->
      <div class="flex flex-col items-center w-full">
        <!-- NFC Input Placeholder, delete later?? -->
        <div class="mb-4 w-full max-w-md">

          <label class="block text-gray-700 font-semibold mb-2">Scan or Enter NFC ID</label>
          <div class="flex gap-2">
            <input
              v-model="nfcId"
              type="text"
              placeholder="Scan NFC Tag..."
              class="w-full p-2 border rounded-md outline-none"
            />
            <Button
              class="bg-[var(--dblue)] hover:bg-blue-400 text-white font-medium"
              @click="handleNfcScan"
            >
              Scan
            </Button>
          </div>
        </div>

        <p
          v-if="showBlueBox"
          class="font-semibold text-lg mb-4 text-left w-full max-w-md"
        >
          A new NFC ID has been scanned!
        </p>

        <!-- Blue Box -->
        <div
          v-if="showBlueBox"
          class="bg-[var(--mblue)] p-8 rounded-2xl shadow-sm w-full max-w-md"
        >
          <h2 class="text-white text-3xl font-bold mb-6">Who is this?</h2>

          <!-- Input Fields -->
          <div class="space-y-4 mb-6">
            <div>
              <label class="block text-white text-sm mb-1 font-semibold">Name</label>
              <input
                v-model="name"
                type="text"
                class="w-full mt-1 p-2 rounded-md bg-gray-100 shadow-inner outline-none"
                placeholder="Enter name"
              />
            </div>
            <div>
              <label class="block text-white text-sm mb-1 font-semibold">Student ID</label>
              <input
                v-model="studentId"
                type="text"
                class="w-full mt-1 p-2 rounded-md bg-gray-100 shadow-inner outline-none"
                placeholder="Enter student ID"
              />
            </div>
          </div>

          <!-- Buttons inside the blue box -->
          <div class="flex justify-between">
            <Button
              class="bg-[var(--orange)] hover:bg-orange-500 text-white font-medium"
              @click="resetFields"
            >
              Cancel
            </Button>
            <Button
              class="bg-[var(--dblue)] hover:bg-blue-400 text-white font-medium"
              @click="confirmAddNewStudent"
            >
              Save
            </Button>
          </div>
        </div>

        <!-- Bottom Buttons -->
        <div class="flex justify-between w-full max-w-md mt-6">
          <RouterLink to="/meetings">
            <Button class="bg-[var(--orange)] hover:bg-orange-500 cursor-pointer text-white font-medium">
              Cancel Meeting
            </Button>
          </RouterLink>

          <Button
            class="bg-[var(--dblue)] hover:bg-blue-400 cursor-pointer text-white font-medium"
            @click="goToCreateNewMeeting"
            :hidden="scannedStudents.length === 0"
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
import { Button } from '@/components/ui/button'

const router = useRouter()

const name = ref('')
const studentId = ref('')
const nfcId = ref('')
const scannedStudents = ref([])

const showBlueBox = ref(false)

async function checkIfNfcExists(nfcId) {
  //ADD LOGIC HERE

  // Checker if popup works
  const existingStudent = nfcId === 'NFC-12345'
    ? { name: 'John Doe', id: '20201433191', nfc: 'NFC-12345' }
    : null
  return existingStudent
}

// Simulate scanning NFC ID
async function handleNfcScan() {
  if (!nfcId.value.trim()) return

  const existingStudent = await checkIfNfcExists(nfcId.value)

  if (existingStudent) {
    // Found in db
    scannedStudents.value.push(existingStudent)
    showBlueBox.value = false
    name.value = ''
    studentId.value = ''
    nfcId.value = ''
  } else {
    // Not found
    showBlueBox.value = true
  }
}

// Save new student
function confirmAddNewStudent() {
  if (name.value.trim() && studentId.value.trim() && nfcId.value.trim()) {
    scannedStudents.value.push({
      name: name.value,
      id: studentId.value,
      nfc: nfcId.value,
    })
    name.value = ''
    studentId.value = ''
    nfcId.value = ''
    showBlueBox.value = false
  }
}

// Delete latest scanned student
function deleteLatestStudent() {
  if (scannedStudents.value.length > 0) {
    scannedStudents.value.pop()
  }
}

// Reset fields
function resetFields() {
  name.value = ''
  studentId.value = ''
  nfcId.value = ''
  showBlueBox.value = false
}

// Navigate to next page, pass info
function goToCreateNewMeeting() {
  router.push({
    name: 'CreateNewMeeting',
    query: { data: JSON.stringify(scannedStudents.value) }
  })
}
</script>


