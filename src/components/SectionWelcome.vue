<template>
  <div class="flex flex-col items-center pt-[50px] space-y-4">
    <!-- Greeting -->
    <h1 class="text-3xl font-bold font-inter">Hello, {{ username }}!</h1>

    <RouterLink to="/scanmeeting">
      <Button
        variant="default"
        class="bg-[var(--dblue)] cursor-pointer hover:bg-[var(--mblue)] text-white"
      >
        <span class="mr-2">+</span> Create New Meeting
      </Button>
    </RouterLink>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from "vue-router";
import { Button } from "@/components/ui/button"

const username = ref('Guest') // start empty

onMounted(async () => {
  try {
    // change logic here idk
    username.value = data.username
  } catch (error) {
    console.error('Failed to fetch username:', error)
    username.value = 'Guest' // fallback
  }
})
</script>
