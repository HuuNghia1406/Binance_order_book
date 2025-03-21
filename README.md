# Binance Order Book Data Processing

## Giới thiệu

Dự án này thu thập dữ liệu từ sổ lệnh (Order Book) của Binance theo thời gian thực, sau đó xử lý và tính toán theo bước giá (step) do người dùng nhập vào. Điều này giúp người dùng có thể phân tích xu hướng thị trường và đặt lệnh chính xác hơn.

## Tính năng

- **Thu thập dữ liệu Order Book** theo thời gian thực từ Binance WebSocket API.
- **Xử lý dữ liệu**: Làm tròn giá của BID (xuống) và ASK (lên) theo bước giá (`step`).
- **Tổng hợp và lưu trữ dữ liệu**: Tổng hợp khối lượng và tổng giá trị của BID/ASK theo từng mức giá.
- **Xuất dữ liệu ra file CSV** để sử dụng trong phân tích sau này.

## Cách cài đặt

### 1. Clone repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Cài đặt các thư viện cần thiết

Dự án sử dụng Python và yêu cầu các thư viện như `pandas`, `numpy`, `aiohttp`, `asyncio`.

```bash
pip install -r requirements.txt
```

## Cách sử dụng

### 1. Thu thập dữ liệu từ Binance

Chạy file `realtime.py` để lấy dữ liệu Order Book theo thời gian thực và lưu vào CSV:

```bash
python realtime.py
```

File CSV sẽ được lưu(bạn cần thay thế đường dẫn cho phù hợp):

```
D:/Python-for-Data-Analyst/binance_order_book/data/realtime/data_streaming.csv
```

### 2. Xử lý dữ liệu theo bước giá

Chạy file `main.py` để nhóm dữ liệu theo bước giá (`step`):

```bash
python main.py
```

Bạn sẽ được yêu cầu nhập giá trị `step` để làm tròn dữ liệu. File kết quả sẽ được lưu tại(bạn cần thay thế đường dẫn cho phù hợp):

```
D:/Python-for-Data-Analyst/binance_order_book/data/realtime/data_streaming_{step}.csv
```

## Ví dụ Output

Sau khi xử lý dữ liệu với `step = 0.1 USDT`, output có dạng:

```
Side   | Price   | Quantity | Total
BID    | 35000.0 | 120.0    | 4200000.0
ASK    | 35000.1 | 100.0    | 3500010.0
```

## Lưu ý

- **API Key** và **Secret Key** đang được hardcode trong `realtime.py`, bạn cần thay thế cho phù hợp với bạn

