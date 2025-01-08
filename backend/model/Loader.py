import os
import json
from backend.model.Node import Node

class ReadWriteLoader:
    def __init__(self,dirPath):
        self.dirPath = dirPath
        return
    def exists(self,file):
        print("Path: ",os.path.join(self.dirPath,file))
        return os.path.exists(os.path.join(self.dirPath,file))
    def read(self,file):
        if not self.exists(file):
            return {}
        with open(os.path.join(self.dirPath,file), 'r') as f:
            return json.load(f)
    def write(self,file, data):
        with open(os.path.join(self.dirPath,file), 'w') as f:
            json.dump(data, f)
        return
# Requirement: project Id and the root Dir
# Parent of : Nodeloader, configLoader
# should also read the config file and the node file
class GraphLoader:
    def __init__(self, ProjectName, rootDir) :
        self.ProjectName = ProjectName
        os.makedirs(os.path.join(rootDir, "Node"), exist_ok=True)
        self.nodeLoader = NodeLoader(ReadWriteLoader(os.path.join(rootDir, "Node")))
        self.ifNotExistsCreate(ProjectName, os.path.join(rootDir,"Project"))
        # self.configLoader = ConfigLoader(ProjectName,os.path.join(rootDir,"Project"))
        self.configLoader = ConfigLoader(ReadWriteLoader(os.path.join(rootDir, "Project", ProjectName)))
        return
    def ifNotExistsCreate(self, ProjectName, rootDir):
        print(os.path.join(rootDir, ProjectName))
        if os.path.exists(os.path.join(rootDir, ProjectName)):
            return
        os.makedirs(os.path.join(rootDir, ProjectName))
        rootNode = Node(True, {"title":"Root"})
        # check if structure.json exists
        structPath = os.path.join(rootDir, ProjectName, "structure.json")
        if not os.path.exists(structPath):
            with open(structPath, 'w') as f:
                json.dump({f"{rootNode.ID}" : [],"nodeTitle":{f"{rootNode.ID}" : f"{rootNode.title}"}}, f)
                # check if node.json exists
        nodePath = os.path.join(rootDir, ProjectName, "node.json")
        if not os.path.exists(nodePath):
            with open(nodePath, 'w') as f:
                json.dump({"K":200}, f)
        self.nodeLoader.writeNodes([rootNode])
        return
    def createNode(self, nodeTitle="New Node", nodeContent=None) :
        newNode = Node(True, {"title":nodeTitle, "content":nodeContent})
        self.nodeLoader.writeNode(newNode.ID, newNode)
        self.configLoader.structureConfig[newNode.ID] = []
        self.configLoader.structureConfig.setdefault("nodeTitle",{})[newNode.ID] = newNode.title
        return newNode.ID
    def insertNodeUrl(self, NodeID, data) :
        node = Node(False,self.nodeLoader.loadNode(NodeID))
        node.insertUrl(data.urlType.value, data)
        self.nodeLoader.writeNode(NodeID, node)
        return node.exportJson()
    def nodeExists(self, NodeID) :
        return self.nodeLoader.nodeExists(NodeID)
    def getNode(self, NodeID) :
        return self.nodeLoader.loadNode(NodeID)
    def createEdge(self,startNodeId, endNodeId):
        self.configLoader.structureConfig[startNodeId].append(endNodeId)
        self.configLoader.writeStructureConfig()
        return self.configLoader.getStructureConfig()
    def setStructureConfigDict(self, key, value) :
        return self.configLoader.setStructureConfig(key, value)
    def getStructure(self) :
        return self.configLoader.getStructureConfig()
    def getNodeConfig(self) :
        return self.configLoader.getNodeConfig()
    def close(self) :
        self.configLoader.writeNodeConfig()
        self.configLoader.writeStructureConfig()
        return
    def importJson(self, json) :
        if "Graph" not in json :
            return {"status": "404", "message": "Invalid Json, Graph key not found"}
        if "Node" not in json :
            return {"status": "404", "message": "Invalid Json, Node key not found"}
        Graph :dict = json["Graph"]
        Node :dict = json["Node"]
        # create node for each node in the json and have the dictionry , the key is the origin and the value is the Id
        NodeIdDict = {
            key: self.createNode(nodeTitle=value["Title"], nodeContent=value["Content"]) for key, value in Node.items()
        }
        for key, value in Graph.items():
            for node in value:
                self.createEdge(NodeIdDict[key], NodeIdDict[node])
        return {"status": "200", "message": "Json imported successfully", "Structure": self.getStructure()}



# Requirement
class ConfigLoader:
    def __init__(self, rwLoader: ReadWriteLoader):
        self.rwLoader = rwLoader
        self.nodeConfig = self.loadNodeConfig()
        self.structureConfig = self.loadStructureConfig()
        return
    def loadStructureConfig(self):
        return self.rwLoader.read("structure.json")
    def loadNodeConfig(self):
        return self.rwLoader.read("node.json")
    def nodeIdList(self) :
        return list(self.structureConfig.keys())
    def setStructureConfig(self, key, value: dict) :
        if key == "structure" :
            return {"status": "404", "message": "Invalid key, structure key can ony be set by the createEdge, createNode method"}
        self.structureConfig[key] = value
        return {"status": "200", "message": "Config set successfully", "structureConfig": self.structureConfig}
    def getNodeConfig(self):
        return self.nodeConfig
    def getStructureConfig(self):
        return self.structureConfig
    def writeNodeConfig(self):
        return self.rwLoader.write("node.json", self.nodeConfig)
    def writeStructureConfig(self):
        return self.rwLoader.write("structure.json", self.structureConfig)

class NodeLoader:
    def __init__(self, rwLoader: ReadWriteLoader) :
        self.rwLoader = rwLoader
        return
    def nodeExists(self, NodeID):
        return self.rwLoader.exists(NodeID)
    def loadNode(self, NodeID):
        return self.rwLoader.read(NodeID)
    def writeNode(self, NodeID, node):
        return self.rwLoader.write(NodeID, node.exportJson())
    def getNodes(self, NodeIDList) :
        nodeList = []
        for NodeID in NodeIDList:
            node = self.loadNode(NodeID)
            nodeList.append(Node(False,node))
        return nodeList
    def writeNodes(self, nodeList: list[Node]) :
        for node in nodeList:
            self.writeNode(node.ID, node)
        return

