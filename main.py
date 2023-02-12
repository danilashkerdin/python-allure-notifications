import argparse
import matplotlib.pyplot as plt
import requests
import json


def parse_summary_json(report_path) -> dict:
    path = f'{report_path}/widgets/summary.json'
    with open(path, 'r') as file:
        data = json.load(file)
    statistic = data['statistic']

    return statistic


def generate_image(broken=0, passed=0, skipped=0, unknown=0, failed=0, total=0, path="pie_chart.png"):

    labels = ['Broken', 'Passed', 'Skipped', 'Unknown', 'Failed']
    sizes = [broken, passed, skipped, unknown, failed]
    colors = ['#ffc107', '#28a745', '#17a2b8', '#800080','#dc3545']

    plt.pie(sizes, colors=colors, shadow=False, startangle=140, autopct='%1.1f%%')
    plt.axis('equal')
    plt.gca().set_aspect("equal")
    centre_circle = plt.Circle((0, 0), 0.80, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.annotate(f"Total\n{total}", (0, 0), fontsize=16, ha='center')
    plt.legend(title='Legend', loc="upper left", labels=labels)
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches='tight')


def send_image(image, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

    files = {'photo': ("pie_chart.png", image)}
    data = {'chat_id': chat_id}

    requests.post(url, files=files, data=data)


def main():
    parser = argparse.ArgumentParser(description='Send pie chart image to Telegram chat')
    parser.add_argument('bot_token', type=str, help='Telegram bot token')
    parser.add_argument('chat_id', type=str, help='Telegram chat id')
    parser.add_argument('report_folder_path', type=str, help='Path to allure report folder')
    args = parser.parse_args()

    result_image_path = "pie_chart.png"

    statistics = parse_summary_json(args.report_folder_path)
    generate_image(**statistics, path=result_image_path)
    with open(result_image_path, "rb") as image:
        send_image(image, args.bot_token, args.chat_id)


if __name__ == '__main__':
    main()