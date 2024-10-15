<!-- components/FileCard.vue -->
<template>
  <v-card>
    <v-card-title>{{ file.filename }}</v-card-title>
    <v-list>
      <v-list-item 
      v-for="(obj, index) in file.content" 
      :key="index" 
      :value="obj"
      :class="obj.type"
      >
        <v-list-item-content >{{ obj.url }}</v-list-item-content>
      </v-list-item>
    </v-list>
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
.url {
  border-radius: 0.5cm !important;
  background: lightblue;
  margin: 20px;
}
</style>
