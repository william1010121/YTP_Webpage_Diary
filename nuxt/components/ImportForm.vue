<!-- components/ImportForm.vue -->
<template>
    <v-dialog :model-value="showForm">
        <v-card>
            <v-card-title>{{ title }}</v-card-title>
            <v-card-text>
                <v-text-field v-model="form.projectId" label="Project ID" />
                <v-file-input v-model="form.file" label="File" accept=".json,.md" />
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="green" @click="importfile(form)">Submit</v-btn>
                <v-btn color="red darken-1" text @click="close">Cancel</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  form: {
    type: Object,
    required: true,
  },
  showForm: {
    type: Boolean,
    required: true,
  },
});
const emit = defineEmits(['importfile', 'close']);
const close = () => emit('close');
const importfile = (form) => emit('importfile', form);
</script>
