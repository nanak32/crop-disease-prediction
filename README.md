# Crop Disease Prediction Expert System

An intelligent knowledge-based system for diagnosing crop diseases specifically **Maize** and **Tomato** using Prolog logic programming and Python. This system leverages expert knowledge encoded as logical rules to help farmers and agricultural professionals identify crop diseases based on observed symptoms.

## Features

- **Interactive Diagnosis**: Step-by-step symptom confirmation interface
- **Knowledge-Based Reasoning**: Uses Prolog for logical disease inference
- **Multi-Crop Support**: Extensible architecture supporting multiple crop types
- **Disease Information**: Detailed descriptions and treatment recommendations for identified diseases
- **User-Friendly GUI**: Simple Tkinter interface for easy navigation
- **Modular Architecture**: Well-organized Python modules for maintainability

## Requirements

- **Python 3.8+**
- **SWI-Prolog** (must be installed and in system PATH)
- **PySwip** - Python SWI-Prolog bridge
- **Tkinter** - Usually included with Python


## How to Use

1. **Select a Crop**: Choose the crop you want to diagnose (e.g., Maize, Tomato)
2. **Answer Questions**: For each disease, review the presented symptoms and answer:
	- **YES** if your crop shows those symptoms
	- **NO** if it doesn't (move to next disease)
3. **View Results**: See a list of identified diseases with:
	- Confirmed symptoms
	- Description of the disease
	- Treatment recommendations
4. **Start Over**: Use the "Start New Diagnosis" button to diagnose another crop

## Knowledge Base Architecture

The Prolog knowledge base (`kb.pl`) contains:

- **Disease Facts**: Definition of diseases per crop
- **Symptom Rules**: Symptoms associated with each disease
- **Query Predicates**: 
  - `get_all_diseases(Crop, Diseases)` - Lists all diseases for a crop
  - `get_disease_info(Crop, Disease, Symptoms, Description, Recommendation)` - Retrieves disease details

### Example Structure
```prolog
% Crop diseases
disease(maize, leaf_blight).
disease(maize, rust).
disease(tomato, early_blight).

% Disease symptoms
symptom(maize, leaf_blight, [yellowing, necrotic_spots, wilting]).
symptom(maize, rust, [orange_pustules, leaf_damage]).

```

## System Components

### `main.py`
Entry point that initializes and launches the application.

### `app.py`
Contains `ExpertSystemApp` class - the main Tkinter GUI application with screens for:
- Crop selection
- Symptom confirmation
- Results display

### `knowledge_base.py`
Contains `KnowledgeBase` class - bridges Python and Prolog:
- Initializes Prolog engine
- Loads knowledge base file
- Provides query methods for disease data

### `config.py`
Centralized configuration:
- Color palette for UI
- Window dimensions
- Crop definitions
- Knowledge base file path

## Technologies Used

- **Prolog**: Knowledge representation and logical inference
- **Python 3**: Application logic and orchestration
- **Tkinter**: Desktop GUI framework
- **PySwip**: Python-Prolog interface