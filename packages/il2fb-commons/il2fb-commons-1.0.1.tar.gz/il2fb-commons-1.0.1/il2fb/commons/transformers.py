# coding: utf-8

from il2fb.commons.organization import Belligerents
from il2fb.commons.spatial import Point2D


def get_2d_pos_transformer(
    dst_field_name='pos',
    src_x_field_name='pos_x',
    src_y_field_name='pos_y',
):

    def _transformer(data):
        data[dst_field_name] = Point2D(
            float(data.pop(src_x_field_name)),
            float(data.pop(src_y_field_name)),
        )

    return _transformer


transform_2d_pos = get_2d_pos_transformer('pos', 'pos_x', 'pos_y')


def get_belligerent_transformer(
    dst_field_name='belligerent',
    src_field_name=None,
):
    if not src_field_name:
        src_field_name = dst_field_name

    def _transformer(data):
        value = data[src_field_name]
        data[dst_field_name] = Belligerents[value.lower()]

    return _transformer


transform_belligerent = get_belligerent_transformer('belligerent')


def get_int_transformer(dst_field_name, src_field_name=None):
    if not src_field_name:
        src_field_name = dst_field_name

    def _transformer(data):
        data[dst_field_name] = int(data[src_field_name])

    return _transformer
