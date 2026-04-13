# Keyman Developer Installation & Build Guide

## Why You Need This

Keyman Developer is the official IDE for building Keyman keyboards. While
this project's source files (`.kmn`, `.kvks`, `.kps`,
`.keyman-touch-layout`) can be edited on any platform, **compiling them
into installable packages requires Keyman Developer**, which runs natively
on Windows.

## Linux Alternative — Already Set Up ✅

This project includes a **Node.js-based Keyman compiler** that works on Linux:

```bash
npx kmc build .
```

The `@keymanapp/kmc` package is already installed in this project. Use this
for quick iterations on Linux. For final builds and Windows-specific testing,
follow the Windows installation below.

---

## Windows Installation (Recommended for Production)

### Option A — Native Windows

1. **Download Keyman Developer**
   - Visit https://keyman.com/developer/
   - Click **Download Keyman Developer**
   - Save the `.msi` installer

2. **Install**
   - Double-click the `.msi` file
   - Accept the license
   - Use default install location (`C:\Program Files (x86)\Keyman Developer`)
   - Click **Install**, then **Finish**

3. **Verify**
   - Open Start Menu → **Keyman Developer**
   - You should see the IDE with a project chooser

### Option B — Windows in a VM (for Linux/macOS users)

1. Install VirtualBox: https://www.virtualbox.org/
2. Get a Windows 10/11 ISO from Microsoft
3. Create a new VM with at least 4GB RAM, 40GB disk
4. Install Windows in the VM
5. Inside Windows, follow Option A above
6. Share the project folder via VirtualBox shared folders

### Option C — Wine on Linux (experimental)

```bash
# Install Wine
sudo apt install wine wine64 winetricks

# Install Keyman Developer through Wine
wine /path/to/keymandeveloper.msi

# Run via Wine
wine "C:\Program Files (x86)\Keyman Developer\Tike.exe"
```

⚠️ Wine support is experimental — some features may not work.

---

## Building the Project

### Using Linux (npm)

```bash
cd /home/dragon/Documents/Keyboard

# Validate first
python3 validate_kmn.py an_alphabet_national.kmn

# Build the keyboard package
npx kmc build .

# Output files will be in build/ directory:
#   build/an_alphabet_national.kmx     (compiled keyboard)
#   build/an_alphabet_national.kvk     (visual keyboard)
#   build/an_alphabet_national.kmp     (installable package)
```

### Using Keyman Developer (Windows)

1. Open Keyman Developer
2. **File → Open Project**
3. Navigate to the project folder
4. Open `an_alphabet_national.kps`
5. Click **Project → Compile All**
6. Compiled files appear in the `build/` subfolder

### Building for Specific Platforms

```bash
# Mobile only (Android/iOS)
npx kmc build --target mobile .

# Desktop only (Windows/macOS)
npx kmc build --target desktop .

# All platforms (default)
npx kmc build .
```

---

## File Outputs

After successful build, expect these files:

| File | Purpose |
|------|---------|
| `build/an_alphabet_national.kmx` | Compiled keyboard binary |
| `build/an_alphabet_national.kvk` | Compiled visual keyboard |
| `build/an_alphabet_national.kmp` | **Installable package** for end users |
| `build/an_alphabet_national.js` | Web/Mobile JavaScript output |

The `.kmp` file is what you distribute to users.

---

## Project Files (Source)

The source files in this directory:

| File | Description |
|------|-------------|
| `an_alphabet_national.kmn` | Keyboard logic (89 rules, VK-based) |
| `an_alphabet_national.kvks` | On-screen keyboard layout |
| `an_alphabet_national.keyman-touch-layout` | Mobile touch layout |
| `an_alphabet_national.kps` | Package metadata |
| `NationalAlphabetRegular5.ttf` | Bundled AN font |
| `an_alphabet_national.ico` | Keyboard icon |
| `welcome.png` | Welcome screen image |
| `readme.htm` | User documentation |
| `LICENSE.md` | License terms |

---

## Common Build Issues

### Error: "Font not found"
Make sure `NationalAlphabetRegular5.ttf` is in the same directory as the `.kps` file.

### Error: "Invalid character in key code"
Run the validator first: `python3 validate_kmn.py an_alphabet_national.kmn`

### Error: "U+0008 produces system breakage"
NEVER map Backspace to U+0008. The current `.kmn` correctly leaves
Backspace unmapped so the system handles it. If you accidentally add such
a rule, the validator will warn you.

### Mobile keyboard shows White Boxes (.notdef)
The font is not loading on mobile. Verify:
1. Font is in package
2. `<DisplayFont>` and `<OSKFont>` in `.kps` reference `National Alphabet`
3. Font name in `.keyman-touch-layout` matches: `"font": "National Alphabet"`
