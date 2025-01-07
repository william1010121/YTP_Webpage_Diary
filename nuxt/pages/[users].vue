<!-- pages/[user].vue -->
<template>
  <v-container>
    {{ files[1] }}
    {{ summary[1] }}
    <v-row>
      <v-col cols="12">
        <v-toolbar flat>
          <v-toolbar-title>User: {{ user }}</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="showForm = true">Add New URL</v-btn>
        </v-toolbar>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-alert v-if="files.length === 0" type="info">
          No files found for this user.
        </v-alert>
      </v-col>
    </v-row>

    <v-row>
      <v-col
        v-for="(file, index) in files"
        :key="index"
        cols="12"
        sm="6"
        md="4"
      >
        <FileCard :file="file" :summary="summary[index]" @resummarize="(date) => {reSummarize(index,date);}"/>
      </v-col>
    </v-row>

    <!-- Dialog for Adding New URL -->
    <v-dialog v-model="showForm" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">Add New URL</span>
        </v-card-title>

        <v-card-text>
          <v-text-field
            v-model="newUrl"
            label="Enter URL"
            required
          ></v-text-field>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="submitUrl">
            Submit
          </v-btn>
          <v-btn color="red darken-1" text @click="showForm = false">
            Cancel
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import FileCard from '~/components/FileCard.vue';

const route = useRoute();
const user = route.params.user;

const files = ref([]);
const summary = ref([]);
const showForm = ref(false);
const newUrl = ref('');

const fetchFiles = async () => {
  try {
    const { $axios } = useNuxtApp();
    const response = await $axios.post('/api/list', { user });
    files.value = response.data.files || [];
    for (let i = 0; i < files.viiialue.length; i++) {
      const file = files.value[i];
      const response = await $axios.post('/api/summary/get_summary', {user, date: file.filename});
      summary.value.push(response || []);
    }
  } catch (error) {
    console.error('Error fetching files:', error);
  }
};

const reSummarize = async (index, date) => {
  try {
    const { $axios } = useNuxtApp();
    const response = await $axios.post('/api/summary/summarize', { user, date});
    summary.value[index] = response || [];
  } catch (error) {
    console.error('Error resummarizing:', error);
  }
};

const submitUrl = async () => {
  if (!newUrl.value) {
    alert('Please enter a URL.');
    return;
  }
  try {
    const { $axios } = useNuxtApp();
    await $axios.post('/api/uploads/url', {
      user,
      url: newUrl.value,
    });
    newUrl.value = '';
    showForm.value = false;
    await fetchFiles(); // Refresh the list
  } catch (error) {
    console.error('Error submitting URL:', error);
  }
};

onMounted(() => {
  fetchFiles();
});
</script>

<style scoped>
/* Add any additional styles if needed */
</style>
