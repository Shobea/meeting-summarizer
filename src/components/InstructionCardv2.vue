<template>
  <div class="flex flex-col items-center text-center space-y-4 md:space-y-2 pl-1.5 pr-1.5 pb-[30px]">
    <!-- Image -->
    <img
      :src="image"
      :alt="title"
      class="w-3/4 md:w-1/2 lg:w-2/5 h-auto origin-center"
    />

    <!-- Title -->
    <h2 class="text-xl md:text-2xl font-bold px-4 md:px-0">
      {{ title }}
    </h2>

    <!-- Description -->
    <p class="text-gray-700 text-sm md:text-base leading-relaxed max-w-xs md:max-w-sm px-4 md:px-0">
      {{ description }}
    </p>
  </div>
</template>

<script>
export default {
  name: 'StepCard',
  props: {
    image: { type: String, required: true },
    title: { type: String, required: true },
    description: { type: String, required: true },
  },
}
</script>