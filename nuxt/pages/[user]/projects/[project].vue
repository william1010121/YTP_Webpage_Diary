<template>
    {{ user }} {{ project }}
    <pre>{{ JSON.stringify(data, null, 2)}}</pre>

</template>
<script setup>
import { useRoute } from 'vue-router';
const route = useRoute();
const user = route.params.user;
const project = route.params.project;
const data= ref({});

const fetchStructure = async () => {
    try {
        const { $axios } = useNuxtApp();
        const response = await $axios.post('/api/get_structure', { user, projectId: project});
        data.value = response.data || {};
        console.log(response);
    } catch (error) {
        console.error('Error fetching structure:', error);
    }
};
onMounted(() => {
    fetchStructure();
});
</script>
