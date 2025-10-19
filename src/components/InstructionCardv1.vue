<template>
  <section class="w-full pb-[30px]">
    <!-- Header -->
    <div class="flex items-center justify-center md:justify-start gap-4 mb-6 px-6">
      <div
        class="w-16 h-16 text-3xl font-bold flex items-center justify-center rounded-full text-white"
        style="background: var(--dblue)"
      >
        {{ number }}
      </div>
      <h2 class="text-3xl font-bold text-gray-900">
        {{ title }}
      </h2>
    </div>

    <!-- Content -->
    <div class="flex flex-col md:flex-row items-start md:items-start w-full px-6">
      <!-- Image column -->
      <div class="flex-shrink-0 md:mr-12 flex items-start justify-center w-full md:w-auto mb-6 md:mb-0">
        <img
          :src="image"
          alt="illustration"
          class="w-auto h-auto max-h-[300px] md:max-h-[420px] object-contain"
        />
      </div>

      <ul class="flex-1 space-y-6 text-base leading-relaxed list-disc pl-6">
        <li v-for="(item, idx) in items" :key="idx">
          {{ item }}
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup>
defineProps({
  number: { type: [Number, String], default: 1 },
  title: { type: String, default: "" },
  image: { type: String, required: true },
  items: { type: Array, default: () => [] },
})
</script>