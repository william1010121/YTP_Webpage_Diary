#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cctype>
#include <algorithm>

// Helper function to trim whitespace from both ends of a string
std::string trim(const std::string &s) {
    size_t start = s.find_first_not_of(" \t\r\n");
    if (start == std::string::npos) return "";
    size_t end = s.find_last_not_of(" \t\r\n");
    return s.substr(start, end - start + 1);
}

// Escape JSON special characters in a string
std::string json_escape(const std::string &src) {
    std::ostringstream oss;
    for (char c : src) {
        switch (c) {
            case '\"': oss << "\\\""; break;
            case '\\': oss << "\\\\"; break;
            case '\t': oss << "\\t";  break;
            case '\n': oss << "\\n";  break;
            default:   oss << c;      break;
        }
    }
    return oss.str();
}

struct Node {
    int id;
    int parent_id;
    int level;
    std::string title;
    std::string content;
};

// Write the graph structure as a JSON object.
// The graph vector is indexed from 0 to nodes.size(), where index 0 holds nodes with no parent.
void write_graph(const std::vector<std::vector<int>> &graph, std::ostream &os) {
    os << "\t\"Graph\": {\n";
    // We output entries for nodes with id from 1 to n.
    for (size_t i = 1; i < graph.size(); i++) {
        os << "\t\t\"" << i << "\": [";
        for (size_t j = 0; j < graph[i].size(); j++) {
            if (j > 0) os << ", ";
            os << "\"" << graph[i][j] << "\"";
        }
        os << "]";
        if (i != graph.size() - 1)
            os << ",\n";
        else
            os << "\n";
    }
    os << "\t},\n";
}

// Write the nodes as a JSON object.
void write_node(const std::vector<Node> &nodes, std::ostream &os) {
    os << "\t\"Node\": {\n";
    for (size_t i = 0; i < nodes.size(); i++) {
        os << "\t\t\"" << nodes[i].id << "\": {\n";
        os << "\t\t\t\"Title\": \"" << json_escape(nodes[i].title) << "\",\n";
        os << "\t\t\t\"Content\": \"" << json_escape(nodes[i].content) << "\"\n";
        os << "\t\t}";
        if (i != nodes.size() - 1)
            os << ",\n";
        else
            os << "\n";
    }
    os << "\t}\n";
}

int main() {
    std::string inputFilename;
    if (!(std::cin >> inputFilename)) {
        std::cerr << "Error reading input filename." << std::endl;
        return 1;
    }

    // Generate output filename by replacing ".md" with ".json" if present
    std::string outputFilename = inputFilename;
    size_t pos = outputFilename.rfind(".md");
    if (pos != std::string::npos && pos == outputFilename.size() - 3) {
        outputFilename.replace(pos, 3, ".json");
    } else {
        outputFilename += ".json";
    }

    std::ifstream fin(inputFilename);
    if (!fin) {
        std::cerr << "Could not open input file: " << inputFilename << std::endl;
        return 1;
    }
    std::ofstream fout(outputFilename);
    if (!fout) {
        std::cerr << "Could not open output file: " << outputFilename << std::endl;
        return 1;
    }

    std::vector<Node> nodes;
    std::string line;
    std::string currentContent;  // Accumulate content lines for the current node

    while (std::getline(fin, line)) {
        std::string trimmed = trim(line);
        if (trimmed.empty())
            continue;

        // Check if the line is a node header (starts with '#')
        if (trimmed[0] == '#') {
            // Save content to previous node if any
            if (!nodes.empty()) {
                nodes.back().content = currentContent;
                currentContent.clear();
            }
            if (nodes.size() >= 100) {
                std::cerr << "Exceeded maximum number of nodes (100)." << std::endl;
                break;
            }
            Node newNode;
            newNode.id = nodes.size() + 1;

            // Count number of '#' characters to determine the level
            int levelCount = 0;
            size_t pos = 0;
            while (pos < trimmed.size() && trimmed[pos] == '#') {
                ++levelCount;
                ++pos;
            }
            newNode.level = levelCount;
            // Skip any additional whitespace after the '#' characters
            while (pos < trimmed.size() && std::isspace(static_cast<unsigned char>(trimmed[pos]))) {
                ++pos;
            }
            newNode.title = trimmed.substr(pos);
            newNode.parent_id = 0; // Default: no parent

            // Find the parent: the nearest previous node with a lower level
            for (int i = static_cast<int>(nodes.size()) - 1; i >= 0; i--) {
                if (nodes[i].level < newNode.level) {
                    newNode.parent_id = nodes[i].id;
                    break;
                }
            }
            nodes.push_back(newNode);
        } else {
            // Append line to current node's content (with newline if needed)
            if (!currentContent.empty())
                currentContent += "\n";
            currentContent += trimmed;
        }
    }
    // Save the last node's content
    if (!nodes.empty()) {
        nodes.back().content = currentContent;
    }
    fin.close();

    // Build the graph: graph[0] holds nodes with no parent; for others, graph[parent_id] holds children.
    std::vector<std::vector<int>> graph(nodes.size() + 1);
    for (const auto &node : nodes) {
        int parent = node.parent_id;
        if (parent >= 0 && parent <= static_cast<int>(nodes.size())) {
            graph[parent].push_back(node.id);
        } else {
            std::cerr << "Invalid parent ID " << parent << " for node " << node.id << std::endl;
        }
    }

    // Write JSON output
    fout << "{\n";
    write_graph(graph, fout);
    write_node(nodes, fout);
    fout << "}\n";
    fout.close();

    std::cout << "JSON output has been written to " << outputFilename << std::endl;
    return 0;
}

