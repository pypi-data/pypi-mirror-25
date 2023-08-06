import re
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

from myotest.wrapper import (
    WrapperObject, StringField, DateTimeField, ListField,
    IDField, FloatField, DurationField, DataframeField, LinkField,
    DictField, DateField
)


class AvroSchemaField(WrapperObject):
    fields = ListField(DictField())
    name = StringField()
    type = StringField()


class Dataset(WrapperObject):
    name = StringField()
    dataframe = DataframeField()
    workout = LinkField()
    describe = DictField()
    avro_schema = AvroSchemaField()

    def resolve_dataframe(self, json, field):
        reader = self.client.fetch_avro(json["cloud_url"])
        return pd.DataFrame(list(reader)).sort_values("time")

    def dataframe_for_slot(self, slot):
        start_time = slot.start_time.total_seconds()
        end_time = slot.end_time.total_seconds()
        df = self.dataframe
        return df[
            (df["time"] < end_time) &
            (df["time"] >= start_time)
        ]

    @property
    def type(self):
        return self.name.split("-")[0]


class SlotValue(WrapperObject):
    type = StringField()
    value = FloatField()


class SlotResult(WrapperObject):
    power = DictField()
    speed = DictField()

    gps_power = DictField()
    gps_speed = DictField()

    distance = FloatField()
    gps_distance = FloatField()
    regularity_90 = FloatField()
    step_count_ratio = FloatField()
    regularity_median = FloatField()


class Slot(WrapperObject):
    id = IDField()
    tags = ListField(StringField())
    type = StringField()
    value = SlotValue()
    text = StringField()
    result = SlotResult()
    end_time = DurationField()
    start_time = DurationField()
    power_type = StringField()
    analysis = ListField(DictField())
    workout = LinkField()

    def resolve_dataframe(self, json, field):
        reader = self.client.fetch_avro(json["cloud_url"])
        return pd.DataFrame(list(reader)).sort_values("time")

    def get_dataframe(self, dataset_name):
        return self.workout.get_dataset(dataset_name).dataframe_for_slot(self)

    @property
    def duration(self):
        return self.end_time - self.start_time


class Workout(WrapperObject):
    id = IDField()
    title = StringField()
    start = DateTimeField()
    end = DateTimeField()
    type = StringField()
    target_duration = DurationField()
    effective_duration = DurationField()

    datasets = ListField(Dataset(), source="data")
    slots = ListField(Slot())

    def _get_datasets(self, base_name):
        if "-" in base_name:
            regexp = re.compile("^{}$".format(base_name))
        else:
            regexp = re.compile("^{}-[0-9]+$".format(base_name))
        return [x for x in self.datasets if re.match(regexp, x.name)]

    def post_resolve_datasets(self, datasets):
        for ds in datasets:
            ds.workout = self

    def get_datasets(self, name):
        return list(self._get_datasets(name))

    def get_dataset(self, name):
        datasets = self._get_datasets(name)
        if len(datasets) > 0:
            return datasets[0]
        else:
            return None

    def resolve_slots(self, json, field):
        slots = self.client.get_slots(json["id"])
        return slots

    def post_resolve_slots(self, slots):
        for s in slots:
            s.workout = self

    def _get_slots(self, tags):
        return [x for x in self.slots if set(tags).issubset(set(x.tags))]

    def get_slot_with_tags(self, tags):
        slots = self._get_slots(tags)
        if len(slots) > 0:
            return slots[0]
        else:
            return None

    def dataset_names(self):
        return [x.name for x in self.datasets]

    def dataset_types(self):
        return set([x.type for x in self.datasets])


class Profile(WrapperObject):
    id = IDField()
    full_name = StringField()
    gender = StringField()
    weight = FloatField()
    height = FloatField()
    leg_length = FloatField()
    waist = FloatField()
    vma = FloatField()
    pma = FloatField()
    birth_date = DateField()
    age = FloatField()

    def resolve_age(self, json, field):
        return relativedelta(date.today(), self.birth_date).years
