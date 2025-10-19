<template>
  <div class="flex gap-3">
    <Button
      class="bg-[var(--mblue)] hover:bg-[var(--dblue)] text-white px-4 cursor-pointer disabled:cursor-default"
      @click="$emit('startRecording')"
      :disabled="isRecording || (isRecordingActive && !isPaused) || audioUrl"
    >
      <Play class="w-5 h-5 mr-1"/> Record
    </Button>
    <Button
      class="bg-gray-400 hover:bg-gray-500 text-white px-4 cursor-pointer disabled:cursor-default"
      @click="$emit('pauseRecording')"
      :disabled="!isRecording"
    >
      <Pause class="w-5 h-5 mr-1" /> Pause
    </Button>
    <Button
      class="bg-[var(--orange)] hover:bg-orange-500 text-white px-4 cursor-pointer disabled:cursor-default"
      @click="$emit('confirmStopRecording')"
      :disabled="!isRecordingActive"
    >
      <Square class="w-5 h-5 mr-1" /> Stop
    </Button>
  </div>
</template>

<script setup>
defineProps({
  isRecording: Boolean,
  isRecordingActive: Boolean,
  isPaused: Boolean,
  audioUrl: String
});

defineEmits(['startRecording', 'pauseRecording', 'confirmStopRecording']);

import { Button } from "@/components/ui/button";
import { Play, Pause, Square } from "lucide-vue-next";
</script>