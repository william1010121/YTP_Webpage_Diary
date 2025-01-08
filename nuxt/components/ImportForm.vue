<!-- components/ImportForm.vue -->
<template>
    <v-dialog :model-value="showForm">
        <v-card>
            <v-card-title>{{ title }}</v-card-title>
            <v-card-text>
                <v-text-field v-model="form.projectId" label="Project ID" />
                <v-select
                    :items="['file', 'text']"
                    v-model="form.type"
                />
                <v-file-input v-if="form.type=='file'" v-model="form.file" label="File" accept=".json,.md" />
                <v-textarea v-if="form.type=='text'" v-model="form.text" label="Text" />
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="green" @click="(form.type=='file' ? importfile(form) : importtext(form))">Import</v-btn>
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
const emit = defineEmits(['importfile', 'close', 'importtext']);
const close = () => emit('close');
const importfile = (form) => emit('importfile', form);
const importtext = (form) => emit('importtext', form);
</script>
