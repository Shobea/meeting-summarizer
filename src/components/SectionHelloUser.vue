<template>
  <section class="flex flex-col md:flex-row items-center justify-center px-4 md:px-20 py-10">
    <!-- Left Text -->
    <div class="flex flex-col max-w-md space-y-5 text-center md:text-left md:-mr-4">
      <h1 class="text-3xl md:text-[40px] font-bold font-inter">{{ title }}</h1>
      <p class="text-base md:text-[20px] text-gray-700 font-inter leading-relaxed">
        {{ description }}
      </p>

      <RouterLink to="/meetings">
        <Button
          class="bg-[var(--mblue)] hover:bg-[var(--dblue)] cursor-pointer text-white text-base md:text-[18px] px-6 py-3 rounded-lg font-inter transition-colors w-fit mx-auto md:mx-0">
          {{ buttonText }}
        </Button>
      </RouterLink>
    </div>

    <!-- Right Image, hidden in smaller screens -->
    <div class="hidden md:flex justify-center w-full md:w-1/2 md:-ml-4">
      <img
        :src="image"
        :alt="title"
        class="w-auto h-auto max-h-[400px] object-contain"
      />
    </div>
  </section>
</template>

<script>
import { Button } from "@/components/ui/button"
export default {
  name: 'WelcomeSection',
  props: {
    title: { type: String, required: true },
    description: { type: String, required: true },
    buttonText: { type: String, required: true },
    image: { type: String, required: true },
  },
}
</script>