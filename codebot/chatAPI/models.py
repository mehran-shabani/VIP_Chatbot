from django.db import models

class APIRequest(models.Model):
    user_input = models.TextField()
    model_used = models.CharField(max_length=50)
    final_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request {self.id} - Model: {self.model_used}"


class APIResponse(models.Model):
    api_request = models.ForeignKey(APIRequest, on_delete=models.CASCADE, related_name='responses')
    model_name = models.CharField(max_length=50)
    raw_response = models.TextField()
    cleaned_response = models.TextField(blank=True)
    cot_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"APIResponse {self.id} (Request {self.api_request_id})"

