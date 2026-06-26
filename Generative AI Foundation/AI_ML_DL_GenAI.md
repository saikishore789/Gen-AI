This is one of the most common interview questions. The easiest way to understand it is to see them as a hierarchy:

```
Artificial Intelligence (AI)
│
├── Machine Learning (ML)
│   │
│   └── Deep Learning (DL)
│        │
│        └── Generative AI (GenAI)
```

Think of them like this:

* **AI** = The goal (make machines intelligent)
* **ML** = One way to achieve AI
* **DL** = One advanced ML technique
* **GenAI** = A DL application that creates new content

---

# 1. Artificial Intelligence (AI)

AI is the broad field of making computers perform tasks that normally require human intelligence.

Examples:

* Playing chess
* Driving a car
* Understanding speech
* Translating languages
* Medical diagnosis
* Chatbots

It does **not** always involve learning.

Example:

Imagine a calculator that always follows predefined rules.

```
IF fever > 102
AND cough = yes
THEN recommend doctor
```

This is AI because it mimics expert decision-making, but it doesn't learn.

### Types of AI

Rule-based AI

```
IF age > 18
THEN eligible
```

Learning AI

Learns from data instead of writing thousands of rules.

---

# 2. Machine Learning (ML)

Machine Learning is a subset of AI where computers learn patterns from data instead of programmers writing every rule.

Instead of:

```
IF salary > 50000
Approve loan
```

We give historical data.

```
Age   Salary   Loan Approved
25    30000    No
40    90000    Yes
35    75000    Yes
```

The ML model discovers the relationship itself.

### Workflow

```
Historical Data
        ↓
Train Model
        ↓
Model learns patterns
        ↓
Predict new data
```

Example

Email Spam Detection

Training data

```
Email                         Spam?
-------------
Win iPhone                     Yes
Meeting tomorrow               No
Get free money                 Yes
```

After training

New email

```
Claim your free lottery
```

Prediction

```
Spam
```

No rules were manually written.

---

## Types of ML

### Supervised Learning

Data has labels.

```
House Size → Price
```

Learn:

```
2000 sqft → ₹80L
```

Predict:

```
2500 sqft → ?
```

Examples

* House price prediction
* Disease prediction
* Fraud detection

---

### Unsupervised Learning

No labels.

Find hidden groups.

Customer data

```
Customer A
Customer B
Customer C
```

Algorithm automatically groups

```
Premium customers
Budget customers
Regular customers
```

Examples

* Customer segmentation
* Recommendation systems

---

### Reinforcement Learning

Learning by rewards.

Robot

```
Move Left
Reward +10

Move Right
Reward -5
```

Eventually it learns the best actions.

Examples

* Self-driving cars
* Robotics
* Games

---

# 3. Deep Learning (DL)

Deep Learning is a subset of ML that uses neural networks with many layers.

Inspired by the human brain.

Traditional ML

```
Input
 ↓
Algorithm
 ↓
Prediction
```

Deep Learning

```
Input
 ↓
Neural Network
 ↓
Hidden Layer
 ↓
Hidden Layer
 ↓
Hidden Layer
 ↓
Prediction
```

The network automatically learns complex features.

Example

Image Recognition

Instead of manually detecting

* Eyes
* Nose
* Ears

Deep Learning automatically learns them.

Input

```
Image
```

Output

```
Cat
```

No manual feature engineering.

---

## Why Deep Learning?

It performs well when there is lots of data.

Examples

* Face recognition
* Speech recognition
* Autonomous driving
* Image classification

---

# 4. Generative AI (GenAI)

Generative AI is a specialized area of Deep Learning that creates new content.

Instead of predicting something...

It generates something.

Examples

Input

```
Write Python code
```

Output

```
Python program
```

Input

```
Create an image of Mars
```

Output

```
New AI-generated image
```

Input

```
Summarize PDF
```

Output

```
Generated summary
```

Unlike traditional ML:

Traditional ML

```
Image
↓
Dog
```

GenAI

```
Text
↓
Generate Dog Image
```

---

# Comparison

| Feature               | AI                        | ML              | DL                                           | GenAI                               |
| --------------------- | ------------------------- | --------------- | -------------------------------------------- | ----------------------------------- |
| Goal                  | Make machines intelligent | Learn from data | Learn complex patterns using neural networks | Generate new content                |
| Needs data?           | Not always                | Yes             | Yes (typically large datasets)               | Yes (typically very large datasets) |
| Learns automatically? | Sometimes                 | Yes             | Yes                                          | Yes                                 |
| Creates new content?  | Usually No                | No              | Mostly No                                    | Yes                                 |
| Typical output        | Decision                  | Prediction      | Prediction                                   | Text, images, audio, video, code    |
| Example               | Chess program             | Spam filter     | Face recognition                             | ChatGPT, image generators           |

---

# Real-world Examples

### Netflix

```
AI
```

Overall intelligent recommendation system.

```
ML
```

Learns your viewing habits.

```
DL
```

Understands video thumbnails and user behavior.

```
GenAI
```

Can generate personalized movie descriptions or promotional artwork.

---

### Banking

AI

```
Virtual assistant
```

ML

```
Fraud detection
```

DL

```
Signature verification
```

GenAI

```
Generate customer email responses
```

---

### Healthcare

AI

```
Hospital chatbot
```

ML

```
Predict diabetes risk
```

DL

```
Detect tumors from MRI images
```

GenAI

```
Generate medical report drafts
```

---

# Interview-Friendly Summary

> **Artificial Intelligence (AI)** is the broad field of building systems that perform tasks requiring human intelligence. **Machine Learning (ML)** is a subset of AI where systems learn patterns from data instead of relying on explicit rules. **Deep Learning (DL)** is a subset of ML that uses multi-layer neural networks to solve complex problems like image and speech recognition. **Generative AI (GenAI)** is a subset of deep learning focused on creating new content such as text, images, audio, video, or code. Tools like ChatGPT use large deep learning models trained on vast datasets to generate human-like responses.

### One-line analogy

Imagine teaching a child:

* **AI:** The goal is to make the child intelligent.
* **ML:** The child learns by studying examples.
* **DL:** The child develops deep understanding by processing many examples through multiple levels of reasoning.
* **GenAI:** The child uses that understanding to create something new—like writing a story, drawing a picture, composing music, or generating computer code.
