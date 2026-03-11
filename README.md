# 🍳 FlavorForge

> **FlavorForge** is a collaborative recipe platform where users can create, explore and improve recipes together.

The goal of the application is to simulate a **community-driven cooking platform** where chefs share recipes and experiment with variations to improve them.

---

## 🌍 Concept

FlavorForge allows users to:

- Discover recipes created by other users
- Add ingredients and cooking instructions
- Share **experiments** (variations of a recipe)
- Vote for the best experiments
- Analyze recipe trends using statistics

The platform encourages **collaboration and creativity in cooking**.

---

## 🚀 Features

### 👤 User System
- User registration
- Login / Logout
- Personalized content
- Recipe ownership protection

### 🍲 Recipes
- Create recipes
- Edit recipes
- Delete your own recipes
- Upload images
- Cooking instructions with steps

### 🥕 Ingredients
- Ingredient database
- Add ingredients to recipes
- Units (g, kg, ml, tsp, cup, etc.)
- Ingredient search system

### 🧪 Experiments
Users can propose improvements to a recipe.

Example:
> Add garlic  
> Use less salt  
> Cook longer  

Experiments can be **voted by the community**.

### 👍 Voting System
- Each user can vote only once
- Best experiments rise to the top

### 📊 Statistics Dashboard
The platform includes a statistics page with **5 interactive charts**:

- Recipes by difficulty
- Recipes created by user
- Recipes per month
- Most used ingredients
- Experiments per recipe

Charts are generated using **Chart.js**.

### 📈 Top Recipes
Displays the **Top 3 recipes** with the most experiments.

### 🔎 Search & Filters
Recipes can be filtered by:

- Name
- Difficulty
- Cooking time

### 📄 Pagination
Recipe lists include pagination to improve performance and usability.

---

## 🧪 Automated Tests

The project includes **42 automated tests** covering:

- Models
- Forms
- Views
- Authentication
- Pagination

All tests pass successfully.

---

## 🛠 Technologies Used

| Technology | Purpose |
|--------|--------|
| **Django** | Backend framework |
| **SQLite** | Database |
| **Bootstrap** | Frontend design |
| **Chart.js** | Data visualization |
| **Python** | Application logic |

---

## 🗂 Project Structure

```

flavorforge
│
├── recipes
│ ├── models.py
│ ├── views.py
│ ├── forms.py
│ ├── tests.py
│
├── templates
│
├── static
│
├── manage.py
│
└── README.md

````

---

## ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/flavorforge.git
````

Go to the project folder:

```bash
cd flavorforge
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start the server:

```bash
python manage.py runserver
```

Open in browser:

```
http://127.0.0.1:8000
```

---

## 📚 Academic Project

This project was developed as part of the **Web Application Development II course**.

It follows a rubric requiring:

* Multiple models and relationships
* Form validation
* Authentication
* Access control
* Statistics and data analysis
* Automated tests
* Pagination and filtering

---

# 👩‍💻 **Quién Está Detrás del Código**

<p align="center">
  <img src="https://github.com/user-attachments/assets/d549c019-35bb-4af8-8e61-8d6885c6cd9b" width="200">
</p>

**Oumniya — Developer & Designer**

---

## ⭐ Final Result

FlavorForge demonstrates how Django can be used to build a **collaborative platform with real-world features**, including authentication, data visualization and automated testing.



