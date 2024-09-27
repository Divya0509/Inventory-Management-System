import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Item
from .serializers import ItemSerializer
from django.shortcuts import get_object_or_404

# Get an instance of a logger
logger = logging.getLogger('items')

class CreateItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.info("CreateItemView: Received POST request to create an item.")
        serializer = ItemSerializer(data=request.data)
        item_name = request.data.get('name', 'Unnamed Item')
        if Item.objects.filter(name=item_name).exists():
            logger.warning(f"CreateItemView: Item '{item_name}' already exists.")
            return Response({'error': 'Item already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            item = serializer.save()
            logger.info(f"CreateItemView: Item '{item.name}' created successfully with ID {item.id}.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"CreateItemView: Invalid data received - {serializer.errors}.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id):
        logger.info(f"GetItemView: Received GET request for item ID {item_id}.")
        item = get_object_or_404(Item, id=item_id)
        serializer = ItemSerializer(item)
        logger.debug(f"GetItemView: Retrieved item - {serializer.data}.")
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateItemView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, item_id):
        logger.info(f"UpdateItemView: Received PUT request for item ID {item_id}.")
        item = get_object_or_404(Item, id=item_id)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            updated_item = serializer.save()
            logger.info(f"UpdateItemView: Item ID {item_id} updated successfully.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error(f"UpdateItemView: Invalid data received for item ID {item_id} - {serializer.errors}.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        logger.info(f"DeleteItemView: Received DELETE request for item ID {item_id}.")
        item = get_object_or_404(Item, id=item_id)
        item.delete()
        logger.info(f"DeleteItemView: Item ID {item_id} deleted successfully.")
        return Response({'message': 'Item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
