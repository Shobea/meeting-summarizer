<template>
  <div
    v-if="modelValue"
    class="fixed inset-0 flex items-center justify-center bg-black/40 z-50"
  >
    <div class="bg-white rounded-2xl shadow-xl p-8 w-[90%] max-w-lg relative">
      <button
        @click="$emit('update:modelValue', false)"
        class="absolute top-3 right-3 text-gray-400 hover:text-gray-600"
      >
        ✕
      </button>

      <!-- Orange popup -->
      <div v-if="type === 'orange'" class="flex flex-col items-center text-center space-y-4">
        <img v-if="data?.image" :src="data.image" alt="popup image" class="w-auto h-40" />
        <h2 class="text-xl font-semibold">{{ data?.title }}</h2>
        <p class="text-gray-600">{{ data?.description }}</p>
        <button
          class="bg-[var(--orange)] hover:bg-orange-500 text-white w-32 rounded-md py-2 cursor-pointer"
          @click="$emit('submit')"
        >
          {{ data?.confirmText || 'Confirm' }}
        </button>
        <button
          class="text-gray-500 text-sm hover:underline cursor-pointer"
          @click="$emit('update:modelValue', false)"
        >
          {{ data?.cancelText || 'Nevermind' }}
        </button>
      </div>

      <!-- Blue popup -->
      <div v-else-if="type === 'blue'" class="flex flex-col items-center text-center space-y-4">
        <img v-if="data?.image" :src="data.image" alt="popup image" class="w-24 h-24" />
        <h2 class="text-xl font-semibold">{{ data?.title }}</h2>
        <p class="text-gray-600">{{ data?.description }}</p>
        <button
          class="bg-[var(--dblue)] hover:bg-[var(--mblue)] text-white w-40 rounded-md py-2"
          @click="$emit('submit')"
        >
          {{ data?.confirmText || 'Continue' }}
        </button>
      </div>

      <!-- Login -->
      <div v-else-if="type === 'login'" class="space-y-6">
        <h2 class="text-2xl font-bold text-left">Log In</h2>
        <div class="space-y-4">
          <div>
            <label class="font-semibold text-gray-700">Username</label>
            <input
              v-model="form.username"
              type="text"
              class="w-full mt-1 p-2 rounded-md bg-gray-100 shadow-inner outline-none"
            />
          </div>
          <div>
            <label class="font-semibold text-gray-700">Password</label>
            <input
              v-model="form.password"
              type="password"
              class="w-full mt-1 p-2 rounded-md bg-gray-100 shadow-inner outline-none"
            />
          </div>
          <div class="flex justify-center pt-2">
            <button
              class="bg-[var(--dblue)] hover:bg-[var(--mblue)] text-white w-32 rounded-md py-2 cursor-pointer"
              @click="handleLogin"
            >
              Log In
            </button>
          </div>
          <p
            class="text-center text-sm text-gray-600 cursor-pointer hover:underline"
            @click="$emit('switch', 'signup')"
          >
            I want to create an account
          </p>
        </div>
      </div>

      <!-- Signup popup -->
      <div v-else-if="type === 'signup'" class="space-y-6">
        <h2 class="text-2xl font-bold text-left">Sign Up</h2>
        <form @submit.prevent="onSignupSubmit" class="space-y-4">

          <FormField v-slot="{ componentField, errorMessage }" name="username">
            <div>
              <label class="font-semibold text-gray-700">Username</label>
              <input
                v-bind="componentField"
                type="text"
                placeholder="Enter username"
                class="w-full mt-1 p-2 rounded-md bg-gray-100 shadow-inner outline-none"
              />
              <p v-if="errorMessage" class="text-sm text-red-500 mt-1">{{ errorMessage }}</p>
            </div>
          </FormField>

          <FormField v-slot="{ componentField, errorMessage }" name="email">
            <div>
              <label class="font-semibold text-gray-700">Email</label>
              <input
                v-bind="componentField"
                type="email"
                placeholder="Enter email"
                class="w-full mt-1 p-2 rounded-md bg-gray-100 shadow-inner outline-none"
              />
              <p v-if="errorMessage" class="text-sm text-red-500 mt-1">{{ errorMessage }}</p>
            </div>
          </FormField>

          <FormField v-slot="{ componentField, errorMessage }" name="password">
            <div>
              <label class="font-semibold text-gray-700">Password</label>
              <input
                v-bind="componentField"
                type="password"
                placeholder="Enter password"
                class="w-full mt-1 p-2 rounded-md bg-gray-100 shadow-inner outline-none"
              />
              <p v-if="errorMessage" class="text-sm text-red-500 mt-1">{{ errorMessage }}</p>
            </div>
          </FormField>

          <div class="flex justify-center pt-2">
            <button
              type="submit"
              class="bg-[var(--dblue)] hover:bg-[var(--mblue)] text-white w-40 rounded-md py-2 cursor-pointer"
            >
              Create Account
            </button>
          </div>
        </form>

        <p
          class="text-center text-sm text-gray-600 cursor-pointer hover:underline"
          @click="$emit('switch', 'login')"
        >
          Go back to log in page
        </p>
      </div>

      <!-- Logout -->
      <div v-else-if="type === 'logout'" class="flex flex-col items-center text-center space-y-6">
        <h2 class="text-2xl font-bold">Are you sure you want to log out?</h2>
        <div class="flex gap-4">
          <button
            class="bg-[#9BD3E5] hover:bg-[#87c4d8] text-white font-medium py-2 px-6 rounded-md"
            @click="$emit('update:modelValue', false)"
          >
            Cancel
          </button>
          <button
            class="bg-[var(--orange)] hover:bg-orange-500 text-white font-medium py-2 px-6 rounded-md"
            @click="$emit('submit')"
          >
            Log out
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue"
import { toast } from "vue-sonner"
import { z } from "zod"
import { useForm } from "vee-validate"
import { toTypedSchema } from "@vee-validate/zod"
import {  FormField } from "@/components/ui/form"

const props = defineProps({
  modelValue: Boolean,
  type: { type: String, default: "orange" },
  data: Object,
})
const emit = defineEmits(["update:modelValue", "submit", "switch"])

const form = ref({ username: "", password: "", email: "" })

// Reset form when popup opens
watch(() => props.modelValue, (val) => {
  if (val) form.value = { username: "", password: "", email: "" }
})

//  Login (add logic)
const handleLogin = () => {
  if (!form.value.username || !form.value.password) {
    toast.error("Please fill in both fields.")
    return
  }
  toast.success(`Welcome back, ${form.value.username}!`)
  emit("submit", { ...form.value })
  emit("update:modelValue", false)
}

// Signup validation
const signupSchema = toTypedSchema(
  z.object({
    username: z.string().min(3, "Username must be at least 8 characters."),
    email: z.string().email("Invalid email address."),
    password: z.string().min(6, "Password must be at least 8 characters."),
  })
)

const { handleSubmit } = useForm({ validationSchema: signupSchema })

// Signup (add logic)
const onSignupSubmit = handleSubmit((values) => {
  toast.success(`Account created! Welcome, ${values.username}!`)
  emit("submit", values)
  emit("update:modelValue", false)
})
</script>
