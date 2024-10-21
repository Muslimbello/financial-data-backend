from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.http import JsonResponse
from matplotlib import pyplot as plt
import pandas as pd
from fetch_stock.models import StockData


def generate_report(request):
    symbol = request.GET.get("symbol", "AAPL")
    stock_data = StockData.objects.filter(symbol=symbol).order_by("date")

    if not stock_data.exists():
        return JsonResponse({"error": "No data available for this symbol"})

    df = pd.DataFrame(list(stock_data.values("date", "close_price")))
    df.set_index("date", inplace=True)
    df.plot(y="close_price")

    plt.savefig("stock_prices.png")

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{symbol}_report.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, f"Stock Report for {symbol}")
    p.drawImage("stock_prices.png", 100, 500, width=400, height=200)

    p.showPage()
    p.save()

    return response
