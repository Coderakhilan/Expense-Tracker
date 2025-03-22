# Expense Tracker
This **Expense Tracker** is a Streamlit-based web application built using python that allows users to log expense, track debts, and settle payments. It uses **Google Sheets** as a database to store and manage financial records. The app also includes an announcement section that shames the person with the highest debt using a set of humorous messages.

# Features
**Expense Log**
Users can log expenses by entering
- Their name
- The amount spent
- The name of the person who paid
**Debt Summary**
- Displays a summary of who owes money and to whom.
- Ranks the person by highest debt.
**Administrator Mode**
- Admins can log expenses and payments
- Requires an admin password to unlock
- Provides direct link to Google Sheets to view full records or manual modification.

# User Guide
1. Open the website
2. *The Expense log* displays all recorded expenses
3. The *Debt Summary* shows who owes and to whom
4. You can enter the admin password in the sidebar to activate admin mode
5. Once authenticated, you can log expenses which asks for *name, amount spent and who paid*
6. You can also log payments which asks for *debtor's name, the amount they are paying*
7. After recording payments or logging expenses, the system will reduce the owed amount, remove fully paid debts, and update *Google Sheets*
8. Clicking on 'View Full Sheet Here' in the sidebar or below the main page will open the Google Sheet containing all the records

# Tech Stack
- Frontend: Streamlit
- Database: Google Sheets via ```gspread```
- Authentication: Google Cloud Service Account

# Dependencies
- ```streamlit```
- ```gspread```
- ```google-auth```
- ```google-auth-oauthlib```
- ```google-auth-httplib2```
- ```oauth2client```
- ```pandas```
- The app connects to *Google Sheets* via a service account and requires cloud credentials which is stored in streamlit's secrets.toml

# Troubleshooting
- If expense is not logging then ensure you're in admin mode, refresh the app and try again and make sure to have stable internet connection.
- If payment is not updated then ensure debtor's name is spelled correctly and confirm that the amount is valid, refresh the app and try again and make sure to have stable internet connection.

# Security
- Any expense or payment logging requires authenticaation
- Only authorised users can modify records in the google sheet.
