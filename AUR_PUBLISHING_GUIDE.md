# Publishing qrcode-pretty to AUR

This guide walks you through publishing your package to the Arch User Repository (AUR).

## Prerequisites

1. **AUR Account**: Register at https://aur.archlinux.org/register
2. **SSH Key**: Add your SSH public key to your AUR account settings at https://aur.archlinux.org/account/
3. **Arch Linux or makepkg**: You need `makepkg` to generate `.SRCINFO`

## Initial Publication Steps

### 1. Clone the AUR Repository (Empty for New Packages)

```bash
# Clone from AUR - this will be empty initially
git clone ssh://aur@aur.archlinux.org/qrcode-pretty.git aur-qrcode-pretty
cd aur-qrcode-pretty
```

### 2. Copy Your PKGBUILD

```bash
# Copy PKGBUILD from your project root
cp ../PKGBUILD .
```

### 3. Generate .SRCINFO

The `.SRCINFO` file is required by AUR and is generated from your PKGBUILD:

```bash
makepkg --printsrcinfo > .SRCINFO
```

**Important:** You must regenerate `.SRCINFO` every time you update the PKGBUILD!

### 4. Review Files

Check that everything looks correct:

```bash
cat PKGBUILD
cat .SRCINFO
```

### 5. Commit and Push (This Publishes the Package!)

```bash
git add PKGBUILD .SRCINFO
git commit -m "Initial import: qrcode-pretty 1.0.3"
git push -u origin master
```

Once pushed, your package will be immediately live at:
**https://aur.archlinux.org/packages/qrcode-pretty**

## Updating the Package

When you release a new version (e.g., 1.0.4):

### 1. Update Your Project's PKGBUILD

In your main project repository, update:
- `pkgver=1.0.4`
- `pkgrel=1` (reset to 1 for new version)

### 2. Update AUR Repository

```bash
cd aur-qrcode-pretty

# Copy updated PKGBUILD
cp ../PKGBUILD .

# Regenerate .SRCINFO
makepkg --printsrcinfo > .SRCINFO

# Commit and push
git add PKGBUILD .SRCINFO
git commit -m "Update to version 1.0.4"
git push
```

## After Publishing

### Update README.md

Once the package is on AUR, update the README to remove the "not yet published" note:

```markdown
### Arch Linux (AUR)

Install from the AUR using your preferred AUR helper:

\`\`\`bash
# Using yay
yay -S qrcode-pretty

# Using paru
paru -S qrcode-pretty
\`\`\`

Or build manually:

\`\`\`bash
git clone https://aur.archlinux.org/qrcode-pretty.git
cd qrcode-pretty
makepkg -si
\`\`\`
```

## Testing Before Publishing

You can test your PKGBUILD locally before publishing:

```bash
# In your project root
makepkg -si

# Or just build without installing
makepkg

# Check the built package
pacman -Qlp qrcode-pretty-*.pkg.tar.zst
```

## Common Issues

### "Repository not found"
- Make sure you've added your SSH key to your AUR account
- Verify the package name doesn't already exist on AUR

### "Could not cd to srcdir"
- The PKGBUILD has the correct `$srcdir/$pkgname` paths (fixed in your current version)

### "Permission denied (publickey)"
- Your SSH key isn't added to your AUR account
- Add it at https://aur.archlinux.org/account/

## AUR Guidelines

Before publishing, review:
- **AUR Submission Guidelines**: https://wiki.archlinux.org/title/AUR_submission_guidelines
- **PKGBUILD Guidelines**: https://wiki.archlinux.org/title/PKGBUILD

Key points:
- Package name should be lowercase and descriptive
- Include accurate dependencies
- Use proper license identifiers
- Test the package builds correctly
- Maintain the package (respond to comments, update regularly)

## Useful Commands

```bash
# Check PKGBUILD syntax
namcap PKGBUILD

# Check built package
namcap qrcode-pretty-*.pkg.tar.zst

# Test in clean chroot (advanced)
extra-x86_64-build
```

## Support

- **AUR Package Page**: https://aur.archlinux.org/packages/qrcode-pretty (after publishing)
- **AUR Wiki**: https://wiki.archlinux.org/title/Arch_User_Repository
- **AUR Mailing List**: https://lists.archlinux.org/mailman3/lists/aur-general.lists.archlinux.org/
