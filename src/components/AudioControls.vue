<template>
  <div :class="{ 'opacity-50 pointer-events-none': isRecordingActive }">
    <p class="font-semibold mb-2">Audio recording:</p>
    <div class="flex items-center gap-3">
      <div class="bg-gray-200 rounded-lg flex items-center justify-between px-4 py-2 shadow-sm flex-1">
        <span class="font-medium">Recording</span>
        <div class="flex items-center gap-3">
          <span>{{ audioDuration }}</span>
          <button
            class="text-gray-700 hover:text-gray-900 disabled:opacity-50 cursor-pointer disabled:cursor-default"
            @click="$emit('togglePlayback')"
            :disabled="!audioUrl || isRecordingActive"
          >
            <Play v-if="!isPlaying" class="w-5 h-5" />
            <Pause v-else class="w-5 h-5" />
          </button>
        </div>
      </div>
      
      <button
        v-if="showDeleteButton"
        class="text-gray-600 hover:text-red-500 cursor-pointer flex items-center justify-center disabled:opacity-50 disabled:hover:text-gray-600 disabled:cursor-default"
        @click="$emit('confirmDelete')"
        :disabled="isRecordingActive || !audioUrl"
      >
        <Trash2 class="w-5 h-5" />
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  audioUrl: String,
  isRecordingActive: Boolean,
  isPlaying: Boolean,
  audioDuration: String,
  showDeleteButton: {  
    type: Boolean,
    default: true 
  }
});

defineEmits(['togglePlayback', 'confirmDelete']);

import { Play, Pause, Trash2 } from "lucide-vue-next";
</script>