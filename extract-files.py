#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.file import File
from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'hardware/qcom-caf/sm8150',
    'device/sony/sm8150-common',
    'hardware/qcom-caf/wlan',
    'hardware/sony',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
    'vendor/qcom/opensource/display',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

libs_add_vendor_suffix = (
    'vendor.somc.hardware.miscta@1.0',
    'com.qualcomm.qti.dpm.api@1.0',
    'libmmosal',
    'vendor.qti.hardware.tui_comm@1.0',
    'vendor.qti.hardware.wifidisplaysession@1.0',
    'com.qualcomm.qti.imscmservice@1.0',
    'com.qualcomm.qti.imscmservice@2.0',
    'com.qualcomm.qti.imscmservice@2.1',
    'com.qualcomm.qti.imscmservice@2.2',
    'com.qualcomm.qti.uceservice@2.0',
    'com.qualcomm.qti.uceservice@2.1',
    'com.qualcomm.qti.uceservice@2.2',
    'vendor.qti.hardware.data.cne.internal.api@1.0',
    'vendor.qti.hardware.data.cne.internal.constants@1.0',
    'vendor.qti.hardware.data.cne.internal.server@1.0',
    'vendor.qti.hardware.data.connection@1.0',
    'vendor.qti.hardware.data.connection@1.1',
    'vendor.qti.hardware.data.dynamicdds@1.0',
    'vendor.qti.hardware.data.iwlan@1.0',
    'vendor.qti.hardware.data.qmi@1.0',
    'vendor.qti.hardware.qseecom@1.0',
    'vendor.qti.ims.callinfo@1.0',
    'vendor.qti.ims.rcsconfig@1.0',
    'vendor.qti.ims.rcsconfig@1.1',
    'vendor.qti.imsrtpservice@3.0',
    'vendor.display.color@1.0',
)

blob_fixups: blob_fixups_user_type = {
        (
            'system_ext/lib64/libwfdnative.so',
            'vendor/lib64/libvpplibrary.so',
            'vendor/lib64/libswiqisettinghelper.so',
            'vendor/lib64/vendor.somc.hardware.swiqi@1.0-impl.so',
        ): blob_fixup()
            .replace_needed('android.hidl.base@1.0.so', 'libhidlbase.so'),
        'product/lib64/libdpmframework.so': blob_fixup()
            .replace_needed('libhidltransport.so', 'libcutils-v29.so'),
        'system_ext/lib64/lib-imsvideocodec.so': blob_fixup()
            .add_needed('libandroid.so')
            .add_needed('lib-imsvtshim.so'),
        (
            'vendor/lib64/vendor.semc.hardware.extlight-V1-ndk_platform.so',
            'vendor/lib/vendor.semc.hardware.extlight-V1-ndk_platform.so',
        ): blob_fixup()
            .replace_needed('android.hardware.light-V1-ndk_platform.so', 'android.hardware.light-V1-ndk.so'),
        'vendor/lib/libsomc_alfortlpserv.so': blob_fixup()
            .add_needed('liblog.so'),
        'vendor/lib/libmorpho_dual_camera.so': blob_fixup()
            .add_needed('libutils.so'),
        'vendor/etc/gps.conf': blob_fixup()
            .binary_regex_replace(b'\x92', b'\x27')
            .regex_replace('XTRA_CA_PATH=/usr/lib/ssl-1.1/certs', 'XTRA_CA_PATH=/system/etc/security/cacerts'),
        }  # fmt: skip

lib_fixups: lib_fixups_user_type = {
        **lib_fixups,
        libs_add_vendor_suffix: lib_fixup_vendor_suffix,
        (
            'libOmxCore',
            'libplatformconfig',
            'libwpa_client',
            'libc2dcolorconvert',
            'libril',
        ): lib_fixup_remove,
}

module = ExtractUtilsModule(
    'sm8150-common',
    'sony',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
