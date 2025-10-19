<template>
  <Navbar />

  <div class="min-h-screen flex flex-col bg-white px-8 py-10">
    <h1 class="font-bold text-5xl mb-10 pl-20">Settings</h1>

    <div class="flex justify-center w-full">
      <div class="w-full max-w-md">
        <h2 class="text-2xl font-bold mb-6 text-left">Account</h2>

        <!-- Username -->
        <div class="mb-5">
          <label class="block text-gray-800 text-sm font-semibold mb-1">Username</label>
          <input
            v-model="username"
            type="text"
            class="w-full p-3 rounded-full bg-gray-100 shadow-inner outline-none"
          />
        </div>

        <!-- Email -->
        <div class="mb-5">
          <label class="block text-gray-800 text-sm font-semibold mb-1">Email</label>
          <input
            v-model="email"
            type="email"
            class="w-full p-3 rounded-full bg-gray-100 shadow-inner outline-none"
          />
        </div>

        <!-- Password -->
        <div class="mb-8">
          <label class="block text-gray-800 text-sm font-semibold mb-1">Password</label>
          <div class="relative">
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              class="w-full p-3 rounded-full bg-gray-100 shadow-inner outline-none pr-10"
            />
            <button
              type="button"
              class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-600 hover:text-blue-600"
              @click="togglePassword"
            >
              <component :is="showPassword ? EyeOff : Eye" class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- Save Changes -->
        <div class="mb-5">
          <button
            class="w-full bg-[#9BD3E5] hover:bg-[#87c4d8] text-white font-medium py-3 rounded-md"
            @click="saveChanges"
          >
            Save Changes
          </button>
        </div>

        <!-- Logout -->
        <div class="text-center">
          <button
            class="text-red-500 font-medium hover:underline"
            @click="showLogoutPopup = true"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Logout confirmation popup -->
  <Popup
    v-model="showLogoutPopup"
    :data="logoutPopupData"
    type="logout"
    @submit="handleLogout"
  />
</template>

<script setup>
import { ref, onMounted } from "vue"
import { Eye, EyeOff } from "lucide-vue-next"
import Navbar from "@/components/Navbar.vue"
import Popup from "@/components/Popup.vue"
import { useRouter } from "vue-router"
import { toast } from "vue-sonner"

const router = useRouter()
const username = ref("")
const email = ref("")
const password = ref("")
const showPassword = ref(false)
const togglePassword = () => (showPassword.value = !showPassword.value)

const showLogoutPopup = ref(false)
const logoutPopupData = ref({
  title: "Are you sure you want to log out?",
  confirmText: "Log out",
  cancelText: "Cancel",
})

// Fetch user details from db
onMounted(async () => {
  // ADD LOGIC
})

async function saveChanges() {
  // ADD LOGIC

  toast.success("Changes saved!")
}

async function handleLogout() {
  // ADD LOGIC
  showLogoutPopup.value = false
  setTimeout(() => router.push({ name: "Home" }))
}
</script>
