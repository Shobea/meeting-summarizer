<template>
  <div
    v-if="audioUrl"
    class="relative w-full h-48 bg-gray-200 rounded-2xl shadow-sm overflow-hidden"
    :class="{ 'opacity-50 pointer-events-none': isRecordingActive }"
  >
    <img
      :src="waveImage"
      alt="wave"
      class="object-contain w-full h-full pointer-events-none"
    />
    
    <!-- Progress overlay bg-->
    <div
      class="absolute top-0 left-0 h-full opacity-40 transition-all duration-200 pointer-events-none"
      :class="progressBgClass"
      :style="{ width: `${progressPercent}%` }"
    ></div>
    
    <div
      class="absolute inset-0 cursor-pointer"
      @click="$emit('seekAudio', $event)"
    ></div>
  </div>
  <div
    v-else
    class="w-full h-48 bg-gray-100 rounded-2xl shadow-sm flex flex-col items-center justify-center text-gray-500"
  >
    <svg class="w-12 h-12 mb-3 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path>
    </svg>
    <p class="text-lg font-medium">No recording available</p>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import waveOrange2 from "@/assets/waveOrange2.png";
import waveBlue2 from "@/assets/waveBlue2.png";
import waveGray2 from "@/assets/waveGray2.png";

const props = defineProps({
  audioUrl: String,
  isRecordingActive: Boolean,
  progressPercent: Number,
  waveImage: String
});

defineEmits(['seekAudio']);

// Compute the background class based on the wave image
const progressBgClass = computed(() => {
  if (props.waveImage === waveOrange2) {
    return 'bg-[var(--orange)]';
  } else if (props.waveImage === waveBlue2) {
    return 'bg-[var(--dblue)]';
  } else if (props.waveImage === waveGray2) {
    return 'bg-gray-400';
  }
  return 'bg-[var(--orange)]'; // Default fallback
});
</script>