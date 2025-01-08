<template>
    <v-row>
        <v-col cols="12">
            <v-toolbar flat>
                <v-toolbar-title>User: {{ user }}</v-toolbar-title>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="showJsonForm = true">Import Json</v-btn>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="showMarkdownForm = true">Import Markdown</v-btn>
            </v-toolbar>
        </v-col>
    </v-row>
    <v-card>
        <v-card-title>Projects</v-card-title>

    <v-list>
        <v-list-item
            v-for="project in data.projects"
            :key="project"
        >
            <v-list-item-title
                class="project"
                @click="() => $router.push(`/${user}/projects/${project}`)"
            >{{ project }}</v-list-item-title>
        </v-list-item>
    </v-list>
    </v-card>

    <ImportForm
        v-if="showJsonForm"
        title="Import Json"
        :form="jsonForm"
        :showForm="showJsonForm"
        @importfile="importJsonFile(jsonForm)"
        @importtext="importJsonText(jsonForm)"
        @close="() => { showJsonForm = false }"
    />
    <ImportForm
        v-if="showMarkdownForm"
        title="Import Markdown"
        :form="markdownForm"
        :showForm="showMarkdownForm"
        @importfile="importMarkdownFile(markdownForm)"
        @importtext="importMarkdownText(markdownForm)"
        @close="() => { showMarkdownForm = false }"
    />

    {{ data }}
    {{ showJsonForm}}
    {{ showMarkdownForm}}
    {{ jsonForm}}
    {{ markdownForm }}
</template>
<script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import ImportForm from '~/components/ImportForm.vue';

const route = useRoute();
const user = route.params.user;
const data = ref({});

const showJsonForm = ref(false);
const showMarkdownForm = ref(false);

const jsonForm = ref({
    projectId: '',
    file: null,
    type: 'file',
});

const markdownForm = ref({
    projectId: '',
    file: null,
    type: 'file',
});
const fetchProjectList = async () => {
    try {
        const { $axios } = useNuxtApp();
        const response = await $axios.post('/api/get_project_list', { user });
        data.value = response.data || {};
    } catch (error) {
        console.error('Error fetching files:', error);
    }
};

const importJson = async (projectId,Json) => {
    try {
        const { $axios } = useNuxtApp();
        const response = await $axios.post('/api/import/json', {
            user,
            projectId: projectId,
            json: Json,
        });
        fetchProjectList();
        showJsonForm.value = false;
    } catch (error) {
        console.error('Error importing json:', error);
    }
};


const importMarkdown = async (projectId, Makrdown)=> {
    try {
        const { $axios } = useNuxtApp();
        const response = await $axios.post('/api/import/markdown', {
            user,
            projectId: projectId,
            markdown: Makrdown,
        });
        fetchProjectList();
        showMarkdownForm.value = false;
    } catch (error) {
        console.error('Error importing markdown:', error);
    }
};

const importJsonFile = async (form) => {
    console.log(form);
    const file = form.file;
    const reader = new FileReader();
    reader.onload = async (e) => {
        importJson(form.projectId, JSON.parse(e.target.result));
    };
    reader.readAsText(file);
};
const importMarkdownFile = async (form) => {
    console.log(form);
    const file = form.file;
    const reader = new FileReader();
    reader.onload = async (e) => {
        importMarkdown(form.projectId, e.target.result);
    };
    reader.readAsText(file);
}; 
const importJsonText = async (form) => {
    importJson(form.projectId, JSON.parse(form.text));
};
const importMarkdownText = async (form) => {
    importMarkdown(form.projectId, form.text);
};




onMounted(() => {
    fetchProjectList();
});
</script>

<style scoped>
.project {
    border-radius: 0.5cm !important;
    background: lightblue;
    margin: 20px;
}
</style>
