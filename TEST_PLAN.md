# AN-Alphabet National de Guinée — Test Plan

This document is the **mandatory pre-delivery checklist** for the AN keyboard
package. It must be completed in full before sending the .kmp file to the
client.

> **Why this matters**: Past deliveries failed because of basic bugs that
> would have been caught by 1 minute of testing (QWERTY instead of AZERTY,
> backspace mapped to U+0008, missing variants). This plan exists to prevent
> a third rejection.

---

## Pre-Test Build Verification

Before testing, ensure the build is clean:

- [ ] `python3 validate_kmn.py an_alphabet_national.kmn` reports 0 errors
- [ ] `npx kmc build file an_alphabet_national.kmn` reports 0 errors, 0 warnings
- [ ] `npx kmc build file an_alphabet_national.kps` reports 0 errors, 0 warnings
- [ ] `an_alphabet_national.kmp` file exists and is < 100 KB
- [ ] Package contents (use `python3 -c "import zipfile; print(zipfile.ZipFile('an_alphabet_national.kmp').namelist())"`):
  - [ ] `an_alphabet_national.kmx`
  - [ ] `an_alphabet_national.kvk`
  - [ ] `an_alphabet_national.js`
  - [ ] `NationalAlphabetRegular5.ttf`
  - [ ] `an_alphabet_national.ico`
  - [ ] `readme.htm`
  - [ ] `welcome.png`
  - [ ] `LICENSE.md`
  - [ ] `kmp.json`
  - [ ] `kmp.inf`

---

## A. Windows Test (Keyman for Windows)

### Installation
- [ ] Double-click `.kmp` → installer launches
- [ ] Welcome screen shows the welcome.png image
- [ ] License screen shows LICENSE.md content
- [ ] Documentation accessible from Start Menu
- [ ] Keyboard appears in Keyman Configuration with name "AN-Alphabet National de Guinée (autres langues)"
- [ ] Icon displays correctly (the black logo)
- [ ] Font is automatically installed

### Layer Tests — Default
Open Notepad. Switch to AN keyboard.
- [ ] Type `a` → AN 'a' glyph appears (NOT Latin 'a')
- [ ] Type `g` → AN 'g' glyph (NOT Latin 'g')
- [ ] Type `e r t y u i o p` → all show AN glyphs
- [ ] Type `q s d f z h j k l m` → AN glyphs
- [ ] Type `w x c v b n` → AN glyphs
- [ ] Type all 10 digits `1 2 3 4 5 6 7 8 9 0` → AN native digits
- [ ] Punctuation `- . , '` → all output correctly

### Layer Tests — Shift
- [ ] Shift + each letter → uppercase AN glyph
- [ ] Shift + 1 → `!`
- [ ] Shift + 4 → `$`
- [ ] Shift + . → `:`
- [ ] Shift + , → `;`

### Layer Tests — AltGr (Right Alt)
- [ ] AltGr + A → á (single dot accent)
- [ ] AltGr + E → é (single dot accent)
- [ ] AltGr + I → ï (diaeresis)
- [ ] AltGr + O → ó (single dot accent)
- [ ] AltGr + U → ù (independent character)

### Layer Tests — AltGr+Shift
- [ ] AltGr+Shift + E → ê (circumflex)
- [ ] AltGr+Shift + O → ô (circumflex)
- [ ] AltGr+Shift + A → Á
- [ ] AltGr+Shift + I → Ï
- [ ] AltGr+Shift + U → Ù

### CRITICAL System Key Tests
- [ ] **Backspace** deletes the previous character (NOT outputs U+0008)
- [ ] **Enter** creates a new line
- [ ] **Tab** moves cursor or inserts tab
- [ ] **Arrow keys** navigate normally
- [ ] **Home/End** work normally
- [ ] **Space** inserts a space
- [ ] **Ctrl+C / Ctrl+V** copy/paste work normally

### Font Rendering
- [ ] No "White Boxes" (□) appear anywhere
- [ ] No `.notdef` glyphs visible
- [ ] All AN characters render with the National Alphabet font
- [ ] Latin characters do NOT bleed through

### Switching to System Keyboard
- [ ] Win+Space switches between AN and system keyboard
- [ ] Switching back to AN preserves the keyboard state

---

## B. macOS Test (Keyman for Mac)

Repeat all tests from Section A on macOS, with these additions:

### macOS-specific
- [ ] Right-Option (⌥) acts as AltGr
- [ ] Caps Lock state is respected for AltGr layer
- [ ] Input source switches via Control+Space
- [ ] Keyboard appears in Input Sources menu bar
- [ ] System Settings shows the keyboard

---

## C. Android Test (Keyman for Android)

### Installation
- [ ] Open .kmp from email/file manager
- [ ] Keyman app launches with install prompt
- [ ] Tap Install
- [ ] Enable in Settings → Languages → Keyboards
- [ ] Switch to AN keyboard via notification or Globe key

### Touch Layout — Default Layer (10/11/11/10 grid)
- [ ] Row 1 has 10 digit keys
- [ ] Row 2 has 11 letter keys: A G E R T Y U I O P £
- [ ] Row 3 has 11 letter keys: Q S D F Z H J K L M %
- [ ] Row 4 has letter keys + punctuation + Shift + Backspace
- [ ] Bottom row has ?123, Globe, Space, period, Enter
- [ ] All keys display AN glyphs (not Latin)

### Long-press Variants
- [ ] Long-press A → popup shows á
- [ ] Long-press E → popup shows é, ê
- [ ] Long-press I → popup shows ï
- [ ] Long-press O → popup shows ó, ô
- [ ] Long-press U → popup shows ù
- [ ] Selecting a variant outputs the correct character

### Globe Key
- [ ] Tapping Globe key switches to system keyboard
- [ ] Returning shows AN keyboard intact

### Shift Layer
- [ ] Tapping Shift switches to uppercase
- [ ] All uppercase letters display correctly
- [ ] Tapping Shift again returns to lowercase

### Numeric Layer
- [ ] Tapping ?123 switches to numeric layer
- [ ] Symbols display correctly
- [ ] Tapping ABC returns to letter layer

### Backspace
- [ ] **CRITICAL**: Tapping backspace DELETES the previous character
- [ ] Long-press backspace deletes multiple characters

---

## D. iOS Test (Keyman for iOS)

Repeat all tests from Section C on iOS, plus:

### iOS-specific
- [ ] Keyboard appears in Settings → General → Keyboard → Keyboards
- [ ] Globe key switches between system and AN
- [ ] Long-press Globe shows keyboard list
- [ ] Predictive text is disabled or doesn't interfere with AN
- [ ] Auto-capitalization works correctly with AN letters

---

## E. Cross-Platform Consistency Tests

For each pair of platforms, type the same text and verify identical output:

- [ ] Windows ↔ macOS: identical text output for all 32 letters
- [ ] Windows ↔ Android: identical text
- [ ] Windows ↔ iOS: identical text
- [ ] Android ↔ iOS: identical text

### Sample test text:
```
abcdefghij klmnopqrst uvwxyz
ABCDEFGHIJ KLMNOPQRST UVWXYZ
1234567890
áéêïóôù ÁÉÊÏÓÔÙ
- . , '
```

---

## F. Real-World Usage Test

### Type sample words in each Guinean language

The keyboard must produce coherent text. Test typing common words in:

- [ ] **Poular** (Pular Futa): pulaar, ɓe, ko
- [ ] **Maninka**: mali, kuma, mɔgɔ
- [ ] **Soussou**: bare, na, mu
- [ ] **Kissi**: bendoo, mafaa
- [ ] **Guerzé** (Kpelle): pele, kɛlɛ

### Mixed-Language Test
- [ ] Type AN text, switch to system keyboard, type French text, switch back
- [ ] Verify both keyboards remain functional after switching

---

## G. Specification Compliance Verification

Verify each client requirement is met:

### Layout
- [ ] Grid is exactly 10/11/11/10 (mobile)
- [ ] Base logic is AZERTY (with G/Z swap as per blackimage.png)
- [ ] 4 layers exist: Default, Shift, AltGr, AltGr+Shift
- [ ] All 32 AN letters visible without Shift on default layer

### Character Set
- [ ] 32 unique AN letters present
- [ ] AN native digits (NOT Arabic numerals)
- [ ] Punctuation: `' , . -` accessible
- [ ] Vowel variants: A(1), E(2), I(1), O(2)

### Variant Input
- [ ] Desktop: AltGr + key for single, AltGr+Shift + key for double
- [ ] Mobile: long-press menu on each base vowel

### Keyboard Purity
- [ ] AN keyboard contains ONLY AN characters (no Latin bleed-through)
- [ ] Globe key allows switching to system AZERTY for French

### "No Unicode injection"
- [ ] Uses VK / scancode mapping (no PUA injection)
- [ ] No White Boxes / .notdef glyphs anywhere

### Metadata & Branding
- [ ] Display name: "AN-Alphabet National de Guinée (autres langues)"
- [ ] Logo (black background, 2 white letters) is integrated
- [ ] Font name shown to user: "National Alphabet"

### Functional Keys (mobile)
- [ ] Backspace works
- [ ] Space bar works
- [ ] Enter/Return works
- [ ] Shift works
- [ ] Globe key works
- [ ] ?123 toggle works

---

## H. Regression Tests (from past deliveries)

These specifically test for bugs from the 2 failed deliveries:

- [ ] **Bug #1**: Layout is AZERTY, NOT QWERTY
- [ ] **Bug #2**: No Latin characters visible (AN purity)
- [ ] **Bug #3**: No duplicate letters
- [ ] **Bug #4**: Backspace deletes (does NOT output U+0008)
- [ ] **Bug #5**: Shift+punctuation works (Shift+. → :, Shift+, → ;)
- [ ] **Bug #6**: Font glyph mapping is correct
- [ ] **Bug #7**: Latin character visibility — none should appear

---

## I. Documentation & Package Quality

- [ ] readme.htm renders correctly in browser
- [ ] LICENSE.md is readable
- [ ] welcome.png displays during install
- [ ] Icon displays at 16, 32, 48, 64, 128, 256 pixel sizes
- [ ] Package metadata shows correct version (1.0)
- [ ] Author information is correct

---

## Sign-off

| Tester | Platform | Date | Pass/Fail | Notes |
|--------|----------|------|-----------|-------|
|        | Windows  |      |           |       |
|        | macOS    |      |           |       |
|        | Android  |      |           |       |
|        | iOS      |      |           |       |

**ONLY deliver to the client when ALL platforms pass ALL tests.**
