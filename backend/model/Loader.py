import os
import json
from model.Node import Node

class GraphLoader:
    def __init__(self, ProjectName, rootDir) :
        self.ProjectName = ProjectName
        self.configLoader = ConfigLoader(ProjectName, rootDir)
        self.nodeLoader = NodeLoader(ProjectName, rootDir)
        return

class ConfigLoader:
    def __init__(self, ProjectName, rootDir) :
        self.ProjectName = ProjectName
        self.rootDir = rootDir
        self.nodeConfig = self.loadNodeConfig()
        self.structureConfig = self.loadStructureConfig()
        return

    def loadStructureConfig(self):
        structPath = os.path.join(self.rootDir, self.ProjectName, "structure.json")
        if not os.path.exists(structPath):
            print("Structure file not found")
            return {}
        with open(structPath, 'r') as f:
            return json.load(f)

    def loadNodeConfig(self):
        nodePath = os.path.join(self.rootDir, self.ProjectName, "node.json")
        if not os.path.exists(nodePath):
            print("Node file not found")
            return {}
        with open(nodePath, 'r') as f:
            return json.load(f)

    def getNodeConfig(self):
        return self.nodeConfig

    def getStructureConfig(self):
        return self.structureConfig
    def writeNodeConfig(self, nodeConfig):
        nodePath = os.path.join(self.rootDir, self.ProjectName, "node.json")
        with open(nodePath, 'w') as f:
            json.dump(nodeConfig, f)
        return
    def writeStructureConfig(self, structureConfig):
        structPath = os.path.join(self.rootDir, self.ProjectName, "structure.json")
        with open(structPath, 'w') as f:
            json.dump(structureConfig, f)
        return

class NodeLoader:
    def __init__(self, ProjectName, rootDir) :
        self.ProjectName = ProjectName
        self.rootDir = rootDir
        self.NodePath = os.path.join(self.rootDir, self.ProjectName)
        return

    def NodePath(self, NodeID):
        return os.path.join(self.NodePath, NodeID)

    def loadNode(self, NodeID):
        nodePath = self.NodePath(NodeID)
        if not os.path.exists(nodePath):
            print("Node file not found")
            return {}
        with open(nodePath, 'r') as f:
            return Node(json.load(f))
    def writeNode(self, NodeID, node):
        nodePath = self.NodePath(NodeID)
        with open(nodePath, 'w') as f:
            json.dump(node.exportJson(), f)
        return

    def getNodes(self, NodeIDList) :
        nodeList = []
        for NodeID in NodeIDList:
            node = self.loadNode(NodeID)
            nodeList.append(Node(node))
        return nodeList
    def writeNodes(self, nodeList) :
        for node in nodeList:
            self.writeNode(node.ID, node)
        return
