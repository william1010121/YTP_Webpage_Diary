import { ref } from 'vue';

export const useGraphData = (user, project, setNodes, setEdges) => {
    const data = ref({});

    const fetchStructure = async () => {
        try {
            const { $axios } = useNuxtApp(); // Assuming useNuxtApp is available here
            const response = await $axios.post('/api/get_structure', { user, projectId: project });
            data.value = response.data || {};
            makeNodes(data.value);
            makeEdges(data.value);
        } catch (error) {
            console.error("Error fetching structure:", error);
        }
    };

    const makeNodes = (structure) => {
        const nodesArray = [];
        if (!structure?.structure?.nodeTitle) { // More robust check
            return;
        }
        const haveNodePosition = structure.structure.nodePosition;
        const NodePosition = haveNodePosition ? structure.structure.nodePosition : {};

        for (const [key, value] of Object.entries(structure.structure.nodeTitle)) {
            const position = NodePosition[key] || { x: 250, y: 5 };
            nodesArray.push({
                id: key,
                type: 'default',
                label: value,
                position: position
            });
        }
        setNodes(nodesArray);
    };

    const makeEdges = (structure) => {
        const edgesArray = [];
        if (!structure?.structure || typeof structure.structure !== 'object') {
            return;
        }
        for (const [key, value] of Object.entries(structure.structure)) {
            if (key === 'nodeTitle' || !Array.isArray(value)) continue;
            for (const connectTo of value) {
                edgesArray.push({
                    id: `${key}-${connectTo}`,
                    source: `${key}`,
                    target: `${connectTo}`,
                    animated: true
                });
            }
        }
        setEdges(edgesArray);
    };

    // For fetching single node information (reused)
    const getNodeInformation = async (nodeId, nodeDataRef) => { // Pass nodeDataRef
        try {
            const { $axios } = useNuxtApp();
            const response = await $axios.post('/api/get_node', { user, projectId: project, nodeId });
            nodeDataRef.value = response.data || {}; // Update the passed ref
        } catch (error) {
            console.error('Error fetching node information:', error);
        }
    };


    return { data, fetchStructure, makeNodes, makeEdges, getNodeInformation };
};
