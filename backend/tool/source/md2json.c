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
 
void input_file(char name[Max_Length], FILE **fin, FILE **fout){
    *fin = fopen(name, "r");
    name[strlen(name) - 2] = '\0';
    strcat(name, "json");
    *fout = fopen(name, "w");
}
void write_graph(int graph[][100], int n, FILE *fp){
    fprintf(fp, "\"Graph\": {\n");
    for (int i = 1; i <= n; i ++){
        fprintf(fp, "\t\"%d\":[", i);
        int j = 0;
        for (; graph[i][j + 1]; j ++){
            fprintf(fp, "\"%d\",", graph[i][j]);
        }
        if (graph[i][j]) fprintf(fp, "\"%d\"", graph[i][j]);
        if( i == n )
          fprintf(fp, "]\n");
        else
          fprintf(fp, "],\n");
    }
    fprintf(fp, "},\n");
}
void write_node(Node *nodes, int node_count, FILE *fp){
    fprintf(fp, "\"Node\": {\n");
    for (int i = 0; i < node_count; i++) {
        fprintf(fp, "\"%d\": {\n", nodes[i].id);
        fprintf(fp, "\"Title\": \"%s\",\n", nodes[i].title);
        fprintf(fp, "\"Content\": \"%s\"\n", nodes[i].content);
        fprintf(fp, "}%s\n", (i == node_count - 1) ? "" : ",");
    }
    fprintf(fp, "}\n");
}
 
 
int main(){
    char str[Max_Length];
    scanf("%s", str);
    FILE *fin, *fout;
    input_file(str, &fin, &fout);
    Node nodes[100];
    int node_count = 0;
    char line[Max_Length], current_content[Max_Length] = "";
    while (fgets(line, Max_Length, fin)){
        char *start = line;
        while (isspace(*start)) start ++;
        char *end = start + strlen(start) - 1;
        while (end > start && isspace(*end)) *end-- = '\0';
        if (start[0] == '#'){
            if (node_count > 0){
                strncpy(nodes[node_count - 1].content, current_content, Max_Length);
                current_content[0] = '\0';
            }
            nodes[node_count].id = node_count + 1;
            int level_count = 0;
            while (*start == '#') start ++, level_count ++;
            nodes[node_count].level = level_count;
            while (isspace(*start)) start++;
            strncpy(nodes[node_count].title, start, Max_Length);
            nodes[node_count].parent_id = 0;
            for (int i = node_count - 1; i >= 0; i --){
                if (nodes[i].level < level_count){
                    nodes[node_count].parent_id = nodes[i].id;
                    break;
                }
            }
            node_count++;
        }
        else {
            if (strlen(current_content)) strcat(current_content, "\\n");
            if (strlen(current_content) + strlen(start) + 1 < Max_Length){
                strcat(current_content, start);
            }
        }
    }
    if (node_count > 0){
        strncpy(nodes[node_count - 1].content, current_content, Max_Length);
    }
    int graph[node_count + 1][100];
    int child_count[node_count + 1];
    memset(graph, 0, sizeof(graph));
    memset(child_count, 0, sizeof(child_count));
    for (int i = 0; i < node_count; i ++){
        graph[nodes[i].parent_id][child_count[nodes[i].parent_id] ++] = nodes[i].id;
    }
    fprintf(fout, "{\n");
    write_graph(graph, node_count, fout);
    write_node(nodes, node_count, fout);
    fprintf(fout, "}");
    return 0;
}
