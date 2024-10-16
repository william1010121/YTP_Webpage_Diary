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
        @click="openDialog(index)"
      >
        <v-list-item-title>{{ obj.title }} {{ index }}</v-list-item-title>
        <v-dialog v-model="dialog[index]" max-width="90%">
          <v-card>
            <v-card-title>URL: {{ obj.position }}</v-card-title>
            <v-card-text>
              <v-textarea v-model="obj.content" label="Summary" required readonly max-rows="20" auto-grow no-resize></v-textarea>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="red darken-1" text @click="closeDialog(index)">Cancel</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script setup>
const props = defineProps({
  file: {
    type: Object,
    required: true,
  },
});

const dialog = reactive(Array(props.file.content.length).fill(false));

const openDialog = (index) => {
  dialog[index] = true;
};

const closeDialog = (index) => {
  dialog[index] = false;
};
</script>

<style scoped>
.url {
  border-radius: 0.5cm !important;
  background: lightblue;
  margin: 20px;
}
</style>
