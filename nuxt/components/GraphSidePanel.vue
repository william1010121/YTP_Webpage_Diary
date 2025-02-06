<template>
    <v-card class="side-panel">
        <v-card-title>Root Node Explorer</v-card-title>
        <v-card-text>
            <v-text-field
                v-model="searchQuery"
                label="Search Root Nodes"
                clearable
                dense
            ></v-text-field>

            <v-list dense nav>
                <v-list-item
                    v-for="rootNode in filteredRootNodes"
                    :key="rootNode.id"
                    @click="$emit('select-node', rootNode.id)"
                    link
                >
                    <v-list-item-title>{{ rootNode.label }}</v-list-item-title>
                </v-list-item>
                <v-list-item v-if="filteredRootNodes.length === 0">
                    <v-list-item-title>No root nodes found.</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-card-text>
    </v-card>
</template>

<script setup>
import { ref, computed, defineProps, defineEmits, watch } from 'vue';

const props = defineProps({
    data: {
        type: Object,
        required: true
    },
    nodes: {
        type: Array,
        required: true
    },
    edges: {
        type: Array,
        required: true
    }
});

const emit = defineEmits(['select-node']);

const searchQuery = ref('');
const rootNodes = ref([]);

const calculateRootNodes = () => {
    if (!props.data?.structure?.nodeTitle) {
        rootNodes.value = [];
        return;
    }

    const allNodeIds = Object.keys(props.data.structure.nodeTitle);
    const targetNodeIds = new Set();

    for (const key in props.data.structure) {
        if (key !== 'nodeTitle' && Array.isArray(props.data.structure[key])) {
            props.data.structure[key].forEach(targetNodeIds.add, targetNodeIds);
        }
    }

    const calculatedRootNodes = allNodeIds
        .filter(nodeId => !targetNodeIds.has(nodeId))
        .map(nodeId => {
            const node = props.nodes.find(n => n.id === nodeId);
            return {
                id: nodeId,
                label: props.data.structure.nodeTitle[nodeId],
                node: node // Include the node object if needed
            };
        });
    rootNodes.value = calculatedRootNodes;
};

watch(
    () => props.data, // Watch for changes in the data prop
    () => {
        calculateRootNodes();
    },
    { immediate: true } // Calculate root nodes immediately on mount
);

const filteredRootNodes = computed(() => {
    const query = searchQuery.value.toLowerCase();
    return rootNodes.value.filter(node => {
        return node.label.toLowerCase().includes(query);
    });
});
</script>

<style scoped>
.side-panel {
    width: 250px; /* Adjust width as needed */
    margin-right: 20px;
}
</style>
