import os
from django.conf import settings
from django.apps import apps
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['DELETE'])
def delete_document(request, model_name, pk):
    try:
        model = apps.get_model('gimao', model_name)
        if model is None:
            return Response({"message": f"Modèle {model_name} non trouvé"}, status=status.HTTP_400_BAD_REQUEST)

        document = model.objects.get(pk=pk)

        if hasattr(document, 'lienDocumentDefaillance'):
            file_path = os.path.join(settings.MEDIA_ROOT, str(document.lienDocumentDefaillance))
        elif hasattr(document, 'lienDocumentIntervention'):
            file_path = os.path.join(settings.MEDIA_ROOT, str(document.lienDocumentIntervention))
        else:
            file_path = None

        if file_path and os.path.exists(file_path):
            os.remove(file_path)

        document.delete()
        return Response({"message": "Document supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)

    except model.DoesNotExist:
        return Response({"message": "Document non trouvé"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
