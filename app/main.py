import sqlite3
from datetime import datetime

DATABASE = "learning_records.db"


def init_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            content TEXT NOT NULL,
            duration INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def add_record():
    subject = input("请输入学习科目：").strip()
    content = input("请输入学习内容：").strip()
    duration_text = input("请输入学习时长（分钟）：").strip()

    if not subject or not content:
        print("科目和学习内容不能为空。")
        return

    try:
        duration = int(duration_text) if duration_text else 0
    except ValueError:
        print("学习时长必须是整数。")
        return

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO records (subject, content, duration, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (subject, content, duration, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )

    connection.commit()
    connection.close()

    print("学习记录添加成功。")


def list_records():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, subject, content, duration, created_at
        FROM records
        ORDER BY id DESC
        """
    )

    records = cursor.fetchall()
    connection.close()

    if not records:
        print("当前还没有学习记录。")
        return

    print("\n学习记录：")
    for record in records:
        record_id, subject, content, duration, created_at = record
        print(
            f"{record_id}. [{subject}] {content} "
            f"({duration} 分钟，{created_at})"
        )


def main():
    init_database()

    while True:
        print("\n===== 学习记录管理工具 =====")
        print("1. 添加学习记录")
        print("2. 查看学习记录")
        print("0. 退出")

        choice = input("请选择操作：").strip()

        if choice == "1":
            add_record()
        elif choice == "2":
            list_records()
        elif choice == "0":
            print("程序已退出。")
            break
        else:
            print("无效选项，请重新输入。")


if __name__ == "__main__":
    main()