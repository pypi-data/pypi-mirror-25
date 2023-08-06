from djotali.campaigns.models import Campaign, Notification


def update_notifications_after_contact_save(sender, instance, created, **kwargs):
    organization = instance.organization
    if created:
        # We create the appropriate notification when a contact is created on campaigns linked to all contacts group
        campaigns_linked_to_all_groups = Campaign.get_linked_to_all_contacts_group(organization)
        notifications = []
        for campaign in campaigns_linked_to_all_groups:
            notifications.append(Notification(contact=instance, campaign=campaign, organization=organization))
        Notification.objects.bulk_create(notifications)
    else:
        # We only update notifications which are not removed when their related contact is removed
        Notification.org_objects.get_queryset_for_organization(organization) \
            .filter(contact=instance, is_removed=0 if instance.is_removed else 1) \
            .update(is_removed=1 if instance.is_removed else 0)
