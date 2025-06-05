import os
import sys
import matplotlib.pyplot as plt

try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
except ImportError as e:
    sys.stderr.write("Required packages not found. Please install gspread and oauth2client.\n")
    raise


def fetch_sheet(sheet_key, worksheet_name, creds_json):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(sheet_key)
    worksheet = sheet.worksheet(worksheet_name)
    return worksheet.get_all_records()


def plot_stats(records):
    if not records:
        print("No data found.")
        return
    dates = [r.get('Date') for r in records]
    mood = [float(r.get('Mood', 0)) for r in records]
    sleep_hours = [float(r.get('Sleep', 0)) for r in records]
    motivation = [float(r.get('Motivation', 0)) for r in records]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, mood, label='Mood')
    plt.plot(dates, sleep_hours, label='Sleep Hours')
    plt.plot(dates, motivation, label='Motivation')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Daily Mood, Sleep, Motivation')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <sheet_key> <worksheet_name> <credentials.json>")
        return
    sheet_key, worksheet_name, creds = sys.argv[1:4]
    records = fetch_sheet(sheet_key, worksheet_name, creds)
    plot_stats(records)


if __name__ == "__main__":
    main()
