<template>
  <div>
    <p class="font-semibold mb-2">Recording:</p>
    
    <!-- Timer Box -->
    <div class="bg-gray-200 rounded-xl shadow-sm w-full h-20 flex items-center justify-center text-3xl font-semibold mb-4">
      {{ formattedTime }}
    </div>
    
    <RecordingControls
      :is-recording="isRecording"
      :is-recording-active="isRecordingActive"
      :is-paused="isPaused"
      :audio-url="audioUrl"
      @start-recording="$emit('startRecording')"
      @pause-recording="$emit('pauseRecording')"
      @confirm-stop-recording="$emit('confirmStopRecording')"
    />
    
    <!-- End meeting button -->
    <div class="flex justify-end w-full mt-8 pt-8">
      <button
        class="bg-[var(--orange)] hover:bg-orange-500 text-white font-medium px-6 py-2 rounded cursor-pointer disabled:opacity-50 disabled:cursor-default disabled:hover:bg-[var(--orange)]"
        @click="$emit('confirmEndMeeting')"
        :disabled="!audioUrl"
      >
        End Meeting
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  formattedTime: String,
  isRecording: Boolean,
  isRecordingActive: Boolean,
  isPaused: Boolean,
  audioUrl: String
});

defineEmits(['startRecording', 'pauseRecording', 'confirmStopRecording', 'confirmEndMeeting']);

import RecordingControls from './RecordingControls.vue';
</script>