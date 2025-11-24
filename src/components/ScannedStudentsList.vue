<template>
  <div class="flex flex-col items-center w-full">
    <!-- Scanned Students Box -->
    <div
      class="bg-[var(--lblue)] p-6 rounded-2xl w-[600px] max-w-full shadow-sm"
    >
      <div class="flex justify-between items-center mb-3">
        <p class="font-medium text-base">Successfully Scanned:</p>
      </div>

      <!-- Scrollable list -->
      <div class="max-h-64 overflow-y-auto pr-2">
        <ul class="space-y-1 text-gray-700 text-sm">
          <li
            v-for="(student, index) in scannedStudents"
            :key="index"
            class="border-b border-gray-200 pb-1"
          >
            {{ student.name }} — {{ student.id }}
          </li>
          <li
            v-if="scannedStudents.length === 0"
            class="text-gray-500 italic"
          >
            No students scanned yet
          </li>
        </ul>
      </div>
    </div>

    <!-- Delete Button -->
    <div class="flex justify-end mt-4 w-[600px] max-w-full">
      <Button
        v-if="scannedStudents.length > 0"
        class="bg-[var(--orange)] hover:bg-orange-500 text-white text-sm font-medium"
        @click="$emit('delete-latest')"
      >
        Delete Latest
      </Button>
    </div>
  </div>
</template>

<script setup>
import { Button } from '@/components/ui/button'

defineProps({
  scannedStudents: {
    type: Array,
    default: () => []
  }
})

defineEmits(['delete-latest'])
</script>
