
# Clash Royale Integration Catoff Bounty

## Description
This Django-based project integrates the Clash Royale API to provide a comprehensive interface for viewing player statistics, battle logs, challenges, and verifying player data using Zero-Knowledge Proofs (ZKPs). The primary aim is to allow users to track and verify their Clash Royale data securely while offering a seamless and informative experience.

### Features
- **Display Player Statistics**: View key player data such as trophies, level, win rates, etc.
- **Fetch and Display Battle Logs**: Access detailed information on past battles.
- **Show Ongoing and Upcoming Challenges**: Stay updated on active and upcoming events in Clash Royale.
- **Zero-Knowledge Proof Generation**: Generate ZKPs for trophy counts, win rates, and challenge participation, ensuring player privacy.
- **Clan Data Integration**: View clan information if the player is part of a clan.
- **Error Handling and Logging**: The application includes robust error handling and detailed logging.

## Screenshots
<img width="1680" alt="Screenshot 2025-01-22 at 07 04 52" src="https://github.com/user-attachments/assets/fdc62f0c-cd2e-4d87-8eb1-bf678bfd2a53" />

### User Interface
Here are some previews of the UI components:

#### Player Stats Page
<img width="1680" alt="Screenshot 2025-01-22 at 07 06 57" src="https://github.com/user-attachments/assets/664e2323-90aa-4dd5-827a-e2a4e2f6fefb" />
<img width="1680" alt="Screenshot 2025-01-22 at 07 07 01" src="https://github.com/user-attachments/assets/46262a3c-62ca-434b-8bac-d017aedd3a27" />


#### Challenges Page
<img width="1680" alt="Screenshot 2025-01-22 at 07 04 52" src="https://github.com/user-attachments/assets/94bcadc3-bd04-4218-8f24-42e2f091eb8f" />

### CLI Interface
The project also includes a developer-friendly CLI for interacting with the Clash Royale API and generating Zero-Knowledge Proofs.

#### CLI Demonstration
<img width="1680" alt="Screenshot 2025-01-22 at 07 08 34" src="https://github.com/user-attachments/assets/66efe913-87b2-4320-8f2b-045b1100b6c4" />



## Installation Instructions
Follow these steps to set up the project locally.

### Prerequisites
- Python >= 3.8
- Django >= 3.2
- Install the necessary dependencies using the `requirements.txt`.

### Step-by-Step Guide:
1. **Clone the repository**:
   ```bash
   git clone https://github.com/vtbossss/Catoff_Bounty.git
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scriptsctivate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Clash Royale API key**:
   - Obtain your API key from Clash Royale and add it to the `.env` file.
   - Example:
     ```env
     CLASH_API_KEY=your_api_key_here
     ```

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

## Configuration
### Clash Royale API Client
- In `api_client.py`, set the API key by modifying the following line:
  ```python
  API_KEY = 'your_api_key_here'
  ```
- The API URL and other configurations can also be modified in this file.

### Environment Configuration
- The project uses `.env` files for sensitive information like the Clash Royale API key.
- To configure additional settings like API endpoints, update the `.env` file accordingly.

## Zero-Knowledge Proofs (ZKPs)
Zero-Knowledge Proofs are used in this project to ensure the privacy and integrity of player data. Specifically, the ZKPs verify:

- **Trophy Verification**: Ensures the player’s trophy count is valid.
- **Win/Loss Rate Verification**: Validates the player’s win rate without revealing personal data.
- **Challenge Participation Verification**: Confirms the player’s involvement in specific challenges.

### Verification Classes:
- **TrophyVerification**: Used to verify the player’s trophy count.
- **WinLossVerification**: Verifies the player’s win/loss record.
- **ChallengeVerification**: Ensures the player’s participation in challenges.

## API Endpoints
### `/players/{player_tag}`
- **Description**: Fetches player statistics (e.g., trophies, level, etc.).
- **Example Request**:
  ```bash
  GET /players/PlayerTag
  ```
- **Example Response**:
  ```json
  {
    "player_tag": "#2P8P9P0Q",
    "trophies": 4500,
    "level": 13
  }
  ```
- **Error Handling Response**:
  ```json
  {
    "error": "Player not found."
  }
  ```

### `/players/{player_tag}/battlelog`
- **Description**: Fetches player battle logs.
- **Example Request**:
  ```bash
  GET /players/PlayerTag/battlelog
  ```
- **Example Response**:
  ```json
  {
    "battlelog": [
      {
        "opponent": "Player1",
        "result": "win",
        "date": "2025-01-22"
      }
    ]
  }
  ```

### `/clans/{clan_tag}`
- **Description**: Retrieves data related to the player’s clan.
- **Example Request**:
  ```bash
  GET /clans/ClanTag
  ```
- **Example Response**:
  ```json
  {
    "clan_tag": "#2P8P9P0Q",
    "clan_name": "Elite Clan"
  }
  ```

### `/challenges`
- **Description**: Fetches ongoing and upcoming challenges.
- **Example Request**:
  ```bash
  GET /challenges
  ```
- **Example Response**:
  ```json
  {
    "challenges": [
      {
        "challenge_name": "2v2 Draft Challenge",
        "start_date": "2025-01-23",
        "end_date": "2025-01-25"
      }
    ]
  }
  ```

## Error Handling
The project handles errors effectively using Django’s built-in exception handling and logging framework. Key error messages are logged for debugging purposes and returned to the user via structured JSON responses.

- Invalid player tags, battle logs, or other inputs result in appropriate 4xx or 5xx HTTP status codes.
- API failures are caught and logged to help identify the issue.

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to your branch (`git push origin feature/your-feature-name`).
5. Create a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author Information
- **Name**: Vaibhav Tiwari
- **Portfolio**: [https://backend-portfolio-lime.vercel.app/](https://backend-portfolio-lime.vercel.app/)
- **GitHub**: [https://github.com/vtbossss](https://github.com/vtbossss)
- **Email**: tiwarijivaibhav@gmail.com

## Miscellaneous Information
- **Known Limitations**: The Clash Royale API may experience rate limiting during heavy usage, so ensure your API key is not exceeded.
- **Future Plans**: Upcoming features will include adding more detailed battle statistics and incorporating player achievement tracking.
- **Acknowledgments**: Thanks to Supercell for providing the Clash Royale API and to the open-source community for their contributions to the project.
