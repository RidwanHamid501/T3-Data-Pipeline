# Tasty Truck Treats (T3) Data Pipeline Project

<img src="https://everydaybest.com/wp-content/uploads/2013/04/food-truckin.jpg" style="width: 400px;" />

## Project Overview

Tasty Truck Treats (T3) operates a fleet of food trucks throughout Lichfield and surrounding areas, offering a variety of culinary options, from gourmet sandwiches to desserts. Each truck has a unique menu and operates semi-independently, allowing T3 to cater to diverse tastes across multiple high-traffic locations. Historically, T3 gathered only monthly sales summaries from each truck, which limited the company’s ability to make timely, data-informed decisions. This project seeks to implement an automated, transaction-level data pipeline to support real-time analytics and enhance T3's ability to optimize its operations, marketing, and menu offerings.

## Project Goals

The main objectives of the T3 data pipeline project are to:
- Build a centralized, automated system for collecting transaction-level data from each truck, providing T3 with real-time insights.
- Create a live, accessible dashboard for internal use by non-technical T3 employees to monitor truck performance.
- Produce regular, automated summary reports to inform executives and support strategic decision-making.

## Stakeholders

1. **Hiram Boulie (Chief Financial Officer)**  
   Hiram’s primary responsibilities include overseeing T3’s financial health and supporting acquisition discussions. His focus is on:
   - Reducing operational costs
   - Increasing overall profitability

2. **Miranda Courcelle (Head of Culinary Experience)**  
   Miranda manages truck menus and locations, aiming to ensure T3’s offerings remain appealing, affordable, and aligned with customer preferences. Her role involves leveraging data to understand customer demand by location and menu type, which is essential for her strategic planning.

## Key Components

The project pipeline includes three main workflows:

1. **ETL Pipeline**: A scheduled extraction, transformation, and loading task that reads transaction data from an S3 bucket, cleans it, and loads it into a cloud-based database.
2. **Dashboard Service**: A cloud-hosted dashboard that connects to the database, allowing stakeholders to view and analyze the most recent data.
3. **Report Generation**: A scheduled task that generates and emails daily summary reports, enabling T3 executives to track daily performance.

Each workflow operates independently but shares a central database, ensuring flexibility and minimizing dependencies among components.

## Deliverables

Upon completion, the project will deliver:
- A fully automated data pipeline for continuous extraction, transformation, and loading of transaction data.
- A live dashboard that enables real-time monitoring and analysis of truck performance.
- Daily summary reports sent to T3 executives, providing insights into the previous day’s performance.

## Summary

The T3 data pipeline project aims to enhance T3’s operational insights by transitioning from monthly sales summaries to a real-time, transaction-level data system. This solution will allow T3 to make informed decisions, optimize truck operations, and improve financial performance, supporting its growth and acquisition objectives.
