import asyncio
import aiohttp
import json
import csv
from collections import defaultdict

# Thiết lập API key và secret key
api_key = "6AYENK2oi6M8zOozPQmWy1C8qVBve21looyXr6GogfRbCaK1ksROxh4or9rJgcOv"
secret_key = "5TTB74FNg8K2bDleUK5aMcUoMTWHcbPi3nZRFT07r5BkT1fruuQVqVhT8FO6ZA52"

# Tên file CSV để lưu dữ liệu
csv_filename = "D:/Python-for-Data-Analyst/binance_order_book/data/realtime/data_streaming.csv"

# Biến để kiểm soát việc chạy
max_data_points = 40  # Giới hạn tổng số dòng dữ liệu (200 dòng)

# Định nghĩa bước nhảy
step_size = 1 / 100000

async def get_realtime_data():
    async with aiohttp.ClientSession() as session:
        headers = {
            "X-MBX-APIKEY": api_key,
            "Sec-WebSocket-Protocol": "json"
        }

        async with session.ws_connect("wss://stream.binance.com/ws", headers=headers) as ws:
            subscribe_message = {
                "method": "SUBSCRIBE",
                "params": ["viteusdt@depth"],
                "id": 1
            }
            await ws.send_json(subscribe_message)

            # Dictionary để lưu bids và asks
            bid_data = defaultdict(lambda: {'quantity': 0, 'total': 0})
            ask_data = defaultdict(lambda: {'quantity': 0, 'total': 0})

            # Biến đếm tổng số dòng đã thu thập
            total_collected = 0

            while total_collected < max_data_points:
                msg = await ws.receive()
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data_received = json.loads(msg.data)

                    if 'b' in data_received and 'a' in data_received:
                        # Xử lý asks
                        for ask in data_received['a']:
                            price = float(ask[0])
                            quantity = float(ask[1])
                            if price > 0 and quantity > 0:  # Thêm chỉ nếu giá trị hợp lệ
                                # Làm tròn giá theo step_size
                                stepped_price = round(price / step_size) * step_size
                                # Cộng dồn quantity và tổng cho cùng một giá
                                ask_data[stepped_price]['quantity'] += quantity
                                ask_data[stepped_price]['total'] = ask_data[stepped_price]['quantity'] * stepped_price
                                total_collected += 1
                                # Dừng nếu đã thu thập đủ 200 dòng
                                if total_collected >= max_data_points:
                                    break
                        # Xử lý bids
                        for bid in data_received['b']:
                            price = float(bid[0])
                            quantity = float(bid[1])
                            if price > 0 and quantity > 0:  # Thêm chỉ nếu giá trị hợp lệ
                                # Làm tròn giá theo step_size
                                stepped_price = round(price / step_size) * step_size
                                # Cộng dồn quantity và tổng cho cùng một giá
                                bid_data[stepped_price]['quantity'] += quantity
                                bid_data[stepped_price]['total'] = bid_data[stepped_price]['quantity'] * stepped_price
                                total_collected += 1
                                # Dừng nếu đã thu thập đủ 200 dòng
                                if total_collected >= max_data_points:
                                    break

                        

                # Dừng vòng lặp nếu đã thu thập đủ dữ liệu từ cả bids và asks
                if total_collected >= max_data_points:
                    break

            # Ghi dữ liệu vào file CSV
            with open(csv_filename, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Side", "Price", "Quantity", "Total"])

                # Ghi dữ liệu bids và sắp xếp theo Price giảm dần
                sorted_bid_data = sorted(bid_data.items(), key=lambda x: x[0], reverse=True)
                for price, info in sorted_bid_data:
                    writer.writerow(['BID', format(price, '.5f'), format(info['quantity'], '.5f'), format(info['total'], '.5f')])

                # Ghi dữ liệu asks và sắp xếp theo Price giảm dần
                sorted_ask_data = sorted(ask_data.items(), key=lambda x: x[0], reverse=True)
                for price, info in sorted_ask_data:
                    writer.writerow(['ASK', format(price, '.5f'), format(info['quantity'], '.5f'), format(info['total'], '.5f')])

            print("Collected {} data points and saved to file.".format(total_collected))

async def main():
    await get_realtime_data()

if __name__ == "__main__":
    asyncio.run(main())
