[app]
title = Помощник
package.name = assistant
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1

# 👇 ГЛАВНОЕ: жёстко пиним Python 3.11 (не даём p4a взять 3.14)
requirements = python3==3.11.9,kivy==2.3.1,cython==0.29.36

orientation = portrait
fullscreen = 0
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 24
# 👇 Меняем NDK на рекомендованный p4a
android.ndk = 27c
android.archs = arm64-v8a
android.accept_sdk_license = True
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 0
