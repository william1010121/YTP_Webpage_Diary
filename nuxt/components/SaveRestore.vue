<!-- https://vueflow.dev/examples/save.html -->
<script setup>
import { Panel, useVueFlow } from '@vue-flow/core'

const flowKey = 'vue-flow--save-restore'

const { nodes, addNodes, dimensions, toObject, fromObject } = useVueFlow()

function onSave() {
  console.log(toObject())
  localStorage.setItem(flowKey, JSON.stringify(toObject()))
}

function onRestore() {
  const flow = JSON.parse(localStorage.getItem(flowKey))
  console.log(flow)
  if (flow) {
    fromObject(flow)
  }
}

function onAdd() {
  const id = nodes.value.length + 1

  const newNode = {
    id: `random_node-${id}`,
    label: `Node ${id}`,
    position: { x: Math.random() * dimensions.value.width, y: Math.random() * dimensions.value.height },
  }

  addNodes([newNode])
}

onMounted(() => {
  onRestore()
})
</script>

<template>
  <Panel position="top-right">
    <div class="buttons">
      <button title="save graph" @click="onSave">
        <Icon name="save" />
      </button>
      <button title="restore graph" @click="onRestore">
        <Icon name="restore" />
      </button>
      <button title="add random node" @click="onAdd">
        <Icon name="add" />
      </button>
    </div>
  </Panel>
</template>
