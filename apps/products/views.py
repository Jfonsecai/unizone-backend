from rest_framework import generics
from apps.users.models import User
from .models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io


# Vista para listar y crear productos
class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Vista para obtener, actualizar y eliminar un producto específico
class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    
# Función para generar el PDF con ReportLab
def generate_invoice_pdf(cart, buyer_email, total, buyer_name, address, city, state, country):
    # Crear un buffer para almacenar el PDF
    buffer = io.BytesIO()

    # Crear un canvas de ReportLab
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Agregar el contenido del PDF
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, height - 50, "Factura de Compra")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, height - 100, f"Nombre del comprador: {buyer_name}")
    pdf.drawString(50, height - 120, f"Correo del comprador: {buyer_email}")
    pdf.drawString(50, height - 140, "Dirección de entrega:")
    pdf.drawString(70, height - 160, f"{address}, {city}, {state}, {country}")

    pdf.drawString(50, height - 200, "Productos comprados:")
    y = height - 230
    for item in cart:
        product_line = f"- {item['name']} (x{item['quantity']}) - ${item['price'] * item['quantity']:.2f}"
        pdf.drawString(70, y, product_line)
        y -= 20

    pdf.drawString(50, y - 20, f"Total: ${total:.2f}")
    pdf.drawString(50, y - 40, "¡Gracias por tu compra!")

    # Finalizar y guardar el PDF en el buffer
    pdf.save()
    buffer.seek(0)
    return buffer


class SimulatePurchaseView(APIView):
    def post(self, request):
        # Log de la solicitud recibida
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Datos recibidos: {request.data}")

        # Obtener los datos
        cart = request.data.get("cart")
        username = request.data.get("username")
        print(username)
        address = request.data.get("address")
        city = request.data.get("city")
        state = request.data.get("state")
        country = request.data.get("country")

        # Validar campos obligatorios
        if not cart:
            return Response({"error": "El carrito no puede estar vacío."}, status=status.HTTP_400_BAD_REQUEST)
        if not username:
            return Response({"error": "El nombre de usuario es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        # Recuperar el usuario
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "El usuario no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Validar dirección
        if not all([address, city, state, country]):
            return Response({"error": "Todos los campos de la dirección son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

        # Calcular el total
        total = sum(item["price"] * item["quantity"] for item in cart)

        # Generar la factura en formato PDF
        pdf_buffer = generate_invoice_pdf(
            cart=cart,
            buyer_email=user.email,
            total=total,
            buyer_name=f"{user.first_name} {user.last_name}",
            address=address,
            city=city,
            state=state,
            country=country,
        )

        # Crear y enviar el correo electrónico
        email = EmailMessage(
            subject="Tu factura de compra",
            body="¡Gracias por tu compra en Unizone! Te enviamos la factura con los detalles de tu compra.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach("factura.pdf", pdf_buffer.getvalue(), "application/pdf")
        email.send()

        return Response({"message": "Compra simulada exitosamente. Factura enviada por correo."}, status=status.HTTP_200_OK)