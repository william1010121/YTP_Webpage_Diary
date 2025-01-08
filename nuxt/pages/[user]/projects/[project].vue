<template>
    {{ nodeData}}
    <v-row>
        <v-col cols="12">
            <v-toolbar flat>
                <v-toolbar-title>User: {{ user }}</v-toolbar-title>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="showStruectureJson = true">Json Structure</v-btn>
            </v-toolbar>
        </v-col>
    </v-row>
    <v-dialog v-model="showStruectureJson">
        <v-card>
            <v-card-title>
                <span class="text-h5">Json Structure</span>
            </v-card-title>
            <v-card-text>
                <VCodeBlock
                    :code="JSON.stringify(data, null, 2)"
                    language="json"
                    prismjs="" />
            </v-card-text>
            <v-card-actions>
                <v-btn color="red darken-1" text @click="showStruectureJson= false">
                    Close
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>

    <v-dialog v-model="showNodeInformation">
        <v-card>
            <v-card-title>{{nodeData.node.title}}</v-card-title>
            <v-card-text>
                <div class="markdown"
                    v-html="(nodeData.node.Summary ? parseMarkdown(nodeData.node.Summary) :  nodeData.node.important_Data[0] ? parseMarkdown(nodeData.node.important_Data[0]['content']) : '' )">
                </div>

                <hr>
                <details>
                    <summary>More Information</summary>
                    <h2>Important Data</h2>
                    <VCodeBlock
                        :code="JSON.stringify(nodeData.node.important_Data, null, 2)"
                        language="json"
                        prismjs="" />
                    <h2>Relate Data</h2>
                    <VCodeBlock
                        :code="JSON.stringify(nodeData.node.relate_Data, null, 2)"
                        language="json"
                        prismjs="" />
                    <h2>Important Data</h2>
                    <VCodeBlock
                        :code="JSON.stringify(nodeData.node.other_Data, null, 2)"
                        language="json"
                        prismjs="" />
                </details>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="red darken-1" text @click="showNodeInformation = false">Close</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
    <client-only>
        <div style="height: 100vh">
            <VueFlow v-model:nodes="nodes" v-model:edges="edges" fit-view-on-init class="vue-flow-basic-example"
                :default-zoom="1.5" :min-zoom="0.2" :max-zoom="4">
                <Background pattern-color="#aaa" :gap="8" />

                <MiniMap />

                <Controls />

                <Panel position="top-right">
                    <div class="buttons">
                        <button title="save graph" @click="saveNodePosition">
                            <Icon name="save" />
                        </button>
                    </div>
                </Panel>

            </VueFlow>
        </div>
    </client-only>

</template>
<script setup>
import { useRoute } from 'vue-router';
const route = useRoute();
const user = route.params.user;
const project = route.params.project;
const data = ref({});
const showStruectureJson = ref(false);
const showNodeInformation = ref(false);


const fetchStructure = async () => {
    try {
        const { $axios } = useNuxtApp();
        const response = await $axios.post('/api/get_structure', { user, projectId: project });
        data.value = response.data || {};
        makeNodes(data);
        makeEdge(data);
    } catch (error) {
    }
};

onMounted(() => {
    fetchStructure();
});


import { h, ref } from 'vue'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import { VueFlow, useVueFlow, Panel } from '@vue-flow/core'

const { onConnect, addEdges, toObject, onNodeDoubleClick } = useVueFlow()

const nodes = ref([
    { id: '1', type: 'input', label: 'Node 1', position: { x: 250, y: 5 } },
    { id: '2', type: 'output', label: 'Node 2', position: { x: 100, y: 100 } },
    { id: '3', type: 'custom', label: 'Node 3', position: { x: 400, y: 100 } },
])

const edges = ref([
    { id: 'e1-2', source: '1', target: '2', type: 'custom' },
    { id: 'e1-3', source: '1', target: '3', animated: true },
])
const makeNodes = (structure) => {
    nodes.value = [];

    if( !('structure' in structure.value) ){
        return;
    }
    // Correct condition check
    if (!("nodeTitle" in structure.value.structure)) {
        return;
    }
    const haveNodePosition = "nodePosition" in structure.value.structure;
    const NodePosition = haveNodePosition ? structure.value.structure.nodePosition : {};

    // Ensure nodeTitle is an object
    if (typeof structure.value.structure.nodeTitle !== 'object') {
        return;
    }

    // Create nodes dynamically
    for (const [key, value] of Object.entries(structure.value.structure.nodeTitle)) {
        const position = key in NodePosition ? NodePosition[key] : { x: 250, y: 5 };
        nodes.value.push({
            id: key,
            type: 'default',
            label: value,
            position: position
        });
    }
};
const makeEdge = (structure) => {
    edges.value = [];
    if( !('structure' in structure.value) ){
        return;
    }
    if( typeof structure.value.structure !== 'object' ){
        return;
    }
    for( const [key,value] of Object.entries(structure.value.structure) ){
        if( key === 'nodeTitle' )
            continue;
        if(!Array.isArray(value)){
            return;
        }
        for( const connectTo of value ){
            edges.value.push({
                id: `${key}-${connectTo}`,
                source: `${key}`,
                target: `${connectTo}`,
                animated: true
            });
        }
    }
};
const getNodePosition = () => {
    const nodeData = toObject()['nodes'];
    const nodePosition = Object.fromEntries(
        nodeData.map((node) => [node.id, node.position])
    )
    return nodePosition;
}
const saveNodePosition = () => {
    const nodePosition = getNodePosition();
    console.log(nodePosition);
    // Save node position to the server
    try {
        const { $axios } = useNuxtApp();
        $axios.post('/api/uploads/setStructureConfig', {
            user, projectId: project, key: "nodePosition", value: nodePosition });
    } catch (error) {
        console.error('Error saving node position:', error);
    }
}
const createEdge = (source, target) => {
    try {
        const { $axios } = useNuxtApp();
        $axios.post('/api/uploads/create_edge', {
            user, projectId: project, StartNode: source, EndNode: target});
    } catch (error) {
        console.error('Error saving edge:', error);
    }
}


onConnect((params) => {
    console.log(params)
    params.animated = true
    addEdges([params])
    createEdge(params.source, params.target)
    saveNodePosition()
})

const nodeData = ref({});
const getNodeInformation = async (nodeId) => {
    try {
        const { $axios } = useNuxtApp();
        const response = await $axios.post('/api/get_node', { user, projectId: project, nodeId });
        nodeData.value = response.data || {};
    } catch (error) {
        console.error('Error fetching node information:', error);
    }
}
const getAndShowNodeInformation = async (nodeId) => {
    await getNodeInformation(nodeId);
    showNodeInformation.value = true;
}


import { marked } from 'marked';
const parseMarkdown = (content) => {
    return marked(content);
}
onNodeDoubleClick((event) => {
    getAndShowNodeInformation(event.node.id);
})



import { createVCodeBlock, VCodeBlock } from '@wdns/vue-code-block';
import Prism from 'prismjs';
import 'prismjs/components/prism-typescript';
</script>

<style>
/* import the necessary styles for Vue Flow to work */
@import '@vue-flow/core/dist/style.css';
/* import the default theme, this is optional but generally recommended */
@import '@vue-flow/core/dist/theme-default.css';
@import '@vue-flow/controls/dist/style.css';
@import '@vue-flow/minimap/dist/style.css';
.markdown {
  margin: 20px;
  overflow: visible;
  white-space: normal;
  background-color: #FAFAFA;
  border-radius: 0.5cm !important;
}
code[class*="language-"],
code[class*="language-"] *,
pre[class*="language-"]
{
  white-space: pre-wrap;
  word-wrap: break-word; 
}
</style>
