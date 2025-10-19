<!-- NOTHING TO CHANGE HERE -->
<template>
  <NavBar />

  <div class="max-w-7xl mx-auto py-12">
    <StepCard
      :number="1"
      title="How to Scan"
      image="/src/assets/scan.png"
      :items="[
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lobortis rhoncus arcu, nec placerat turpis elementum sit amet.',
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lobortis rhoncus arcu, nec placerat turpis elementum sit amet.',
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lobortis rhoncus arcu, nec placerat turpis elementum sit amet.'
      ]"
    />

    <StepCard
      :number="2"
      title="How to Create Meeting"
      image="src/assets/speech.png"
      :items="[
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lobortis rhoncus arcu, nec placerat turpis elementum sit amet.',
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lobortis rhoncus arcu, nec placerat turpis elementum sit amet.',
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lobortis rhoncus arcu, nec placerat turpis elementum sit amet.'
      ]"
    />

    <StepCard
      :number="3"
      title="How to View Summary"
      image="src/assets/summarize.png"
      :items="[
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lobortis rhoncus arcu, nec placerat turpis elementum sit amet.',
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lobortis rhoncus arcu, nec placerat turpis elementum sit amet.',
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lobortis rhoncus arcu, nec placerat turpis elementum sit amet.'
      ]"
    />
  </div>
</template>

<script setup>
import NavBar from '@/components/Navbar.vue'
import StepCard from "@/components/InstructionCardv1.vue"
</script>