<script setup>
defineProps(['name'])
import { mdiContentSave, mdiRestore, mdiPlus } from '@mdi/js'
</script>

<template>
    <v-icon :icon="mdiContentSave" v-if="name==='save'" size="x-large"></v-icon>
    <v-icon :icon="mdiRestore" v-if="name==='restore'"></v-icon>
    <v-icon :icon="mdiPlus" v-if="name==='add'"></v-icon>
</template>
