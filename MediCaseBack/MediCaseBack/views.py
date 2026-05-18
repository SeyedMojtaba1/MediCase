import requests
from django.http import HttpResponse
from django.core.cache import cache

MIRRORS = [
    "https://lib.arvancloud.ir/swagger-ui/4.9.1/",
]

def swagger_asset(request, filename):
    cache_key = f"swagger_asset_{filename}"
    cached = cache.get(cache_key)

    if cached:
        return HttpResponse(cached["content"], content_type=cached["content_type"])

    for mirror in MIRRORS:
        try:
            url = mirror + filename
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                content_type = r.headers.get("Content-Type", "text/plain")

                cache.set(cache_key, {
                    "content": r.content,
                    "content_type": content_type
                }, 60 * 60 * 24)  # cache 1 day

                return HttpResponse(r.content, content_type=content_type)
        except Exception:
            continue

    return HttpResponse("File not found", status=404)
