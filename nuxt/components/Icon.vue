<script setup>
defineProps(['name'])
import { mdiContentSave, mdiRestore, mdiPlus, mdiArrowLeftRightBold, mdiArrowUpDownBold } from '@mdi/js'
</script>

<template>
    <v-icon :icon="mdiContentSave" v-if="name==='save'" size="x-large"></v-icon>
    <v-icon :icon="mdiRestore" v-if="name==='restore'"></v-icon>
    <v-icon :icon="mdiPlus" v-if="name==='add'"></v-icon>
    <v-icon :icon="mdiArrowLeftRightBold" v-if="name==='layout LR'"></v-icon>
    <v-icon :icon="mdiArrowUpDownBold" v-if="name==='layout TB'"></v-icon>
</template>
