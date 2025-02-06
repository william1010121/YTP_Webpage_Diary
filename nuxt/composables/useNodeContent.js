export const useNodeContent = () => {

    const unescapeContent = (content) => {
        if (!content) return ''; // Handle null or undefined content
        return content.replace(/\\n/g, '\n').replace(/\\t/g, '\t').replace(/\\\\/g, '\\');
    };

    const giveContent = (nodeData) => {
        if (!nodeData || !nodeData.node) return '';

        const node = nodeData.node;
        const summaryContent = node.Summary;
        const importantDataContent = node.important_Data?.[0]?.content; // Safe access

        return unescapeContent(summaryContent || importantDataContent || '');
    };

    return { giveContent };
};
