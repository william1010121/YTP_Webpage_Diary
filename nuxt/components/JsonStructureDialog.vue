<template>
    <v-dialog :modelValue="show">
        <v-card>
            <v-card-title>
                <span class="text-h5">Json Structure</span>
            </v-card-title>
            <v-card-text>
                <VCodeBlock :code="JSON.stringify(data, null, 2)" language="json" prismjs="" />
            </v-card-text>
            <v-card-actions>
                <v-btn color="red darken-1" text @click="$emit('close')">
                    Close
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
import { VCodeBlock } from '@wdns/vue-code-block'; // Ensure this is correctly imported

const props = defineProps({
    show: {
        type: Boolean,
        required: true
    },
    data: {
        type: Object,
        default: () => ({})
    }
});

const emit = defineEmits(['close']);
</script>
