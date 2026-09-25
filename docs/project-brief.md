# Project brief

**Earthquake magnitude estimation | Python · pandas · scikit-learn · Matplotlib · Seaborn**

Rachid EL MAGROUA — Network & Cybersecurity Engineer  
[LinkedIn](https://www.linkedin.com/in/rachid-el-magroua/) · [GitHub](https://github.com/rachidelmagrouaIng)

## Problem and approach

This academic group project studies how regression models estimate magnitude from recorded earthquake attributes. The workflow covers data exploration, missing values, outliers, categorical encoding, ensemble models and evaluation. Repository maintenance adds a separate chronological benchmark with event deduplication and train-only preprocessing.

## Skills demonstrated by the repository

| Skill | Evidence |
| --- | --- |
| Data analysis | Descriptive statistics, distributions and correlation plots in the v2 notebook |
| Model development | Random Forest, Gradient Boosting and GridSearchCV experiments |
| Evaluation | MAE, MSE, RMSE, R² and a median baseline |
| Data quality review | Repeated event IDs, schema checks and explicit leakage discussion |
| Reproducibility | Pinned dependencies, fixed evaluation seed, dataset hash and exported predictions |
| Software practices | Command-line entry point, five pipeline tests and GitHub Actions configuration |
| Technical communication | English/French overview, academic report and documented limitations |

These are team-project and repository capabilities. The source materials do not assign each implementation task to a specific team member.

## Result to discuss

The maintained evaluation uses 602 unique event IDs, split into 481 training and 121 later test events. With longitude, latitude and depth, Gradient Boosting obtains MAE **0.401** and R² **0.582** on this holdout. This is retrospective regression on observed events. It does not forecast future earthquakes.

The key lesson is that attractive model scores need a credible evaluation design. The historical notebooks produce much lower errors, but repeated events, preprocessing before the split and target-related catalog attributes limit those results.

## Current development

The academic experiments are available. Current repository work focuses on documentation and reproducibility; planned extensions include rolling temporal evaluation, regional holdouts and error analysis. See [ROADMAP.md](../ROADMAP.md).

## Team and context

Academic year: 2024/2025. Team: Rachid EL MAGROUA, Anas DARRAZ, Ilyas MAJDOUBI and Nabil EL HILALI. Supervisor: Asmae BENTALB.

My primary focus is networks and cybersecurity. This project complements that background with Python data analysis and evidence-based model evaluation.
