<template>
  <div class="w-full max-w-md">
    <!-- NFC Status -->
    <div class="mb-4">
      <div class="flex items-center gap-2 mb-2">
        <div :class="['w-3 h-3 rounded-full', nfcSupport === 'supported' ? 'bg-green-500' : nfcSupport === 'unsupported' ? 'bg-red-500' : 'bg-yellow-500']"></div>
        <span class="text-sm font-medium">
          {{ nfcStatusText }}
        </span>
      </div>
      
      <!-- Scanning Indicator -->
      <div v-if="isScanning && nfcSupport === 'supported'" class="bg-blue-100 border border-blue-400 rounded-md p-3">
        <p class="text-blue-800 text-sm font-medium">
          📱 Ready - Tap an NFC tag to your phone
        </p>
      </div>
    </div>

    <!-- Student ID Input -->
    <div class="mb-4">
      <label class="block text-gray-700 font-semibold mb-2">Or Enter Student ID Manually</label>
      <div class="flex gap-2">
        <input 
          v-model="studentIdInput" 
          type="text" 
          placeholder="Enter Student ID manually..." 
          class="w-full p-2 border rounded-md outline-none" 
          @keyup.enter="handleManualSubmit"
        />
        <Button 
          class="bg-[var(--dblue)] hover:bg-blue-400 text-white font-medium" 
          @click="handleManualSubmit"
          :disabled="!studentIdInput.trim()"
        >
          Submit
        </Button>
      </div>
      <p class="text-sm text-gray-500 mt-2">
        Use if automatic scanning doesn't work
      </p>
    </div>

    <p v-if="showBlueBox" class="font-semibold text-lg mb-4 text-left">
      A new NFC ID has been scanned!
    </p>

    <!-- Debug Info (Development Only) -->
    <div v-if="isDevelopment && debugInfo" class="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
      <h4 class="font-semibold text-sm mb-2">Debug Info:</h4>
      <p class="text-xs text-gray-600">{{ debugInfo }}</p>
    </div>

    <!-- Test Buttons (Development Only) -->
    <div v-if="isDevelopment" class="mb-6">
      <p class="text-sm text-gray-600 mb-2">Test with sample Student IDs:</p>
      <div class="flex gap-2 flex-wrap">
        <Button 
          @click="testStudentId('S001')" 
          class="bg-green-500 hover:bg-green-600 text-white text-xs font-medium"
        >
          John (S001)
        </Button>
        <Button 
          @click="testStudentId('S002')" 
          class="bg-blue-500 hover:bg-blue-600 text-white text-xs font-medium"
        >
          Jane (S002)
        </Button>
        <Button 
          @click="testStudentId('S003')" 
          class="bg-purple-500 hover:bg-purple-600 text-white text-xs font-medium"
        >
          Mike (S003)
        </Button>
        <Button 
          @click="testStudentId('999999')" 
          class="bg-red-500 hover:bg-red-600 text-white text-xs font-medium"
        >
          Invalid (999999)
        </Button>
      </div>
    </div>

    <!-- Student ID Not Found Popup -->
    <Popup
      v-model="showStudentNotFoundPopup"
      type="orange"
      :data="popupData"
      @submit="closeStudentNotFoundPopup"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Button } from '@/components/ui/button'
import Popup from '../Popup.vue'

const props = defineProps({
  nfcSupport: {
    type: String,
    default: 'checking'
  },
  isScanning: {
    type: Boolean,
    default: false
  },
  showBlueBox: {
    type: Boolean,
    default: false
  },
  isDevelopment: {
    type: Boolean,
    default: false
  },
  checkStudentExists: {
    type: Function,
    required: true
  }
})

const emit = defineEmits(['tag-scanned', 'manual-submit', 'simulate-scan'])

const studentIdInput = ref('')
const showStudentNotFoundPopup = ref(false)
const debugInfo = ref('')
const popupData = ref({
  title: 'Student ID Not Found',
  description: 'This Student ID is not in the database. Please scan you student ID card first to register.',
  confirmText: 'OK',
  cancelText: 'Cancel'
})

const nfcStatusText = computed(() => {
  switch (props.nfcSupport) {
    case 'supported':
      return 'NFC is supported - Tap a tag to scan'
    case 'unsupported':
      return 'NFC not supported on this device/browser'
    default:
      return 'Checking NFC support...'
  }
})

// Listen for NFC tag scans
function handleNfcTagScanned(event) {
  const tagData = event.detail.tagData
  emit('tag-scanned', tagData)
}

async function handleManualSubmit() {
  if (!studentIdInput.value.trim()) {
    return
  }

  const studentId = studentIdInput.value.trim()
  debugInfo.value = `Checking student ID: "${studentId}"`
  console.log('🔍 Checking student ID:', studentId)

  try {
    // Use the provided function to check if student exists
    const student = await props.checkStudentExists(studentId)
    debugInfo.value += ` | Found: ${student ? 'YES' : 'NO'}`
    
    if (student && student.nfc_id) {
      // Student exists and has NFC ID, emit the NFC ID
      console.log('✅ Student found:', student)
      debugInfo.value += ` | NFC ID: ${student.nfc_id}`
      emit('manual-submit', student.nfc_id)
      studentIdInput.value = ''
      debugInfo.value = '' // Clear debug info after success
    } else {
      // Student not found or has no NFC ID, show popup
      console.log('❌ Student ID not found in database or no NFC ID associated')
      debugInfo.value += ' | Student not found or missing NFC ID'
      showStudentNotFoundPopup.value = true
    }
  } catch (error) {
    console.error('Error checking student:', error)
    debugInfo.value += ` | Error: ${error.message}`
    // Show error popup
    popupData.value = {
      title: 'Error',
      description: 'Failed to check student database. Please try again.',
      confirmText: 'OK'
    }
    showStudentNotFoundPopup.value = true
  }
}

function testStudentId(studentId) {
  studentIdInput.value = studentId
  handleManualSubmit()
}

function simulateScan(nfcId) {
  emit('simulate-scan', nfcId)
}

function closeStudentNotFoundPopup() {
  showStudentNotFoundPopup.value = false
  studentIdInput.value = '' // Clear the input
}

onMounted(() => {
  window.addEventListener('nfc-tag-scanned', handleNfcTagScanned)
})

onUnmounted(() => {
  window.removeEventListener('nfc-tag-scanned', handleNfcTagScanned)
})
</script>