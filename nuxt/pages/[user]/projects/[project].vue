<template>
    <v-row no-gutters>
        <v-col cols="3" v-if="!isRootNodeIdMode">
            <GraphSidePanel :data="data" :nodes="nodes" :edges="edges" @select-node="handleSelectNode" />
        </v-col>
        <v-col cols="isRootNodeIdMode.value ? 9 : 12">
            <v-row v-if="!isRootNodeIdMode">
                <v-col cols="12">
                    <v-toolbar flat>
                        <v-toolbar-title>User: {{ user }}</v-toolbar-title>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="showJsonStructureDialog">Json Structure</v-btn>
                    </v-toolbar>
                </v-col>
            </v-row>

            <json-structure-dialog :show="showStruectureJson" :data="data" @close="showStruectureJson = false"
                @click:outside="showStruectureJson = false" @keydown.esc="showStruectureJson = false" />
            <node-information-dialog :show="showNodeInformation" :node-data="nodeData" :id="previewId"
                @click:outside="showNodeInformation = false" @close="showNodeInformation = false"
                @keydown.esc="showNodeInformation = false" />

            <client-only>
                <div style="height: 100vh">
                    <VueFlow v-model:nodes="nodes" v-model:edges="edges" fit-view-on-init class="vue-flow-basic-example"
                        :default-zoom="1.5" :min-zoom="0.2" :max-zoom="4" @node-double-click="handleNodeDoubleClick"
                        @connect="handleConnect">
                        <Background pattern-color="#aaa" :gap="8" />
                        <MiniMap v-if="!isRootNodeIdMode" />
                        <Controls v-if="!isRootNodeIdMode" />
                        <Panel position="top-right">
                            <div class="buttons">
                                <button title="save graph" @click="onSaveNodePosition" v-if="!isRootNodeIdMode">
                                    <Icon name="save" />
                                </button>
                                <button title="layout graph TB" @click="onLayoutGraph('TB')" v-if="!isRootNodeIdMode">
                                    <Icon name="layout TB" />
                                </button>
                                <button title="layout graph LR" @click="onLayoutGraph('LR')" v-if="!isRootNodeIdMode">
                                    <Icon name="layout LR" />
                                </button>
                                <button title="show all graph" @click="onShowFullGraph" v-if="!isRootNodeIdMode">
                                    <Icon name="show all" />
                                </button>
                            </div>
                        </Panel>
                    </VueFlow>
                </div>
            </client-only>
        </v-col>
    </v-row>

</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useNuxtApp } from '#app';
import { Background } from '@vue-flow/background';
import { Controls } from '@vue-flow/controls';
import { MiniMap } from '@vue-flow/minimap';
import { VueFlow, useVueFlow, Panel } from '@vue-flow/core';
import { MdPreview } from 'md-editor-v3';
import 'md-editor-v3/lib/preview.css';
import { useLayout } from '~/utils/useLayout';
// import JsonStructureDialog from './JsonStructureDialog.vue';
// import NodeInformationDialog from './NodeInformationDialog.vue';
// import GraphSidePanel from './GraphSidePanel.vue'; // Import the new component
import { useGraphData } from './composables/useGraphData';
import { useGraphInteraction } from './composables/useGraphInteraction';
import { useNodeContent } from './composables/useNodeContent';



const route = useRoute();
const user = route.params.user;
const project = route.params.project;
const rootNodeId = route.query.rootNodeId;
const isRootNodeIdMode = ref(!!rootNodeId);

// --- Dialog Visibility ---
const showStruectureJson = ref(false);
const showNodeInformation = ref(false);
const showJsonStructureDialog = () => showStruectureJson.value = true;


// --- Vue Flow Setup ---
const { setNodes, setEdges, fitView, toObject } = useVueFlow();
const previewId = 'preview-only';

const nodes = ref([]);
const edges = ref([]);


// --- Data Fetching and Graph Population ---
const { data, fetchStructure, makeNodes, makeEdges } = useGraphData(user, project, setNodes, setEdges);

onMounted(async () => {
    await fetchStructure();
    await onLayoutGraph('TB');
    console.log('Root Node Id Mode:', isRootNodeIdMode.value);
    console.log('Root Node Id:', rootNodeId);
    console.log('Data:', data.value);
    if (isRootNodeIdMode.value) {
        if( !data.value?.structure) return;
        if( !data.value.structure.hasOwnProperty(rootNodeId)) return;
        handleSelectNode(rootNodeId);
    }
});


// --- Graph Layout ---
const { layout } = useLayout();
const onLayoutGraph = async (direction) => {
    setNodes(layout(nodes.value, edges.value, direction));
    await nextTick(fitView);
};


// --- Graph Interaction (Save Position, Create Edge) ---
const { onSaveNodePosition, handleConnect } = useGraphInteraction(
    user,
    project,
    toObject,
    useNuxtApp,
    setEdges,
    nodes,
    edges
);


// --- Node Information Handling ---
const nodeData = ref({});
const { getNodeInformation } = useGraphData(user, project, setNodes, setEdges); // Re-use composable for node info
const { giveContent } = useNodeContent(); // Use composable for content extraction

const handleNodeDoubleClick = async (event) => {
    await fetchNodeAndShowDialog(event.node.id);
};

const fetchNodeAndShowDialog = async (nodeId) => {
    await getNodeInformation(nodeId, nodeData); // Pass nodeData ref
    showNodeInformation.value = true;
};


// --- Side Panel Node Selection and Tree View ---
const getDescendantNodes = (startNodeId, structure) => {
    const descendants = new Set();
    const queue = [startNodeId];
    descendants.add(startNodeId);

    while (queue.length > 0) {
        const currentNodeId = queue.shift();
        const connectedNodes = structure.structure[currentNodeId]; // Directly access structure from data.value

        if (connectedNodes && Array.isArray(connectedNodes)) {
            connectedNodes.forEach(childId => {
                if (!descendants.has(childId)) {
                    descendants.add(childId);
                    queue.push(childId);
                }
            });
        }
    }
    return descendants;
};


const applyTreeView = (selectedNodeId) => {
    if (!data.value?.structure) return;

    const descendantNodes = getDescendantNodes(selectedNodeId, data.value);
    const descendantNodeIds = Array.from(descendantNodes);

    const updatedNodes = nodes.value.map(node => ({
        ...node,
        hidden: !descendantNodeIds.includes(node.id) // Hide if not a descendant
    }));

    const visibleEdges = edges.value.filter(edge =>
        descendantNodeIds.includes(edge.source) && descendantNodeIds.includes(edge.target)
    );
    const updatedEdges = edges.value.map(edge => ({
        ...edge,
        hidden: !visibleEdges.some(visibleEdge => visibleEdge.id === edge.id) // Hide if not in visibleEdges
    }));


    setNodes(updatedNodes);
    setEdges(updatedEdges);
    nextTick(fitView); // Fit view after updating visibility
};


const handleSelectNode = async (nodeId) => {
    const node = nodes.value.find(n => n.id === nodeId);
    if (node) {
        await applyTreeView(nodeId); // Apply tree view on side panel selection
        fitView({ nodes: [node] , duration: 500 }); // Center view on selected node with animation
    }
};

// const handleNodeDoubleClick = async (event) => {
//     await fetchNodeAndShowDialog(event.node.id);
//     await applyTreeView(event.node.id); // Apply tree view on double click
// };


const onShowFullGraph = () => {
    const updatedNodes = nodes.value.map(node => ({ ...node, hidden: false }));
    const updatedEdges = edges.value.map(edge => ({ ...edge, hidden: false }));
    setNodes(updatedNodes);
    setEdges(updatedEdges);
    nextTick(fitView);
};
</script>

<style>
/* Import necessary styles - Keep as is, they are well organized */
@import '@vue-flow/core/dist/style.css';
@import '@vue-flow/core/dist/theme-default.css';
@import '@vue-flow/controls/dist/style.css';
@import '@vue-flow/minimap/dist/style.css';

.vue-flow-basic-example {
    background-color: #f0f0f0;
    /* Optional background for VueFlow area */
}
.markdown {
    margin: 20px;
    overflow: visible;
    white-space: normal;
    background-color: #FAFAFA;
    border-radius: 0.5cm !important;
}

code[class*="language-"],
code[class*="language-"] *,
pre[class*="language-"] {
    white-space: pre-wrap;
    word-wrap: break-word;
}
</style>


