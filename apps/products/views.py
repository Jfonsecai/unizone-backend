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


# class SimulatePurchaseView(APIView):
#     def post(self, request):
#         # Datos enviados desde el frontend
#         cart = request.data.get('cart')  # Lista de productos en el carrito
#         buyer_email = request.data.get('email')  # Correo del comprador

#         if not cart or not buyer_email:
#             return Response({"error": "Cart and email are required"}, status=status.HTTP_400_BAD_REQUEST)

#         # Simular el cálculo del total
#         total = sum(item['price'] * item['quantity'] for item in cart)

#         # Generar la factura como un archivo PDF
#         context = {
#             'cart': cart,
#             'buyer_email': buyer_email,
#             'total': total,
#         }
#         html_content = render_to_string('/templates/products/plantilla_factura.html', context)
#         pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
#         HTML(string=html_content).write_pdf(pdf_file.name)

#         # Enviar el correo con la factura
#         email = EmailMessage(
#             subject="Tu factura de compra",
#             body="¡Gracias por tu compra en Unizone! Te enviamos la factura con los detalles de tu compra.",
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             to=[buyer_email],
#         )
#         email.attach_file(pdf_file.name)
#         email.send()

#         # Eliminar el archivo temporal después de enviar el correo
#         pdf_file.close()

#         return Response({"message": "Purchase simulated successfully. Receipt sent via email."}, status=status.HTTP_200_OK)
    
# Función para generar el PDF con ReportLab
# def generate_invoice_pdf(cart, buyer_email, total):
#     # Crear un buffer para almacenar el PDF
#     buffer = io.BytesIO()

#     # Crear un canvas de ReportLab
#     pdf = canvas.Canvas(buffer, pagesize=letter)
#     width, height = letter

#     # Agregar el contenido del PDF
#     pdf.setFont("Helvetica-Bold", 16)
#     pdf.drawString(50, height - 50, "Factura de Compra")

#     pdf.setFont("Helvetica", 12)
#     pdf.drawString(50, height - 100, f"Correo del comprador: {buyer_email}")
#     pdf.drawString(50, height - 120, "Productos comprados:")

#     y = height - 150
#     for item in cart:
#         product_line = f"- {item['name']} (x{item['quantity']}) - ${item['price'] * item['quantity']:.2f}"
#         pdf.drawString(70, y, product_line)
#         y -= 20

#     pdf.drawString(50, y - 20, f"Total: ${total:.2f}")
#     pdf.drawString(50, y - 40, "¡Gracias por tu compra!")

#     # Finalizar y guardar el PDF en el buffer
#     pdf.save()
#     buffer.seek(0)
#     return buffer

def generate_invoice_pdf(cart, buyer_name, buyer_email, total):
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
    pdf.drawString(50, height - 140, "Productos comprados:")

    y = height - 170
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
        # Datos enviados desde el frontend
        cart = request.data.get('cart')  # Lista de productos en el carrito
        username = request.data.get('username')  # Username del comprador

        if not cart or not username:
            return Response({"error": "El carrito y el nombre de usuario son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

        # Recuperar usuario
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        buyer_email = user.email
        buyer_name = f"{user.first_name} {user.last_name}"

        # Calcular el total
        total = sum(item['price'] * item['quantity'] for item in cart)

        # Generar la factura en formato PDF
        pdf_buffer = generate_invoice_pdf(cart, buyer_name, buyer_email, total)

        # Crear y enviar el correo electrónico
        email = EmailMessage(
            subject="Tu factura de compra",
            body=f"¡Hola {buyer_name}! Gracias por tu compra en Unizone. Adjuntamos la factura con los detalles.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[buyer_email],
        )
        email.attach("factura.pdf", pdf_buffer.getvalue(), "application/pdf")
        email.send()

        return Response({"message": "Compra simulada exitosamente. Factura enviada por correo."}, status=status.HTTP_200_OK)


# Vista para simular la compra
# class SimulatePurchaseView(APIView):
#     def post(self, request):
#         # Datos enviados desde el frontend
#         cart = request.data.get('cart')  # Lista de productos en el carrito
#         buyer_email = request.data.get('email')  # Correo del comprador

#         if not cart or not buyer_email:
#             return Response({"error": "El carrito y el correo son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

#         # Calcular el total
#         total = sum(item['price'] * item['quantity'] for item in cart)

#         # Generar la factura en formato PDF
#         pdf_buffer = generate_invoice_pdf(cart, buyer_email, total)

#         # Crear y enviar el correo electrónico
#         email = EmailMessage(
#             subject="Tu factura de compra",
#             body="¡Gracias por tu compra en Unizone! Te enviamos la factura con los detalles de tu compra.",
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             to=[buyer_email],
#         )
#         email.attach("factura.pdf", pdf_buffer.getvalue(), "application/pdf")
#         email.send()

#         return Response({"message": "Compra simulada exitosamente. Factura enviada por correo."}, status=status.HTTP_200_OK)

