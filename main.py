from neo4j import GraphDatabase
from swiplserver import PrologMQI

# Function to create a connection to Neo4j
def create_neo4j_connection(uri, user, password):
    return GraphDatabase.driver(uri, auth=(user, password))

# Function to create nodes and relationships in Neo4j
def create_neo4j_graph(driver):
    # Create a connection to Prolog server
    prolog_thread = PrologMQI().create_thread()

    # Consult the Prolog file
    prolog_thread.query("consult('D:/assignment/family.pl')")

    with driver.session() as session:
        # Define a dictionary to map Prolog predicates to Neo4j relationship types
        relationship_mapping = {
            "father": "FATHER_OF",
            "mother": "MOTHER_OF",
            "grandfather": "GRANDFATHER_OF",
            "grandmother": "GRANDMOTHER_OF",
            "uncle": "UNCLE_OF",
            "aunt": "AUNT_OF",
            "brother": "BROTHER_OF",
            "sister": "SISTER_OF"
        }

        # Iterate over each rule and query Prolog for relationships
        for prolog_rule, neo4j_relationship in relationship_mapping.items():
            # Query Prolog for relationships based on the rule
            for fact in prolog_thread.query(f"{prolog_rule}(X, Y)"):
                # Create nodes and relationships in Neo4j
                session.run(f"MERGE (person1:Person {{name: $person1_name}}) "
                            f"MERGE (person2:Person {{name: $person2_name}}) "
                            f"MERGE (person1)-[:{neo4j_relationship}]->(person2)",
                            person1_name=fact["X"], person2_name=fact["Y"])

    # Close Prolog connection
    del prolog_thread

def query_relationship(driver, person1_name, person2_name):
    with driver.session() as session:
        for relationship_type in ["FATHER_OF", "MOTHER_OF", "GRANDFATHER_OF", "GRANDMOTHER_OF", "UNCLE_OF", "AUNT_OF", "BROTHER_OF", "SISTER_OF"]:
            query = f"MATCH (p1:Person)-[r:{relationship_type}]->(p2:Person) WHERE p1.name = $person1_name AND p2.name = $person2_name RETURN type(r) AS relationship LIMIT 1"
            result = session.run(query, person1_name=person1_name, person2_name=person2_name)
            record = result.single()
            if record:
                if relationship_type == "FATHER_OF":
                    return(f"{person1_name} is father of {person2_name}")
                elif relationship_type == "MOTHER_OF":
                    return(f"{person1_name} is mother of {person2_name}")
                elif relationship_type == "GRANDFATHER_OF":
                    return(f"{person1_name} is grandfather of {person2_name}")
                elif relationship_type == "GRANDMOTHER_OF":
                    return(f"{person1_name} is grandmother of {person2_name}")
                elif relationship_type == "UNCLE_OF":
                    return(f"{person1_name} is uncle of {person2_name}")
                elif relationship_type == "AUNT_OF":
                    return(f"{person1_name} is aunt of {person2_name}")
                elif relationship_type == "BROTHER_OF":
                    return(f"{person1_name} is brother of {person2_name}")
                elif relationship_type == "SISTER_OF":
                    return(f"{person1_name} is sister of {person2_name}")
                break
        else:
            return("NO")

def get_all_node_names(driver):
    node_names = []
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN n.name AS name")
        for record in result:
            node_names.append(record["name"])
    return node_names

import spacy
import re

def add_custom_entity_rules(nlp):
    # Define lowercase names
    lowercase_names = ["ibtisam", "salman", "mahnoor", "mustafa", "ayesha", "eman", "saneeaa", "hira", "abdullah", "rehan"]

    # Add special cases for lowercase names
    for name in lowercase_names:
        nlp.tokenizer.add_special_case(name, [{"ORTH": name.lower()}])

    # Add special cases for relationship terms
    relationship_terms = ["uncle", "aunt", "brother", "sister"]
    for term in relationship_terms:
        nlp.tokenizer.add_special_case(term, [{"ORTH": term}])

    # Define patterns to match lowercase names
    patterns = [{"label": "PERSON", "pattern": [{"LOWER": {"IN": lowercase_names}}]}]

    # Add a new rule to the entity recognizer
    ruler = nlp.add_pipe("entity_ruler")
    ruler.add_patterns(patterns)

nlp = spacy.load("en_core_web_sm")
add_custom_entity_rules(nlp)


def extract_name(input_text):
    # Process the input text using spaCy
    doc = nlp(input_text)
    
    # Extract entities from the processed text
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Filter entities labeled as PERSON (names)
    names = [entity[0] for entity in entities if entity[1] == 'PERSON']
    
    return names


def extract_relationship(input_text):
    # Define patterns to extract person name and relationship
    patterns = [
        (r"tell me about (.+)'s relationship", lambda match: (match.group(1), "relationship")),
        (r"who is (.+)'s (.+)", lambda match: (match.group(1), match.group(2))),
        (r"who is the brother of (.+)", lambda match: (match.group(2), match.group(1))),
    ]
    
    # Try to match input text with each pattern
    for pattern, extractor in patterns:
        match = re.match(pattern, input_text.lower())
        if match:
            return extractor(match)
    
    return None, None

#NEO4J SECTION
neo4j_uri = "bolt://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "12345678"
driver = create_neo4j_connection(neo4j_uri, neo4j_user, neo4j_password)
create_neo4j_graph(driver)
names = []
names = get_all_node_names(driver)


#main SECTION

while True:
    name_to_check = input("Hello, How can I help You: ")
    if name_to_check.lower() == 'exit':
        break
    
    name_to_check = extract_name(name_to_check)
    name_to_check = ', '.join(name_to_check)
    name_to_check = name_to_check.lower()
    
    for name in names:
        check = query_relationship(driver, name_to_check, name)
        if check != "NO":
            print(check)
            break
    else:
        print(f"Sorry, we don't know how {name_to_check} is related to anyone.")

driver.close()