[app]
title = Помощник
package.name = assistant
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1

requirements = python3,kivy,cython

orientation = portrait
fullscreen = 0
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.debug_artifact = apk
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0 
