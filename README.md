---
# Bellabeat Case Study – Smart Device Usage Analysis  

## Project Overview  
This case study analyzes user activity data from Bellabeat smart devices to uncover usage trends, behavioral insights, and recommendations for improving Bellabeat’s product marketing strategy. The project focuses on one of Bellabeat's key products, the **Time wellness watch**, which tracks activity, sleep, and stress.  

## Business Task  
Identify how users interact with Bellabeat's smart devices and provide actionable insights to guide future marketing decisions.  

## Data Source  
The dataset was made publicly available through [FitBit Fitness Tracker Data](https://www.kaggle.com/datasets/arashnic/fitbit).  
Data used in this project includes:  
- Daily activity  
- Sleep tracking  
- Heart rate  
- Step counts  
- Calorie expenditure  
- Weight and BMI  

## Tools & Technologies  
- **Python**: Data cleaning, analysis, and statistical exploration  
- **Pandas, NumPy, Matplotlib, Seaborn**: EDA and visualizations  
- **Power BI**: Data modeling and interactive dashboard creation  

## Data Cleaning & Preparation  
Performed using Python. Key steps:  
- Merged and standardized datasets  
- Converted date/time formats for consistency  
- Removed duplicates and null values  
- Created features for analysis (e.g., active minutes by intensity level)  

## 📊 Analysis Summary  
- Users with higher activity minutes tend to burn more calories  
- Peak heart rate aligns with working hours, showing users’ most active periods  
- Longer sleep durations correlate with lower step counts  
- Majority of users are in a sedentary category, with very few being highly active  
- Activity is lower on weekends compared to weekdays  
---

## Dashboard Overview  

An interactive Power BI dashboard was created to summarize all key metrics and trends from the analysis.  
It includes:  
- Daily activity and step trends  
- Sleep vs activity comparisons  
- Heart rate by hour  
- Weekly and user-level behavioral patterns  
- Calorie burn vs intensity correlations  

![image](https://github.com/user-attachments/assets/00280355-4ad1-4459-a1ba-cc82d2a3b191)
![image](https://github.com/user-attachments/assets/87827e80-c0cb-40c9-a9a7-36ba79dd0076)

**Insight Highlights:**  
- Majority of users are sedentary and need engagement nudges  
- Active minutes and calorie burn have a strong direct relationship  
- Users are less active on weekends  
- Peak activity (heart rate) aligns with daytime routines  
- Higher sleep duration often links to lower step counts  

---

## Recommendations  
- Develop personalized notifications to encourage higher activity levels in sedentary users  
- Promote weekend wellness campaigns to balance out drop in activity  
- Introduce sleep/activity balance insights in the app to guide healthier routines  
- Market Time as a lifestyle tool to promote habit-building among less active users  

## Folder Structure  
```
/notebooks          # Jupyter notebooks for EDA and data cleaning  
/visualizations     # Saved images of plots used in the report  
/dashboard.pbix     # Power BI dashboard file  
/README.md          # Project documentation  
```

## License  
This project is shared publicly for viewing and inspiration. For use in your own projects, please contact the repository owner.  

---
