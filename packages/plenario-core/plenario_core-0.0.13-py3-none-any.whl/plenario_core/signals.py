from django.db.models.signals import ModelSignal


data_set_registered = ModelSignal(
    providing_args=['meta_model'], use_caching=True)

# data_set_submitted_for_approval = ModelSignal(
#     providing_args=['meta_model'], use_caching=True)
data_set_approved = ModelSignal(
    providing_args=['meta_model'], use_caching=True)
# data_set_rejected = ModelSignal(
#     providing_args=['meta_model', 'reason'], use_caching=True)

data_set_table_created = ModelSignal(
    providing_args=['meta_model'], use_caching=True)
data_set_table_dropped = ModelSignal(
    providing_args=['meta_model', 'reason'], use_caching=True)

data_set_erred = ModelSignal(
    providing_args=['meta_model', 'reason'], use_caching=True)

data_set_fixed = ModelSignal(
    providing_args=['meta_model', 'reason'], use_caching=True)
