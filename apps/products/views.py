from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.conf import settings

# Vista para listar y crear productos
class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Vista para obtener, actualizar y eliminar un producto específico
class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SimulatePurchaseView(APIView):
    def post(self, request):
        # Datos enviados desde el frontend
        cart = request.data.get('cart')  # Lista de productos en el carrito
        buyer_email = request.data.get('email')  # Correo del comprador

        if not cart or not buyer_email:
            return Response({"error": "Cart and email are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Simular el cálculo del total
        total = sum(item['price'] * item['quantity'] for item in cart)

        # Generar la factura como un archivo PDF
        context = {
            'cart': cart,
            'buyer_email': buyer_email,
            'total': total,
        }
        html_content = render_to_string('/templates/products/plantilla_factura.html', context)
        pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        HTML(string=html_content).write_pdf(pdf_file.name)

        # Enviar el correo con la factura
        email = EmailMessage(
            subject="Tu factura de compra",
            body="¡Gracias por tu compra en Unizone! Te enviamos la factura con los detalles de tu compra.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[buyer_email],
        )
        email.attach_file(pdf_file.name)
        email.send()

        # Eliminar el archivo temporal después de enviar el correo
        pdf_file.close()

        return Response({"message": "Purchase simulated successfully. Receipt sent via email."}, status=status.HTTP_200_OK)

