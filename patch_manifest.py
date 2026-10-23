
manifest_path = 'android/app/src/main/AndroidManifest.xml'
with open(manifest_path, 'r') as f:
    content = f.read()

permissions = '''<uses-permission android:name="android.permission.CAMERA" />
    <uses-feature android:name="android.hardware.camera" android:required="false" />
    <uses-feature android:glEsVersion="0x00020000" android:required="true" />
    <application android:hardwareAccelerated="true" android:usesCleartextTraffic="true" '''

if 'android.permission.CAMERA' not in content:
    content = content.replace('<application', permissions, 1)

with open(manifest_path, 'w') as f:
    f.write(content)
print("Manifest patched successfully.")
