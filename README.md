README
Project Overview
This project is built with Django and is designed to be multi-threaded for better performance and scalability.

Getting Started
Install the required dependencies from the requirements.txt file:

bash
Copy
Edit
pip install -r requirements.txt
The project uses a relational database (PostgreSQL) as its primary data store. Make sure PostgreSQL is installed and configured before running the project.

UUIDs are used as IDs across the system to enhance security and prevent sequential ID guessing.

Key Features
User Profiles: After creating a user through the User model, ensure you complete the associated user profile (with full name) to access profile-related functionalities.

Wallet Constraints: Wallet balances cannot have negative values, ensuring logical consistency in all transactions.

Notifications: Instead of actual notifications, the project uses logging and database records to mimic the notification process. No real notifications are sent.

Atomic Transactions: All financial transactions are performed atomically to ensure consistency and reliability.

Service Design Pattern:
The project follows the Service Design Pattern, improving:

Code readability.

Scalability for future enhancements.

Easier debugging and troubleshooting.

Note: In the GET methods, the design pattern is intentionally not followed for two reasons:

To allow comparison between different coding styles.
Simplifying GET methods is logical since they are less complex and don't benefit significantly from added abstraction.
Custom Serializers for Transactions:
Transaction serializers are deliberately written with field renaming using source. This demonstrates the project's ability to adapt to team and product manager requirements for output adjustments, ensuring better collaboration and flexibility.

Database Notes
The database contains non-validated data and is uploaded in its current state for demo purposes. You can use it as-is to explore the project's functionality.
Important Notes on Security
The project is not highly secure. For example:
Data protection is not fully implemented.
Admin panel restrictions for preventing data modification are not enforced.
This is strictly a demo project and should not be used in production environments. In real-world applications, ignoring such security measures would pose critical vulnerabilities.
