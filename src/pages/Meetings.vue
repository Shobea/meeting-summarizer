<template>
  <NavBar />
  <SectionWelcome />

  <!-- Completed Meetings Section -->
  <section class="mt-10 flex justify-center">
    <div class="w-full max-w-6xl px-6">
      <h2 class="font-semibold text-lg mb-4">Completed Meetings</h2>

      <!-- Meeting Cards Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 justify-items-center"
>

        <!-- UNCOMMENT THIS AND REPLACE WITH THE ONE BELOW (not sure with this but if there's something lacking here, edit MeetingCard.vue first)
         <MeetingCard
            v-for="(meeting, index) in meetings"
            :key="meeting.UniqueID"
            :meetingId="meeting.UniqueID"
            :title="meeting.name"
            :attendees="meeting.attendees"
            :date="meeting.date"
            :time="meeting.time"
            :waveImage="getWaveImage(index)"
            @delete="openDeletePopup(index)"
          />
        -->

        <MeetingCard
          v-for="(meeting, index) in displayedMeetings"
          :key="index"
          :title="meeting.title"
          :attendees="meeting.attendees"
          :date="meeting.date"
          :time="meeting.time"
          :wave-image="getWaveImage(index)"
          @delete="openDeletePopup(index)"
        />
      </div>

      <!-- More / Show Less Button -->
      <div class="flex justify-center mt-6">
        <button
          class="text-sm text-gray-500 hover:text-gray-700 transition-colors cursor-pointer"
          @click="toggleShowMore"
          v-if="meetings.length > 9"
        >
          {{ showAll ? "Show less" : "More" }}
        </button>
      </div>
    </div>
  </section>

  <Popup
    v-if="showPopup"
    v-model="showPopup"
    type="orange"
    :data="popupData"
    @submit="confirmDelete"
  />
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import NavBar from "@/components/Navbar.vue";
import SectionWelcome from "@/components/SectionWelcome.vue";
import MeetingCard from "@/components/MeetingCard.vue";
import Popup from "@/components/Popup.vue";

import waveOrange2 from "@/assets/waveOrange2.png";
import waveBlue2 from "@/assets/waveBlue2.png";
import waveGray2 from "@/assets/waveGray2.png";
import trashImage from "@/assets/trash.png";

// Static data, replace with db stuff
const meetings = ref([
  { title: "Meeting 1", attendees: ["Student1", "Student2", "Student3"], date: "01/01/25", time: "9AM" },
  { title: "Meeting 2", attendees: ["Student1", "Student2"], date: "02/01/25", time: "10AM" },
  { title: "Meeting 3", attendees: ["Student1", "Student2", "Student3"], date: "03/01/25", time: "11AM" },
  { title: "Meeting 4", attendees: ["Student1"], date: "04/01/25", time: "9AM" },
  { title: "Meeting 5", attendees: ["Student1", "Student2"], date: "05/01/25", time: "10AM" },
  { title: "Meeting 6", attendees: ["Student1", "Student2", "Student3"], date: "06/01/25", time: "11AM" },
  { title: "Meeting 7", attendees: ["Student1"], date: "07/01/25", time: "9AM" },
  { title: "Meeting 8", attendees: ["Student1", "Student2"], date: "08/01/25", time: "10AM" },
  { title: "Meeting 9", attendees: ["Student1", "Student2", "Student3"], date: "09/01/25", time: "11AM" },
  { title: "Meeting 10", attendees: ["Student1", "Student2"], date: "10/01/25", time: "1PM" },
  { title: "Meeting 11", attendees: ["Student1"], date: "11/01/25", time: "2PM" },
]);

const showAll = ref(false);
const showPopup = ref(false);
const selectedIndex = ref(null);

// Display only first 9 by default, change if you want
const displayedMeetings = computed(() =>
  showAll.value ? meetings.value : meetings.value.slice(0, 9)
);

// Popup content, change if you want
const popupData = ref({
  title: "Delete this meeting?",
  description: "Are you sure you want to delete this meeting? This action cannot be undone.",
  confirmText: "Yes, delete",
  cancelText: "Nevermind",
  image: trashImage,
});

function openDeletePopup(index) {
  selectedIndex.value = index;
  showPopup.value = true;
}

// Wave color logic, DELETE LATER, replace with actual image stored in db
function getWaveImage(index) {
  const position = (index + 1) % 3;
  if (position === 1) return waveOrange2;
  if (position === 2) return waveBlue2;
  return waveGray2;
}

// Delete logic
function confirmDelete() {
  if (selectedIndex.value !== null) {
    // Tester, delete below
    meetings.value.splice(selectedIndex.value, 1);

    //ADD LOGIC HERE
  }

  showPopup.value = false;
  selectedIndex.value = null;
}

// Toggle more or show less
function toggleShowMore() {
  showAll.value = !showAll.value;
}

// Fetch meetings from db
onMounted(async () => {
 //ADD LOGIC HERE
});
</script>
