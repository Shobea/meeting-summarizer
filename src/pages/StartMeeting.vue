<template>
  <div class="min-h-screen flex flex-col justify-center items-center bg-white px-6 py-10">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 w-full max-w-6xl items-start">
      <!-- LEFT SECTION -->
      <div class="flex flex-col space-y-6">
        <WaveformDisplay
          :audio-url="audioUrl"
          :is-recording-active="isRecordingActive"
          :progress-percent="progressPercent"
          :wave-image="meetingData.waveImage"
          @seek-audio="seekAudio"
        />

        <AudioControls
          :audio-url="audioUrl"
          :is-recording-active="isRecordingActive"
          :is-playing="isPlaying"
          :audio-duration="audioDuration"
          @toggle-playback="togglePlayback"
          @confirm-delete="confirmDelete"
        />
      </div>

      <!-- RIGHT SECTION -->
      <div class="flex flex-col justify-between h-full space-y-6">
        <div>
          <h1 class="text-3xl font-bold mb-2">{{ meetingData.meetingName }}</h1>

          <MeetingHeader
            :formatted-time="formattedTime"
            :is-recording="isRecording"
            :is-recording-active="isRecordingActive"
            :is-paused="isPaused"
            :audio-url="audioUrl"
            :meeting-data="meetingData"
            @start-recording="startRecording"
            @pause-recording="pauseRecording"
            @confirm-stop-recording="confirmStopRecording"
            @confirm-end-meeting="confirmEndMeeting"
          />
        </div>
      </div>
    </div>

    <!-- POPUPS -->
    <Popup
      v-if="showDeletePopup"
      v-model="showDeletePopup"
      type="orange"
      :data="{
        image: trashImage,
        title: 'Delete Recording?',
        description: 'Are you sure you want to delete this recording?',
        confirmText: 'Delete',
        cancelText: 'Nevermind'
      }"
      @submit="deleteRecording"
    />

    <Popup
      v-if="showStopPopup"
      v-model="showStopPopup"
      type="orange"
      :data="{
        image: stopImage,
        title: 'Stop Recording?',
        description: `Once you stop, this meeting's recording will be saved, and you won't be able to record more.`,
        confirmText: 'Yes, stop it',
        cancelText: 'Nevermind'
      }"
      @submit="stopRecording"
      @update:model-value="handleStopPopupClose"
    />

    <Popup
      v-if="showEndMeetingPopup"
      v-model="showEndMeetingPopup"
      type="orange"
      :data="{
        image: speechImage,
        title: 'End Meeting?',
        description: `Ending will save and summarize the meeting. You won't be able to return to this session.`,
        confirmText: 'Yes, end it',
        cancelText: 'Nevermind'
      }"
      @submit="endMeeting"
    />

    <!-- Processing Overlay -->
    <div
      v-if="isProcessing"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-2xl p-8 flex flex-col items-center gap-4 shadow-xl max-w-sm mx-4">
        <div class="w-12 h-12 border-4 border-[#8CBED6] border-t-transparent rounded-full animate-spin"></div>
        <h3 class="text-xl font-semibold text-gray-800">Processing Meeting</h3>
        <p class="text-gray-600 text-center text-sm">
          Transcribing audio and generating summary...
          <br />
          This may take a moment.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { v4 as uuidv4 } from "uuid";

import WaveformDisplay from '@/components/SectionWaveForm.vue';
import AudioControls from '@/components/AudioControls.vue';
import MeetingHeader from '@/components/SectionMeeting.vue';
import Popup from '@/components/Popup.vue';

import { processMeeting } from '@/services/api';

import trashImage from "@/assets/trash.png";
import stopImage from "@/assets/stopRecording2.png";
import speechImage from "@/assets/speech.png";

const route = useRoute();
const router = useRouter();

const meetingData = ref({
  meetingID: uuidv4(),
  waveImage: '',
  meetingName: 'Meeting',
  meetingDescription: '',
  students: [],
  waveImageName: '',
  date: new Date().toLocaleDateString(),
  time: new Date().toLocaleTimeString()
});

// Get meeting data from previous page
onMounted(() => {
  if (route.query.meetingData) {
    try {
      meetingData.value = { ...meetingData.value, ...JSON.parse(route.query.meetingData) };
      console.log('Loaded meeting data:', meetingData.value);
    } catch (e) {
      console.error('Error parsing meeting data:', e);
    }
  }
});

// States
const isRecording = ref(false);
const isRecordingActive = ref(false);
const isPaused = ref(false);
const isPlaying = ref(false);
const time = ref(0);
const progressPercent = ref(0);
const audioUrl = ref(null);
const audioDuration = ref("0:00");
let audio = null;
let timerInterval = null;
const mediaRecorder = ref(null);
const audioChunks = ref([]);

const showDeletePopup = ref(false);
const showStopPopup = ref(false);
const showEndMeetingPopup = ref(false);
const isProcessing = ref(false);
const processingError = ref(null);

const formattedTime = computed(() => {
  const m = Math.floor(time.value / 60).toString().padStart(2, "0");
  const s = (time.value % 60).toString().padStart(2, "0");
  return `${m}:${s}`;
});

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder.value = new MediaRecorder(stream);
    audioChunks.value = [];

    mediaRecorder.value.ondataavailable = (e) => {
      audioChunks.value.push(e.data);
    };

    mediaRecorder.value.onstop = () => {
      const blob = new Blob(audioChunks.value, { type: "audio/webm" });
      audioUrl.value = URL.createObjectURL(blob);
      setupAudioElement();
      audioDuration.value = formattedTime.value;
      isPaused.value = false;
    };

    mediaRecorder.value.start();
    isRecording.value = true;
    isRecordingActive.value = true;
    isPaused.value = false;
    timerInterval = setInterval(() => time.value++, 1000);
  } catch (err) {
    console.error("Mic access error:", err);
    alert("Microphone access denied.");
  }
}

function pauseRecording() {
  if (mediaRecorder.value && mediaRecorder.value.state === "recording") {
    mediaRecorder.value.pause();
    isRecording.value = false;
    isPaused.value = true;
    clearInterval(timerInterval);
  }
}

function confirmStopRecording() {
  if (mediaRecorder.value && mediaRecorder.value.state === "recording") {
    mediaRecorder.value.pause();
    isRecording.value = false;
    isPaused.value = true;
    clearInterval(timerInterval);
  }
  showStopPopup.value = true;
}

function stopRecording() {
  showStopPopup.value = false;
  if (mediaRecorder.value && mediaRecorder.value.state !== "inactive") {
    mediaRecorder.value.stop();
    isRecording.value = false;
    isRecordingActive.value = false;
    isPaused.value = false;
    setTimeout(() => (time.value = 0), 300);
  }
}

function handleStopPopupClose() {
  showStopPopup.value = false;
  if (mediaRecorder.value && mediaRecorder.value.state === "paused") {
    mediaRecorder.value.resume();
    isRecording.value = true;
    isPaused.value = false;
    timerInterval = setInterval(() => time.value++, 1000);
  }
}

function setupAudioElement() {
  if (audio) audio.pause();
  audio = new Audio(audioUrl.value);

  audio.addEventListener("timeupdate", () => {
    if (audio.duration) {
      progressPercent.value = (audio.currentTime / audio.duration) * 100;
    }
  });

  audio.addEventListener("ended", () => {
    isPlaying.value = false;
    progressPercent.value = 100;
  });
}

function togglePlayback() {
  if (!audio) return;
  if (isPlaying.value) audio.pause();
  else audio.play();
  isPlaying.value = !isPlaying.value;
}

function seekAudio(event) {
  if (!audio || isRecordingActive.value) return;
  const rect = event.currentTarget.getBoundingClientRect();
  const clickX = event.clientX - rect.left;
  const percent = clickX / rect.width;
  audio.currentTime = percent * audio.duration;
  progressPercent.value = percent * 100;
}

function confirmDelete() {
  showDeletePopup.value = true;
}

function deleteRecording() {
  showDeletePopup.value = false;
  progressPercent.value = 0;
  time.value = 0;
  isPlaying.value = false;
  audioUrl.value = null;
  audioDuration.value = "0:00";
  isRecordingActive.value = false;
  isPaused.value = false;
  if (audio) audio.pause();
}

function confirmEndMeeting() {
  showEndMeetingPopup.value = true;
}

async function endMeeting() {
  showEndMeetingPopup.value = false;
  clearInterval(timerInterval);
  if (audio) audio.pause();

  // Process the meeting recording with ML models
  isProcessing.value = true;
  processingError.value = null;
  
  let transcription = "";
  let summary = "";
  let detectedLanguage = "";

  try {
    // Get the audio blob from recorded chunks
    if (audioChunks.value.length > 0) {
      const audioBlob = new Blob(audioChunks.value, { type: "audio/webm" });
      
      console.log("Processing meeting recording...");
      const result = await processMeeting(audioBlob);
      
      transcription = result.transcription || "";
      summary = result.summary || "";
      detectedLanguage = result.language || "";
      
      console.log("Meeting processed successfully:", result);
    }
  } catch (error) {
    console.error("Error processing meeting:", error);
    processingError.value = error.message || "Failed to process meeting";
    // Continue saving even if processing fails
  } finally {
    isProcessing.value = false;
  }

  // Save meeting data with transcription and summary
  const dataToSave = {
    meetingID: meetingData.value.meetingID,
    name: meetingData.value.meetingName,
    description: meetingData.value.meetingDescription,
    students: meetingData.value.students,
    audio: audioUrl.value,
    waveImage: meetingData.value.waveImage,
    date: meetingData.value.date,
    time: meetingData.value.time,
    transcription: transcription,
    summary: summary,
    language: detectedLanguage
  };

  // Save to database
  await saveMeetingToDatabase(dataToSave);

  router.push("/meetings");
}

async function saveMeetingToDatabase(data) {
  try {
    // Add logic
    console.log("Saving to backend (placeholder):", data);
  } catch (err) {
    console.error("Error saving meeting:", err);
  }
}

onUnmounted(() => {
  clearInterval(timerInterval);
  if (audio) audio.pause();
});
</script>
