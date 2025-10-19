<template>
  <div>
    <Navbar />

    <div class="min-h-screen bg-white flex flex-col justify-center items-center py-10 px-6">
      <div class="max-w-6xl w-full grid grid-cols-1 lg:grid-cols-2 gap-12">
        <!-- LEFT SIDE -->
        <div class="flex flex-col items-center space-y-6">
          <!-- Recording Section -->
          <div class="w-full">
            <WaveformDisplay
              :audio-url="audioUrl"
              :is-recording-active="isRecordingActive"
              :progress-percent="progressPercent"
              :wave-image="waveBlue"
              @seek-audio="seekAudio"
            />

            <AudioControls
              :audio-url="audioUrl"
              :is-recording-active="isRecordingActive"
              :is-playing="isPlaying"
              :audio-duration="audioDuration"
              :show-delete-button="false"
              @toggle-playback="togglePlayback"
            />
          </div>
        </div>

        <!-- RIGHT SIDE -->
        <div class="flex flex-col space-y-4">
          <div>
            <!-- Meeting Info -->
            <h1 class="text-3xl font-bold mb-2">{{ meeting.name || "Meeting Title" }}</h1>
            <p class="text-gray-700 mb-4">
              {{ meeting.description || "Meeting description goes here..." }}
            </p>

            <!-- Meeting Details -->
            <div class="flex justify-between text-sm text-gray-800">
              <div>
                <p class="font-semibold">Meeting with:</p>
                <p v-for="(student, index) in attendees" :key="index">
                  {{ student.name }} : {{ student.school_ID }}
                </p>
              </div>
              <div class="text-right">
                <p class="font-semibold">Date:</p>
                <p>{{ meeting.date || "DD/MM/YY" }}</p>
                <p>{{ meeting.time || "00:00 AM" }}</p>
              </div>
            </div>
          </div>

          <!-- Summary Section -->
          <div class="mt-4">
            <h2 class="font-semibold mb-2">Summary</h2>
            <p class="text-gray-700 mb-2">
              {{ summaryText || "Summary will appear here once available." }}
            </p>
          </div>

          <!-- Go Back Button -->
          <div class="flex justify-end pt-8">
            <RouterLink to="/meetings">
              <Button class="bg-[#8CBED6] hover:bg-[#7BB1CA] text-white font-medium px-6">
                Go Back
              </Button>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import WaveformDisplay from "@/components/SectionWaveForm.vue";
import AudioControls from "@/components/AudioControls.vue";
import { Button } from "@/components/ui/button";
import Navbar from "@/components/Navbar.vue";
import waveBlue from "@/assets/waveBlue2.png";

const route = useRoute();
const meeting = ref({});
const attendees = ref([]);
const audioUrl = ref(null);
const summaryText = ref("");
const isPlaying = ref(false);
const isRecordingActive = ref(false);
const progressPercent = ref(0);
const audioDuration = ref("00:00");

// Fetch meeting details
onMounted(async () => {
  const meetingId = route.params.id;
  console.log("Fetching data for meeting:", meetingId);

  // ADD LOGIC HERE
});

// Audio controls
function togglePlayback() {
  // ADD LOGIC HERE
  console.log("Toggling playback...");
}

function seekAudio() {
  // ADD LOGIC HERE
  console.log("Seeking audio...");
}

</script>
