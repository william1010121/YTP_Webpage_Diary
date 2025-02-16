<template>
    <v-dialog :modelValue="show">
        <v-card>
            <v-card-title>{{ nodeData?.node?.title }}</v-card-title>
            <v-card-text>
                <div class="markdown">
                    <MdPreview :id="id" :modelValue="content" theme="dark" preview-theme="github" />
                </div>
                <hr>
                <details>
                    <summary>More Information</summary>
                    <h2>Important Data</h2>
                    <VCodeBlock :code="JSON.stringify(nodeData?.node?.important_Data, null, 2)" language="json"
                        prismjs="" />
                    <h2>Relate Data</h2>
                    <VCodeBlock :code="JSON.stringify(nodeData?.node?.relate_Data, null, 2)" language="json" prismjs="" />
                    <h2>Other Data</h2>
                    <VCodeBlock :code="JSON.stringify(nodeData?.node?.other_Data, null, 2)" language="json" prismjs="" />
                </details>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="red darken-1" text @click="$emit('close')">Close</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script setup>
import { defineProps, defineEmits, computed } from 'vue';
import { MdPreview } from 'md-editor-v3';
import { VCodeBlock } from '@wdns/vue-code-block';
import { useNodeContent } from '../composables/useNodeContent'; // Adjust path if needed


const props = defineProps({
    show: {
        type: Boolean,
        required: true
    },
    nodeData: {
        type: Object,
        default: () => ({})
    },
    id: {
        type: String,
        required: true
    }
});

const emit = defineEmits(['close']);

const { giveContent } = useNodeContent();
const content = computed(() => filterContent(giveContent(props.nodeData)));
const filterContent = (content) => {
    // remove the space betweeen \n and ```, ``` and \n, because it will cause the code block not working
    // ex: \n   ``` -> \n\n```, ```  \n -> ```\n\n
    return content.replace(/\n\s*```/g, '\n\n```').replace(/```\s*\n/g, '```\n\n');
};

</script>
