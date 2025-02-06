import { useVueFlow } from '@vue-flow/core';

export const useGraphInteraction = (user, project, toObjectFn, nuxtApp, setEdges, nodes, edges) => {

    const getNodePosition = () => {
        const nodeData = toObjectFn()['nodes'];
        return Object.fromEntries(
            nodeData.map((node) => [node.id, node.position])
        );
    };

    const saveNodePosition = async () => {
        const nodePosition = getNodePosition();
        try {
            const { $axios } = nuxtApp();
            await $axios.post('/api/uploads/setStructureConfig', {
                user, projectId: project, key: "nodePosition", value: nodePosition
            });
            console.log("Node positions saved.");
        } catch (error) {
            console.error('Error saving node position:', error);
        }
    };

    const createEdge = async (source, target) => {
        try {
            const { $axios } = nuxtApp();
            await $axios.post('/api/uploads/create_edge', {
                user, projectId: project, StartNode: source, EndNode: target
            });
            console.log("Edge created on server.");
        } catch (error) {
            console.error('Error saving edge:', error);
        }
    };

    const onSaveNodePosition = () => {
        saveNodePosition();
    };

    const handleConnect = (params) => {
        params.animated = true;
        setEdges([...edges.value, params]); // Update edges reactively
        createEdge(params.source, params.target);
        saveNodePosition();
    };


    return { onSaveNodePosition, handleConnect };
};
