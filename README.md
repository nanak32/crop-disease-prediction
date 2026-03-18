# Crop Disease Expert System

An intelligent knowledge-based system for diagnosing crop diseases using Prolog logic programming and Python. This system leverages expert knowledge encoded as logical rules to help farmers and agricultural professionals identify crop diseases based on observed symptoms.

## 📋 Features

- **Interactive Diagnosis**: Step-by-step symptom confirmation interface
- **Knowledge-Based Reasoning**: Uses Prolog for logical disease inference
- **Multi-Crop Support**: Extensible architecture supporting multiple crop types
- **Disease Information**: Detailed descriptions and treatment recommendations for identified diseases
- **User-Friendly GUI**: Simple Tkinter interface for easy navigation
- **Modular Architecture**: Well-organized Python modules for maintainability

## 🏗️ Project Structure

```
agricultural-disease-prediction/
├── interface/                    # Python application code
│   ├── main.py                  # Entry point
│   ├── app.py                   # Tkinter GUI application
│   ├── knowledge_base.py        # Prolog interface layer
│   └── config.py                # UI and app configuration
├── knowledge_base/              # Prolog knowledge base
│   └── kb.pl                    # Disease rules, facts, and logic
├── docs/                        # Documentation
└── README.md                    # This file
```

## 🔧 Requirements

- **Python 3.8+**
- **SWI-Prolog** (must be installed and in system PATH)
- **PySwip** - Python SWI-Prolog bridge
- **Tkinter** - Usually included with Python

## 📦 Installation

### 1. Install SWI-Prolog

**Windows:**
```bash
# Download and install from: https://www.swi-prolog.org/download/stable
# Or use Chocolatey:
choco install swi-prolog
```

**macOS:**
```bash
brew install swi-prolog
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install swi-prolog
```

### 2. Clone the Repository

```bash
git clone https://github.com/yourusername/agricultural-disease-prediction.git
cd agricultural-disease-prediction
```

### 3. Install Python Dependencies

```bash
pip install pyswip
```

## ▶️ Running the Application

```bash
cd interface
python main.py
```

The GUI window will open with the crop selection screen.

## 📖 How to Use

1. **Select a Crop**: Choose the crop you want to diagnose (e.g., Maize, Tomato)
2. **Answer Questions**: For each disease, review the presented symptoms and answer:
	- **YES** if your crop shows those symptoms
	- **NO** if it doesn't (move to next disease)
3. **View Results**: See a list of identified diseases with:
	- Confirmed symptoms
	- Description of the disease
	- Treatment recommendations
4. **Start Over**: Use the "Start New Diagnosis" button to diagnose another crop

## 🧠 Knowledge Base Architecture

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

% Disease information
disease_info(maize, leaf_blight, Desc, Rec) :- ...
```

## 🔌 System Components

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

## 🛠️ Extending the System

### Add a New Crop

1. **Update `config.py`**:
```python
CROPS = [
	 ("maize", "🌽"),
	 ("tomato", "🍅"),
	 ("wheat", "🌾"),  # Add new crop
]
```

2. **Update `kb.pl`**:
```prolog
% Add disease facts
disease(wheat, septoria_tritici).
disease(wheat, powdery_mildew).

% Add symptom and description rules
symptom(wheat, septoria_tritici, [brown_spots, leaf_damage]).
disease_info(wheat, septoria_tritici, ...) :- ...
```

### Add a New Disease

1. Edit `kb.pl` and add:
	- Disease fact
	- Associated symptoms
	- Description and recommendations

## 📝 Configuration Options

Edit `interface/config.py` to customize:

- **Window size**: `WINDOW_WIDTH`, `WINDOW_HEIGHT`
- **Colors**: `COLORS` dictionary
- **Crops**: `CROPS` list
- **Knowledge base path**: `KB_PATH`

## ⚠️ Troubleshooting

### "Prolog not found" error
- Ensure SWI-Prolog is installed: `swipl --version`
- Add SWI-Prolog to system PATH if needed

### "kb.pl not found" error
- Verify `knowledge_base/kb.pl` exists
- Check KB_PATH in `config.py` points to correct location

### PySwip import error
- Install PySwip: `pip install pyswip`
- For Windows, you may need to build from source

## 📚 Technologies Used

- **Prolog**: Knowledge representation and logical inference
- **Python 3**: Application logic and orchestration
- **Tkinter**: Desktop GUI framework
- **PySwip**: Python-Prolog interface

## 📖 Academic Context

This project is part of **DCIT 313 - Knowledge-Based Systems** course, demonstrating:
- Knowledge engineering and representation
- Expert systems design
- Prolog programming
- Man-machine interfaces for intelligent systems

## 📄 License

[Specify your license here - e.g., MIT, GPL, etc.]

## 👤 Author

[Your name/organization]

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📧 Support

For issues and questions, please open an issue on GitHub.

*** End Patch

