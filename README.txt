ZAID DINO RUNNER — ANDROID PROJECT

Project files:
- main.py
- buildozer.spec
- .github/workflows/build-apk.yml (automatic cloud APK build)

ANDROID-ONLY BUILD STEPS
1. Create/sign in to a GitHub account.
2. Create a new repository named zaid-dino-runner. Private is fine.
3. Upload main.py and buildozer.spec to the repository root.
4. On GitHub, choose Add file > Create new file.
5. In the filename box enter: .github/workflows/build-apk.yml
6. Paste the workflow content from this project's same path, then commit it to main.
7. Open the repository's Actions tab.
8. Select "Build ZAID Dino Runner APK", choose Run workflow, then Run workflow.
   A push to main also starts a build automatically.
9. Wait for the workflow to finish with a green check.
10. Open that completed run and download the artifact named ZAID-Dino-Runner-APK.
11. Extract the downloaded artifact ZIP. It contains the .apk file.
12. Tap the APK to install. Android may ask permission to install from that browser/file manager; only enable it for the app you used to download/open your own APK, then turn it off again if desired.

IMPORTANT
- This uses GitHub Actions cloud runners; no Linux installation is needed on your phone.
- First build can take a while because Android build tools must be downloaded.
- Keep the repository private if you do not want the source code public.
- Never put passwords, API keys, or private signing keys in the repository.
- A debug APK is for testing and sharing directly. Public Play Store publishing needs a separately signed release/AAB process.
- If the build fails, open the failed run and share the last error lines (hide any personal information).

Official references:
https://github.com/kivy/buildozer
https://github.com/ArtemSBulgakov/buildozer-action
https://docs.github.com/en/repositories/working-with-files/managing-files/creating-new-files
