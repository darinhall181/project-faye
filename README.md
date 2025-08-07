# Project Faye

Buntin group is an independent advertising agency recognized by ADWEEK as a "Top US Ad Agency" specializing in building Brand Conviction. This project was introduced summer 2025 in order to move Buntin into the age of Artificial Intelligence. This uses Streamlit to host a local portal helping Buntin employees with their individual workflow. Some features include Deep Web Search, Reader File Report (both powered by Buntin GPT), and Conviction score. 

[Click Here](https://buntingpt.streamlit.app/) to view the final product. 

## General Overview

This Artificial Intelligence platform runs off of Google's Gemini--trained on specific data accumulated and tailored by Buntin professionals since its inception in 1972. The provided insights from the platform includes resources from the internet as well as personal insights from our strategy, media, and executive team.

## Faye Key Features

### 📑 Document Uploading

Uploading documents places them into a local drive. Uploading documents allows you to further give the program more context regarding your prompt and will help tailor the final result of the solution. By uploading your documents, Faye also stores the files locally which can be used to train Buntin GPT through a constant *session state*. This allows for future referencing of files and information rather than having to start completely anew when prompting an online LLM. 

### 👨‍💻 Deep Web Search

Deep Web Search utilizes ChatGPT's abiltity to throughouly scower the internet, finding resources quickly so you don't have to. Buntin GPT has been trained to prioritize usage of certain well-documented and trusted websites to ensure data quality regarding general market research, but will also link specific information and websites tailored to the specific request. Through the Deep Web Search feature, Faye will also provide helpful follow-up questions regarding your research, emulating the traditional approach to general market research. 

### 💡 Conviction Score Insights

At Buntin, we pride ourselves on our vast industry knowledge and expertise due to being in the advertising industry over fifty years. Our *Buntin Conviction Score* stands as the amalgamation of this information, creating a score for a brand based on our Four Pillars: Practical, Emotional, Personal, and Causal. These pillars are how we in turn numerically quantify qualitative information, providing business insights to help tangibly advance client growth. 

### 📝 Market Research Report Generator

This feature creates a birds-eye-view of a particular product or industry to aid in the kick-off of of new business. This general market research report, exported in either Word, PDF, or LaTex format, includes information regarding the product, its main competitors, and answers any questions regarding the initial topic. This report also creates the template for further editing and populating of new  insights gained by the employee. 

## Developer Note

This project is containerized using [*Docker*](https://www.docker.com/), which allows for consistent and reproducible environments across different machines. Docker packages all dependencies, code, and configuration into isolated containers, making it easier to build, ship, and run the app anywhere. More information on how to use Docker [here](https://docker-curriculum.com/). The application is built with Streamlit, a Python-based web framework designed for creating interactive data apps with minimal effort. To learn more about how to use Streamlit (especially its API references), click [here](https://docs.streamlit.io/get-started). The app is intended to be deployed to the web and can be hosted via services like Streamlit Community Cloud, GitHub Pages (for static assets), or other container-based platforms. This repository is maintained and version-controlled through GitHub for collaborative development, testing, and deployment.

If you have any questions or concerns regarding access please email me at dah181@case.edu or contact@darinhall.com. Thanks! :+1: