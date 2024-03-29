from applications.maintenance.models.shared.cause_status import CauseStatus
from applications.maintenance.services.cleaning.status import CleaningStatusUpdater
from applications.maintenance.services.emails.expired import MaintenanceOperationExpiredEmail
from applications.maintenance.services.emails.pending import MaintenanceOperationPendingEmail
from applications.maintenance.services.itv.status import ItvStatusUpdater
from applications.maintenance.services.odometer.status import OdometerStatusUpdater
from applications.maintenance.services.revision.status import RevisionStatusUpdater
from applications.maintenance.services.wheels.status import WheelsStatusUpdater
from applications.tenants.models import Tenant

tenants = Tenant.objects.all()

for tenant in tenants:

    # CLEANING
    cleaning_updater = CleaningStatusUpdater(tenant)
    cleaning_updater.update()

    for cleaning in cleaning_updater.updates_to_pending:
        MaintenanceOperationPendingEmail(tenant, cleaning, 'limpieza').send()

    for cleaning in cleaning_updater.updates_to_expired:
        MaintenanceOperationExpiredEmail(tenant, cleaning, 'limpieza').send()

    # ITV
    itv_updater = ItvStatusUpdater(tenant)
    itv_updater.update()

    for itv in itv_updater.updates_to_pending:
        MaintenanceOperationPendingEmail(tenant, itv, 'ITV').send()

    for itv in itv_updater.updates_to_expired:
        MaintenanceOperationExpiredEmail(tenant, itv, 'ITV').send()

    # REVISION
    revision_updater = RevisionStatusUpdater(tenant)
    revision_updater.update()

    for revision in revision_updater.updates_to_pending:
        cause = 'kilometraje' if revision.cause_status == CauseStatus.KILOMETERS else 'fecha de revisión'
        MaintenanceOperationPendingEmail(tenant, revision, 'revisión', cause).send()

    for revision in revision_updater.updates_to_expired:
        cause = 'kilometraje' if revision.cause_status == CauseStatus.KILOMETERS else 'fecha de revisión'
        MaintenanceOperationExpiredEmail(tenant, revision, 'revisión', cause).send()

    # WHEELS
    wheels_updater = WheelsStatusUpdater(tenant)
    wheels_updater.update()

    for wheels in wheels_updater.updates_to_pending:
        cause = 'kilometraje' if wheels.cause_status == CauseStatus.KILOMETERS else 'fecha de revisión'
        MaintenanceOperationPendingEmail(tenant, wheels, 'cambio de neumáticos', cause).send()

    for wheels in wheels_updater.updates_to_expired:
        cause = 'kilometraje' if wheels.cause_status == CauseStatus.KILOMETERS else 'fecha de revisión'
        MaintenanceOperationExpiredEmail(tenant, wheels, 'cambio de neumáticos', cause).send()

    # ODOMETER
    odometer_updater = OdometerStatusUpdater(tenant)
    odometer_updater.update()

    for odometer in odometer_updater.updates_to_pending:
        MaintenanceOperationPendingEmail(tenant, odometer, 'cambio de kilometraje').send()

    for odometer in odometer_updater.updates_to_expired:
        MaintenanceOperationExpiredEmail(tenant, odometer, 'cambio de kilometraje').send()
