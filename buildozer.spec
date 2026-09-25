[app]
title = Калькулятор
package.name = calculator
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0.0

requirements = python3,kivy==2.2.1

orientation = portrait
fullscreen = 1

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

android.allow_backup = True
android.permissions =

p4a.branch = master
