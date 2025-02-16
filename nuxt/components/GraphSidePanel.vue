<template>
    <v-card class="side-panel">
        <v-card-title>Root Node Explorer</v-card-title>
        <v-card-text>
            <!-- 保留搜尋框 -->
            <v-text-field
                v-model="searchQuery"
                label="Search Root Nodes"
                clearable
                dense
            ></v-text-field>

            <v-list dense nav>
                <!-- 若 currentParent 存在則顯示返回上層選項 -->
                <v-list-item v-if="currentParent" @click="goToParent" link>
                    <v-list-item-title>← 返回上層</v-list-item-title>
                </v-list-item>
                <v-list-item
                    v-for="node in displayNodes"
                    :key="node.id"
                    @click="selectNode(node.id)"
                    link
                >
                    <v-list-item-title>{{ node.label }}</v-list-item-title>
                </v-list-item>
                <v-list-item v-if="displayNodes.length === 0">
                    <v-list-item-title>No nodes found.</v-list-item-title>
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

// 用來追蹤目前選擇的父節點 (null 表示顯示 root 節點)
const currentParent = ref(null);

// 計算 root 節點，原始邏輯保留，僅在 currentParent 為 null 時使用
const rootNodes = computed(() => {
    if (!props.data?.structure?.nodeTitle) return [];
    const allNodeIds = Object.keys(props.data.structure.nodeTitle);
    const targetNodeIds = new Set();
    for (const key in props.data.structure) {
        if (key !== 'nodeTitle' && Array.isArray(props.data.structure[key])) {
            props.data.structure[key].forEach(id => targetNodeIds.add(id));
        }
    }
    return allNodeIds
        .filter(id => !targetNodeIds.has(id))
        .map(id => ({
            id,
            label: props.data.structure.nodeTitle[id],
            // 可依需要傳回 node 物件
        }));
});

// 根據 currentParent 決定顯示清單：如果 currentParent 為 null 則顯示 rootNodes，否則顯示其子節點
const displayNodes = computed(() => {
    let nodesList = [];
    if (!props.data?.structure) return nodesList;
    if (!currentParent.value) {
        nodesList = rootNodes.value;
    } else {
        const childrenIds = props.data.structure[currentParent.value] || [];
        nodesList = childrenIds.map(id => ({
            id,
            label: props.data.structure.nodeTitle[id] || id
        }));
    }
    // 若有搜尋值則過濾
    const query = searchQuery.value.toLowerCase();
    return nodesList.filter(node => node.label.toLowerCase().includes(query));
});

// 當外部 data 改變時，若 currentParent 失效則重設為 null
watch(
    () => props.data,
    () => {
        // ...existing code...
    }
);

// 點擊節點：更新 currentParent、清除搜尋字串，並傳遞事件至父組件作 subtree view
const selectNode = (nodeId) => {
    currentParent.value = nodeId;
    searchQuery.value = ''; // 清空搜尋框
    emit('select-node', nodeId);
};

// 計算當前節點的父節點，如果有多個則選第一個，若無則回到 root (null)
const goToParent = () => {
    let parentId = null;
    if (props.data?.structure) {
        for (const key in props.data.structure) {
            if (key === 'nodeTitle') continue;
            const children = props.data.structure[key];
            if (Array.isArray(children) && children.includes(currentParent.value)) {
                parentId = key;
                break;
            }
        }
    }
    currentParent.value = parentId;
    emit('select-node', parentId);
};
</script>

<style scoped>
.side-panel {
    width: 250px; /* Adjust width as needed */
    margin-right: 20px;
}
</style>
