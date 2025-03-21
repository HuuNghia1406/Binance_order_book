import pandas as pd
import numpy as np

def group_by_step(order_book, step):
    # Tạo một bản copy để tránh cảnh báo SettingWithCopyWarning
    order_book = order_book.copy()

    # Áp dụng làm tròn cho BID (làm tròn xuống) và ASK (làm tròn lên)
    order_book['Price'] = np.where(
        order_book['Side'] == 'BID',
        np.floor(order_book['Price'].astype(float) / step) * step,  # BID làm tròn XUỐNG
        np.ceil(order_book['Price'].astype(float) / step) * step     # ASK làm tròn LÊN
    )
    
    # Group by và tính tổng
    grouped_order_book = order_book.groupby(['Side', 'Price'])[['Quantity', 'Total']].sum().reset_index()

    # Sắp xếp theo Side (BID trước) và Price giảm dần
    grouped_order_book['Side'] = pd.Categorical(
        grouped_order_book['Side'],
        categories=['ASK', 'BID'],
        ordered=True
    )
    grouped_order_book = grouped_order_book.sort_values(
        ['Side', 'Price'],
        ascending=[True, False]
    )
    
    return grouped_order_book

# Đọc dữ liệu từ file CSV đã tạo
order_book = pd.read_csv('D:/Python-for-Data-Analyst/binance_order_book/data/realtime/test.csv')

# Nhập step
step = float(input("Nhập giá trị step: "))

# Group by
grouped_order_book = group_by_step(order_book, step)

# Lưu kết quả vào file CSV
output_filename = f'D:/Python-for-Data-Analyst/binance_order_book/data/realtime/data_streaming_{step}.csv'
pd.set_option('display.float_format', '{:.4f}'.format)
grouped_order_book.to_csv(output_filename, index=False, float_format='%.4f')

print(f"\nĐã lưu dữ liệu vào file '{output_filename}'")
