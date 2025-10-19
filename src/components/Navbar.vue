<template> 
  <nav class="w-full flex items-center justify-between px-6 py-4 bg-white shadow-sm relative">
    <!-- Left -->
    <div class="text-base font-medium text-gray-800 cursor-pointer">
      Mapua Malayan Colleges Mindanao
    </div>

    <!-- Right -->
    <div class="hidden md:flex items-center space-x-8 text-gray-700 font-medium">
      <RouterLink
        to="/settings"
        class="hover:text-[var(--dblue)] transition-colors flex items-center"
        title="Settings"
      >
        <Settings class="w-5 h-5 mr-1" />
      </RouterLink>

      <RouterLink to="/howto" class="hover:text-[var(--dblue)] transition-colors">How to</RouterLink>
      <RouterLink to="/meetings" class="hover:text-[var(--dblue)] transition-colors">Meetings</RouterLink>
      <RouterLink to="/" class="hover:text-[var(--dblue)] transition-colors">Home</RouterLink>

      <!-- Desktop login button -->
      <Button
        class="bg-[var(--dblue)] hover:bg-[var(--mblue)] cursor-pointer text-white rounded-lg"
        @click="openLoginPopup"
      >
        Login
      </Button>
    </div>

    <!-- Mobile menu button -->
    <Button
      variant="ghost"
      size="icon"
      @click="isOpen = !isOpen"
      class="md:hidden text-gray-700 hover:text-[var(--dblue)]"
    >
      <Menu v-if="!isOpen" class="w-6 h-6" />
      <X v-else class="w-6 h-6" />
    </Button>

    <!-- Mobile dropdown menu -->
    <div
      v-if="isOpen"
      class="absolute top-full left-0 w-full bg-white shadow-md border-t md:hidden flex flex-col items-center space-y-4 py-4"
    >
      <!-- Settings mobile -->
      <RouterLink
        to="/settings"
        class="hover:text-[var(--dblue)] transition-colors flex items-center"
        @click="isOpen = false"
      >
         Settings
      </RouterLink>

      <RouterLink to="/howto" class="hover:text-[var(--dblue)] transition-colors" @click="isOpen = false">
        How to
      </RouterLink>
      <RouterLink to="/meetings" class="hover:text-[var(--dblue)] transition-colors" @click="isOpen = false">
        Meetings
      </RouterLink>
      <RouterLink to="/" class="hover:text-[var(--dblue)] transition-colors" @click="isOpen = false">
        Home Page
      </RouterLink>

      <!-- Mobile login button -->
      <Button
        class="w-[90%] text-white font-medium cursor-pointer bg-[var(--dblue)] hover:bg-[color-mix(in srgb, var(--dblue) 85%, black)] rounded-lg"
        @click="() => { isOpen = false; openLoginPopup() }"
      >
        Login
      </Button>
    </div>
  </nav>

  <!-- Login popup -->
  <Popup
    v-model="showPopup"
    :type="popupType"
    :data="popupData"
    @submit="handleSubmit"
    @switch="handleSwitch"
  />
</template>

<script setup>
import { ref } from "vue"
import { Button } from "@/components/ui/button"
import { Menu, X, Settings } from "lucide-vue-next"
import Popup from "@/components/Popup.vue"

// states
const isOpen = ref(false)
const showPopup = ref(false)
const popupType = ref("login")
const popupData = ref({ username: "", password: "", email: "" })

const openLoginPopup = () => {
  popupType.value = "login"
  popupData.value = { username: "", password: "" }
  showPopup.value = true
}

const handleSubmit = (data) => {
  console.log("User submitted:", popupType.value, data)
  showPopup.value = false
}

const handleSwitch = (type) => {
  popupType.value = type
  popupData.value = { username: "", password: "", email: "" }
}
</script>
