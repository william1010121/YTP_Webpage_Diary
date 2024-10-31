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
        <v-dialog v-model="dialog[index]" max-width="50%">
          <v-card>
            <v-card-title>URL: {{ obj.position }}</v-card-title>
            <v-card-text class="markdown">
              <div v-html="parseMarkdown(obj.content)"></div>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="red darken-1" text @click="closeDialog(index)">Cancel</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-list-item>
    </v-list>
    <v-btn @click="summaryDialog = true" class="url">Summary</v-btn>
    <v-dialog v-model="summaryDialog" max-width="50%">
      <v-card>
        <v-card-title>Summary</v-card-title>
        <v-card-text class="markdown">
          <div v-html="parseMarkdown(summary.data.summary.response)"></div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green" @click="handleResummarize">Resummarize</v-btn>
        </v-card-actions>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red darken-1" text @click="summaryDialog = false">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup>
import { marked } from 'marked';
const props = defineProps({
  file: {
    type: Object,
    required: true,
  },
  summary: {
    type: Object,
    required: true,
  },
});
const emit = defineEmits([
  "resummarize"
]);
const handleResummarize = () => {
  emit("resummarize", props.file.filename);
};
const dialog = reactive(Array(props.file.content.length).fill(false));
const summaryDialog = ref(false);

const openDialog = (index) => {
  dialog[index] = true;
};

const closeDialog = (index) => {
  dialog[index] = false;
};

const parseMarkdown = (content) => {
  console.log(content);
  return marked(content);
};
</script>

<style scoped>
.url {
  border-radius: 0.5cm !important;
  background: lightblue;
  margin: 20px;
}

.v-list-item-title {
  white-space: wrap;
  overflow: visible;
}

.markdown {
  margin: 20px;
  overflow: visible;
  white-space: normal;
  background-color: #FAFAFA;
  border-radius: 0.5cm !important;
}
</style>
