<template>
  <!-- DELETE THE ONE BELOW AND UNCOMMENT THIS:
   <RouterLink
    :to="`/viewmeeting/${meetingId}`" 
    class="w-64 p-4 rounded-2xl shadow-md flex flex-col gap-3 cursor-pointer bg-white border border-gray-100 hover:shadow-lg transition"
  > -->
  <RouterLink to="/viewmeeting"
    class="w-64 p-4 rounded-2xl shadow-md flex flex-col gap-3 cursor-pointer bg-white border border-gray-100 hover:shadow-lg transition"
  >
    <!-- Waveform image -->
    <div class="flex justify-center">
      <img
        :src="waveImage"
        alt="Waveform"
        class="w-full h-15 object-contain"
      />
    </div>

    <!-- Title + Delete icon -->
    <div class="flex items-center justify-between">
      <h2 class="font-semibold text-lg text-gray-800">{{ title }}</h2>
      <button
       @click.stop.prevent="$emit('delete')"
        class="text-gray-500 hover:text-red-500 transition-colors cursor-pointer"
        aria-label="Delete meeting"
      >
        <Trash2 class="w-5 h-5" />
      </button>
    </div>

    <!-- Details -->
    <div class="text-sm text-gray-600">
      <p>With {{ attendees.join(', ') }}</p>
      <p>{{ date }} , {{ time }}</p>
    </div>
  </RouterLink>
</template>

<script setup>
import { Trash2 } from "lucide-vue-next";

defineProps({
  //Uncomment this: meetingId: { type: [String, Number], required: true }
  title: { type: String },
  attendees: { type: Array },
  date: { type: String},
  time: { type: String },
  waveImage: { type: String },
});
</script>
