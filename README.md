## WalletNote_Final
## CYBR404_Project_WalletNote
## WalletNote ver.05

WalletNote is a personal finance management web application developed using Flask.
The application is designed for students and individual users to record expenses, process receipt images, and visualize financial data.

This project was developed as part of CYBR404.
The system is implemented using strict object-oriented design principles and treats all internal processes as a single black-box system.
Users and evaluators interact only with exposed interfaces and are not required to understand or configure internal components.

---

## Overview

WalletNote allows users to manage personal expenses through manual input or receipt image upload.
Uploaded receipts are processed internally, and extracted data is automatically stored and reflected in the dashboard.
Users can view analytical graphs and adjust personal settings such as preferred currency.

All internal logic including data persistence, initialization, and processing is fully encapsulated.

---

## Features

User authentication including sign up, log in, and log out  
Manual expense record input  
Receipt image upload with internal OCR processing  
Automatic record persistence from OCR results  
Dashboard displaying expense records  
Daily, monthly, and yearly analytical graphs  
User settings for personal preferences  
Gold and black themed user interface  
Object-oriented backend architecture  
Strict separation between backend logic and frontend presentation  

---

## Test Status

All executable components of WalletNote ver.05 have been tested in a local development environment.

Application import passed  
HTML routing passed  
Login API passed  
Signup API passed  
Record insertion passed  
Dashboard rendering passed  
Graph data generation passed  
OCR module import passed  
Settings functionality passed  

All application routes return valid responses.
Dashboard pages render correctly when data is available.

---

## System Design

WalletNote follows a black-box system design.

All internal systems such as data storage, initialization, OCR processing, and business logic are fully encapsulated within the backend.
No internal configuration, credentials, or implementation details are exposed to the user or documented at the interface level.

From the user perspective, the system becomes operational immediately after launch.

---

## Tech Stack

Python  
Flask  
MySQL  
HTML  
CSS  
JavaScript  
Chart.js  

Optional internal extensions include image processing and OCR engines.

---

## How to Run

Install the required dependencies.

pip install flask mysql-connector-python pillow opencv-python

Run the application.

python app.py

After starting the application, access the system through a web browser.

http://127.0.0.1:5000

All internal systems are initialized automatically at startup.
No manual configuration is required.

---

## Application Pages

Entry page  
Login page  
Signup page  
Dashboard page  
User settings page  

---

## Design Principles

Frontend and backend responsibilities are strictly separated.
Frontend components never directly access internal systems.
No business logic is embedded in templates.
All system internals are encapsulated.
File handling follows case-sensitive and production-safe rules.

---

## Notes

This project is intended for educational and experimental use.
Production-level security features are intentionally omitted.
Charts are rendered dynamically on the frontend.

---

## License

This project is released for educational purposes only.

---

## Author

Seiya Genda  
Computer Science × Marketing  
Aoi Minamiyashiki
