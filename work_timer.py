
import pandas as pd
from datetime import datetime
import os

# ファイルパス設定（必要に応じてパスを調整）
CSV_FILE = "work_log.csv"
STATE_FILE = "work_state.txt"

# 初期化：CSVファイルがなければ作成
if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=["開始時刻", "終了時刻", "作業時間（分）"])
    df_init.to_csv(CSV_FILE, index=False)

# 状態ファイルの取得
def get_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return int(f.read())
    return None

# 状態ファイルにインデックスを書き込む
def set_state(index):
    with open(STATE_FILE, "w") as f:
        f.write(str(index))

# 状態ファイルを削除（リセット）
def clear_state():
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

# 作業時間を記録するメイン関数
def toggle_work():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df = pd.read_csv(CSV_FILE)
    state_index = get_state()

    if state_index is None:
        # 作業開始を記録
        df.loc[len(df)] = [now, "", ""]
        df.to_csv(CSV_FILE, index=False)
        set_state(len(df) - 1)
        print("✅ 作業開始を記録しました。")
    else:
        # 作業終了を記録し、時間を計算
        start_time = datetime.strptime(df.loc[state_index, "開始時刻"], '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
        duration = round((end_time - start_time).total_seconds() / 60)
        df.loc[state_index, "終了時刻"] = now
        df.loc[state_index, "作業時間（分）"] = duration
        df.to_csv(CSV_FILE, index=False)
        clear_state()
        print(f"✅ 作業終了を記録しました（所要時間: {duration} 分）")

# 実行
if __name__ == "__main__":
    toggle_work()
