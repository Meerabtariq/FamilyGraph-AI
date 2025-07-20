# FamilyGraph AI

**FamilyGraph AI** is a chatbot that uses **Prolog rules**, **Neo4j graph database**, and **NLP (SpaCy)** to answer family relationship queries.  
Example:
- **"Who is Ayesha?"** → *Ayesha is mother of Salman.*
  
---

## Features
- Prolog-based family tree (`family.pl`).
- Neo4j graph for storing relationships as nodes and edges.
- NLP (SpaCy) for understanding natural language queries.
- Interactive terminal-based chatbot.

---

## Project Structure
FamilyGraphAI/
│── main.py
│── family.pl
│── requirements.txt
│── README.md

---

## Install Requirements
pip install -r requirements.txt
python -m spacy download en_core_web_sm

---

## Set Up Neo4j
Run Neo4j on bolt://localhost:7687.
Update main.py if username/password are different.

---

## Run the Project
python main.py
