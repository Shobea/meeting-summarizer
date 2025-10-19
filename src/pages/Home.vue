<!-- NOTHING TO CHANGE HERE -->
<template>
  <NavBar />
  <SectionHelloUser
    title="Welcome!"
    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lobortis rhoncus arcu, nec placerat turpis elementum sit amet. Ut ultrices enim"
    buttonText="Let’s get started!"
    image="/src/assets/homepage.png"
  />

  <div class="flex flex-col md:flex-row items-center justify-center gap-8 md:gap-12 md:space-x-8">     
    <InstructionCardv2
      image="/src/assets/scan.png"
      title="Scan."
      description="Scan student IDs and start the session."
    />

    <InstructionCardv2
      image="/src/assets/speech.png"
      title="Meet."
      description="Meet and record the conversation."
    />

    <InstructionCardv2
      image="/src/assets/summarize.png"
      title="Summarize."
      description="Get an instant summary after every meeting."
    />
  </div>

</template>

<script setup>
import NavBar from '@/components/Navbar.vue'
import SectionHelloUser from '@/components/SectionHelloUser.vue';
import InstructionCardv2 from '@/components/InstructionCardv2.vue';
</script>