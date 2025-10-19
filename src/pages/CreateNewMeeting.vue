<template>
  <div class="min-h-screen flex flex-col justify-center items-center bg-white px-8 py-10">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-5xl items-start">
      <!-- LEFT SECTION -->
      <div class="flex flex-col space-y-6">

        <div class="relative bg-gray-200 rounded-2xl shadow-sm w-full h-48 flex items-center justify-center">
          <img :src="selectedWave" alt="wave" class="object-contain w-3/4" />

          <!-- Edit icon -->
          <button
            class="absolute top-3 right-3 text-gray-700 hover:text-gray-900"
            @click="showWavePicker = !showWavePicker"
          >
            <Pencil class="w-5 h-5" />
          </button>

          <!-- Wave picker -->
          <div
            v-if="showWavePicker"
            class="absolute top-12 right-3 bg-white shadow-md rounded-lg p-3 flex gap-3 z-10"
          >
            <img
              v-for="(wave, index) in waveOptions"
              :key="index"
              :src="wave"
              @click="selectWave(wave)"
              class="w-16 h-10 object-contain rounded-md border-2 border-transparent hover:border-blue-400 cursor-pointer transition"
            />
          </div>
        </div>

        <!-- Meeting with list -->
        <div>
          <p class="font-semibold mb-2">Meeting with:</p>
          <ul class="text-gray-700 text-sm space-y-1">
            <li v-for="(student, index) in scannedStudents" :key="index">
              {{ student.name }} : {{ student.id }}
            </li>
            <li v-if="scannedStudents.length === 0" class="text-gray-500 italic">
              No students added yet
            </li>
          </ul>
        </div>
      </div>

      <!-- RIGHT SECTION -->
      <div class="flex flex-col justify-between h-full space-y-6">
        <!-- Meeting Info -->
        <div>
          <!-- Editable title -->
          <div class="flex items-center mb-2">
            <input
              v-if="editingTitle"
              v-model="meetingTitle"
              class="border-b-2 border-gray-400 outline-none text-5xl font-bold w-2/3"
              @blur="editingTitle = false"
              autofocus
            />
            <h1 v-else class="text-5xl font-bold">{{ meetingTitle }}</h1>
            <button
              class="ml-2 text-gray-600 hover:text-gray-900"
              @click="editingTitle = true"
            >
              <Pencil class="w-5 h-5" />
            </button>
          </div>

          <label class="block font-semibold mt-3">Description</label>
          <textarea
            v-model="meetingDescription"
            rows="3"
            class="bg-gray-200 rounded-lg w-full p-3 mt-1 outline-none shadow-inner"
          ></textarea>
        </div>

        <!-- Buttons -->
        <div class="flex justify-between w-full mt-auto pt-6">
          <RouterLink to="/scan">
            <Button class="bg-[#8CBED6] hover:bg-[#7BB1CA] text-white font-medium px-6">
              Go Back
            </Button>
          </RouterLink>

          <Button 
            class="bg-[#8CBED6] hover:bg-[#7BB1CA] text-white font-medium px-6"
            @click="startMeeting"
          >
            Start Meeting
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Button } from "@/components/ui/button";
import { Pencil } from "lucide-vue-next";

import waveBlue2 from "@/assets/waveBlue2.png";
import waveGray2 from "@/assets/waveGray2.png";
import waveOrange2 from "@/assets/waveOrange2.png";

const route = useRoute();
const router = useRouter();

// Get the scanned data from route state
const scannedStudents = computed(() => {
  try {
    return JSON.parse(route.query.data || '[]')
  } catch (e) {
    return []
  }
});

const waveOptions = [waveOrange2, waveBlue2, waveGray2];
const selectedWave = ref(waveOrange2);
const showWavePicker = ref(false);
const meetingTitle = ref("Meeting 1");
const meetingDescription = ref("");
const editingTitle = ref(false);

function selectWave(wave) {
  selectedWave.value = wave;
  showWavePicker.value = false;
}

function startMeeting() {
  // Prepare meeting data to pass
  const meetingData = {
    waveImage: selectedWave.value,
    meetingName: meetingTitle.value,
    meetingDescription: meetingDescription.value,
    students: scannedStudents.value,
    waveImageName: getWaveImageName(selectedWave.value)
  };

  // Navigate to StartMeeting with data
  router.push({
    path: '/startmeeting',
    query: {
      meetingData: JSON.stringify(meetingData)
    }
  });
}

function getWaveImageName(wave) {
  if (wave === waveOrange2) return 'waveOrange2';
  if (wave === waveBlue2) return 'waveBlue2';
  if (wave === waveGray2) return 'waveGray2';
  return 'waveOrange2';
}
</script>
