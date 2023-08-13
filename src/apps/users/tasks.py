from celery import shared_task


@shared_task()
def send_activation_email(request, link, user):
    request.app.state.email_service.send_activation_email(
        name=user.username,
        link=link,
        email=user.email
    )
