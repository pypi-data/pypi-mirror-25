from plenario_core import signals
from plenario_mailer_core import mailer


# signals.data_set_registered.connect()
signals.data_set_approved.connect(mailer.send_data_set_approved_email)
signals.data_set_table_created.connect(mailer.send_data_set_ready_email)
# signals.data_set_table_dropped.connect()
signals.data_set_erred.connect(mailer.send_data_set_erred_email)
signals.data_set_fixed.connect(mailer.send_data_set_fixed_email)
