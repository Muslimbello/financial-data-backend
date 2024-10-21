import matplotlib.pyplot as plt
from io import BytesIO
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from fetch_stock.models import StockData
from ...backtesting.services import Backtest
from ...predict_stock.services import StockPredictor


class ReportGenerator:
    def __init__(self, stock_symbol):
        self.stock_symbol = stock_symbol

    def generate_plot(self):
        stock_data = StockData.objects.filter(symbol=self.stock_symbol).order_by("date")
        dates = [data.date for data in stock_data]
        prices = [data.close_price for data in stock_data]

        plt.figure(figsize=(10, 6))
        plt.plot(dates, prices)
        plt.title(f"{self.stock_symbol} Stock Price")
        plt.xlabel("Date")
        plt.ylabel("Price")

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        return graphic.decode("utf-8")

    def generate_report(self, format="json"):
        backtest = Backtest(
            self.stock_symbol, 10000
        )  # Assuming $10,000 initial investment
        backtest_results = backtest.run_backtest()

        predictor = StockPredictor()
        predictions = predictor.predict(self.stock_symbol)

        plot = self.generate_plot()

        report_data = {
            "stock_symbol": self.stock_symbol,
            "backtest_results": backtest_results,
            "predictions": predictions.tolist(),
            "plot": plot,
        }

        if format == "pdf":
            return self.generate_pdf_report(report_data)
        else:
            return report_data

    def generate_pdf_report(self, report_data):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.drawString(100, 750, f"Report for {self.stock_symbol}")
        p.drawString(
            100,
            700,
            f"Total Return: {report_data['backtest_results']['total_return_percent']}%",
        )
        p.drawString(
            100,
            675,
            f"Max Drawdown: {report_data['backtest_results']['max_drawdown_percent']}%",
        )
        p.drawString(
            100,
            650,
            f"Trades Executed: {report_data['backtest_results']['number_of_trades']}",
        )
        p.drawImage(
            BytesIO(base64.b64decode(report_data["plot"])),
            100,
            300,
            width=400,
            height=300,
        )
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer
