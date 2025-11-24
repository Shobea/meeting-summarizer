<template>
  <div v-if="!isSaved" class="bg-[var(--mblue)] p-8 rounded-2xl shadow-sm w-full max-w-md">
    <h2 class="text-white text-3xl font-bold mb-6">Who is this?</h2>
    
    <!-- Input Fields -->
    <div class="space-y-4 mb-6">
      <div>
        <label class="block text-white text-sm mb-1 font-semibold">Name</label>
        <input 
          v-model="localName"
          type="text" 
          class="w-full mt-1 p-2 rounded-md bg-gray-100 shadow-inner outline-none" 
          placeholder="Enter name" 
        />
      </div>
      <div>
        <label class="block text-white text-sm mb-1 font-semibold">Student ID</label>
        <input 
          v-model="localStudentId"
          type="text" 
          class="w-full mt-1 p-2 rounded-md bg-gray-100 shadow-inner outline-none" 
          placeholder="Enter student ID" 
        />
      </div>
    </div>
    
    <!-- Buttons -->
    <div class="flex justify-end">
      <Button 
        class="bg-[var(--dblue)] hover:bg-blue-400 text-white font-medium" 
        @click="handleSave"
        :disabled="!localName.trim() || !localStudentId.trim() || isLoading"
      >
        {{ isLoading ? 'Saving...' : 'Scan More' }}
      </Button>
    </div>

    <!-- Messages -->
    <div v-if="message" class="mt-4 p-3 rounded-md text-center text-sm font-medium" 
         :class="messageType === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
      {{ message }}
    </div>
  </div>

  <!-- Success State -->
  <div v-else class="bg-green-100 border border-green-400 p-6 rounded-2xl text-green-800 text-center">
    <div class="text-4xl mb-2">✅</div>
    <h3 class="text-lg font-bold mb-2">Student Registered!</h3>
    <p class="text-sm mb-2">{{ savedStudentName }} has been saved.</p>
    <Button 
      class="bg-green-600 hover:bg-green-700 text-white"
      @click="resetForm"
    >
      Register Another
    </Button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Button } from '@/components/ui/button'

const props = defineProps({
  name: String,
  studentId: String,
  nfcId: String,
})

const emit = defineEmits(["update:name", "update:studentId", "update:nfcId", "save"])

const isLoading = ref(false)
const message = ref('')
const messageType = ref('')
const isSaved = ref(false)
const savedStudentName = ref('')

const localName = ref(props.name || '')
const localStudentId = ref(props.studentId || '')
const localNfcId = ref(props.nfcId || '')

watch(() => props.name, (val) => (localName.value = val || ''))
watch(() => props.studentId, (val) => (localStudentId.value = val || ''))
watch(() => props.nfcId, (val) => (localNfcId.value = val || ''))

const resetForm = () => {
  localName.value = ''
  localStudentId.value = ''
  localNfcId.value = ''
  isSaved.value = false
  message.value = ''
  messageType.value = ''
  savedStudentName.value = ''

  emit("update:name", "")
  emit("update:studentId", "")
  emit("update:nfcId", "")
}

const handleSave = () => {
  if (!localName.value.trim() || !localStudentId.value.trim()) return

  emit("save", {
  name: localName.value.trim(),
  school_id: localStudentId.value.trim(), // Lowercase here is okay
  nfc_id: localNfcId.value.trim()
})

}
</script>
