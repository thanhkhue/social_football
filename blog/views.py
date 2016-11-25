from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "HEAD"])
def home(request):
	return render(request, 'v2/fiuzu/pg_home.html')