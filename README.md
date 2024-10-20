# Solana-IPFS-Supply-Chain-Multi

Solana-IPFS-Supply-Chain-Multi is an innovative blockchain-based solution that combines the power of Solana's high-performance blockchain with IPFS (InterPlanetary File System) to create a robust, transparent, and efficient supply chain management system.

## Key Features:

- **Decentralized Architecture**: Leverages Solana blockchain for secure and fast transactions, and IPFS for distributed data storage.
- **Product Tracking**: Enables real-time tracking of products throughout the supply chain.
- **Organization Management**: Supports various types of organizations involved in the supply chain process.
- **Transaction Logging**: Records all product transfers between organizations with cryptographic verification.
- **Data Integrity**: Utilizes hashing techniques to ensure the integrity of product and transaction data.
- **IPFS Integration**: Stores and retrieves product certificates and additional data using IPFS, ensuring data availability and immutability.

This project aims to enhance supply chain transparency, reduce fraud, and improve overall efficiency by providing a decentralized and tamper-resistant system for managing product lifecycles and organizational interactions.



# Deployment Guide

This guide will walk you through the process of cloning and deploying the Solana-IPFS-Supply-Chain-Multi project. Follow these steps carefully to get the project up and running on your local machine.

## Prerequisites

Before you begin, make sure you have the following installed on your system:

- Python (3.7 or higher)
- pip (Python package manager)
- Git
- A text editor or IDE of your choice (e.g., Visual Studio Code, PyCharm)

## Step 1: Clone the Repository

1. Open your terminal or command prompt.
2. Navigate to the directory where you want to store the project.
3. Run the following command to clone the repository:
```
git clone https://github.com/mihirpanpatil/solana-ipfs-supply-chain-multi.git
```

5. Once the cloning is complete, navigate into the project directory:


## Step 2: Set Up a Virtual Environment

1. Create a virtual environment to isolate the project dependencies:
```
python -m venv venv
```

3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

## Step 3: Install Dependencies

1. With the virtual environment activated, install the required packages:
```
pip install -r requirements.txt
```


Note: If `requirements.txt` doesn't exist, you may need to install Django manually:
```
pip install django
```


## Step 4: Configure the Database

1. Run the following commands to set up the database:
```
python manage.py makemigrations python manage.py migrate
```


## Step 5: Create a Superuser (Admin)

1. Create a superuser account to access the Django admin panel:
```
python manage.py createsuperuser
```


3. Follow the prompts to set up your username, email, and password.

## Step 6: Run the Development Server

1. Start the Django development server:
```
python manage.py runserver
```


3. Open your web browser and go to `http://127.0.0.1:8000/` to view the application.

## Step 7: Access the Admin Panel

1. Go to `http://127.0.0.1:8000/admin/` in your web browser.
2. Log in using the superuser credentials you created earlier.

## Additional Configuration (Optional)

### Setting Up IPFS

If you want to use IPFS functionality:

1. Install IPFS on your system following the official IPFS documentation.
2. Start the IPFS daemon before running the Django server.

### Configuring Solana

To interact with the Solana blockchain:

1. Install the Solana CLI tools following the official Solana documentation.
2. Set up a Solana wallet and ensure it's properly configured for the network you're using (devnet, testnet, or mainnet).

## Troubleshooting

- If you encounter any "Module not found" errors, make sure your virtual environment is activated and all dependencies are installed correctly.
- For database-related issues, try deleting the `db.sqlite3` file and running the migration commands again.
- If you face issues with IPFS or Solana integration, ensure that their respective services are running and properly configured.

## Next Steps

- Explore the `supply_chain` app in the project to understand the structure and functionality.
- Review the models in `supply_chain/models.py` to understand the data structure.
- Check `supply_chain/views.py` and `supply_chain/urls.py` to see how different pages and functionalities are implemented.

Congratulations! You have successfully set up and deployed the Solana-IPFS-Supply-Chain-Multi project. Happy coding!
