
<template>
    <v-app>
        <v-main>
            <v-app-bar color="indigo darken-2" dark elevation="4">
                <v-app-bar-title>User: {{ user }}</v-app-bar-title>

                <v-spacer></v-spacer>

                <v-btn color="amber darken-2" class="ml-2" @click="openImportForm('json')">
                    Import Json
                </v-btn>
                <v-btn color="amber darken-2" class="ml-2" @click="openImportForm('markdown')">
                    Import Markdown
                </v-btn>
            </v-app-bar>

            <v-container class="pa-4 grey lighten-5">
                <v-row justify="center">
                    <v-col cols="12" md="8">
                        <v-text-field v-model="searchQuery" label="Search Projects" single-line hide-details
                            prepend-inner-icon="mdi-magnify" class="project-search" clearable density="compact"
                            variant="outlined"></v-text-field>

                        <v-card class="mt-4" elevation="2">
                            <v-card-title>Projects</v-card-title>
                            <v-divider></v-divider>
                            <v-list v-if="filteredProjects.length > 0">
                                <v-list-item v-for="project in filteredProjects" :key="project" class="project-item">
                                    <v-list-item-title class="project-title" @click="navigateToProject(project)">{{
                                        project }}</v-list-item-title>
                                </v-list-item>
                            </v-list>
                            <v-card-text v-else>
                                No projects found.
                            </v-card-text>
                        </v-card>

                        <ImportForm />

                        <v-card class="mt-4" elevation="1">
                            <v-card-title>Debug Data</v-card-title>
                            <v-card-text class="pa-4">
                                <details>
                                    <summary>Show Debug Data</summary>
                                    <pre>{{ data }}</pre>
                                    <pre>showImportForm: {{ showImportForm }}</pre>
                                    <pre>importForm: {{ importForm }}</pre>
                                </details>
                            </v-card-text>
                        </v-card>
                    </v-col>
                </v-row>
            </v-container>
        </v-main>
    </v-app>
</template>


<script setup>
import { onMounted, ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router'; //Import useNuxtApp
import { useNuxtApp } from 'nuxt/app'; // Correct import for useNuxtApp
import ImportForm from '~/components/ImportForm.vue';

const route = useRoute();
const router = useRouter();
const user = route.params.user;
const data = ref({ projects: [] });
const searchQuery = ref(''); // For project search

const showImportForm = ref(false);
const importFormTitle = ref('');
const importType = ref('');

const importForm = ref({
    projectId: '',
    file: null,
    text: '',
    type: 'file',
});

// Computed property for filtered projects
const filteredProjects = computed(() => {
    const query = searchQuery.value.toLowerCase();
    return data.value.projects.filter(project => project.toLowerCase().includes(query));
});


const fetchProjectList = async () => {
    try {
        const {$axios} = useNuxtApp() // use NuxtApp properly
        const response = await $axios.post('/api/get_project_list', { user });
        data.value = response.data || { projects: [] };
    } catch (error) {
        console.error('Error fetching project list:', error);
    }
};

const importData = async (payload) => {
    try {
        const {$axios} = useNuxtApp() // use NuxtApp properly
        const response = await $axios.post(`/api/import/${importType.value}`, {
            user,
            ...payload
        });
        fetchProjectList();
        closeImportForm();
    } catch (error) {
        console.error(`Error importing ${importType.value}:`, error);
    }
};

const importFile = async (form) => {
    if (!form.file) {
        console.warn("No file selected for import.");
        return;
    }

    const reader = new FileReader();
    reader.onload = async (e) => {
        const projectId = form.projectId;
        let content;

        if (importType.value === 'json') {
            try {
                content = JSON.parse(e.target.result);
            } catch (parseError) {
                console.error("Error parsing JSON file:", parseError);
                return;
            }
            await importData({ projectId: projectId, json: content });
        } else if (importType.value === 'markdown') {
            content = e.target.result;
            await importData({ projectId: projectId, markdown: content });
        }
    };
    reader.readAsText(form.file);
};

const importText = async (form) => {
    const projectId = form.projectId;
    const textContent = form.text;

    if (!textContent) {
        console.warn("No text content provided for import.");
        return;
    }

    if (importType.value === 'json') {
        let content;
        try {
            content = JSON.parse(textContent);
        } catch (parseError) {
            console.error("Error parsing JSON text:", parseError);
            return;
        }
        await importData({ projectId: projectId, json: content });
    } else if (importType.value === 'markdown') {
        await importData({ projectId: projectId, markdown: textContent });
    }
};

const openImportForm = (type) => {
    importType.value = type;
    importFormTitle.value = `Import ${type.charAt(0).toUpperCase() + type.slice(1)}`;
    showImportForm.value = true;
    importForm.value = {
        projectId: '',
        file: null,
        text: '',
        type: 'file',
    };
};

const closeImportForm = () => {
    showImportForm.value = false;
};

const navigateToProject = (project) => {
    router.push(`/${user}/projects/${project}`);
};

onMounted(() => {
    fetchProjectList();
});
</script>

<style scoped>
.project-search {
    max-width: 100%;
    /* Take full width of its container */
    margin-bottom: 16px;
    /* Add some space below the search box */
}

.project-item {
    border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.project-item:last-child {
    border-bottom: none;
}

.project-title {
    cursor: pointer;
    font-weight: 600;
    font-size: 1.1rem;
    padding: 12px 16px;
    display: block;
}

.project-title:hover {
    background-color: rgba(0, 0, 0, 0.04);
}

.v-card-text details {
    padding: 12px;
    border: 1px solid rgba(0, 0, 0, 0.12);
    border-radius: 4px;
    background-color: white;
}
</style>
