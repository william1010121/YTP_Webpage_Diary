#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
#include <ctype.h>

#define Max_Length 10000

typedef struct Node{
    int id;
    int parent_id;
    int level;
    char title[Max_Length];
    char content[Max_Length];
} Node;

// Updated function to escape JSON special characters without altering UTF-8 characters
char* json_escape(const char* src, char* dest, size_t dest_size){
    size_t j = 0;
    for(size_t i = 0; src[i] != '\0' && j < dest_size - 1; i++){
        if(j >= dest_size - 1){
            break;
        }
        switch(src[i]){
            case '\"':
                if(j + 2 >= dest_size) break;
                dest[j++] = '\\';
                dest[j++] = '\"';
                break;
            case '\\':
                if(j + 2 >= dest_size) break;
                dest[j++] = '\\';
                dest[j++] = '\\';
                break;
            case '\t':
                if(j + 2 >= dest_size) break;
                dest[j++] = '\\';
                dest[j++] = 't';
                break;
            case '\n':
                if(j + 2 >= dest_size) break;
                dest[j++] = '\\';
                dest[j++] = 'n';
                break;
            default:
                // Directly copy the character if it's not a special JSON character
                dest[j++] = src[i];
                break;
        }
    }
    dest[j] = '\0';
    return dest;
}

void input_file(char name[Max_Length], FILE **fin, FILE **fout){
    *fin = fopen(name, "r");
    if(*fin == NULL){
        fprintf(stderr, "Error opening input file.\n");
        exit(1);
    }
    // Replace the last two characters with "json"
    size_t len = strlen(name);
    if(len < 2){
        fprintf(stderr, "Input filename too short to replace extension.\n");
        fclose(*fin);
        exit(1);
    }
    name[len - 2] = '\0'; // Remove last two characters
    strcat(name, "json");
    *fout = fopen(name, "w");
    if(*fout == NULL){
        fprintf(stderr, "Error opening output file.\n");
        fclose(*fin);
        exit(1);
    }
}

void write_graph(int graph[][100], int n, FILE *fp){
    fprintf(fp, "\t\"Graph\": {\n");
    for (int i = 1; i <= n; i ++){
        fprintf(fp, "\t\t\"%d\":[", i);
        int j = 0;
        // Iterate until a zero is found (assuming 0 is not a valid node ID)
        for (; graph[i][j] != 0; j ++){
            if(j > 0){
                fprintf(fp, ", ");
            }
            fprintf(fp, "\"%d\"", graph[i][j]);
            // Prevent exceeding the array bounds
            if(j >= 99){
                break;
            }
        }
        fprintf(fp, "]");
        if( i != n )
            fprintf(fp, ",\n");
        else
            fprintf(fp, "\n");
    }
    fprintf(fp, "\t},\n");
}

void write_node(Node *nodes, int node_count, FILE *fp){
    char escaped_title[Max_Length * 2];    // Allocate sufficient space for escaped strings
    char escaped_content[Max_Length * 2];
    
    fprintf(fp, "\t\"Node\": {\n");
    for (int i = 0; i < node_count; i++) {
        json_escape(nodes[i].title, escaped_title, sizeof(escaped_title));
        json_escape(nodes[i].content, escaped_content, sizeof(escaped_content));
        
        fprintf(fp, "\t\t\"%d\": {\n", nodes[i].id);
        fprintf(fp, "\t\t\t\"Title\": \"%s\",\n", escaped_title);
        fprintf(fp, "\t\t\t\"Content\": \"%s\"\n", escaped_content);
        fprintf(fp, "\t\t}%s\n", (i == node_count - 1) ? "" : ",");
    }
    fprintf(fp, "\t}\n");
}

int main(){
    char str[Max_Length];
    if(scanf("%9999s", str) != 1){
        fprintf(stderr, "Error reading input filename.\n");
        return 1;
    }

    FILE *fin, *fout;
    input_file(str, &fin, &fout);

    Node nodes[100];
    int node_count = 0;
    char line[Max_Length], current_content[Max_Length] = "";

    while (fgets(line, Max_Length, fin)){
        char *start = line;
        // Trim leading whitespace
        while (isspace((unsigned char)*start)) start ++;
        // Trim trailing whitespace
        char *end = start + strlen(start) - 1;
        while (end > start && isspace((unsigned char)*end)) *end-- = '\0';
        if (start[0] == '#'){
            if (node_count > 0){
                strncpy(nodes[node_count - 1].content, current_content, Max_Length - 1);
                nodes[node_count - 1].content[Max_Length - 1] = '\0';
                current_content[0] = '\0';
            }
            if(node_count >= 100){
                fprintf(stderr, "Exceeded maximum number of nodes (100).\n");
                break;
            }
            nodes[node_count].id = node_count + 1;
            int level_count = 0;
            while (*start == '#') { start ++; level_count ++; }
            nodes[node_count].level = level_count;
            // Trim any whitespace after the hashes
            while (isspace((unsigned char)*start)) start++;
            strncpy(nodes[node_count].title, start, Max_Length - 1);
            nodes[node_count].title[Max_Length - 1] = '\0';
            nodes[node_count].parent_id = 0;
            // Find the parent node
            for (int i = node_count - 1; i >= 0; i --){
                if (nodes[i].level < level_count){
                    nodes[node_count].parent_id = nodes[i].id;
                    break;
                }
            }
            node_count++;
        }
        else {
            if (strlen(current_content)) strcat(current_content, "\n");
            if (strlen(current_content) + strlen(start) + 1 < Max_Length){
                strcat(current_content, start);
            }
            else{
                fprintf(stderr, "Content exceeds maximum length for node %d.\n", node_count);
            }
        }
    }
    if (node_count > 0){
        strncpy(nodes[node_count - 1].content, current_content, Max_Length - 1);
        nodes[node_count - 1].content[Max_Length - 1] = '\0';
    }
    fclose(fin);

    // Initialize graph and child_count
    int graph[node_count + 1][100];
    int child_count[node_count + 1];
    memset(graph, 0, sizeof(graph));
    memset(child_count, 0, sizeof(child_count));

    // Build the graph
    for (int i = 0; i < node_count; i ++){
        int parent = nodes[i].parent_id;
        if(parent >= 0 && parent <= node_count){
            if(child_count[parent] < 100){
                graph[parent][child_count[parent]++] = nodes[i].id;
            }
            else{
                fprintf(stderr, "Exceeded maximum children for node %d.\n", parent);
            }
        }
        else{
            fprintf(stderr, "Invalid parent ID %d for node %d.\n", parent, nodes[i].id);
        }
    }

    // Write JSON output
    fprintf(fout, "{\n");
    write_graph(graph, node_count, fout);
    write_node(nodes, node_count, fout);
    fprintf(fout, "}\n");
    fclose(fout);
    
    return 0;
}
