# Daniel Couch
# Collection of routines/queries in Python for graph databases.
# Currently only has Cypher queries; Gremlin queries coming soon.

# TODO:

from neo4j.v1 import GraphDatabase, basic_auth
import gremlin_python
import sys

# Error messages go here.
ERR_INIT_1 = "Error - Failed to initialize DBRun..." \
        "db_type must be either 'neo4j' or 'tinkerpop'."
ERR_INIT_2 = "Error - Failed to initialize DBRun..." \
        "must provide database settings."
ERR_MISMATCH = "Error - Query failed..." \
        "number of labels and values must match."


# ID values for queries (only for those with serializable output)
QMATCH = 1
QNEIGHBORS = 2
QSP = 3
QSPS = 4
QMR = 5
QL = 6


class GDBC():
    """
    GDBC = Graph DataBase Connector
    Connects to given graph database (neo4j / tinkerpop)
    and executes queries in the database's query language
    (cypher / gremlin, respectively)
    """

    def __init__(self, db_type, db_url="", db_uname="", db_pw=""):
        """
        Initialize DBRun based , including a driver if using Neo4j.

        Args:
        db_type (str):  Either 'neo4j' or 'gremlin'.
        db_url (str):   URL of database.
        db_uname (str): Username to access database.
        db_pw (str):    Password to access database.

        TODO:
            - Allow additional parameters for authentication.
            - What is the connector for tinkerpop?
        """
        self.db_type = db_type
        # Initialize a driver if we're using Neo4j.
        # What if it's tinkerpop?
        if db_type == 'neo4j':
            if not (db_url and db_uname and db_pw):
                print("\n\n\nWarning --- URL, username, and password not all provided!!!\n\n\n")
            try:
                self.db_driver = GraphDatabase.driver(db_url,
                        auth=basic_auth(db_uname, db_pw))
            except:
                print(sys.exc_info()[0])
                raise
        elif db_type == 'tinkerpop':

            print("todo...")
        else:
            sys.exit(ERR_INIT_1)


    def validate_query(self, labels, id_types, id_vals):
        """
        The query methods here work by performing a set of queries,
        one for each element in the labels/id_vals/id_types.
        This method ensures that the query is valid; i.e. that
        each of the inputs are of the same length.

        Args:
        labels (list str):      The labels used for each query.
        id_types (list str):    The type of the id value in the database (e.g. uid).
        id_vals (list str):     The id values/lookup values for each query.
        """
        if type(labels) is str:
            labels = [labels]
            id_types = [id_types]
            id_vals = [id_vals]
            return [labels, id_types, id_vals]
        # Make sure query parameters match up.
        elif not (len(labels) == len(id_vals) == len(id_types)):
            sys.exit(ERR_MISMATCH)
        else:
            return [labels, id_types, id_vals]


    def convert_format(self, data, output_type, qid):
        """
        Convert data to an object of the given output_type.
        For instance, if output_type is "JSON" then we obtain
        a JSON object that can be directly placed into the frontend.

        Args:
        data (obj):         Results from a query in cypher or gremlin.
        output_type (str):  One of ['JSON'...].
        qid (int):          Identifier for query type, see header of gdb-py.py.
        """
        if output_type == "JSON":
            output_data = {"links": [], "nodes": []}
            if self.db_type == 'neo4j':
                records = data.records()
                if qid == QMATCH:
                    # Match should just give a single result.
                    if (records is None):
                        print("Warning --- no record found for MATCH")
                        return None
                    else:
                        for record in records:
                            extract_record = record[0]
                            new_node = extract_record["properties"]
                            new_node["id"] = extract_record["id"]
                            output_data["nodes"].append(new_node)
                elif qid == QNEIGHBORS:
                    for record in records:
                        rel = record['r']
                        node = record['m']
                        node_props = node.properties
                        node_props["id"] = node.id
                        output_data["nodes"].append(node.properties)
                        output_data["links"].append({"source": rel.start, "target": rel.end, "type": rel.type})
                elif qid == QSP:
                    for record in records:
                        record_nodes = record['nodes(p)']
                        # For each node, get its properties and ID.
                        for node in record_nodes:
                            node_properties = node.properties
                            node_properties["id"] = node.id
                            output_data["nodes"].append(node_properties)
                        record_relations = record["relationships(p)"]
                        for relation in record_relations:
                            output_data["links"].append({"source": relation.start,
                                "target": relation.end,
                                "type": relation.type})
                elif qid == QMR:
                    # TODO: Should be single... Go back and change this.
                    for record in records:
                        result = record[0]["properties"]
                        result["id"] = record[0]["id"]
                        output_data["nodes"].append(result["nodes"][0])
            else:
                print("Gremlin to go here.")

            if (output_data["nodes"] == [] and output_data["links"] == []):
                return None
        else:
            print("What other output data is there???")
        return output_data
    
    
    def match_node(self, labels, id_types, id_vals, output="JSON"):
        """
        Match a given label, id type and id value to its node
        in the database.

        Args:
        labels (list str):      The labels used for each query.
        id_types (list str):    The type of the id value in the database (e.g. uid).
        id_vals (list str):     The id values/lookup values for each query.
        output (str):           Output format of the method.
        """
        labels, id_types, id_vals = self.validate_query(labels, id_types, id_vals)
        if self.db_type == "neo4j":
            for query_num in range(len(labels)):
                label = labels[query_num]
                id_val = id_vals[query_num]
                id_type = id_types[query_num]
                query = "MATCH (n:%s {%s: \"%s\"}) RETURN {id:id(n), properties:properties(n)}" % (label, id_type, id_val)
                session = self.db_driver.session()
                result = session.run(query)
                session.close()

        return self.convert_format(result, output, QMATCH)


    def request_neighbors(self, labels, id_types, id_vals, output="JSON"):
        """
        For a set of nodes that belongs to a set of corresponding labels,
        find the neighbors for each of the node. 
        Query i is executed using the ith label, the ith id_type and the ith id_val.

        Args:
        labels (list str):      A list of the labels to be used.
        id_types (list str):    Identifiers to use for the queries.
        id_vals (list str):     Values of the ids to use.
        output (str):           Output format (JSON, ...)

        TODO:
            - Generalize relation exclusion.
        """
        labels, id_vals, id_types = self.validate_query(labels, id_vals, id_types)
        if self.db_type == 'neo4j':
            for query_num in range(len(labels)):
                label = labels[query_num]
                id_type= id_types[query_num]
                id_val= id_vals[query_num]
                # Construct query from parameters.
                query = "MATCH (n:" + label + "{" + id_type + ":\"" + id_val + "\"})-[r]-(m) WHERE type(r)<>\"has_synonym\" RETURN r, m"
                # Create session of database.
                session = self.db_driver.session()
                result = session.run(query)
                session.close()
        else:
            print("Coming soon...")
        return self.convert_format(result, output, QNEIGHBORS)


    def shortest_path(self, labels, id_types, id_vals, limit, length=None, output="JSON"):
        """
        IMPORTANT!!! This method does not compute the shortest path between more
        than TWO nodes (see the method group_shortest_paths). Rather, it computes
        the shortest path between two nodes. Also note the argument 'limit'.

        Args:
        labels (list str):      A list of the labels to be used.
        id_types (list str):    Identifiers to use for the queries.
        id_vals (list str):     Values of the ids to use.
        limit (int):            How many shortest paths to compute.
        output (str):           Output format (JSON, ...)
        """
        labels, id_vals, id_types = self.validate_query(labels, id_vals, id_types)
        if self.db_type == 'neo4j':
            # Set part of query that determines maximum length of shortest paths to consider.
            if length == None:
                length_param = ""
            else:
                length_param = ".." + str(length)
            query = "MATCH p=shortestPath((n:%s {%s:\"%s\"})-[*%s]-(m:%s{%s:\"%s\"})) RETURN nodes(p), relationships(p) LIMIT %s" % (labels[0], id_types[0], id_vals[0], 
                    length_param, 
                    labels[1], id_types[1], id_vals[1], str(limit))
            session = self.db_driver.session()
            result = session.run(query)
            session.close()
        else:
            print("Gremlin coming soon...")
        return self.convert_format(result, output, QSP)

    def group_shortest_paths(self, labels, id_types, id_vals, limit, output="JSON"):
        """
        Compute all shortest paths between sets of labels/vals/types.
        Done via combinatorial use of shortest_path.

        Args:
        labels (list str):      A list of the labels to be used.
        id_types (list str):    Identifiers to use for the queries.
        id_vals (list str):     Values of the ids to use.
        limit (int):            How many shortest paths to compute.
        output (str):           Output format (JSON, ...)
        """
        labels, id_vals, id_types = self.validate_query(labels, id_vals, id_types)
        # Store results of each shortest path in here.
        results = []
        # Construct 3-tuple of parameters from each query
        paramset = [(labels[i], id_types[i], id_vals[i]) for i in range(len(labels))]
        for param1 in list(paramset):
            for param2 in paramset:
                if param1 != param2:
                    labels = [param1[0], param2[0]]
                    id_types = [param1[1], param2[1]]
                    id_vals = [param[2], param2[2]]
                    results.append(self.shortest_path(labels, id_types, id_vals, limit, output))
            paramaset.remove(param1)
        return self.convert_format(results, output, QSPS)


    def match_relation(self, labels, id_types, id_vals, relation, output="JSON"):
        """
        Check for the existence of a relation between nodes.
        TCH (n:%s)-[has_synonym]-(m:Synonym {name: \"%s\"}) RETURN {id:id(n), pr    operties:properties(n)}" % (label, keyword)
        Args:
        labels (list str):      A list of the labels to be used.
        id_types (list str):    Identifiers to use for the queries.
        id_vals (list str):     Values of the ids to use.
        relation (str):         Name of the relation.
        output (str):           Output format (JSON, ...)
        """
        #labels, id_vals, id_types = self.validate_query(labels, id_vals, id_types)
        results = []
        if self.db_type == 'neo4j':
            query = "MATCH (n:%s)-[%s]-(m:%s {%s: \"%s\"}) RETURN {id:id(n), properties:properties(n)}" % (labels[0], relation, labels[1], id_types[1], id_vals[1])
            session = self.db_driver.session()
            results = session.run(query)
            session.close()
        return self.convert_format(results, output, QMR)

    def add_link(self, labels, node1_id, node2_id):
        """
        This method adds a d3-formatted link between two nodes given their ids.
        Currently assumes id lookup type is 'uid'.

        Args:
        labels (list):  A list of two strings; the labels that each node is in.
        node1_id (int): The id of one node in the database.
        node2_id (int): The id of the other node in the database.

        Returns:
            dict {source_id, target_id, relation_type} if it exists, else None.
        """
        link = None
        if self.db_type == 'neo4j':
            session = self.db_driver.session()
            query = "MATCH (n:%s {uid:\"%s\"})-[r]-(m:%s {uid:\"%s\"}) RETURN r" % (labels[0], node1_id, labels[1], node2_id)
            results = session.run(query)
            for rel in results.records():
                if rel:
                    link = {"source": rel['r'].start, "target": rel['r'].end, "type": rel['r'].type}
        return link


    def global_statistics(self):
        """
        Statistics for the entire graph.
        """
        if self.db_type == 'neo4j':
            pass
        return 0

    def single_node_statistics(self, label, id_type, id_val):
        """
        Computer various statistics for a single node.
        
        Args:
        label (str):    The label of the node.
        id_type (str):  Field to use for id.
        id_val (str):   Id value.

        Returns:
            List of statistics
        """
        # How many neighbors the node has.
        if self.db_type == 'neo4j':
            session = self.db_driver.session()
            num_neighbors_query = "MATCH (n:%s{%s:\"%s\"})-[r]-(m) WHERE type(r)<>\"has_synonym\" RETURN COUNT(m)" % (label, id_type, id_val)
            num_neighbors = session.run(num_neighbors_query).single()[0]
            return [num_neighbors]

