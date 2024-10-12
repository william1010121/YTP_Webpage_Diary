<!-- components/FileCard.vue -->
<template>
  <v-card class="ma-2" outlined>
    <v-card-title>{{ file.filename }}</v-card-title>
    <v-card-text>{{ file.content }}</v-card-text>
  </v-card>
</template>

<script setup>
defineProps({
  file: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped>
/* You can add additional styles if needed */
</style>
